"""Derive arena modifiers from MMO world region data."""

from __future__ import annotations

from typing import Any, Dict

from .world_region_manager import WorldRegionManager

DEFAULT_CONFIG: Dict[str, Any] = {
    "xp_multiplier": 1.0,
    "stamina_regen_step": 1.0,
    "hazard_damage_multiplier": 1.0,
    "source_region": None,
    "biome": None,
    "description": "Standard arena conditions.",
}

BIOME_RULES: Dict[str, Dict[str, Any]] = {
    "desert": {
        "stamina_regen_step": 0.5,
        "xp_multiplier": 1.15,
        "description": "Desert heat slows stamina regen but awards extra experience.",
    },
    "forest": {
        "xp_multiplier": 1.2,
        "description": "Forest growth grants bonus experience from victories.",
    },
    "tundra": {
        "hazard_damage_multiplier": 1.25,
        "description": "Tundra chill makes arena hazards more punishing.",
    },
    "plains": {
        "xp_multiplier": 1.05,
        "description": "Calm plains offer a slight experience boost.",
    },
}


class EventModifierManager:
    """Compute arena modifiers using stored MMO regions."""

    def __init__(self, region_manager: WorldRegionManager | None = None) -> None:
        self.region_manager = region_manager or WorldRegionManager()
        self.config: Dict[str, Any] = dict(DEFAULT_CONFIG)

    def refresh(self) -> Dict[str, Any]:
        """Recalculate modifiers from the newest world region."""

        config: Dict[str, Any] = dict(DEFAULT_CONFIG)
        regions = self.region_manager.get_regions()
        description_parts: list[str] = []
        if regions:
            latest = regions[-1]
            config["source_region"] = latest.get("name")
            biome = str(latest.get("biome", "")).lower()
            config["biome"] = biome or None
            rule = BIOME_RULES.get(biome)
            if rule:
                for key, value in rule.items():
                    if key == "description":
                        description_parts.append(str(value))
                    else:
                        config[key] = value
            recommended = latest.get("recommended_level")
            if isinstance(recommended, (int, float)) and recommended >= 10:
                config["hazard_damage_multiplier"] += 0.1
                description_parts.append("High level threats increase hazard danger.")
            feature = latest.get("feature", {})
            if isinstance(feature, dict) and feature.get("type") == "monument":
                config["xp_multiplier"] += 0.05
                description_parts.append("Faction monument inspires additional experience gains.")
        config["xp_multiplier"] = max(0.0, float(config["xp_multiplier"]))
        config["stamina_regen_step"] = max(0.0, float(config["stamina_regen_step"]))
        config["hazard_damage_multiplier"] = max(0.0, float(config["hazard_damage_multiplier"]))
        if description_parts:
            config["description"] = " ".join(description_parts)
        else:
            config["description"] = DEFAULT_CONFIG["description"]
        self.config = config
        return dict(self.config)

    def get_config(self) -> Dict[str, Any]:
        """Return the last calculated modifier configuration."""

        return dict(self.config)
