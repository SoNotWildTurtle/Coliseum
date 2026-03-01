"""Generate a concise project-state report in the repository root."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.analysis_skill import ProjectAnalysisSkill


OUTPUT = ROOT / "PROJECT_STATE_ANALYSIS.md"


def main() -> None:
    skill = ProjectAnalysisSkill(ROOT)
    analysis = skill.analyze()
    report = skill.render_markdown(analysis)
    OUTPUT.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
