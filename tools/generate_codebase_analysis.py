"""Generate docs/CODEBASE_ANALYSIS.md from the repository source tree."""

from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "CODEBASE_ANALYSIS.md"
START_MARKER = "<!-- AUTO-GENERATED:codebase-analysis:start -->"
END_MARKER = "<!-- AUTO-GENERATED:codebase-analysis:end -->"
SKIP_DIRS = {".git", "__pycache__", "venv", ".venv", "node_modules"}


def _is_skipped_path(path: Path) -> bool:
    """Return True when a path belongs to generated or virtualenv content."""
    for part in path.parts:
        lowered = part.lower()
        if part in SKIP_DIRS:
            return True
        if lowered.startswith(".venv") or lowered.startswith("venv"):
            return True
    return False


def walk_py_files(root: Path) -> list[Path]:
    """Return a list of python files under the given root."""
    files: list[Path] = []
    for path in root.rglob("*.py"):
        if _is_skipped_path(path):
            continue
        files.append(path)
    return files


def parse_file(path: Path) -> dict[str, object]:
    """Parse a Python module and extract metadata for the analysis doc."""
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    module: dict[str, object] = {
        "path": str(path.relative_to(ROOT)),
        "docstring": ast.get_docstring(tree) or "",
        "imports": [],
        "from_imports": [],
        "globals": [],
        "classes": [],
        "functions": [],
    }
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                module["imports"].append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module["from_imports"].append(
                {
                    "module": node.module or "",
                    "names": [alias.name for alias in node.names],
                    "level": node.level,
                }
            )
        elif isinstance(node, ast.Assign):
            targets: list[str] = []
            for target in node.targets:
                if isinstance(target, ast.Name):
                    targets.append(target.id)
                elif isinstance(target, ast.Tuple):
                    for elt in target.elts:
                        if isinstance(elt, ast.Name):
                            targets.append(elt.id)
            module["globals"].extend(targets)
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name):
                module["globals"].append(node.target.id)
        elif isinstance(node, ast.FunctionDef):
            module["functions"].append(_function_entry(node))
        elif isinstance(node, ast.AsyncFunctionDef):
            module["functions"].append(_function_entry(node, async_flag=True))
        elif isinstance(node, ast.ClassDef):
            module["classes"].append(_class_entry(node))
    return module


def _function_entry(
    node: ast.FunctionDef | ast.AsyncFunctionDef, async_flag: bool = False
) -> dict[str, object]:
    return {
        "name": node.name,
        "args": [arg.arg for arg in node.args.args],
        "returns": ast.unparse(node.returns) if node.returns else "",
        "doc": ast.get_docstring(node) or "",
        "async": async_flag,
    }


def _class_entry(node: ast.ClassDef) -> dict[str, object]:
    entry: dict[str, object] = {
        "name": node.name,
        "bases": [ast.unparse(base) for base in node.bases],
        "doc": ast.get_docstring(node) or "",
        "methods": [],
        "class_vars": [],
    }
    for item in node.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            entry["methods"].append(
                _function_entry(item, async_flag=isinstance(item, ast.AsyncFunctionDef))
            )
        elif isinstance(item, ast.Assign):
            for target in item.targets:
                if isinstance(target, ast.Name):
                    entry["class_vars"].append(target.id)
        elif isinstance(item, ast.AnnAssign):
            if isinstance(item.target, ast.Name):
                entry["class_vars"].append(item.target.id)
    return entry


def build_analysis(modules: list[dict[str, object]]) -> str:
    """Convert parsed module data into Markdown for the analysis doc."""
    modules.sort(key=lambda module: module["path"])
    import_map = _build_import_map(modules)
    lines: list[str] = []
    lines.append("## How to Regenerate")
    lines.append("")
    lines.append("```bash")
    lines.append("python tools/generate_codebase_analysis.py")
    lines.append("python tools/generate_codebase_graphs.py")
    lines.append("```")
    lines.append("")
    lines.append("## Entry Points")
    lines.append("")
    lines.append("- `main.py` -> `hololive_coliseum.game.main()`")
    lines.append("- `python -m hololive_coliseum` -> `hololive_coliseum.game.main()`")
    lines.append("")
    lines.append("## High-Level Pipelines")
    lines.append("")
    lines.append("### Game Runtime Loop")
    lines.append("")
    lines.append("- `Game.__init__` configures managers, loads settings, and builds menus.")
    lines.append("- `LevelManager.setup_level` instantiates player/enemies and map objects.")
    lines.append("- `Game.run` handles menu state, input, AI, collisions, HUD, saves.")
    lines.append("")
    lines.append("### Asset Pipeline")
    lines.append("")
    lines.append("- `placeholder_sprites.ensure_placeholder_sprites` writes missing PNGs.")
    lines.append("- `game._load` loads images or falls back to an in-memory icon surface.")
    lines.append("")
    lines.append("### Save/Load Pipeline")
    lines.append("")
    lines.append("- `save_manager.load_settings/load_inventory` read JSON from `SavedGames`.")
    lines.append("- `save_manager.save_settings/save_inventory` persist state on exit.")
    lines.append("- `wipe_saves` removes files under `SavedGames`.")
    lines.append("")
    lines.append("### Auto-Dev Pipeline")
    lines.append("")
    lines.append("- `auto_dev_*` managers feed `AutoDevPipeline` and HUD summaries.")
    lines.append(
        "- `WorldGenerationManager.generate_region_from_seed` composes MMO metadata."
    )
    lines.append("")
    lines.append("### Networking and State Sync")
    lines.append("")
    lines.append("- `network.NetworkManager` handles sockets and relay state.")
    lines.append("- `node_registry` and `state_sync` store shared state snapshots.")
    lines.append("")
    lines.append("## Module Inventory")
    lines.append("")
    for module in modules:
        lines.extend(_render_module(module, import_map.get(module["path"], [])))
    return "\n".join(lines) + "\n"


def _build_import_map(modules: list[dict[str, object]]) -> dict[str, list[str]]:
    import_map: dict[str, list[str]] = {}
    for module in modules:
        path = module["path"]
        imports = set(module.get("imports", []))
        for item in module.get("from_imports", []):
            base = item.get("module") or ""
            level = item.get("level", 0)
            if base:
                if level:
                    base = "." * level + base
                imports.add(base)
        import_map[path] = sorted(imports)
    return import_map


def _render_module(module: dict[str, object], imports: list[str]) -> list[str]:
    lines: list[str] = []
    lines.append("### `" + module["path"] + "`")
    doc = (module.get("docstring") or "").strip().replace("\n", " ")
    lines.append("")
    lines.append("- docstring: " + (doc if doc else "(none)"))
    lines.append("- imports:")
    lines.extend(_format_list(imports))
    globals_list = sorted(set(module.get("globals", [])))
    lines.append("- globals:")
    lines.extend(_format_list(globals_list))
    classes = module.get("classes", [])
    lines.append("- classes:")
    if not classes:
        lines.append("  - (none)")
    else:
        for cls in classes:
            bases = ", ".join(cls.get("bases", [])) or "(none)"
            lines.append("  - " + cls["name"] + " (bases: " + bases + ")")
            cls_doc = (cls.get("doc") or "").strip().replace("\n", " ")
            if cls_doc:
                lines.append("    doc: " + cls_doc)
            class_vars = sorted(set(cls.get("class_vars", [])))
            lines.append("    class_vars:")
            lines.extend(_format_list(class_vars, indent="      "))
            methods = cls.get("methods", [])
            lines.append("    methods:")
            if not methods:
                lines.append("      - (none)")
            else:
                for method in methods:
                    args = ", ".join(method.get("args", []))
                    returns = method.get("returns") or ""
                    sig = method["name"] + "(" + args + ")"
                    if returns:
                        sig += " -> " + returns
                    lines.append("      - " + sig)
    funcs = module.get("functions", [])
    lines.append("- functions:")
    if not funcs:
        lines.append("  - (none)")
    else:
        for func in funcs:
            args = ", ".join(func.get("args", []))
            returns = func.get("returns") or ""
            sig = func["name"] + "(" + args + ")"
            if returns:
                sig += " -> " + returns
            lines.append("  - " + sig)
    lines.append("")
    return lines


def _format_list(items: list[str], indent: str = "  ") -> list[str]:
    if not items:
        return [f"{indent}- (none)"]
    return [f"{indent}- {item}" for item in items]


def main() -> None:
    modules = [parse_file(path) for path in walk_py_files(ROOT)]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    content = build_analysis(modules)
    existing = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
    if START_MARKER in existing and END_MARKER in existing:
        pre, rest = existing.split(START_MARKER, 1)
        _, post = rest.split(END_MARKER, 1)
        updated = pre + START_MARKER + "\n" + content + END_MARKER + post
    else:
        updated = (
            "# Codebase Analysis\n\n"
            "Manual notes can live outside the auto-generated section below.\n\n"
            f"{START_MARKER}\n{content}{END_MARKER}\n"
        )
    OUTPUT.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
