"""Tests for camera manager."""

import pytest

pytest.importorskip("pygame")
import pygame

from hololive_coliseum import CameraManager, ThirdPersonCamera


def test_camera_follow_and_apply():
    cam = CameraManager()
    rect = pygame.Rect(100, 100, 10, 10)
    cam.follow(rect, (200, 200))
    applied = cam.apply(rect)
    assert applied.center == (100, 100)


def test_third_person_camera_offsets_view():
    cam = ThirdPersonCamera()
    rect = pygame.Rect(100, 100, 10, 10)
    cam.follow(rect, (200, 200))
    applied = cam.apply(rect)
    assert applied.centery == 50


def test_camera_shake(monkeypatch):
    cam = CameraManager()
    rect = pygame.Rect(0, 0, 10, 10)
    now = 1000

    monkeypatch.setattr(pygame.time, "get_ticks", lambda: now)
    cam.shake(100, 5)
    cam.update()
    shaken = cam.apply(rect)
    assert shaken.topleft != rect.topleft

    now = 1200
    monkeypatch.setattr(pygame.time, "get_ticks", lambda: now)
    cam.update()
    reset = cam.apply(rect)
    assert reset.topleft == rect.topleft
