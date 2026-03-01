"""Story map definitions and metadata."""

from __future__ import annotations

"""Utilities to generate maps for story mode."""

from typing import List, Dict


def create_story_maps(characters: List[str]) -> Dict[str, Dict]:
    """Return a dictionary of map data for the 20 story chapters.

    Each chapter spawns minion enemies with counts that increase over time.
    Every third chapter also includes a boss from the provided roster.
    """
    maps: Dict[str, Dict] = {}
    map_width = 1600
    map_height = 600
    ground_y = map_height - 50
    side_gap = 0

    def _ground_gaps_from_segments(
        segments: list[tuple[int, int, int, int]],
        width: int,
        min_gap: int = 40,
    ) -> list[tuple[int, int]]:
        ranges = sorted((seg[0], seg[0] + seg[2]) for seg in segments)
        gaps: list[tuple[int, int]] = []
        cursor = 0
        for start, end in ranges:
            if start - cursor >= min_gap:
                gaps.append((cursor, start))
            cursor = max(cursor, end)
        if width - cursor >= min_gap:
            gaps.append((cursor, width))
        return gaps
    boss_index = 0
    for i in range(1, 21):
        hazards = []
        # Introduce hazard types gradually: spikes first, then ice, lava and acid
        hazard_pool = ["spike"]
        if i >= 6:
            hazard_pool.append("ice")
        if i >= 11:
            hazard_pool.append("lava")
        if i >= 15:
            hazard_pool.append("lightning")
        if i >= 14:
            hazard_pool.append("quicksand")
        if i >= 16:
            hazard_pool.append("frost")
        if i >= 17:
            hazard_pool.append("fire")
        if i >= 18:
            hazard_pool.append("acid")
        if i >= 19:
            hazard_pool.append("silence")
        if i >= 12:
            hazard_pool.append("regen")
        count = max(i // 5 + 1, len(hazard_pool))
        lane_width = max(1, map_width - side_gap * 2 - 60)
        for j in range(count):
            htype = hazard_pool[j % len(hazard_pool)]
            x = side_gap + (j * 170) % lane_width
            y = ground_y - 30 - (j % 2) * 30
            hazards.append({"type": htype, "rect": (x, y, 40, 20)})

        if i <= 20:
            hazards.append(
                {
                    "type": "spike",
                    "rect": (map_width - side_gap - 180, ground_y - 20, 40, 20),
                }
            )
        if i >= 8:
            hazards.append(
                {
                    "type": "wind",
                    "rect": (side_gap - 40, ground_y - 50, 100, 40),
                    "force": 2,
                }
            )
        if i >= 7:
            hazards.append(
                {"type": "bounce", "rect": (side_gap + 120, ground_y - 30, 70, 20)}
            )
        if i >= 13:
            hazards.append(
                {
                    "type": "teleport",
                    "rect": (map_width - side_gap - 260, ground_y - 40, 70, 20),
                    "target": (side_gap + 120, ground_y - 130),
                }
            )

        gravity_zones = []
        # Alternate low and high gravity, add more zones in later chapters
        if i % 2 == 0:
            gravity_zones.append(
                {"rect": (side_gap + 200, 400, 120, 50), "multiplier": 0.2}
            )
        else:
            gravity_zones.append(
                {"rect": (side_gap + 360, 420, 100, 40), "multiplier": 1.5}
            )
        if i <= 20:
            gravity_zones.append(
                {
                    "rect": (map_width - side_gap - 260, 420, 120, 50),
                    "multiplier": 1.5,
                }
            )
        if i >= 9:
            gravity_zones.append(
                {"rect": (side_gap + 520, 380, 120, 50), "multiplier": 2.0}
            )
        if i >= 15:
            gravity_zones.append(
                {"rect": (side_gap + 40, 360, 100, 40), "multiplier": 0.5}
            )

        # Keep a full-width base floor for consistent story-map dimensions.
        floor = [(side_gap, ground_y, map_width - side_gap * 2, 50)]
        platforms = list(floor)
        variant = i % 4
        if variant == 0:
            platforms.extend(
                [
                    (side_gap + 140, 440, 140, 20),
                    (side_gap + 420, 380, 140, 20),
                    (side_gap + 720, 320, 140, 20),
                ]
            )
        elif variant == 1:
            platforms.extend(
                [
                    (side_gap + 120, 480, 110, 20),
                    (side_gap + 320, 430, 110, 20),
                    (side_gap + 520, 380, 110, 20),
                    (side_gap + 720, 330, 110, 20),
                ]
            )
        elif variant == 2:
            platforms.extend(
                [
                    (side_gap + 120, 420, 180, 20),
                    (side_gap + 460, 380, 180, 20),
                    (side_gap + 820, 340, 180, 20),
                ]
            )
        else:
            platforms.extend(
                [
                    (side_gap + 240, 460, 120, 20),
                    (side_gap + 500, 410, 180, 20),
                    (side_gap + 840, 350, 140, 20),
                ]
            )
        for j in range(i // 5):
            platforms.append(
                (side_gap + 80 + j * 170, 440 - 25 * j, 130, 18)
            )
        if i >= 9:
            platforms.append((map_width - 320, 360, 160, 20))
        moving_platforms = []
        if i >= 6:
            moving_platforms.append(
                {
                    "rect": (map_width // 2 + 140, 490, 100, 20),
                    "offset": (0, -120),
                    "speed": 2,
                }
            )
        if i >= 10:
            moving_platforms.append(
                {
                    "rect": (side_gap + 80, 500, 90, 20),
                    "offset": (180, 0),
                    "speed": 2,
                }
            )
        if i >= 12:
            moving_platforms.append(
                {
                    "rect": (side_gap + 540, 360, 90, 20),
                    "offset": (180, 0),
                    "speed": 3,
                }
            )
        if i >= 16:
            moving_platforms.append(
                {
                    "rect": (map_width - side_gap - 320, 320, 90, 20),
                    "offset": (140, -80),
                    "speed": 2,
                }
            )
        crumbling_platforms = []
        if i >= 8:
            crumbling_platforms.append({"rect": (side_gap + 260, 470, 90, 20)})
        if i >= 12:
            crumbling_platforms.append({"rect": (side_gap + 460, 430, 90, 20)})
        if i >= 15:
            crumbling_platforms.append({"rect": (side_gap + 720, 390, 90, 20)})

        minions = 1 + (i - 1) // 2 + (1 if i % 5 == 0 else 0)
        data: Dict[str, object] = {
            "gravity_zones": gravity_zones,
            "hazards": hazards,
            "platforms": platforms,
            "moving_platforms": moving_platforms,
            "crumbling_platforms": crumbling_platforms,
            "minions": minions,
        }
        if i <= 20:
            data["size"] = (map_width, map_height)
            data["ground_gaps"] = _ground_gaps_from_segments(floor, map_width)
            data["spawn"] = (side_gap + 120, ground_y - 60)
        if i % 3 == 0:
            boss_name = characters[boss_index % len(characters)]
            boss_index += 1
            data["boss"] = boss_name
            data["minions"] += 1  # extra challenge on boss stages
        maps[f"Chapter {i}"] = data
    return maps
