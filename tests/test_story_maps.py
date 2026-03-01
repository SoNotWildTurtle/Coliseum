"""Tests for story maps."""

from hololive_coliseum.story_maps import create_story_maps


def test_create_story_maps():
    chars = [f"C{i}" for i in range(1, 5)]
    maps = create_story_maps(chars)
    assert len(maps) == 20
    assert maps["Chapter 3"]["boss"] == "C1"
    assert all("minions" in m for m in maps.values())
    assert maps["Chapter 1"]["minions"] == 1
    assert maps["Chapter 2"]["minions"] >= maps["Chapter 1"]["minions"]
    assert maps["Chapter 3"]["minions"] > maps["Chapter 2"]["minions"]
    assert maps["Chapter 1"]["hazards"]
    # Early chapters use only spike traps
    assert all(h["type"] == "spike" for h in maps["Chapter 1"]["hazards"])
    # Ice hazards appear by chapter 6
    assert any(h["type"] == "ice" for h in maps["Chapter 6"]["hazards"])
    # Lava hazards appear by chapter 11
    assert any(h["type"] == "lava" for h in maps["Chapter 11"]["hazards"])
    # Acid hazards appear by chapter 18
    assert any(h["type"] == "acid" for h in maps["Chapter 18"]["hazards"])
    # Lightning hazards appear by chapter 15
    assert any(h["type"] == "lightning" for h in maps["Chapter 15"]["hazards"])
    # Wind hazards appear by chapter 8
    assert any(h["type"] == "wind" for h in maps["Chapter 8"]["hazards"])
    # Quicksand appears by chapter 14
    assert any(h["type"] == "quicksand" for h in maps["Chapter 14"]["hazards"])
    # Fire hazards appear by chapter 17
    assert any(h["type"] == "fire" for h in maps["Chapter 17"]["hazards"])
    # Frost hazards appear by chapter 16
    assert any(h["type"] == "frost" for h in maps["Chapter 16"]["hazards"])
    # Silence hazards appear by chapter 19
    assert any(h["type"] == "silence" for h in maps["Chapter 19"]["hazards"])
    # Regen zones appear by chapter 12
    assert any(h["type"] == "regen" for h in maps["Chapter 12"]["hazards"])
    # Gravity zones increase from one to three by late chapters
    assert len(maps["Chapter 2"]["gravity_zones"]) == 2
    assert any(z["rect"][0] > 800 for z in maps["Chapter 2"]["gravity_zones"])
    assert len(maps["Chapter 4"]["gravity_zones"]) == 2
    assert any(z["rect"][0] > 800 for z in maps["Chapter 4"]["gravity_zones"])
    assert len(maps["Chapter 8"]["gravity_zones"]) >= 2
    assert len(maps["Chapter 15"]["gravity_zones"]) >= 3
    assert len(maps["Chapter 15"]["hazards"]) >= len(maps["Chapter 1"]["hazards"])
    # Platforms are included and grow more complex with gaps later on
    assert "platforms" in maps["Chapter 1"]
    assert maps["Chapter 1"]["platforms"][0][2] == 1600
    assert any(h["rect"][0] > 800 for h in maps["Chapter 1"]["hazards"])
    assert maps["Chapter 3"]["platforms"][0][2] == 1600
    assert any(h["rect"][0] > 800 for h in maps["Chapter 3"]["hazards"])
    assert maps["Chapter 5"]["platforms"][0][2] == 1600
    assert any(h["rect"][0] > 800 for h in maps["Chapter 5"]["hazards"])
    assert maps["Chapter 6"]["platforms"][0][2] == 1600
    assert any(h["rect"][0] > 800 for h in maps["Chapter 6"]["hazards"])
    assert maps["Chapter 7"]["platforms"][0][2] == 1600
    assert any(h["rect"][0] > 800 for h in maps["Chapter 7"]["hazards"])
    assert maps["Chapter 8"]["platforms"][0][2] == 1600
    assert any(h["rect"][0] > 800 for h in maps["Chapter 8"]["hazards"])
    assert maps["Chapter 9"]["size"] == (1600, 600)
    assert maps["Chapter 9"]["platforms"][0][2] == 1600
    assert any(h["rect"][0] > 800 for h in maps["Chapter 9"]["hazards"])
    assert maps["Chapter 10"]["size"] == (1600, 600)
    assert maps["Chapter 10"]["platforms"][0][2] == 1600
    assert any(h["rect"][0] > 800 for h in maps["Chapter 10"]["hazards"])
    assert maps["Chapter 11"]["size"] == (1600, 600)
    assert maps["Chapter 11"]["platforms"][0][2] == 1600
    assert any(h["rect"][0] > 800 for h in maps["Chapter 11"]["hazards"])
    assert maps["Chapter 12"]["size"] == (1600, 600)
    assert maps["Chapter 12"]["platforms"][0][2] == 1600
    assert any(h["rect"][0] > 800 for h in maps["Chapter 12"]["hazards"])
    assert maps["Chapter 13"]["size"] == (1600, 600)
    assert maps["Chapter 13"]["platforms"][0][2] == 1600
    assert any(h["rect"][0] > 800 for h in maps["Chapter 13"]["hazards"])
    assert maps["Chapter 14"]["size"] == (1600, 600)
    assert maps["Chapter 14"]["platforms"][0][2] == 1600
    assert any(h["rect"][0] > 800 for h in maps["Chapter 14"]["hazards"])
    assert maps["Chapter 15"]["size"] == (1600, 600)
    assert maps["Chapter 15"]["platforms"][0][2] == 1600
    assert any(h["rect"][0] > 800 for h in maps["Chapter 15"]["hazards"])
    assert maps["Chapter 16"]["size"] == (1600, 600)
    assert maps["Chapter 16"]["platforms"][0][2] == 1600
    assert any(h["rect"][0] > 800 for h in maps["Chapter 16"]["hazards"])
    assert maps["Chapter 17"]["size"] == (1600, 600)
    assert any(p[0] > 800 for p in maps["Chapter 17"]["platforms"])
    assert any(h["rect"][0] > 800 for h in maps["Chapter 17"]["hazards"])
    assert maps["Chapter 18"]["size"] == (1600, 600)
    assert any(p[0] > 800 for p in maps["Chapter 18"]["platforms"])
    assert any(h["rect"][0] > 800 for h in maps["Chapter 18"]["hazards"])
    assert maps["Chapter 19"]["size"] == (1600, 600)
    assert any(p[0] > 800 for p in maps["Chapter 19"]["platforms"])
    assert any(h["rect"][0] > 800 for h in maps["Chapter 19"]["hazards"])
    assert maps["Chapter 20"]["size"] == (1600, 600)
    assert any(p[0] > 800 for p in maps["Chapter 20"]["platforms"])
    assert any(h["rect"][0] > 800 for h in maps["Chapter 20"]["hazards"])
    assert maps["Chapter 10"]["moving_platforms"]
