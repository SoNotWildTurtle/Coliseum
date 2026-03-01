# GitHub Code Requirements

This project follows several conventions to keep pull requests easy to review.

- Keep lines under 100 characters and avoid trailing spaces.
- Provide a short module-level docstring for each file describing its purpose.
- Do not commit binary image or sound files; placeholder assets are created at runtime.
- Run `pip install -r requirements.txt` and `pytest -q` before committing to ensure tests pass.
- Use Python 3.10+ (the codebase uses modern type syntax).
- Use descriptive commit messages and keep pull requests focused.
- Tests that depend on Pygame should call `pytest.importorskip("pygame")`.

Refer to `AGENTS.md` for additional contributor guidelines.
