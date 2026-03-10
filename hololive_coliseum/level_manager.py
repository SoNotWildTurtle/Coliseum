"""Level progression and unlock management."""

from .player import Enemy, BossEnemy, get_player_class
from .gravity_zone import GravityZone
from .platform import Platform, MovingPlatform, CrumblingPlatform
from .save_manager import load_inventory
from .ally_fighter import AllyFighter


class LevelManager:
    """Handle level initialization and reset logic."""

    def __init__(self, game):
        self.game = game

    def setup_level(self) -> None:
        """Initialize or reset gameplay objects for the current selection."""
        g = self.game
        if getattr(g, "player", None) is not None:
            if hasattr(g, "_save_profile_checkpoint"):
                g._save_profile_checkpoint()
            g.coins = g.player.currency_manager.get_balance()
        g.final_time = 0
        g.end_time = 0
        g.show_end_options = False
        g.status_manager._effects.clear()
        g.score = 0
        import os
        import pygame
        g.platforms = pygame.sprite.Group()
        image_dir = os.path.join(os.path.dirname(__file__), "..", "Images")

        def _name_to_file(n: str) -> str:
            base = n.replace(" ", "_").replace("'", "").replace(".", "")
            return f"{base}_right.png"

        name = g.selected_character or "Gawr Gura"
        player_cls = get_player_class(name)
        img = os.path.join(image_dir, _name_to_file(name))
        g.player = player_cls(100, g.ground_y - 60, img)
        g.player.sound_manager = g.sound_manager
        if getattr(g, "autoplay", False):
            g.player.lives = max(1, int(getattr(g, "autoplay_lives", 3)))
        else:
            g.player.lives = max(1, int(getattr(g, "match_lives", 3)))
        if getattr(g, "autoplay", False):
            g._autoplay_log(
                f"Level setup char={name} map={g.selected_map} chapter={g.selected_chapter}"
            )
        if hasattr(g, "apply_vote_balancing"):
            g.apply_vote_balancing(name, g.player)
        g._refresh_weapon_sfx(g.player)
        g.player.camera_manager = g.camera_manager
        g.team_manager.set_team(g.player, 0)
        # Randomize weather and apply its movement effects.
        g.environment_manager.randomize_weather()
        g.player.friction_multiplier = g.environment_manager.get("friction", 1.0)
        if getattr(g, "coins", 0):
            g.player.currency_manager.add(g.coins)
        g.player.platforms = g.platforms
        if hasattr(g, "_hydrate_player_from_profile"):
            g._hydrate_player_from_profile(g.player)
        else:
            inv = load_inventory()
            if inv:
                g.player.inventory.load_from_dict(inv)
        g.difficulty = g.difficulty_levels[g.difficulty_index]
        g.all_sprites = pygame.sprite.Group(g.player)
        g.projectiles = pygame.sprite.Group()
        g.melee_attacks = pygame.sprite.Group()
        g.gravity_zones = pygame.sprite.Group()
        g.healing_zones = pygame.sprite.Group()
        g.damage_numbers = pygame.sprite.Group()
        g.hazard_manager.clear()
        g.hazards = g.hazard_manager.hazards
        g.powerups = pygame.sprite.Group()
        g.enemies = pygame.sprite.Group()
        g.npc_manager.enemies = g.enemies
        g.npc_manager.allies.empty()
        g.allies = g.npc_manager.allies
        g.ai_manager.enemies = g.enemies
        g.spawn_manager.clear()
        g.combat_manager.last_enemy_damage = 0
        g.hazard_manager.last_damage = 0
        if g.selected_chapter:
            g.map_manager.set_current(g.selected_chapter)
        elif g.selected_map:
            g.map_manager.set_current(g.selected_map)
        map_data = g.map_manager.get_current() or {}
        if not g.selected_chapter and not g.selected_map:
            map_data = dict(map_data)
            map_data["minions"] = 0
        map_size = map_data.get("size")
        if isinstance(map_size, (list, tuple)) and len(map_size) == 2:
            g.world_width = int(map_size[0])
            g.world_height = int(map_size[1])
        else:
            g.world_width = g.width
            g.world_height = g.height
        g.ground_y = g.world_height - 50
        g.ground_gaps = list(map_data.get("ground_gaps", []))
        spawn = map_data.get(
            "spawn",
            (int(g.world_width * 0.2), g.ground_y - 60),
        )
        if isinstance(spawn, (list, tuple)) and len(spawn) == 2:
            g.player.spawn_point = pygame.math.Vector2(spawn[0], spawn[1])
            g.player.pos.update(spawn)
            g.player.rect.topleft = (int(spawn[0]), int(spawn[1]))
            g.player.velocity.update(0, 0)
        g.player.ground_gaps = list(g.ground_gaps)
        if hasattr(g, "objective_manager"):
            g.objective_manager.ensure_region_objectives(
                map_data,
                g.selected_map or g.selected_chapter or "Arena",
            )

        faction = map_data.get(
            "faction",
            g.selected_chapter
            or g.selected_map
            or ("Arena Challengers" if g.multiplayer else "Arena"),
        )
        minion_reward = map_data.get("minion_reputation", 5)
        boss_reward = map_data.get("boss_reputation", 20)

        enemy_start = int(min(g.world_width - 200, max(g.world_width * 0.65, 320)))
        if g.autoplay:
            ally_count = int(getattr(g, "autoplay_allies", 0))
        else:
            ally_count = int(getattr(g, "match_allies", 0))
        if ally_count > 0:
            for idx in range(ally_count):
                name = g.characters[(idx + 1) % len(g.characters)] if g.characters else "Gawr Gura"
                ally_img = os.path.join(image_dir, _name_to_file(name))
                ally = AllyFighter(
                    int(g.player.spawn_point.x + (idx + 1) * 50),
                    g.ground_y - 60,
                    ally_img,
                    difficulty=g.difficulty,
                )
                ally.platforms = g.platforms
                ally.ground_gaps = list(g.ground_gaps)
                ally.world_width = g.world_width
                ally.spawn_point = pygame.math.Vector2(
                    g.player.spawn_point.x + (idx + 1) * 50,
                    g.player.spawn_point.y,
                )
                ally.camera_manager = g.camera_manager
                ally.sound_manager = g.sound_manager
                if g.autoplay:
                    ally.lives = max(1, int(getattr(g, "autoplay_ally_lives", 3)))
                else:
                    ally.lives = max(1, int(getattr(g, "match_lives", 3)))
                g.allies.add(ally)
                g.all_sprites.add(ally)
                g.team_manager.set_team(ally, 0)
                g._refresh_weapon_sfx(ally)
        for i in range(g.ai_players):
            e = Enemy(
                enemy_start + i * 60,
                g.ground_y - 60,
                os.path.join(image_dir, "enemy_right.png"),
                difficulty=g.difficulty,
                faction=faction,
                reputation_reward=minion_reward,
            )
            e.platforms = g.platforms
            e.ground_gaps = list(g.ground_gaps)
            e.world_width = g.world_width
            e.last_ai_action = -e.AI_LEVELS[g.difficulty]["react_ms"]
            e.sound_manager = g.sound_manager
            g.enemies.add(e)
            g.all_sprites.add(e)
            g.team_manager.set_team(e, 1)
            g._refresh_weapon_sfx(e)
        for gz in map_data.get("gravity_zones", []):
            rect = pygame.Rect(*gz["rect"])
            zone = GravityZone(rect, gz.get("multiplier", 1.0))
            g.gravity_zones.add(zone)
            g.all_sprites.add(zone)
        for p in map_data.get("platforms", []):
            rect = pygame.Rect(*p)
            plat = Platform(rect)
            g.platforms.add(plat)
            g.all_sprites.add(plat)
        for cp in map_data.get("crumbling_platforms", []):
            rect = pygame.Rect(*(cp["rect"] if isinstance(cp, dict) else cp))
            delay = cp.get("delay", 60) if isinstance(cp, dict) else 60
            plat = CrumblingPlatform(rect, delay)
            g.platforms.add(plat)
            g.all_sprites.add(plat)
        g.hazard_manager.load_from_data(map_data.get("hazards", []))
        for h in g.hazard_manager.hazards:
            g.all_sprites.add(h)
        for mp in map_data.get("moving_platforms", []):
            rect = pygame.Rect(*mp["rect"])
            plat = MovingPlatform(rect, mp.get("offset", (0, 0)), mp.get("speed", 1))
            g.platforms.add(plat)
            g.all_sprites.add(plat)
        # Spawn additional enemies from map data
        minions = map_data.get("minions", 0)
        start_x = enemy_start + g.ai_players * 60
        for i in range(minions):
            e = Enemy(
                start_x + i * 60,
                g.ground_y - 60,
                os.path.join(image_dir, "enemy_right.png"),
                difficulty=g.difficulty,
                faction=faction,
                reputation_reward=minion_reward,
            )
            e.platforms = g.platforms
            e.ground_gaps = list(g.ground_gaps)
            e.world_width = g.world_width
            e.sound_manager = g.sound_manager
            g.enemies.add(e)
            g.all_sprites.add(e)
            g.team_manager.set_team(e, 1)
            g._refresh_weapon_sfx(e)
        boss_name = map_data.get("boss")
        if boss_name:
            img_path = os.path.join(image_dir, _name_to_file(boss_name))
            boss = BossEnemy(
                int(min(g.world_width - 150, max(g.world_width * 0.8, 520))),
                g.ground_y - 60,
                img_path,
                g.difficulty,
                faction=faction,
                reputation_reward=boss_reward,
            )
            boss.health_manager.max_health = 200
            boss.health_manager.health = 200
            boss.platforms = g.platforms
            boss.ground_gaps = list(g.ground_gaps)
            boss.world_width = g.world_width
            boss.sound_manager = g.sound_manager
            g.enemies.add(boss)
            g.all_sprites.add(boss)
            g.team_manager.set_team(boss, 1)
            g._refresh_weapon_sfx(boss)
        now = pygame.time.get_ticks()
        g.mob_spawn_config = dict(map_data.get("mob_spawn", {}) or {})
        if getattr(g, "match_mobs", False):
            if not g.mob_spawn_config:
                g.mob_spawn_config = {
                    "interval": int(getattr(g, "match_mob_interval", 3500)),
                    "wave": int(getattr(g, "match_mob_wave", 2)),
                    "max": int(getattr(g, "match_mob_max", 8)),
                }
            else:
                g.mob_spawn_config.setdefault(
                    "interval", int(getattr(g, "match_mob_interval", 3500))
                )
                g.mob_spawn_config.setdefault(
                    "wave", int(getattr(g, "match_mob_wave", 2))
                )
                g.mob_spawn_config.setdefault(
                    "max", int(getattr(g, "match_mob_max", 8))
                )
        g.mob_spawn_enabled = (
            bool(g.mob_spawn_config)
            or bool(getattr(g, "autoplay_mobs", False))
            or bool(getattr(g, "match_mobs", False))
        )
        tuning = getattr(g, "auto_dev_tuning", None)
        if tuning and g.mob_spawn_config:
            g.mob_spawn_config = tuning.adjust_mob_spawn_config(g.mob_spawn_config)
        g.mob_spawn_last = now
        base_offsets = [
            ("heal", 5000),
            ("mana", 6000),
            ("speed", 7000),
            ("stamina", 8000),
            ("shield", 9000),
            ("attack", 10000),
            ("defense", 10500),
            ("life", 11000),
            ("xp", 11500),
        ]
        base_schedule = {name: delay for name, delay in base_offsets}
        tuning = getattr(g, "auto_dev_tuning", None)
        adjusted = base_schedule
        if tuning:
            adjusted = tuning.recommend_spawn_timers(base_schedule)
            g.auto_dev_support_plan = tuning.support_plan()
        else:
            g.auto_dev_support_plan = None
        projection_manager = getattr(g, "auto_dev_projection_manager", None)
        if projection_manager:
            summary = projection_manager.projection_summary()
            g.auto_dev_projection_summary = summary or None
        else:
            g.auto_dev_projection_summary = None
        for name, delay in base_offsets:
            g.spawn_manager.schedule(name, now + int(adjusted.get(name, delay)))
        g.apply_event_modifiers()
