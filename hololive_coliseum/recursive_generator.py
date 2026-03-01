"""Chain existing generators to build game data in one call."""

from __future__ import annotations

from .class_generator import ClassGenerator
from .skill_generator import SkillGenerator
from .subclass_generator import SubclassGenerator
from .trade_skill_generator import TradeSkillGenerator
from .auto_balancer import AutoBalancer


class RecursiveGenerator:
    """Generate classes, subclasses, skills and trade skills recursively."""

    def __init__(self) -> None:
        self.class_gen = ClassGenerator()
        self.subclass_gen = SubclassGenerator()
        self.skill_gen = SkillGenerator()
        self.trade_gen = TradeSkillGenerator()
        self.balancer = AutoBalancer()

    def generate_all(
        self, base_classes: dict[str, dict[str, int]], professions: list[str]
    ) -> dict[str, object]:
        """Generate dependent records for classes and professions."""

        classes = {
            name: self.class_gen.create(name, stats)
            for name, stats in base_classes.items()
        }
        subclasses = {
            name: self.subclass_gen.create(cls, "Elite") for name, cls in classes.items()
        }
        skills = {
            name: self.skill_gen.generate(name, cls.get("attack", 0))
            for name, cls in classes.items()
        }
        trade_skills = {p: self.trade_gen.generate(p) for p in professions}
        balanced = self.balancer.balance(classes)
        return {
            "classes": classes,
            "subclasses": subclasses,
            "skills": skills,
            "trade_skills": trade_skills,
            "balanced": balanced,
        }
