"""Pytest fixtures for Hololive Coliseum tests."""

import os
import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pytest.importorskip("pygame")
