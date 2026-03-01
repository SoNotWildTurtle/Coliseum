"""Tests for mmo builder."""

import pytest

from hololive_coliseum import (
    MMOBuilder,
    WorldSeedManager,
    WorldGenerationManager,
    WorldRegionManager,
    WorldPlayerManager,
    VotingManager,
)


def test_builder_creates_managers():
    builder = MMOBuilder()
    managers = builder.build()
    assert isinstance(managers["world_seed"], WorldSeedManager)
    assert isinstance(managers["world_gen"], WorldGenerationManager)
    assert isinstance(managers["world_region"], WorldRegionManager)
    assert isinstance(managers["world_player"], WorldPlayerManager)
    assert isinstance(managers["voting"], VotingManager)
