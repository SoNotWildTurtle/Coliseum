"""Tests for screenshot manager."""

import os
import pytest

from hololive_coliseum.screenshot_manager import ScreenshotManager

pygame = pytest.importorskip("pygame")


def test_capture_saves_file(tmp_path):
    pygame.display.init()
    surface = pygame.Surface((10, 10))
    surface.fill((255, 0, 0))
    sm = ScreenshotManager()
    sm.directory = tmp_path
    path = sm.capture(surface, "test.png")
    assert os.path.exists(path)
    pygame.display.quit()
