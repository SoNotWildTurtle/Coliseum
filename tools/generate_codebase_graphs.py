"""Generate docs/CODEBASE_GRAPHS.md with module and call interaction graphs."""

from __future__ import annotations

import ast
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "CODEBASE_GRAPHS.md"
START_MARKER = "<!-- AUTO-GENERATED:codebase-graphs:start -->"
END_MARKER = "<!-- AUTO-GENERATED:codebase-graphs:end -->"
SKIP_DIRS = {".git", "__pycache__", "venv", ".venv", "node_modules"}
INCLUDE_ROOT = {"main.py"}
INCLUDE_PACKAGE = "hololive_coliseum"


class ModuleInfo:
    """Container for parsed module details."""

    def __init__(self, path: Path, module_name: str) -> None:
        self.path = path
        self.module_name = module_name
        self.imports: set[str] = set()
        self.from_imports: dict[str, str] = {}
        self.functions: set[str] = set()
        self.classes: dict[str, set[str]] = {}
        self.calls: dict[str, set[str]] = defaultdict(set)


def walk_py_files(root: Path) -> list[Path]:
    """Return python files that should be included in the graphs."""
    files: list[Path] = []
    for path in root.rglob("*.py"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        rel = path.relative_to(root)
        if rel.parts[0] == INCLUDE_PACKAGE or rel.name in INCLUDE_ROOT:
            files.append(path)
    return files


def module_name_from_path(path: Path) -> str:
    rel = path.relative_to(ROOT)
    if rel.name == "__init__.py":
        parts = rel.parts[:-1]
    else:
        parts = rel.with_suffix("").parts
    return ".".join(parts)


def parse_module(path: Path) -> ModuleInfo:
    module_name = module_name_from_path(path)
    info = ModuleInfo(path, module_name)
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                info.imports.add(alias.name)
                if alias.asname:
                    info.from_imports[alias.asname] = alias.name
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            if node.level:
                base = "." * node.level + base if base else "." * node.level
            for alias in node.names:
                name = alias.asname or alias.name
                info.from_imports[name] = base + "." + alias.name if base else alias.name
        elif isinstance(node, ast.FunctionDef):
            info.functions.add(node.name)
        elif isinstance(node, ast.ClassDef):
            methods = set()
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    methods.add(item.name)
            info.classes[node.name] = methods
    collect_calls(info, tree)
    return info


def collect_calls(info: ModuleInfo, tree: ast.Module) -> None:
    """Collect call edges for module-level and class methods."""

    def resolve_call_name(node: ast.AST, current_class: str | None) -> str | None:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name):
                owner = node.value.id
                return f"{owner}.{node.attr}"
        return None

    class CallVisitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.current = "module"
            self.current_class: str | None = None

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            prev_current = self.current
            prev_class = self.current_class
            self.current_class = node.name
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    self.current = f"{node.name}.{item.name}"
                    self.generic_visit(item)
            self.current = prev_current
            self.current_class = prev_class

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            if self.current == "module":
                self.current = node.name
                self.generic_visit(node)
                self.current = "module"

        def visit_Call(self, node: ast.Call) -> None:
            called = resolve_call_name(node.func, self.current_class)
            if called:
                info.calls[self.current].add(called)
            self.generic_visit(node)

    CallVisitor().visit(tree)


def build_module_dependency_graph(modules: dict[str, ModuleInfo]) -> list[str]:
    lines: list[str] = []
    lines.append("```mermaid")
    lines.append("flowchart TD")
    for module, info in modules.items():
        for imp in sorted(info.imports):
            target = resolve_local_import(imp, modules)
            if target:
                lines.append(f"  {sanitize(module)} --> {sanitize(target)}")
    lines.append("```")
    return lines


def build_call_graph(modules: dict[str, ModuleInfo]) -> list[str]:
    lines: list[str] = []
    lines.append("```mermaid")
    lines.append("flowchart TD")
    for module, info in modules.items():
        for caller, callees in info.calls.items():
            caller_id = sanitize(f"{module}:{caller}")
            for callee in sorted(callees):
                target = resolve_call_target(callee, info, modules)
                if not target:
                    continue
                callee_id = sanitize(target)
                lines.append(f"  {caller_id} --> {callee_id}")
    lines.append("```")
    return lines


def resolve_local_import(import_name: str, modules: dict[str, ModuleInfo]) -> str | None:
    if import_name in modules:
        return import_name
    if import_name.startswith("."):
        dotted = import_name.lstrip(".")
        if dotted in modules:
            return dotted
    if import_name in modules:
        return import_name
    for name in modules:
        if name.endswith(import_name):
            return name
    return None


def resolve_call_target(
    call: str, info: ModuleInfo, modules: dict[str, ModuleInfo]
) -> str | None:
    if call in info.functions:
        return f"{info.module_name}:{call}"
    for cls, methods in info.classes.items():
        if call == f"{cls}.{call.split('.')[-1]}" or call in methods:
            if call.startswith(cls + "."):
                return f"{info.module_name}:{call}"
    if "." in call:
        owner, name = call.split(".", 1)
        target = info.from_imports.get(owner)
        if target:
            target_module = target.rsplit(".", 1)[0]
            target_symbol = target.rsplit(".", 1)[-1]
            if target_module in modules:
                return f"{target_module}:{target_symbol}"
    imported = info.from_imports.get(call)
    if imported:
        target_module = imported.rsplit(".", 1)[0]
        target_symbol = imported.rsplit(".", 1)[-1]
        if target_module in modules:
            return f"{target_module}:{target_symbol}"
    return None


def sanitize(label: str) -> str:
    return label.replace(".", "_").replace(":", "__").replace("-", "_")


def build_document(modules: dict[str, ModuleInfo]) -> str:
    lines: list[str] = []
    lines.append("## Module Dependency Graph")
    lines.append("")
    lines.append("Local module imports within the `hololive_coliseum` package and root")
    lines.append("entry points. External libraries are excluded.")
    lines.append("")
    lines.extend(build_module_dependency_graph(modules))
    lines.append("")
    lines.append("## Call Graph")
    lines.append("")
    lines.append("Function/method calls resolved within the local package. Indirect or")
    lines.append("dynamic calls may not appear, but this captures the primary flow.")
    lines.append("")
    lines.extend(build_call_graph(modules))
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    modules: dict[str, ModuleInfo] = {}
    for path in walk_py_files(ROOT):
        info = parse_module(path)
        modules[info.module_name] = info
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    content = build_document(modules)
    existing = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
    if START_MARKER in existing and END_MARKER in existing:
        pre, rest = existing.split(START_MARKER, 1)
        _, post = rest.split(END_MARKER, 1)
        updated = pre + START_MARKER + "\n" + content + END_MARKER + post
    else:
        updated = (
            "# Codebase Graphs\n\n"
            "Manual notes can live outside the auto-generated section below.\n\n"
            f"{START_MARKER}\n{content}\n{END_MARKER}\n"
        )
    OUTPUT.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
