# Agent Coding Guidelines

This repository uses many small modules with unit tests.
Follow these tips to keep pull requests easy to review and merge:

- Keep lines under 100 characters when possible and avoid trailing spaces.
- Each module should include a short docstring explaining its purpose.
- Update README and docs when adding or changing features.
- Do not commit binary images or sound assets; placeholder files are created at runtime.
- Run `pytest -q` before committing to ensure all tests pass.
- Use descriptive commit messages summarizing changes.
- Avoid committing merge conflict markers and keep pull requests small.
- Tests that depend on Pygame should call `pytest.importorskip("pygame")` so the
  suite can skip cleanly when the dependency is missing.

These guidelines help maintainers review PRs quickly and keep the code base consistent.
