"""Main game module handling menus, gameplay loop and networking."""

import os
import random
import math
import json
from datetime import datetime, timedelta, timezone
import pygame
from cryptography.hazmat.primitives import serialization

from .player import (
    PlayerCharacter,
    GuraPlayer,
    WatsonPlayer,
    InaPlayer,
    KiaraPlayer,
    CalliopePlayer,
    FaunaPlayer,
    KroniiPlayer,
    IRySPlayer,
    MumeiPlayer,
    BaelzPlayer,
    FubukiPlayer,
    MikoPlayer,
    AquaPlayer,
    PekoraPlayer,
    MarinePlayer,
    SuiseiPlayer,
    AyamePlayer,
    NoelPlayer,
    FlarePlayer,
    SubaruPlayer,
    SoraPlayer,
    Enemy,
    BossEnemy,
    character_class_exists,
    CHARACTER_CLASSES,
    get_player_class,
)
from .projectile import Projectile, ExplodingProjectile
from .melee_attack import MeleeAttack
from .gravity_zone import GravityZone
from .hazards import SpikeTrap, IceZone, LavaZone
from .hazard_manager import HazardManager
from .powerup import PowerUp
from .healing_zone import HealingZone
from .loot_manager import LootManager
from .damage_number import CheerText
from .map_manager import MapManager
from .environment_manager import EnvironmentManager
from .spawn_manager import SpawnManager
from .event_manager import EventManager
from .event_modifier_manager import EventModifierManager
from .save_manager import (
    load_inventory,
    load_settings,
    save_inventory,
    save_settings,
    wipe_saves,
)
from .network import NetworkManager
from .node_registry import load_nodes
from .keybind_manager import KeybindManager
from .input_manager import InputManager
from .chat_manager import ChatManager
from .accessibility_manager import AccessibilityManager
from .menus import MenuMixin, MENU_BG_COLOR, MENU_TEXT_COLOR
from .accounts import (
    register_account,
    delete_account,
    AccountsManager,
    load_private_key,
)
from .status_effects import (
    StatusEffectManager,
    FreezeEffect,
    SlowEffect,
    SpeedEffect,
    ShieldEffect,
    AttackEffect,
    DefenseEffect,
)
from .ai_manager import AIManager
from .npc_manager import NPCManager
from .ally_manager import AllyManager
from .menu_manager import MenuManager
from .game_state_manager import GameStateManager
from .sound_manager import SoundManager
from .hud_manager import HUDManager
from .camera_manager import CameraManager
from .combat_manager import CombatManager
from .level_manager import LevelManager
from .item_manager import ItemManager, Item
from .score_manager import ScoreManager
from .team_manager import TeamManager
from .world_generation_manager import WorldGenerationManager
from .world_player_manager import WorldPlayerManager
from .mmo_presence_manager import MMOPresenceManager
from .shared_state_manager import SharedStateManager
from .state_verification_manager import StateVerificationManager
from .mmo_backend_manager import MMOBackendManager
from .mmo_world_state_manager import MMOWorldStateManager
from .auto_dev_pipeline import AutoDevPipeline
from .mining_manager import MiningManager
from .iteration_manager import IterationManager
from .auto_dev_feedback_manager import AutoDevFeedbackManager
from .auto_dev_tuning_manager import AutoDevTuningManager
from .auto_dev_projection_manager import AutoDevProjectionManager
from .screenshot_manager import ScreenshotManager
from .voting_manager import VotingManager
from .achievement_manager import AchievementManager
from .reputation_manager import ReputationManager
from .objective_manager import ObjectiveManager
from .economy_manager import EconomyManager
from .placeholder_sprites import ensure_placeholder_sprites
from .ai_autoplayer import AutoPlayer, KeyState
from .ally_fighter import AllyFighter
from .ai_experience_manager import AIExperienceManager
from .ai_experience_store import AIExperienceStore
from .ai_interaction_manager import AIInteractionManager
from .game_setup import configure_story_and_ui
from .game_mmo_logic import GameMMOLogic
from .game_mmo_flow import GameMMOFlow
from .game_mmo_ui import GameMMOUI
from .game_mmo_automation import GameMMOAutomation
from .mmo_ui import (
    draw_mmo_backdrop,
    draw_mmo_command_panel,
    draw_mmo_footer,
    draw_mmo_header,
    draw_mmo_status_panel,
    mmo_palette,
)
from .mob import MobEnemy
from .ui_metrics import (
    build_ui_metrics_from_user_scale,
    normalize_user_font_scale,
)
from .ui_debug import UIDebugger
from .profile_store import Profile, ProfileStore


CHARACTER_PLAN_FILE = os.path.join(
    os.path.dirname(__file__), '..', 'docs', 'DEV_PLAN_CHARACTERS.md'
)


def load_character_names() -> list[str]:
    """Read character names from ``DEV_PLAN_CHARACTERS.md``."""
    names: list[str] = []
    try:
        with open(CHARACTER_PLAN_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('- **'):
                    names.append(line.split('**')[1])
    except OSError:
        pass
    return names


class Game(MenuMixin, GameMMOLogic, GameMMOFlow, GameMMOAutomation, GameMMOUI):
    """Main game class with menus, AI opponents, networking and settings."""

    @staticmethod
    def _event_target_id(target: object | None) -> str:
        if target is None:
            return "none"
        return f"{target.__class__.__name__}:{id(target)}"

    def emit_event(self, event: dict[str, object]) -> None:
        """Emit an optional gameplay event to the active sink."""

        sink = getattr(self, "event_sink", None)
        if sink is None:
            return
        payload = dict(event)
        payload.setdefault("type", "unknown")
        payload.setdefault("source", "game")
        payload.setdefault("amount", 0.0)
        payload.setdefault("target_id", "unknown")
        payload.setdefault("frame", int(getattr(self, "_event_frame", 0)))
        payload.setdefault("t_ms", int(pygame.time.get_ticks()))
        try:
            sink(payload)
        except Exception:
            return

    def __init__(self, width: int = 1280, height: int = 720):
        if os.environ.get("SDL_VIDEODRIVER") is None:
            force_visible = os.environ.get("HOLO_AUTOPLAY_VISIBLE") == "1"
            headless = os.environ.get("PYGAME_HEADLESS") == "1"
            headless = headless or os.environ.get("PYTEST_CURRENT_TEST")
            if os.name != "nt":
                if not os.environ.get("DISPLAY") and not os.environ.get(
                    "WAYLAND_DISPLAY"
                ):
                    headless = True
            if headless and not force_visible:
                os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()
        self.settings = load_settings()
        self.event_sink = None
        self._event_frame = 0
        self.coins = self.settings.get("coins", 0)
        self.profile_store = ProfileStore()
        self.profile_id = str(
            os.environ.get("HOLO_PROFILE_ID")
            or self.settings.get("account_id")
            or "default"
        )
        self.profile: Profile = self.profile_store.load(self.profile_id)
        self.profile_warnings: list[str] = list(self.profile.validation_warnings)
        self._bootstrap_profile_from_legacy_settings()
        self._apply_profile_to_global_progression()
        self.width = self.settings.get("width", width)
        self.height = self.settings.get("height", height)
        self.world_width = self.width
        self.world_height = self.height
        self.window_sizes = [
            (960, 540),
            (1024, 576),
            (1280, 720),
            (1366, 768),
            (1440, 900),
            (1600, 900),
            (1680, 1050),
            (1920, 1080),
            (1024, 768),
            (1280, 800),
            (1280, 960),
            (800, 600),
        ]
        self.window_size_index = 0
        if (self.width, self.height) in self.window_sizes:
            self.window_size_index = self.window_sizes.index(
                (self.width, self.height)
            )
        self.volume = self.settings.get("volume", 1.0)
        self.sfx_profile = self.settings.get("sfx_profile", "Default")
        self.sound_manager = SoundManager(self.volume, profile=self.sfx_profile)
        self.mixer_ready = self.sound_manager.mixer_ready
        self.auto_dev_manager = AutoDevFeedbackManager()
        self.auto_dev_tuning = AutoDevTuningManager(self.auto_dev_manager)
        self.auto_dev_projection_manager = AutoDevProjectionManager(
            self.auto_dev_manager,
            self.auto_dev_tuning,
        )
        self.auto_dev_projection_summary: dict | None = None
        self.auto_dev_support_plan: dict | None = None
        self.world_generation_manager = WorldGenerationManager(
            feedback_manager=self.auto_dev_manager,
            tuning_manager=self.auto_dev_tuning,
            projection_manager=self.auto_dev_projection_manager,
        )
        self.event_modifier_manager = EventModifierManager(
            self.world_generation_manager.region_manager
        )
        self.match_modifiers = self.event_modifier_manager.get_config()
        self.xp_multiplier = float(
            self.match_modifiers.get("xp_multiplier", 1.0)
        )
        self.mining_manager = MiningManager(
            world_gen=self.world_generation_manager
        )
        self.mining_enabled = self.settings.get("mining", False)
        self.autoplay_mining = os.environ.get("HOLO_AUTOPLAY_MINING") == "1"
        self.autoplay_mining_intensity = float(
            os.environ.get("HOLO_AUTOPLAY_MINING_INTENSITY", "0.2") or 0.2
        )
        if self.autoplay_mining_intensity <= 0:
            self.autoplay_mining_intensity = 0.2
        self.input_method = self.settings.get("input_method", "auto")
        self.display_modes = ["Windowed", "Borderless", "Fullscreen"]
        stored_display_mode = self.settings.get("display_mode")
        if stored_display_mode in self.display_modes:
            self.display_mode = stored_display_mode
        else:
            self.display_mode = (
                "Fullscreen"
                if self.settings.get("fullscreen", False)
                else "Windowed"
            )
        self.fullscreen = self.display_mode == "Fullscreen"
        self.hud_font_sizes = [10, 12, 14, 16, 18]
        self.hud_font_size = int(self.settings.get("hud_font_size", 14))
        if self.hud_font_size not in self.hud_font_sizes:
            self.hud_font_size = 14
        self.autoplay = os.environ.get("HOLO_AUTOPLAY") == "1"
        self.autoplay_flow = os.environ.get("HOLO_AUTOPLAY_FLOW") == "1"
        self.autoplay_explorer = self.autoplay and (
            os.environ.get("HOLO_AUTOPLAY_EXPLORER", "1") == "1"
        )
        self.autoplay_force_mmo = self.autoplay and (
            os.environ.get("HOLO_AUTOPLAY_FORCE_MMO", "0") == "1"
        )
        self.autoplay_extended = (
            self.autoplay and os.environ.get("HOLO_AUTOPLAY_EXTENDED", "0") == "1"
        )
        self.autoplay_full = self.autoplay and (
            os.environ.get("HOLO_AUTOPLAY_FULL", "0") == "1"
        )
        autoplay_ms = int(os.environ.get("HOLO_AUTOPLAY_DURATION", "0") or 0)
        if autoplay_ms <= 0 and self.autoplay_extended:
            autoplay_ms = int(
                os.environ.get("HOLO_AUTOPLAY_EXTENDED_DURATION", "60000") or 60000
            )
        if self.autoplay and autoplay_ms > 0:
            self.autoplay_deadline = pygame.time.get_ticks() + autoplay_ms
        else:
            self.autoplay_deadline = None
        self.autoplay_menu_delay = int(
            os.environ.get("HOLO_AUTOPLAY_MENU_DELAY", "700") or 700
        )
        self.autoplay_menu_state = None
        self.autoplay_menu_stage = 0
        self.autoplay_last_menu_step = pygame.time.get_ticks()
        self.autoplay_preview_index = 0
        self.autoplay_preview_count = 0
        self.autoplay_preview_wait_start = pygame.time.get_ticks()
        self.autoplay_preview_pause_logged = False
        self.autoplay_flow_start = pygame.time.get_ticks()
        self.autoplay_menu_seen: dict[str, set[str]] = {}
        self.autoplay_menu_resume_state: str | None = None
        self.autoplay_menu_resume_time = 0
        self.autoplay_pause_tested = False
        self.autoplay_vote_category: str | None = None
        self.autoplay_vote_seen: dict[str, set[str]] = {}
        self.autoplay_pending_results = ["victory", "game_over"]
        self.autoplay_menu_quick = self.autoplay and (
            os.environ.get("HOLO_AUTOPLAY_MENU_QUICK", "0") == "1"
        )
        self.autoplay_allow_system_actions = self.autoplay and (
            os.environ.get("HOLO_AUTOPLAY_SYSTEM_ACTIONS", "0") == "1"
        )
        self.autoplay_preview_delay = int(
            os.environ.get("HOLO_AUTOPLAY_PREVIEW_DELAY", "800") or 800
        )
        self.autoplay_mmo_fast = self.autoplay and (
            os.environ.get("HOLO_AUTOPLAY_MMO_FAST", "1") == "1"
        )
        self.match_lives = int(self.settings.get("match_lives", 3) or 3)
        self.match_allies = int(self.settings.get("match_allies", 0) or 0)
        self.match_mobs = bool(self.settings.get("match_mobs", False))
        self.match_mob_interval = int(
            self.settings.get("match_mob_interval", 3500) or 3500
        )
        self.match_mob_wave = int(self.settings.get("match_mob_wave", 2) or 2)
        self.match_mob_max = int(self.settings.get("match_mob_max", 8) or 8)
        self.autoplay_menu_budget = int(
            os.environ.get("HOLO_AUTOPLAY_MENU_BUDGET", "0") or 0
        )
        self.autoplay_vote_limit = int(
            os.environ.get("HOLO_AUTOPLAY_VOTE_LIMIT", "3") or 3
        )
        self.autoplay_learning_interval = int(
            os.environ.get("HOLO_AUTOPLAY_LEARN_INTERVAL", "1200") or 1200
        )
        self.autoplay_last_feedback = pygame.time.get_ticks()
        self.autoplay_last_health: float | None = None
        self.autoplay_last_kills = 0
        self.autoplay_mmo_state: str | None = None
        self.autoplay_mmo_overlay_index = 0
        self.autoplay_mmo_overlay_seen: set[str] = set()
        self.autoplay_mmo_last_step = pygame.time.get_ticks()
        self.autoplay_mmo_toggle_index = 0
        self.autoplay_mmo_layer_index = 0
        self.autoplay_mmo_overlay_limit = int(
            os.environ.get("HOLO_AUTOPLAY_MMO_OVERLAY_LIMIT", "6") or 6
        )
        self.autoplay_tuning = self.settings.get("autoplay_tuning", {})
        self.autoplay_trace = self.autoplay and (
            os.environ.get("HOLO_AUTOPLAY_TRACE", "0") == "1"
        )
        self.autoplay_trace_console = self.autoplay_trace and (
            os.environ.get("HOLO_AUTOPLAY_TRACE_CONSOLE", "1") == "1"
        )
        self.autoplay_trace_overlay = self.autoplay_trace and (
            os.environ.get("HOLO_AUTOPLAY_TRACE_OVERLAY", "1") == "1"
        )
        self.autoplay_monitor = self.autoplay and (
            os.environ.get("HOLO_AUTOPLAY_MONITOR", "1") == "1"
        )
        self.autoplay_monitor_interval = int(
            os.environ.get("HOLO_AUTOPLAY_MONITOR_INTERVAL", "1200") or 1200
        )
        self.autoplay_trace_interval = int(
            os.environ.get("HOLO_AUTOPLAY_TRACE_INTERVAL", "200") or 200        
        )
        self.autoplay_trace_limit = int(
            os.environ.get("HOLO_AUTOPLAY_TRACE_LIMIT", "6") or 6
        )
        self.autoplay_trace_lines: list[str] = []
        self.autoplay_trace_last = pygame.time.get_ticks()
        self.autoplay_input_trace_last = pygame.time.get_ticks()
        self.autoplay_monitor_last = pygame.time.get_ticks()
        autoplay_levels_env = os.environ.get("HOLO_AUTOPLAY_LEVELS")
        if autoplay_levels_env is None and self.autoplay_extended:
            autoplay_levels_env = "6"
        self.autoplay_levels_target = int(autoplay_levels_env or 3)
        self.autoplay_level_index = 0
        autoplay_ai_env = os.environ.get("HOLO_AUTOPLAY_AI_PLAYERS")
        self.autoplay_ai_players = int(autoplay_ai_env or 0)
        if self.autoplay and autoplay_ai_env is None:
            self.autoplay_ai_players = max(2, self.autoplay_ai_players)
        autoplay_allies_env = os.environ.get("HOLO_AUTOPLAY_ALLIES")
        self.autoplay_allies = int(autoplay_allies_env or 0)
        if self.autoplay and autoplay_allies_env is None:
            self.autoplay_allies = 1
        self.autoplay_ally_lives = int(
            os.environ.get("HOLO_AUTOPLAY_ALLY_LIVES", "3") or 3
        )
        self.autoplay_lives = int(
            os.environ.get("HOLO_AUTOPLAY_LIVES", "5") or 5
        ) if self.autoplay else 3
        self.autoplay_agent_enabled = self.autoplay
        self.autoplay_feature_counts: dict[str, int] = {}
        self.autoplay_skill_audit = self.autoplay and (
            os.environ.get("HOLO_AUTOPLAY_SKILL_AUDIT", "1") == "1"
        )
        self.autoplay_skill_audit_interval = int(
            os.environ.get("HOLO_AUTOPLAY_SKILL_AUDIT_INTERVAL", "1200") or 1200
        )
        self.autoplay_skill_audit_last = pygame.time.get_ticks()
        self.autoplay_skill_audit_completed: set[str] = set()
        self.autoplay_skill_audit_force = self.autoplay and (
            os.environ.get("HOLO_AUTOPLAY_SKILL_AUDIT_FORCE", "1") == "1"
        )
        self.autoplay_skill_audit_report = self.autoplay and (
            os.environ.get("HOLO_AUTOPLAY_SKILL_AUDIT_REPORT", "1") == "1"
        )
        self.autoplay_skill_audit_report_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "SavedGames",
            "skill_audit.json",
        )
        self.autoplay_skill_audit_runner = self.autoplay and (
            os.environ.get("HOLO_AUTOPLAY_SKILL_AUDIT_RUNNER", "0") == "1"
        )
        self.autoplay_skill_audit_runner_index = 0
        self.debug_sfx = self.settings.get("debug_sfx", False)
        self.autoplay_action_required = ()
        self.autoplay_character_action_counts: dict[str, dict[str, int]] = {}
        self.autoplay_character_action_missing: dict[str, set[str]] = {}
        self.autoplay_log_enabled = self.autoplay and (
            os.environ.get("HOLO_AUTOPLAY_LOG", "1") == "1"
        )
        self.autoplay_log_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "SavedGames",
            "autoplay.log",
        )
        self.autoplay_generation_interval = int(
            os.environ.get("HOLO_AUTOPLAY_GENERATION_INTERVAL", "8000") or 8000
        )
        self.autoplay_level_extension = int(
            os.environ.get("HOLO_AUTOPLAY_LEVEL_EXTENSION", "8") or 8
        )
        self.autoplay_mobs = self.autoplay and (
            os.environ.get("HOLO_AUTOPLAY_MOBS", "1") == "1"
        )
        self.mob_spawn_interval = int(
            os.environ.get("HOLO_MOB_SPAWN_INTERVAL", "3500") or 3500
        )
        self.mob_spawn_wave = int(
            os.environ.get("HOLO_MOB_WAVE", "2") or 2
        )
        self.mob_spawn_max = int(
            os.environ.get("HOLO_MOB_MAX", "8") or 8
        )
        self.mob_spawn_last = pygame.time.get_ticks()
        self.mob_spawn_enabled = False
        self.mob_spawn_config: dict[str, object] = {}
        autoplay_level_limit_env = os.environ.get("HOLO_AUTOPLAY_LEVEL_LIMIT")
        if autoplay_level_limit_env is None and self.autoplay_extended:
            autoplay_level_limit_env = "120"
        self.autoplay_level_limit = int(autoplay_level_limit_env or 0)
        self.autoplay_next_generation = pygame.time.get_ticks()
        if self.mining_enabled:
            self.mining_manager.start()
        default_keys = {
            "shoot": pygame.K_z,
            "melee": pygame.K_x,
            "jump": pygame.K_SPACE,
            "block": pygame.K_LSHIFT,
            "parry": pygame.K_c,
            "dodge": pygame.K_LCTRL,
            "special": pygame.K_v,
            "use_item": pygame.K_h,
            "use_mana": pygame.K_j,
            "sprint": pygame.K_RSHIFT,
        }
        self.keybind_manager = KeybindManager(default_keys)
        self.keybind_manager.load_from_dict(self.settings.get("key_bindings", {}))
        self.chat_manager = ChatManager()
        self.chat_input = ""
        self.achievement_manager = AchievementManager()
        self.achievement_manager.load_from_dict(
            {"achievements": self.profile.achievements.get("unlocked_ids", [])}
        )
        self.reputation_manager = ReputationManager()
        self.reputation_manager.load_from_dict(
            self.profile.reputation.get("factions", {})
        )
        self.objective_manager = ObjectiveManager()
        self.objective_manager.load_from_dict(
            self.settings.get("objectives", {})
        )
        self.economy_manager = EconomyManager()
        self.mmo_factions = [
            "Celestial Guard",
            "Verdant Coalition",
            "Forge Guild",
            "Tide Watch",
            "Skyward Circuit",
        ]
        self.mmo_ai_seed = int(os.environ.get("HOLO_MMO_AI_SEED", "17") or 17)
        self._mmo_seed_economy()
        self.loot_manager = LootManager({"Enemy": ["potion", "mana_potion"]})
        pygame.joystick.init()
        self.joysticks = [
            pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())
        ]
        for j in self.joysticks:
            j.init()
        default_controller = {
            "shoot": 0,
            "melee": 1,
            "jump": 2,
            "block": 4,
            "parry": 5,
            "dodge": 6,
            "special": 3,
            "use_item": 7,
            "use_mana": 8,
            "sprint": 9,
        }
        self.controller_bindings = self.settings.get(
            "controller_bindings", default_controller
        )
        self.input_manager = InputManager(
            self.keybind_manager.bindings,
            self.controller_bindings,
            self.joysticks,
            self.input_method,
        )
        self.screen = self._apply_display_mode()
        self.arena_backdrop: pygame.Surface | None = None
        self.arena_backdrop_size: tuple[int, int] = (0, 0)
        self.ground_surface: pygame.Surface | None = None
        self.ground_surface_size: tuple[int, int] = (0, 0)
        pygame.display.set_caption("Hololive Coliseum")
        self.clock = pygame.time.Clock()
        self.running = False
        # splash -> main_menu -> mode -> char -> map/chapter -> playing -> victory -> mmo
        self.state = "splash"
        self.menu_index = 0
        self.state_manager = GameStateManager(self.state)
        self.menu_manager = MenuManager()
        self.return_state = "main_menu"
        ui_debug_overlay = os.environ.get("HOLO_UI_DEBUG_OVERLAY", "0") == "1"
        ui_debug_log = os.environ.get("HOLO_UI_DEBUG_LOG", "0") == "1"
        ui_debug_log_frames = os.environ.get("HOLO_UI_DEBUG_LOG_FRAMES", "0") == "1"
        ui_debug_output_dir = os.path.join(
            os.path.dirname(__file__),
            "..",
            "SavedGames",
            "ui_debug",
        )
        self.ui_debugger = UIDebugger(
            enabled=ui_debug_overlay,
            output_dir=ui_debug_output_dir,
            log_enabled=ui_debug_log,
            log_frames=ui_debug_log_frames,
            headless=(os.environ.get("PYGAME_HEADLESS") == "1"),
        )
        self.ui_debug_summary_path: str | None = None
        profile_unlocks = self.profile.progression.get("unlocks", {})
        if not isinstance(profile_unlocks, dict):
            profile_unlocks = {}
        self.mmo_unlocked = bool(
            profile_unlocks.get(
                "mmo_unlocked",
                self.settings.get("mmo_unlocked", False),
            )
        )
        self.mmo_pending = False
        self.mmo_player_id = "player"
        shard_setting = str(
            os.environ.get(
                "HOLO_MMO_SHARD",
                self.settings.get("mmo_shard", "public"),
            )
            or "public"
        )
        self.mmo_shard_mode = "auto" if shard_setting == "auto" else "fixed"
        self.mmo_shard_id = shard_setting if self.mmo_shard_mode == "fixed" else "public"
        self.mmo_shard_selected = False
        self.mmo_shard_stats: dict[str, int] = {}
        self.mmo_shard_count = int(
            os.environ.get("HOLO_MMO_SHARD_COUNT", "4") or 4
        )
        self.mmo_shard_announce_interval = int(
            os.environ.get("HOLO_MMO_SHARD_ANNOUNCE_MS", "4000") or 4000
        )
        self.mmo_last_shard_announce = 0
        self.mmo_shard_migrate_threshold = int(
            os.environ.get("HOLO_MMO_SHARD_MIGRATE_DELTA", "3") or 3
        )
        self.mmo_shard_migrate_cooldown_ms = int(
            os.environ.get("HOLO_MMO_SHARD_MIGRATE_COOLDOWN_MS", "15000") or 15000
        )
        self.mmo_last_shard_migration = 0
        self.mmo_shard_choice_index = 0
        self.mmo_speed = 0.06
        self.mmo_state_interval = 250
        self.mmo_last_state_sync = pygame.time.get_ticks()
        self.mmo_last_persist = 0
        self.mmo_message = ""
        self.mmo_flash_messages: list[dict[str, object]] = []
        self.mmo_starfield: list[dict[str, object]] = []
        self.mmo_starfield_size: tuple[int, int] = (0, 0)
        self.mmo_plan_cooldown = 15000
        self.mmo_last_plan = 0
        self.mmo_plan_summary = ""
        self.mmo_pipeline_boost_cooldown = 12000
        self.mmo_auto_dev_interval = 12000
        self.mmo_last_auto_dev_tick = pygame.time.get_ticks()
        self.mmo_auto_dev_shipment_cooldown = 6000
        self.mmo_last_shipment_auto = pygame.time.get_ticks()
        self.mmo_focus_region_name = None
        self.mmo_focus_region_threat = 0.0
        self.mmo_account_log = self._normalize_account_log(
            self.settings.get("account_log", [])
        )
        self.mmo_account_tiers = ["guest", "user", "pro", "admin"]
        self.mmo_account_tier_costs = {
            "guest": 0,
            "user": 50,
            "pro": 150,
            "admin": 300,
        }
        self.mmo_last_pipeline_boost = 0
        self.mmo_trial_unlocked = False
        self.mmo_trial_active = False
        self.mmo_remote_states: dict[str, SharedStateManager] = {}
        self.mmo_presence_timeout_ms = int(
            os.environ.get("HOLO_MMO_PRESENCE_TIMEOUT_MS", "6000") or 6000
        )
        self.mmo_presence = MMOPresenceManager(
            timeout_ms=self.mmo_presence_timeout_ms
        )
        self.mmo_remote_positions = self.mmo_presence.positions
        self.mmo_auto_agents: list[dict[str, object]] = []
        self.mmo_ai_count = int(os.environ.get("HOLO_MMO_AI", "4") or 4)
        self.mmo_ai_radius = 0.08
        self.mmo_ui_show_panel = bool(
            self.settings.get("mmo_show_panel", True)
        )
        self.mmo_region_index = 0
        self.mmo_region_scroll = 0
        self.mmo_biome_filter = "all"
        self.mmo_filters = ["all", "plains", "forest", "desert", "tundra"]      
        self.mmo_zoom = float(self.settings.get("mmo_zoom", 1.0) or 1.0)        
        if self.mmo_zoom <= 0:
            self.mmo_zoom = 1.0
        self.mmo_show_minimap = bool(
            self.settings.get("mmo_show_minimap", True)
        )
        self.mmo_show_event_log = bool(
            self.settings.get("mmo_show_event_log", True)
        )
        self.mmo_favorites = set(
            self.settings.get("mmo_favorites", []) or []
        )
        self.mmo_waypoint: dict[str, object] | None = None
        self.mmo_show_details = False
        self.mmo_show_help = False
        self.mmo_show_favorites = False
        self.mmo_show_quest_log = False
        self.mmo_show_growth = False
        self.mmo_show_party = False
        self.mmo_show_network = False
        self.mmo_overlay_mode = "overview"
        self.mmo_overlays = [
            "overview",
            "details",
            "favorites",
            "quests",
            "growth",
            "party",
            "network",
            "help",
            "notifications",
            "market",
            "factions",
            "operations",
            "hub_settings",
            "guilds",
            "events",
            "contracts",
            "intel",
            "patrols",
            "infrastructure",
            "timeline",
            "logistics",
            "survey",
            "diplomacy",
            "research",
            "crafting",
            "market_orders",
            "strategy",
            "campaign",
            "expeditions",
            "roster",
            "alerts",
            "command",
            "bounties",
            "influence",
            "fleet",
            "projects",
            "academy",
        ]
        self.mmo_show_market = False
        self.mmo_show_factions = False
        self.mmo_show_operations = False
        self.mmo_show_hub_settings = False
        self.mmo_show_guilds = False
        self.mmo_show_events = False
        self.mmo_show_contracts = False
        self.mmo_show_intel = False
        self.mmo_show_infrastructure = False
        self.mmo_show_patrols = False
        self.mmo_show_timeline = False
        self.mmo_show_logistics = False
        self.mmo_show_survey = False
        self.mmo_show_diplomacy = False
        self.mmo_show_research = False
        self.mmo_show_crafting = False
        self.mmo_show_market_orders = False
        self.mmo_show_strategy = False
        self.mmo_show_campaign = False
        self.mmo_show_expeditions = False
        self.mmo_show_roster = False
        self.mmo_show_alerts = False
        self.mmo_show_command = False
        self.mmo_show_bounties = False
        self.mmo_show_influence = False
        self.mmo_show_fleet = False
        self.mmo_show_projects = False
        self.mmo_show_academy = False
        self.mmo_show_account = False
        self.mmo_show_account_audit = False
        self.mmo_show_account_audit = False
        self.mmo_show_account_audit = False
        self.mmo_account_audit_filter = "all"
        self.mmo_account_audit_upgrades_only = False
        self.mmo_show_bounties = False
        self.mmo_show_influence = False
        self.mmo_show_fleet = False
        self.mmo_show_projects = False
        self.mmo_show_academy = False
        self.mmo_show_account = False
        self.mmo_help_page = 0
        self.mmo_show_tour = False
        self.mmo_tour_step = 0
        self.mmo_seen_tour = bool(self.settings.get("mmo_seen_tour", False))
        self.mmo_region_actions = [
            "Teleport",
            "Pin Objective",
            "Generate Plan",
            "Build Outpost",
            "Remove Outpost",
            "Assign Patrol",
            "Open Trade Route",
            "Close Trade Route",
            "Dispatch Operation",
            "Queue Match",
            "Leave Match",
            "Accept Match",
            "Decline Match",
            "Launch Match",
            "Migrate Shard",
            "Cycle Shard",
            "Confirm Shard",
        ]
        self.mmo_action_index = 0
        self.mmo_floating_messages: list[dict[str, object]] = []
        self.mmo_event_log: list[str] = []
        self.mmo_event_log_limit = 10
        self.mmo_notifications: list[dict[str, object]] = []
        self.mmo_show_notifications = False
        self.mmo_world_events = self.settings.get("mmo_world_events", []) or [] 
        if not isinstance(self.mmo_world_events, list):
            self.mmo_world_events = []
        self.mmo_world_tombstones = (
            self.settings.get("mmo_world_tombstones", []) or []
        )
        if not isinstance(self.mmo_world_tombstones, list):
            self.mmo_world_tombstones = []
        self.mmo_world_tombstone_ttl_ms = int(
            os.environ.get("HOLO_MMO_TOMBSTONE_TTL_MS", "60000") or 60000
        )
        self.mmo_contracts = self.settings.get("mmo_contracts", []) or []       
        if not isinstance(self.mmo_contracts, list):
            self.mmo_contracts = []
        self.mmo_bounties = self.settings.get("mmo_bounties", []) or []
        if not isinstance(self.mmo_bounties, list):
            self.mmo_bounties = []
        self.mmo_influence = self.settings.get("mmo_influence", {}) or {}
        if not isinstance(self.mmo_influence, dict):
            self.mmo_influence = {}
        self.mmo_projects = self.settings.get("mmo_projects", []) or []
        if not isinstance(self.mmo_projects, list):
            self.mmo_projects = []
        self.mmo_training_queue = self.settings.get("mmo_training_queue", []) or []
        if not isinstance(self.mmo_training_queue, list):
            self.mmo_training_queue = []
        self.mmo_directives = self.settings.get("mmo_directives", []) or []
        if not isinstance(self.mmo_directives, list):
            self.mmo_directives = []
        self.mmo_world_tick_interval = 1000
        self.mmo_last_world_tick = pygame.time.get_ticks()
        self.mmo_sort_modes = ["name", "level", "distance", "biome", "threat"]
        self.mmo_sort_mode = str(
            self.settings.get("mmo_sort_mode", "name") or "name"
        )
        if self.mmo_sort_mode not in self.mmo_sort_modes:
            self.mmo_sort_mode = "name"
        default_layers = {
            "routes": True,
            "outposts": True,
            "events": True,
            "contracts": True,
            "agents": True,
            "remotes": True,
            "heatmap": True,
            "resources": True,
            "expeditions": True,
            "bounties": True,
        }
        self.mmo_layers = dict(default_layers)
        self.mmo_layers.update(self.settings.get("mmo_layers", {}) or {})
        self.mmo_weather_cache: dict[str, list[str]] = {}
        self.mmo_weather_forecast_steps = 3
        self.mmo_resource_cache: dict[str, tuple[str, int]] = {}
        self.mmo_threat_history = self.settings.get("mmo_threat_history", {}) or {}
        if not isinstance(self.mmo_threat_history, dict):
            self.mmo_threat_history = {}
        self.mmo_threat_history_window = int(
            self.settings.get("mmo_threat_history_window", 6) or 6
        )
        self.mmo_last_patrol_dispatch = pygame.time.get_ticks()
        self.mmo_patrol_dispatch_interval = 6000
        self.mmo_contract_index = 0
        self.mmo_event_index = 0
        self.mmo_operation_index = 0
        self.mmo_directive_index = 0
        self.mmo_bounty_index = 0
        self.mmo_influence_index = 0
        self.mmo_fleet_index = 0
        self.mmo_project_index = 0
        self.mmo_training_index = 0
        self.mmo_infra_index = 0
        self.mmo_patrol_index = 0
        self.mmo_timeline_index = 0
        self.mmo_logistics_index = 0
        self.mmo_survey_index = 0
        self.mmo_stockpile = self.settings.get("mmo_stockpile", {}) or {}
        if not isinstance(self.mmo_stockpile, dict):
            self.mmo_stockpile = {}
        self.mmo_shipments = self.settings.get("mmo_shipments", []) or []       
        if not isinstance(self.mmo_shipments, list):
            self.mmo_shipments = []
        self.mmo_credits = int(self.settings.get("mmo_credits", 250) or 250)
        self.mmo_market_orders = self.settings.get("mmo_market_orders", []) or []
        if not isinstance(self.mmo_market_orders, list):
            self.mmo_market_orders = []
        self.mmo_crafting_queue = self.settings.get("mmo_crafting_queue", []) or []
        if not isinstance(self.mmo_crafting_queue, list):
            self.mmo_crafting_queue = []
        self.mmo_crafting_index = 0
        self.mmo_market_index = 0
        self.mmo_strategy = self.settings.get("mmo_strategy", {}) or {}
        if not isinstance(self.mmo_strategy, dict):
            self.mmo_strategy = {}
        self.mmo_strategy.setdefault("focus", "resources")
        self.mmo_strategy.setdefault("mode", "balanced")
        self.mmo_strategy_options = ["resources", "threat", "influence"]
        self.mmo_stats = self.settings.get("mmo_stats", {}) or {}
        if not isinstance(self.mmo_stats, dict):
            self.mmo_stats = {}
        self.mmo_campaign_status = self.settings.get("mmo_campaign_status", {}) or {}
        if not isinstance(self.mmo_campaign_status, dict):
            self.mmo_campaign_status = {}
        self.mmo_expeditions = self.settings.get("mmo_expeditions", []) or []
        if not isinstance(self.mmo_expeditions, list):
            self.mmo_expeditions = []
        self.mmo_alerts = self.settings.get("mmo_alerts", []) or []
        if not isinstance(self.mmo_alerts, list):
            self.mmo_alerts = []
        self.mmo_expedition_index = 0
        self.mmo_roster_index = 0
        self.mmo_alert_index = 0
        self.mmo_last_alert_time = 0
        self.mmo_directive_sequence = max(1, len(self.mmo_directives) + 1)
        self.mmo_bounty_sequence = max(1, len(self.mmo_bounties) + 1)
        self.mmo_project_sequence = max(1, len(self.mmo_projects) + 1)
        self.mmo_training_sequence = max(1, len(self.mmo_training_queue) + 1)
        self.mmo_outposts = self.settings.get("mmo_outposts", []) or []
        if not isinstance(self.mmo_outposts, list):
            self.mmo_outposts = []
        self.mmo_trade_routes = self.settings.get("mmo_trade_routes", []) or []
        if not isinstance(self.mmo_trade_routes, list):
            self.mmo_trade_routes = []
        self.mmo_operations = self.settings.get("mmo_operations", []) or []
        if not isinstance(self.mmo_operations, list):
            self.mmo_operations = []
        self.mmo_guilds = [
            {
                "name": "Starlight Vanguard",
                "focus": "Exploration",
                "rank": "Bronze",
                "influence": 18,
            },
            {
                "name": "Crimson Anvil",
                "focus": "Crafting",
                "rank": "Silver",
                "influence": 32,
            },
            {
                "name": "Emerald Chorus",
                "focus": "Diplomacy",
                "rank": "Gold",
                "influence": 44,
            },
        ]
        self._mmo_seed_guilds()
        self._mmo_seed_contracts()
        self.ai_progression = self.settings.get("ai_progression", {})
        if not isinstance(self.ai_progression, dict):
            self.ai_progression = {}
        self.ai_playthroughs = int(self.ai_progression.get("playthroughs", 0))
        self.mmo_ai_level = int(self.ai_progression.get("mmo_level", 1))
        if self.mmo_ai_level < 1:
            self.mmo_ai_level = 1
        self.ai_experience_manager = AIExperienceManager(
            experience_level=max(1, self.ai_playthroughs + 1)
        )
        self.ai_experience_store = AIExperienceStore()
        self.ai_experience_interval = int(
            os.environ.get("HOLO_AI_EXPERIENCE_INTERVAL", "5000") or 5000
        )
        self.ai_experience_last_log = pygame.time.get_ticks()
        self.main_menu_options = [
            "Quick Start",
            "New Game",
            "Character Select",
            "Map Select",
            "Match Options",
            "MMO",
            "Settings",
            "Accounts",
            "How to Play",
            "Credits",
            "Achievements",
            "Records",
            "Goals",
            "Vote",
            "Exit",
        ]
        if not self.mmo_unlocked and "MMO" in self.main_menu_options:
            self.main_menu_options.remove("MMO")
        if self.autoplay_force_mmo and "MMO" not in self.main_menu_options:
            insert_at = 2 if len(self.main_menu_options) > 2 else len(
                self.main_menu_options
            )
            self.main_menu_options.insert(insert_at, "MMO")
        self.mode_options = ["Story", "Arena", "Custom", "Back"]
        self.solo_multi_options = ["Solo", "Multiplayer", "Back"]
        self.mp_type_options = ["Offline", "Online", "Back"]
        self.online_multiplayer = False
        self.pause_options = [
            "Resume",
            "Inventory",
            "Equipment",
            "Achievements",
            "Main Menu",
        ]
        self.game_over_options = ["Play Again", "Main Menu"]
        self.victory_options = ["Play Again", "Main Menu"]
        self.post_victory_plan: dict[str, object] | None = None
        self.post_victory_focus: dict[str, object] | None = None
        self.victory_action_message = ""
        self.arena_wins = int(self.settings.get("arena_wins", 0) or 0)
        self.last_victory_final = False
        self.final_time = 0
        self.end_time = 0
        self.show_end_options = False
        self.boss_present_last = False
        self.boss_banner_until = 0
        self.victory_flash_until = 0
        self.game_over_flash_until = 0
        self.best_time = self.settings.get("best_time", 0)
        self.score_manager = ScoreManager(
            self.settings.get("best_score", 0)
        )
        self.kills = 0
        self.iteration_manager = IterationManager()
        self.screenshot_manager = ScreenshotManager()
        self.show_fps = self.settings.get("show_fps", False)
        self.item_manager = ItemManager()
        self.accessibility_manager = AccessibilityManager()
        stored_accessibility = self.settings.get("accessibility", {})
        if isinstance(stored_accessibility, dict):
            self.accessibility_manager.options.update(stored_accessibility)
        self.settings_options = [
            "Controls",
            "Display",
            "Audio",
            "System",
            "Back",
        ]
        self.settings_controls_options = [
            "Key Bindings",
            "Controller Bindings",
            "Input Method",
            "Back",
        ]
        self.settings_display_options = [
            "Window Size",
            "Display Mode",
            "HUD Size",
            "Show FPS",
            "Back",
        ]
        self.settings_audio_options = [
            "Volume",
            "SFX Profile",
            "SFX Debug",
            "Back",
        ]
        self.settings_system_options = [
            "Reset Records",
            "Wipe Saves",
            "Accessibility",
            "Node Settings",
            "Accounts",
            "Back",
        ]
        self.match_options = [
            "Lives",
            "Allies",
            "AI Players",
            "Mob Waves",
            "Mob Interval",
            "Mob Wave",
            "Mob Cap",
            "Back",
        ]
        self.info_options = ["Back"]
        self.key_options = [
            "jump",
            "shoot",
            "melee",
            "block",
            "parry",
            "dodge",
            "special",
            "use_item",
            "use_mana",
            "sprint",
            "Back",
        ]
        self.controller_options = list(self.key_options)
        self.rebind_action: str | None = None
        self.font_scale_options = [0.9, 1.0, 1.1, 1.25, 1.4]
        if (
            self.accessibility_manager.options.get("font_scale")
            not in self.font_scale_options
        ):
            self.accessibility_manager.options["font_scale"] = 1.0
        self.accessibility_options = [
            "Font Scale",
            "High Contrast",
            "Input Prompts",
            "Colorblind Mode",
            "Back",
        ]
        self.node_options = [
            "Start Node",
            "Stop Node",
            "Latency Helper",
            "Background Mining",
            "Back",
        ]
        self.account_options = [
            "Register Account",
            "Delete Account",
            "Renew Key",
            "Back",
        ]
        self.account_id = str(self.settings.get("account_id", "player") or "player")
        self.mining_manager.player_id = self.account_id
        self.mmo_player_id = self.account_id or "player"
        self.accounts_manager = AccountsManager()
        self.network_manager: NetworkManager | None = None
        self.node_hosting = False
        self.latency_helper = False
        preferred = [
            n for n in load_character_names() if character_class_exists(n)
        ]
        if not preferred:
            preferred = ["Gawr Gura"]
        seen = set()
        self.characters = []
        for name in preferred:
            if name in seen:
                continue
            seen.add(name)
            self.characters.append(name)
        if len(self.characters) < 20:
            for name in CHARACTER_CLASSES.keys():
                if name in seen:
                    continue
                self.characters.append(name)
                seen.add(name)
                if len(self.characters) >= 20:
                    break
        random.shuffle(self.characters)
        self.character_filters = [
            "All",
            "Striker",
            "Guardian",
            "Caster",
            "Skirmisher",
        ]
        self.character_filter = "All"
        self.character_preview_cache: dict[str, dict[str, object]] = {}
        image_dir = os.path.join(os.path.dirname(__file__), "..", "Images") 
        ensure_placeholder_sprites(image_dir, self.characters)
        self.voting_manager = VotingManager(self.characters)
        self.biome_voting_manager = VotingManager(
            ["plains", "forest", "desert", "tundra"], category="biome"
        )
        self.world_generation_manager.voting_manager = self.voting_manager
        self.world_generation_manager.biome_manager = self.biome_voting_manager
        self.mmo_verifier = StateVerificationManager()
        self.mmo_shared_state = SharedStateManager(
            tolerances={"pos_x": 0.02, "pos_y": 0.02},
            verifier=self.mmo_verifier,
        )
        self.mmo_world_state = MMOWorldStateManager(verifier=self.mmo_verifier)
        self.mmo_world_state_cache: dict[str, dict[str, object]] = {}
        self.mmo_shard_cache_ttl_ms = int(
            os.environ.get("HOLO_MMO_SHARD_CACHE_TTL_MS", "120000") or 120000
        )
        self.mmo_world_state_interval = int(
            os.environ.get("HOLO_MMO_WORLD_STATE_INTERVAL", "1000") or 1000
        )
        self.mmo_last_world_state_sync = pygame.time.get_ticks()
        self.mmo_match_queue_size = int(
            os.environ.get("HOLO_MMO_MATCH_SIZE", "2") or 2
        )
        self.mmo_match_group: list[str] | None = None
        self.mmo_match_status = "idle"
        self.mmo_match_id: str | None = None
        self.mmo_match_found_at: int | None = None
        self.mmo_match_ready_at: int | None = None
        self.mmo_match_timeout_ms = int(
            os.environ.get("HOLO_MMO_MATCH_TIMEOUT_MS", "12000") or 12000
        )
        self.mmo_match_ready_timeout_ms = int(
            os.environ.get("HOLO_MMO_MATCH_READY_TIMEOUT_MS", "8000") or 8000
        )
        self.mmo_backend = MMOBackendManager()
        self.mmo_pipeline = AutoDevPipeline()
        self.world_player_manager = WorldPlayerManager(
            self.world_generation_manager,
            self.world_generation_manager.region_manager,
        )
        self._setup_mmo_agents()
        saved_mmo_pos = self.settings.get("mmo_position")
        if isinstance(saved_mmo_pos, (list, tuple)) and len(saved_mmo_pos) == 2:
            self.world_player_manager.set_position(
                self.mmo_player_id,
                (float(saved_mmo_pos[0]), float(saved_mmo_pos[1])),
            )
        self.map_manager = MapManager()
        self.environment_manager = EnvironmentManager()
        self.spawn_manager = SpawnManager()
        self.event_manager = EventManager()
        self.status_manager = StatusEffectManager()
        self.status_manager.set_event_sink(self.emit_event)
        self.hazard_manager = HazardManager(       
            self.status_manager,
            analytics=self.auto_dev_manager,       
            objective_manager=self.objective_manager,
        )
        self.hazard_manager.set_event_sink(self.emit_event)
        self.vote_adjustments: dict[str, int] = {}
        arena_width = max(self.width + 600, int(self.width * 1.8))
        arena_height = self.height
        arena_ground = arena_height - 50
        side_gap = max(140, int(arena_width * 0.08))

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

        default_floor = [(side_gap, arena_ground, arena_width - side_gap * 2, 50)]
        default_map = {
            "size": (arena_width, arena_height),
            "spawn": (side_gap + 90, arena_ground - 60),
            "ground_gaps": _ground_gaps_from_segments(default_floor, arena_width),
            "gravity_zones": [
                {
                    "rect": (arena_width // 2 - 80, arena_ground - 150, 120, 50),
                    "multiplier": 0.2,
                },
                {
                    "rect": (arena_width // 2 + 120, arena_ground - 190, 90, 40),
                    "multiplier": 2.0,
                },
            ],
            "hazards": [
                {"type": "spike", "rect": (arena_width // 3, arena_ground - 20, 40, 20)},
                {"type": "ice", "rect": (arena_width // 2 + 80, arena_ground - 20, 60, 20)},
                {"type": "lava", "rect": (arena_width // 2 - 140, arena_ground - 20, 70, 20)},
            ],
            "platforms": [
                *default_floor,
                (side_gap + 160, arena_ground - 160, 160, 20),
                (arena_width // 2 - 80, arena_ground - 230, 160, 20),
                (arena_width - side_gap - 320, arena_ground - 200, 180, 20),
                (arena_width // 2 + 220, arena_ground - 150, 120, 20),
            ],
            "moving_platforms": [
                {
                    "rect": (arena_width // 2 - 60, arena_ground - 260, 120, 20),
                    "offset": (0, 90),
                    "speed": 2,
                },
            ],
            "minions": 1,
        }
        self.map_manager.add_map("Default", default_map)
        sky_floor = [
            (side_gap, arena_ground, arena_width // 2 - side_gap - 140, 50),
            (
                arena_width // 2 + 140,
                arena_ground,
                arena_width - side_gap - (arena_width // 2 + 140),
                50,
            ),
        ]
        sky_map = {
            "size": (arena_width, arena_height),
            "spawn": (side_gap + 100, arena_ground - 60),
            "ground_gaps": _ground_gaps_from_segments(sky_floor, arena_width),
            "gravity_zones": [
                {"rect": (side_gap + 60, arena_ground - 210, 120, 40), "multiplier": 0.6},
                {
                    "rect": (arena_width - side_gap - 240, arena_ground - 190, 120, 40),
                    "multiplier": 1.4,
                },
            ],
            "hazards": [
                {
                    "type": "wind",
                    "rect": (arena_width // 2 - 80, arena_ground - 70, 160, 40),
                    "force": 2.5,
                },
                {"type": "spike", "rect": (side_gap + 120, arena_ground - 20, 40, 20)},
            ],
            "platforms": [
                *sky_floor,
                (side_gap + 140, arena_ground - 170, 140, 20),
                (arena_width - side_gap - 320, arena_ground - 190, 160, 20),
                (arena_width // 2 - 70, arena_ground - 260, 140, 20),
            ],
            "moving_platforms": [
                {
                    "rect": (arena_width // 2 - 60, arena_ground - 300, 120, 20),
                    "offset": (160, 0),
                    "speed": 2,
                },
            ],
            "crumbling_platforms": [
                {"rect": (arena_width // 2 - 180, arena_ground - 330, 90, 20), "delay": 80},
            ],
            "minions": 2,
        }
        canyon_floor = [
            (side_gap, arena_ground, arena_width // 2 - side_gap - 170, 50),
            (
                arena_width // 2 + 170,
                arena_ground,
                arena_width - side_gap - (arena_width // 2 + 170),
                50,
            ),
        ]
        canyon_map = {
            "size": (arena_width, arena_height),
            "spawn": (side_gap + 110, arena_ground - 60),
            "ground_gaps": _ground_gaps_from_segments(canyon_floor, arena_width),
            "gravity_zones": [
                {"rect": (side_gap + 40, arena_ground - 110, 120, 40), "multiplier": 1.6},
                {
                    "rect": (arena_width - side_gap - 200, arena_ground - 90, 120, 40),
                    "multiplier": 0.7,
                },
            ],
            "hazards": [
                {"type": "quicksand", "rect": (arena_width // 2 - 80, arena_ground - 10, 160, 20)},
                {"type": "spike", "rect": (arena_width // 2 + 160, arena_ground - 20, 40, 20)},
                {
                    "type": "teleport",
                    "rect": (side_gap - 20, arena_ground - 20, 80, 20),
                    "target": (side_gap + 120, arena_ground - 170),
                },
            ],
            "platforms": [
                *canyon_floor,
                (arena_width // 2 - 80, arena_ground - 210, 160, 20),
                (side_gap + 120, arena_ground - 140, 140, 20),
                (arena_width - side_gap - 280, arena_ground - 180, 140, 20),
                (arena_width // 2 + 220, arena_ground - 120, 120, 20),
            ],
            "moving_platforms": [
                {
                    "rect": (arena_width // 2 - 140, arena_ground - 270, 120, 20),
                    "offset": (200, 0),
                    "speed": 2,
                },
            ],
            "minions": 2,
        }
        forge_floor = [
            (side_gap, arena_ground, arena_width // 2 - side_gap - 90, 50),
            (
                arena_width // 2 + 90,
                arena_ground,
                arena_width - side_gap - (arena_width // 2 + 90),
                50,
            ),
        ]
        forge_map = {
            "size": (arena_width, arena_height),
            "spawn": (side_gap + 100, arena_ground - 60),
            "ground_gaps": _ground_gaps_from_segments(forge_floor, arena_width),
            "gravity_zones": [
                {"rect": (arena_width // 2 - 120, arena_ground - 160, 240, 40), "multiplier": 1.2},
            ],
            "hazards": [
                {"type": "lava", "rect": (arena_width // 2 - 140, arena_ground - 20, 280, 20)},
                {"type": "acid", "rect": (side_gap + 80, arena_ground - 20, 70, 20)},
                {"type": "fire", "rect": (arena_width - side_gap - 150, arena_ground - 20, 70, 20)},
                {"type": "lightning", "rect": (arena_width // 2 - 50, arena_ground - 70, 100, 30)},
            ],
            "platforms": [
                *forge_floor,
                (arena_width // 2 - 200, arena_ground - 170, 140, 20),
                (arena_width // 2 + 60, arena_ground - 190, 140, 20),
                (side_gap + 100, arena_ground - 240, 120, 20),
                (arena_width - side_gap - 240, arena_ground - 230, 120, 20),
            ],
            "crumbling_platforms": [
                {"rect": (arena_width - side_gap - 260, arena_ground - 260, 110, 20), "delay": 70},
            ],
            "minions": 3,
        }
        crystal_floor = [(side_gap, arena_ground, arena_width - side_gap * 2, 50)]
        crystal_map = {
            "size": (arena_width, arena_height),
            "spawn": (side_gap + 110, arena_ground - 60),
            "ground_gaps": _ground_gaps_from_segments(crystal_floor, arena_width),
            "gravity_zones": [
                {"rect": (arena_width // 2 - 120, arena_ground - 210, 240, 40), "multiplier": 0.8},
            ],
            "hazards": [
                {
                    "type": "lightning",
                    "rect": (side_gap + 80, arena_ground - 30, 90, 30),
                    "damage": 5,
                },
                {
                    "type": "bounce",
                    "rect": (arena_width - side_gap - 200, arena_ground - 20, 80, 20),
                },
                {
                    "type": "teleport",
                    "rect": (arena_width // 2 - 50, arena_ground - 20, 100, 20),
                    "target": (side_gap + 40, arena_ground - 120),
                },
            ],
            "platforms": [
                *crystal_floor,
                (side_gap + 140, arena_ground - 190, 140, 20),
                (arena_width - side_gap - 300, arena_ground - 190, 140, 20),
                (arena_width // 2 - 80, arena_ground - 140, 160, 20),
                (arena_width // 2 + 220, arena_ground - 240, 120, 20),
            ],
            "moving_platforms": [
                {
                    "rect": (arena_width // 2 - 70, arena_ground - 320, 140, 20),
                    "offset": (0, 80),
                    "speed": 2,
                },
            ],
            "minions": 2,
        }
        verdant_floor = [
            (side_gap, arena_ground, arena_width // 2 - side_gap - 110, 50),
            (
                arena_width // 2 + 110,
                arena_ground,
                arena_width - side_gap - (arena_width // 2 + 110),
                50,
            ),
        ]
        verdant_map = {
            "size": (arena_width, arena_height),
            "spawn": (side_gap + 120, arena_ground - 60),
            "ground_gaps": _ground_gaps_from_segments(verdant_floor, arena_width),
            "gravity_zones": [
                {"rect": (side_gap + 60, arena_ground - 130, 140, 40), "multiplier": 1.1},
            ],
            "hazards": [
                {"type": "poison", "rect": (arena_width // 2 - 90, arena_ground - 20, 180, 20)},
                {
                    "type": "silence",
                    "rect": (arena_width - side_gap - 170, arena_ground - 70, 90, 40),
                },
                {"type": "regen", "rect": (side_gap + 60, arena_ground - 70, 90, 40)},
                {"type": "bounce", "rect": (arena_width // 2 - 40, arena_ground - 70, 80, 20)},
            ],
            "platforms": [
                *verdant_floor,
                (arena_width // 2 - 220, arena_ground - 150, 160, 20),
                (arena_width // 2 + 60, arena_ground - 210, 160, 20),
                (side_gap + 120, arena_ground - 250, 120, 20),
                (arena_width - side_gap - 260, arena_ground - 250, 140, 20),
            ],
            "crumbling_platforms": [
                {"rect": (arena_width - side_gap - 220, arena_ground - 260, 110, 20), "delay": 90},
            ],
            "minions": 2,
        }
        self.map_manager.add_map("Sky Spires", sky_map)
        self.map_manager.add_map("Canyon Run", canyon_map)
        self.map_manager.add_map("Forge Pit", forge_map)
        self.map_manager.add_map("Crystal Rift", crystal_map)
        self.map_manager.add_map("Verdant Ruins", verdant_map)
        neon_floor = [
            (side_gap, arena_ground, arena_width // 2 - side_gap - 120, 50),
            (
                arena_width // 2 + 120,
                arena_ground,
                arena_width - side_gap - (arena_width // 2 + 120),
                50,
            ),
        ]
        neon_map = {
            "size": (arena_width, arena_height),
            "spawn": (side_gap + 90, arena_ground - 60),
            "ground_gaps": _ground_gaps_from_segments(neon_floor, arena_width),
            "gravity_zones": [
                {"rect": (arena_width // 2 - 70, arena_ground - 190, 120, 40), "multiplier": 0.6},
            ],
            "hazards": [
                {"type": "poison", "rect": (arena_width // 2 - 40, arena_ground - 20, 80, 20)},
                {"type": "shock", "rect": (side_gap + 120, arena_ground - 20, 40, 20)},
                {"type": "spike", "rect": (arena_width - side_gap - 160, arena_ground - 20, 40, 20)},
            ],
            "platforms": [
                *neon_floor,
                (side_gap + 120, arena_ground - 160, 160, 20),
                (arena_width // 2 - 90, arena_ground - 230, 180, 20),
                (arena_width - side_gap - 300, arena_ground - 190, 160, 20),
            ],
            "moving_platforms": [
                {
                    "rect": (arena_width // 2 - 60, arena_ground - 280, 120, 20),
                    "offset": (140, 0),
                    "speed": 2,
                },
            ],
            "mob_spawn": {"interval": 3200, "wave": 2, "max": 10},
            "minions": 1,
        }
        citadel_floor = [(side_gap, arena_ground, arena_width - side_gap * 2, 50)]
        citadel_map = {
            "size": (arena_width, arena_height),
            "spawn": (side_gap + 110, arena_ground - 60),
            "ground_gaps": _ground_gaps_from_segments(citadel_floor, arena_width),
            "gravity_zones": [
                {"rect": (side_gap + 120, arena_ground - 220, 130, 50), "multiplier": 0.4},
                {"rect": (arena_width - side_gap - 260, arena_ground - 220, 130, 50), "multiplier": 1.6},
            ],
            "hazards": [
                {"type": "ice", "rect": (arena_width // 2 - 60, arena_ground - 20, 120, 20)},
                {"type": "lava", "rect": (side_gap + 200, arena_ground - 20, 60, 20)},
            ],
            "platforms": [
                *citadel_floor,
                (side_gap + 140, arena_ground - 170, 150, 20),
                (arena_width // 2 - 100, arena_ground - 250, 200, 20),
                (arena_width - side_gap - 320, arena_ground - 170, 160, 20),
            ],
            "crumbling_platforms": [
                {"rect": (arena_width // 2 - 200, arena_ground - 310, 120, 20), "delay": 70},
                {"rect": (arena_width // 2 + 80, arena_ground - 310, 120, 20), "delay": 70},
            ],
            "mob_spawn": {"interval": 2800, "wave": 3, "max": 12},
            "minions": 2,
        }
        self.map_manager.add_map("Neon Docks", neon_map)
        self.map_manager.add_map("Citadel Span", citadel_map)
        aurora_floor = [
            (side_gap, arena_ground, arena_width // 2 - side_gap - 150, 50),
            (
                arena_width // 2 + 150,
                arena_ground,
                arena_width - side_gap - (arena_width // 2 + 150),
                50,
            ),
        ]
        aurora_map = {
            "size": (arena_width, arena_height),
            "spawn": (side_gap + 120, arena_ground - 60),
            "ground_gaps": _ground_gaps_from_segments(aurora_floor, arena_width),
            "gravity_zones": [
                {"rect": (arena_width // 2 - 90, arena_ground - 210, 140, 50), "multiplier": 0.5},
                {"rect": (arena_width - side_gap - 260, arena_ground - 150, 120, 40), "multiplier": 1.5},
            ],
            "hazards": [
                {"type": "tundra", "rect": (arena_width // 2 - 60, arena_ground - 20, 120, 20)},
                {"type": "ice", "rect": (side_gap + 160, arena_ground - 20, 60, 20)},
                {"type": "shock", "rect": (arena_width - side_gap - 200, arena_ground - 20, 60, 20)},
            ],
            "platforms": [
                *aurora_floor,
                (side_gap + 160, arena_ground - 170, 140, 20),
                (arena_width // 2 - 100, arena_ground - 240, 200, 20),
                (arena_width - side_gap - 340, arena_ground - 200, 160, 20),
            ],
            "moving_platforms": [
                {
                    "rect": (arena_width // 2 - 60, arena_ground - 290, 120, 20),
                    "offset": (0, 80),
                    "speed": 2,
                },
            ],
            "mob_spawn": {"interval": 3000, "wave": 3, "max": 12},
            "minions": 2,
        }
        self.map_manager.add_map("Aurora Bastion", aurora_map)
        ember_floor = [(side_gap, arena_ground, arena_width - side_gap * 2, 50)]
        ember_map = {
            "size": (arena_width, arena_height),
            "spawn": (side_gap + 140, arena_ground - 60),
            "ground_gaps": _ground_gaps_from_segments(ember_floor, arena_width),
            "gravity_zones": [
                {"rect": (arena_width // 2 - 120, arena_ground - 200, 160, 50), "multiplier": 0.35},
            ],
            "hazards": [
                {"type": "lava", "rect": (arena_width // 2 - 80, arena_ground - 20, 160, 20)},
                {"type": "burn", "rect": (side_gap + 200, arena_ground - 20, 60, 20)},
                {"type": "spike", "rect": (arena_width - side_gap - 200, arena_ground - 20, 60, 20)},
            ],
            "platforms": [
                *ember_floor,
                (side_gap + 200, arena_ground - 180, 140, 20),
                (arena_width // 2 - 110, arena_ground - 250, 220, 20),
                (arena_width - side_gap - 340, arena_ground - 200, 160, 20),
            ],
            "crumbling_platforms": [
                {"rect": (arena_width // 2 - 200, arena_ground - 310, 120, 20), "delay": 60},
            ],
            "mob_spawn": {"interval": 2600, "wave": 3, "max": 14},
            "minions": 2,
        }
        beacon_floor = [
            (side_gap, arena_ground, arena_width // 2 - side_gap - 170, 50),
            (
                arena_width // 2 + 170,
                arena_ground,
                arena_width - side_gap - (arena_width // 2 + 170),
                50,
            ),
        ]
        beacon_map = {
            "size": (arena_width, arena_height),
            "spawn": (side_gap + 120, arena_ground - 60),
            "ground_gaps": _ground_gaps_from_segments(beacon_floor, arena_width),
            "gravity_zones": [
                {"rect": (side_gap + 100, arena_ground - 220, 140, 50), "multiplier": 0.55},
                {"rect": (arena_width - side_gap - 260, arena_ground - 220, 140, 50), "multiplier": 1.45},
            ],
            "hazards": [
                {"type": "wind", "rect": (arena_width // 2 - 100, arena_ground - 80, 200, 40), "force": 2.8},
                {"type": "shock", "rect": (side_gap + 140, arena_ground - 20, 60, 20)},
            ],
            "platforms": [
                *beacon_floor,
                (side_gap + 160, arena_ground - 170, 160, 20),
                (arena_width // 2 - 90, arena_ground - 240, 180, 20),
                (arena_width - side_gap - 340, arena_ground - 200, 160, 20),
            ],
            "moving_platforms": [
                {"rect": (arena_width // 2 - 70, arena_ground - 300, 140, 20), "offset": (180, 0), "speed": 2},
            ],
            "mob_spawn": {"interval": 3200, "wave": 2, "max": 12},
            "minions": 2,
        }
        self.map_manager.add_map("Ember Foundry", ember_map)
        self.map_manager.add_map("Beacon Ridge", beacon_map)
        storm_floor = [
            (side_gap, arena_ground, arena_width // 2 - side_gap - 150, 50),
            (
                arena_width // 2 + 150,
                arena_ground,
                arena_width - side_gap - (arena_width // 2 + 150),
                50,
            ),
        ]
        storm_map = {
            "size": (arena_width, arena_height),
            "spawn": (side_gap + 120, arena_ground - 60),
            "ground_gaps": _ground_gaps_from_segments(storm_floor, arena_width),
            "gravity_zones": [
                {"rect": (arena_width // 2 - 120, arena_ground - 220, 160, 50), "multiplier": 0.7},
                {"rect": (arena_width // 2 + 40, arena_ground - 140, 140, 40), "multiplier": 1.4},
            ],
            "hazards": [
                {"type": "shock", "rect": (arena_width // 2 - 60, arena_ground - 20, 120, 20)},
                {"type": "wind", "rect": (side_gap + 160, arena_ground - 90, 120, 40), "force": 2.2},
            ],
            "platforms": [
                *storm_floor,
                (side_gap + 160, arena_ground - 170, 150, 20),
                (arena_width // 2 - 90, arena_ground - 240, 180, 20),
                (arena_width - side_gap - 340, arena_ground - 200, 160, 20),
            ],
            "moving_platforms": [
                {"rect": (arena_width // 2 - 70, arena_ground - 300, 140, 20), "offset": (0, 90), "speed": 2},
            ],
            "mob_spawn": {"interval": 2900, "wave": 3, "max": 12},
            "minions": 2,
        }
        verdant_floor = [(side_gap, arena_ground, arena_width - side_gap * 2, 50)]
        verdant_forge_map = {
            "size": (arena_width, arena_height),
            "spawn": (side_gap + 120, arena_ground - 60),
            "ground_gaps": _ground_gaps_from_segments(verdant_floor, arena_width),
            "gravity_zones": [
                {"rect": (side_gap + 120, arena_ground - 210, 140, 40), "multiplier": 0.6},
            ],
            "hazards": [
                {"type": "poison", "rect": (arena_width // 2 - 90, arena_ground - 20, 180, 20)},
                {"type": "regen", "rect": (side_gap + 200, arena_ground - 20, 60, 20)},
            ],
            "platforms": [
                *verdant_floor,
                (side_gap + 160, arena_ground - 160, 150, 20),
                (arena_width // 2 - 100, arena_ground - 230, 200, 20),
                (arena_width - side_gap - 340, arena_ground - 200, 160, 20),
            ],
            "crumbling_platforms": [
                {"rect": (arena_width // 2 - 210, arena_ground - 290, 130, 20), "delay": 70},
            ],
            "mob_spawn": {"interval": 3000, "wave": 2, "max": 10},
            "minions": 2,
        }
        self.map_manager.add_map("Storm Archive", storm_map)
        self.map_manager.add_map("Verdant Forge", verdant_forge_map)
        configure_story_and_ui(self, image_dir)
        self._apply_profile_meta_selection()
        if self.autoplay_full and self.chapters:
            self.autoplay_levels_target = len(self.chapters)
            self.autoplay_deadline = None
        self.camera_manager = CameraManager()

        # Stage setup
        self.ground_y = self.height - 50
        self.level_start_time = 0
        self.base_level_limit = 60
        if self.autoplay and self.autoplay_level_limit > 0:
            self.base_level_limit = self.autoplay_level_limit
        self.level_limit = self.base_level_limit  # seconds
        self.npc_manager = NPCManager()
        self.allies = self.npc_manager.allies
        self.ai_manager = AIManager(self.npc_manager.enemies)
        self.ally_manager = AllyManager(self.npc_manager.allies)
        self.ai_interaction_manager = AIInteractionManager()
        self.ai_interaction_enabled = (
            os.environ.get("HOLO_AI_CALLOUTS", "1") == "1"
        )
        self.team_manager = TeamManager()
        self.combat_manager = CombatManager(
            self.status_manager,
            self.team_manager,
            sound_manager=self.sound_manager,
        )
        self.combat_manager.combat_event_sink = self.emit_event
        self.level_manager = LevelManager(self)
        self.autoplayer: AutoPlayer | None = (
            AutoPlayer(self, self.autoplay_tuning) if self.autoplay else None
        )
        self._setup_level()
        if self.autoplay:
            self.level_start_time = pygame.time.get_ticks()
        self.holo_hype_until = 0
        self.holo_hype_active = False
        self.holo_hype_trigger = 5
        self.holo_hype_attack_bonus = 2
        self.holo_hype_speed_bonus = 0.2
        self.combo_cheer_level = 0
        self.holo_cheer_phrases = [
            "Kira Kira!",
            "Encore!",
            "Idol Rush!",
            "Holo Hype!",
        ]
        self.holo_cheer_colors = [
            (120, 220, 255),
            (255, 170, 220),
            (255, 210, 120),
            (180, 255, 210),
        ]
        self.holo_cheer_color_idx = 0
        self.holo_highlight_until = 0
        self.arena_intro_until = 0
        self.arena_intro_title = ""
        self.arena_intro_subtitle = ""
        self.holo_sign_until = 0
        self.holo_audience_until = 0
        self.holo_spotlight_swap_until = 0

    @property
    def last_hazard_damage(self) -> int:
        return self.hazard_manager.last_damage

    @last_hazard_damage.setter
    def last_hazard_damage(self, value: int) -> None:
        self.hazard_manager.last_damage = value

    @property
    def last_enemy_damage(self) -> int:
        return self.combat_manager.last_enemy_damage

    @last_enemy_damage.setter
    def last_enemy_damage(self, value: int) -> None:
        self.combat_manager.last_enemy_damage = value

    @property
    def score(self) -> int:
        return self.score_manager.score

    @score.setter
    def score(self, value: int) -> None:
        self.score_manager.score = value

    @property
    def best_score(self) -> int:
        return self.score_manager.best_score

    @best_score.setter
    def best_score(self, value: int) -> None:
        self.score_manager.best_score = value

    @property
    def key_bindings(self) -> dict[str, int]:
        """Current keyboard mapping from :class:`KeybindManager`."""
        return self.keybind_manager.bindings

    def _setup_level(self) -> None:
        """Initialize or reset gameplay objects based on the chosen character."""
        self.level_manager.setup_level()
        self.score_manager.reset()
        self.boss_present_last = False
        self.boss_banner_until = 0
        self.level_limit = self.base_level_limit
        character = getattr(self, "selected_character", "") or ""
        current_map = getattr(self, "selected_map", "") or self.map_manager.current or ""
        self.auto_dev_manager.start_match(character, current_map)
        now = pygame.time.get_ticks()
        self.arena_intro_until = now + 2200
        self.arena_intro_title = "Hololive Coliseum"
        if character:
            self.arena_intro_subtitle = f"Featuring {character}"
        else:
            self.arena_intro_subtitle = f"Stage: {current_map or 'Arena'}"
        difficulty = getattr(self, "difficulty", "Normal")
        bonus = {"Hard": 1, "Elite": 2, "Adaptive": 3}.get(difficulty, 0)  
        self.ai_experience_manager.set_experience_level(
            max(1, self.ai_playthroughs + 1 + bonus)
        )
        self._autoplay_reset_character_audit(character)

    def apply_event_modifiers(self) -> None:
        """Refresh arena modifiers derived from MMO world regions."""

        config = self.event_modifier_manager.refresh()
        self.match_modifiers = config
        self.xp_multiplier = float(config.get("xp_multiplier", 1.0))
        step = float(config.get("stamina_regen_step", 1.0))
        if getattr(self, "player", None):
            self.player.stamina_manager.set_regen_step(step)
        self.hazard_manager.set_damage_multiplier(
            float(config.get("hazard_damage_multiplier", 1.0))
        )

    def _cycle_volume(self) -> None:
        """Cycle master volume using :class:`SoundManager`."""
        self.volume = self.sound_manager.cycle_volume()

    def _cycle_sfx_profile(self) -> None:
        profiles = list(self.sound_manager.SFX_PROFILES.keys())
        current = self.sound_manager.profile
        if current not in profiles:
            current = "Default"
        idx = profiles.index(current)
        next_profile = profiles[(idx + 1) % len(profiles)]
        self.sound_manager.set_profile(next_profile)
        self.sfx_profile = self.sound_manager.profile

    def _cycle_window_size(self) -> None:
        """Cycle through predefined window sizes."""
        self.window_size_index = (self.window_size_index + 1) % len(
            self.window_sizes
        )
        self.width, self.height = self.window_sizes[self.window_size_index]
        self.world_width = self.width
        self.world_height = self.height
        self.ground_y = self.height - 50
        self.screen = self._apply_display_mode()
        self._apply_font_scale()

    def _cycle_display_mode(self) -> None:
        """Cycle display modes between windowed, borderless, and fullscreen."""
        idx = self.display_modes.index(self.display_mode)
        self.display_mode = self.display_modes[(idx + 1) % len(self.display_modes)]
        if self.display_mode == "Fullscreen":
            info = pygame.display.Info()
            if info.current_w and info.current_h:
                self.width = info.current_w
                self.height = info.current_h
                self.world_width = self.width
                self.world_height = self.height
        self.fullscreen = self.display_mode == "Fullscreen"
        self.ground_y = self.height - 50
        self.screen = self._apply_display_mode()
        self._apply_font_scale()

    def _cycle_hud_size(self) -> None:
        """Cycle through HUD font sizes and apply immediately."""
        idx = self.hud_font_sizes.index(self.hud_font_size)
        self.hud_font_size = self.hud_font_sizes[(idx + 1) % len(self.hud_font_sizes)]
        self._apply_font_scale()

    def _apply_font_scale(self) -> None:
        """Apply accessibility and resolution-aware scaling to UI fonts."""
        user_scale = float(self.accessibility_manager.options.get("font_scale", 1.0))
        user_scale = normalize_user_font_scale(user_scale)
        self.accessibility_manager.options["font_scale"] = user_scale
        self.ui_metrics = build_ui_metrics_from_user_scale(
            user_scale,
            self.width,
            self.height,
        )
        scale = self.ui_metrics.ui_scale
        self.effective_font_scale = scale
        self.title_font = pygame.font.SysFont(None, max(28, int(64 * scale)))
        self.menu_font = pygame.font.SysFont(None, max(18, int(32 * scale)))
        self.autoplay_trace_font = pygame.font.SysFont(
            None, max(12, int(18 * scale))
        )
        self.small_font = pygame.font.SysFont(None, max(14, int(20 * scale)))
        hud_font = pygame.font.SysFont(
            None, max(10, int(self.hud_font_size * scale))
        )
        self.hud_manager = HUDManager(
            hud_font,
            metrics=self.ui_metrics,
            debugger=getattr(self, "ui_debugger", None),
        )
        if getattr(self, "ui_debugger", None) is not None:
            self.ui_debugger.set_metadata(
                resolution=f"{self.width}x{self.height}",
                effective_font_scale=round(self.effective_font_scale, 4),
                ui_scale=round(self.ui_metrics.ui_scale, 4),
            )
        if os.environ.get("HOLO_UI_DEBUG") == "1":
            debug_state = (
                int(self.width),
                int(self.height),
                round(self.effective_font_scale, 4),
                round(self.ui_metrics.ui_scale, 4),
            )
            if getattr(self, "_ui_debug_last", None) != debug_state:
                self._ui_debug_last = debug_state
                print(
                    "[UI] "
                    f"{self.width}x{self.height} "
                    f"effective_font_scale={self.effective_font_scale:.3f} "
                    f"ui_scale={self.ui_metrics.ui_scale:.3f}"
                )

    def _sync_player_selection_lists(self) -> None:
        """Ensure selection lists match the number of human players."""
        count = max(1, int(self.human_players))
        if len(self.character_selections) < count:
            self.character_selections.extend([None] * (count - len(self.character_selections)))
        if len(self.character_selections) > count:
            self.character_selections = self.character_selections[:count]
        if len(self.map_selections) < count:
            self.map_selections.extend([None] * (count - len(self.map_selections)))
        if len(self.map_selections) > count:
            self.map_selections = self.map_selections[:count]
        if self.selected_character and not self.character_selections[0]:
            self.character_selections[0] = self.selected_character
        self.character_select_index = min(self.character_select_index, count - 1)
        self.map_select_index = min(self.map_select_index, count - 1)

    def _refresh_weapon_sfx(self, actor) -> None:
        """Assign weapon SFX tag for melee events based on equipped weapon."""
        if actor is None or not hasattr(actor, "equipment"):
            return
        weapon = actor.equipment.get("weapon")
        if weapon is None:
            actor.weapon_sfx_event = None
            return
        class_name = weapon.__class__.__name__.lower()
        if class_name in {"sword", "axe", "spear", "bow", "wand"}:
            actor.weapon_sfx_event = class_name
            return
        actor.weapon_sfx_event = "weapon"

    def _toggle_fullscreen(self) -> None:
        """Switch between windowed and fullscreen display modes."""
        self.display_mode = "Fullscreen" if not self.fullscreen else "Windowed"
        self.fullscreen = self.display_mode == "Fullscreen"
        if self.fullscreen:
            info = pygame.display.Info()
            if info.current_w and info.current_h:
                self.width = info.current_w
                self.height = info.current_h
        self.world_width = self.width
        self.world_height = self.height
        self.ground_y = self.height - 50
        self.screen = self._apply_display_mode()
        self._apply_font_scale()

    def _apply_display_mode(self) -> pygame.Surface:
        """Apply the current window size and fullscreen settings."""
        self.fullscreen = self.display_mode == "Fullscreen"
        if self.display_mode == "Fullscreen":
            flags = pygame.FULLSCREEN
        elif self.display_mode == "Borderless":
            flags = pygame.NOFRAME
        else:
            flags = pygame.RESIZABLE
        return pygame.display.set_mode((self.width, self.height), flags, 32)

    def _get_arena_backdrop(self) -> pygame.Surface:
        size = (self.width, self.height)
        if self.arena_backdrop is not None and self.arena_backdrop_size == size:
            return self.arena_backdrop
        width, height = size
        surface = pygame.Surface(size)
        top = (12, 18, 28)
        bottom = (5, 8, 15)
        for y in range(height):
            ratio = y / max(1, height - 1)
            r = int(top[0] + (bottom[0] - top[0]) * ratio)
            g = int(top[1] + (bottom[1] - top[1]) * ratio)
            b = int(top[2] + (bottom[2] - top[2]) * ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
        overlay = pygame.Surface(size, pygame.SRCALPHA)
        rng = random.Random(41 + width + height)
        for _ in range(6):
            x = rng.randint(-200, width)
            y = rng.randint(0, height // 2)
            w = rng.randint(260, 420)
            h = rng.randint(120, 200)
            pygame.draw.polygon(
                overlay,
                (20, 40, 60, rng.randint(20, 40)),
                [(x, y), (x + w, y - 40), (x + w + 60, y + h), (x + 60, y + h)],
            )
        surface.blit(overlay, (0, 0))
        self.arena_backdrop = surface
        self.arena_backdrop_size = size
        return surface

    def _ui_debug_mode(self) -> str:
        """Map current game state to coarse UI diagnostics mode."""
        if self.state == "mmo":
            return "mmo"
        if self.menu_drawers.get(self.state) is not None:
            return "menu"
        return "hud"


    def _get_ground_surface(self, width: int) -> pygame.Surface:
        size = (width, max(0, self.height - self.ground_y))
        if self.ground_surface is not None and self.ground_surface_size == size:
            return self.ground_surface
        width, height = size
        surface = pygame.Surface((max(1, width), max(1, height)), pygame.SRCALPHA)
        top = (70, 70, 80)
        bottom = (35, 35, 45)
        for y in range(height):
            ratio = y / max(1, height - 1)
            r = int(top[0] + (bottom[0] - top[0]) * ratio)
            g = int(top[1] + (bottom[1] - top[1]) * ratio)
            b = int(top[2] + (bottom[2] - top[2]) * ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
        pygame.draw.rect(surface, (100, 100, 120), pygame.Rect(0, 0, width, 4))
        rng = random.Random(width * 11 + height * 7)
        for _ in range(max(6, width // 90)):
            bx = rng.randint(8, max(8, width - 16))
            by = rng.randint(8, max(8, height - 10))
            pygame.draw.rect(surface, (85, 85, 95), pygame.Rect(bx, by, 10, 4))
        self.ground_surface = surface
        self.ground_surface_size = size
        return surface

    def _draw_stage_barriers(self) -> None:
        height = self.height - self.ground_y
        if height <= 0:
            return
        bar_width = 10
        bar_height = max(0, height - 6)
        left = pygame.Rect(0, self.ground_y + 3, bar_width, bar_height)
        right = pygame.Rect(
            self.world_width - bar_width, self.ground_y + 3, bar_width, bar_height
        )
        left = self.camera_manager.apply(left)
        right = self.camera_manager.apply(right)
        pygame.draw.rect(self.screen, (60, 70, 90), left)
        pygame.draw.rect(self.screen, (60, 70, 90), right)
        pygame.draw.rect(self.screen, (120, 140, 170), left, 2)
        pygame.draw.rect(self.screen, (120, 140, 170), right, 2)

    def _draw_world_sprites(self, group) -> None:
        """Draw world sprites through the camera transform."""
        for sprite in group:
            image = getattr(sprite, "image", None)
            rect = getattr(sprite, "rect", None)
            if image is None or rect is None:
                continue
            self.screen.blit(image, self.camera_manager.apply(rect))

    def _draw_revive_glow(self, now: int) -> None:
        player = getattr(self, "player", None)
        if player is None or player.revive_until <= now:
            return
        rect = self.camera_manager.apply(player.rect)
        radius = max(rect.width, rect.height) // 2 + 10
        pulse = (math.sin(now / 120) + 1) * 0.5
        alpha = 120 + int(80 * pulse)
        glow = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (120, 200, 255, alpha), (radius, radius), radius, 3)
        self.screen.blit(glow, glow.get_rect(center=rect.center))

    def _apply_pending_respawn(self, now: int) -> None:
        player = getattr(self, "player", None)
        if player is None or not getattr(player, "pending_respawn", False):
            player = None
        if player is not None and getattr(player, "pending_respawn", False):
            spawn = getattr(
                player,
                "spawn_point",
                pygame.math.Vector2(100, self.ground_y - 60),
            )
            player.begin_revive((int(spawn.x), int(spawn.y)), now)
        for ally in list(getattr(self, "allies", [])):
            if not getattr(ally, "pending_respawn", False):
                continue
            spawn = getattr(
                ally,
                "spawn_point",
                pygame.math.Vector2(140, self.ground_y - 60),
            )
            ally.begin_revive((int(spawn.x), int(spawn.y)), now)

    def _handle_fall_deaths(self, now: int) -> None:
        fall_limit = self.ground_y + 200
        player = getattr(self, "player", None)
        if player is not None and player.rect.top > fall_limit:
            if player.lives > 0:
                player.lives -= 1
                if player.lives > 0:
                    spawn = getattr(
                        player,
                        "spawn_point",
                        pygame.math.Vector2(100, self.ground_y - 60),
                    )
                    player.begin_revive((int(spawn.x), int(spawn.y)), now)
                    self._autoplay_record_feature("fall:revive")
            if player.lives == 0:
                player.health = 0
                self._autoplay_record_feature("fall:death")
        for ally in list(getattr(self, "allies", [])):
            if ally.rect.top <= fall_limit:
                continue
            if ally.lives > 0:
                ally.lives -= 1
                if ally.lives > 0:
                    spawn = getattr(
                        ally,
                        "spawn_point",
                        pygame.math.Vector2(140, self.ground_y - 60),
                    )
                    ally.begin_revive((int(spawn.x), int(spawn.y)), now)
            if ally.lives == 0:
                ally.health = 0
        for enemy in list(self.enemies):
            if enemy.rect.top > fall_limit:
                enemy.kill()
                self.kills += 1
                self.score += 1

    def _ai_targets(self) -> list[pygame.sprite.Sprite]:
        targets = []
        if getattr(self, "player", None):
            targets.append(self.player)
        targets.extend(list(getattr(self, "allies", [])))
        return targets

    def _mob_spawn_points(self) -> list[tuple[int, int]]:
        default_points = [
            (int(self.world_width * 0.15), self.ground_y - 60),
            (int(self.world_width * 0.85), self.ground_y - 60),
            (int(self.world_width * 0.45), self.ground_y - 60),
        ]
        config = self.mob_spawn_config or {}
        points = config.get("points")
        if isinstance(points, list) and points:
            return [
                (int(p[0]), int(p[1]))
                for p in points
                if isinstance(p, (list, tuple)) and len(p) == 2
            ]
        return default_points

    def _spawn_mob_wave(self, now: int) -> None:
        if len(self.enemies) >= self.mob_spawn_max:
            return
        points = self._mob_spawn_points()
        wave = max(1, int(self.mob_spawn_config.get("wave", self.mob_spawn_wave)))
        image_dir = os.path.join(os.path.dirname(__file__), "..", "Images")
        for idx in range(wave):
            if len(self.enemies) >= self.mob_spawn_max:
                break
            px, py = points[idx % len(points)]
            mob = MobEnemy(
                px,
                py,
                os.path.join(image_dir, "enemy_right.png"),
                difficulty=self.difficulty,
            )
            mob.platforms = self.platforms
            mob.ground_gaps = list(self.ground_gaps)
            mob.spawn_x = px
            mob.sound_manager = self.sound_manager
            self.enemies.add(mob)
            self.all_sprites.add(mob)
            self.team_manager.set_team(mob, 2)
        self._autoplay_trace("Mob wave spawned", now=now)

    def _maybe_spawn_mobs(self, now: int) -> None:
        if not self.mob_spawn_enabled:
            return
        interval = int(self.mob_spawn_config.get("interval", self.mob_spawn_interval))
        if interval <= 0:
            return
        if now - self.mob_spawn_last < interval:
            return
        self.mob_spawn_last = now
        self._spawn_mob_wave(now)

    def open_vote_menu(self) -> None:
        """Open the vote category selection menu."""
        self.vote_categories = ["Character", "Biome", "Back"]
        self._set_state("vote_category")
        self.menu_index = 0

    def _set_state(self, state: str) -> None:
        """Helper to update game and managers with a new state."""
        previous = self.state
        self.state = state
        self.state_manager.change(state)
        self.menu_manager.reset()
        self.menu_index = self.menu_manager.index
        self._autoplay_trace(f"State -> {state}")
        if self.autoplay_log_enabled:
            self._autoplay_log(f"State -> {state}")
        if previous == "mmo" and state != "mmo":
            self._mmo_network_leave()
        if state != "mmo":
            self.autoplay_mmo_state = None
            self.mmo_trial_active = False
        if state == "mmo" and previous != "mmo":
            self._mmo_network_join()
            self._request_mmo_snapshot()
            self._request_mmo_world_snapshot()
        if state in {"char", "map"}:
            self._sync_player_selection_lists()
            if state == "char":
                self.character_select_index = 0
            if state == "map":
                self.map_select_index = 0
                if self.multiplayer and self.human_players > 1:
                    self.map_selections = [None] * max(1, int(self.human_players))
                self.map_select_message = ""
        if state == "playing":
            self.autoplay_last_health = None
            self.autoplay_last_kills = self.kills
            self.autoplay_last_feedback = pygame.time.get_ticks() 

    def _unlock_mmo(self) -> None:
        """Unlock the MMO hub after finishing the story."""
        if self.mmo_unlocked:
            return
        self.mmo_unlocked = True
        if "MMO" not in self.main_menu_options:
            insert_at = 2 if len(self.main_menu_options) > 2 else len(self.main_menu_options)
            self.main_menu_options.insert(insert_at, "MMO")

    def _ensure_mmo_world(self) -> None:
        """Ensure MMO regions exist so the hub can render."""
        self.world_generation_manager.sync_world()
        regions = self.world_generation_manager.region_manager.get_regions()    
        if regions:
            self._mmo_seed_operations()
            self._mmo_seed_events()
            self._mmo_seed_expeditions()
            self._mmo_seed_directives()
            self._mmo_seed_bounties()
            self._mmo_seed_projects()
            self._mmo_seed_training()
            return
        seed_manager = self.world_generation_manager.seed_manager
        for _ in range(6):
            seed = f"{random.getrandbits(128):032x}"
            seed_manager.add_seed(seed)
            self.world_generation_manager.generate_region_from_seed(seed, self.mmo_player_id)
        self._mmo_seed_operations()
        self._mmo_seed_events()
        self._mmo_seed_expeditions()
        self._mmo_seed_directives()
        self._mmo_seed_bounties()
        self._mmo_seed_projects()
        self._mmo_seed_training()

    def _enter_mmo_mode(self) -> None:
        """Switch to the MMO hub screen."""
        if not self.mmo_unlocked and not self.autoplay_force_mmo:
            self.mmo_message = "MMO locked. Complete the final story chapter to unlock."
            self._set_state("main_menu")
            return
        self._select_mmo_shard()
        if self.autoplay and self.autoplay_mmo_fast:
            self.mmo_pending = False
            if not self.mmo_seen_tour:
                self.mmo_show_tour = True
                self.mmo_tour_step = 0
            self._set_state("mmo")
            return
        self._ensure_mmo_world()
        self.mmo_backend.upsert_regions(
            self.world_generation_manager.region_manager.get_regions()
        )
        self._mmo_sync_state(pygame.time.get_ticks(), force=True)
        self.mmo_pending = False
        if not self.mmo_seen_tour:
            self.mmo_show_tour = True
            self.mmo_tour_step = 0
        self._set_state("mmo")

    def _mmo_focus_selected(self) -> None:
        region = self._mmo_selected_region()
        if not region:
            self.mmo_message = "No region selected."
            return
        pos = region.get("position")
        if not pos or len(pos) != 2:
            self.mmo_message = "Selected region missing position."
            return
        self.world_player_manager.set_position(
            self.mmo_player_id, (float(pos[0]), float(pos[1]))
        )
        self.mmo_message = f"Focused on {region.get('name', 'region')}."

    def _mmo_cycle_filter(self) -> None:
        idx = self.mmo_filters.index(self.mmo_biome_filter)
        self.mmo_biome_filter = self.mmo_filters[(idx + 1) % len(self.mmo_filters)]
        self.mmo_region_index = 0
        self.mmo_region_scroll = 0
        self.mmo_message = f"Filter: {self.mmo_biome_filter.title()}"

    def _mmo_toggle_favorite(self) -> None:
        region = self._mmo_selected_region()
        if not region:
            self.mmo_message = "No region selected."
            return
        name = str(region.get("name", "region"))
        if name in self.mmo_favorites:
            self.mmo_favorites.remove(name)
            self.mmo_message = f"Unfavorited {name}."
        else:
            self.mmo_favorites.add(name)
            self.mmo_message = f"Favorited {name}."

    def _update_mmo_controls(self) -> None:
        """Update MMO player position based on keyboard input."""
        keys = pygame.key.get_pressed()
        speed = self.mmo_speed * (2 if keys[pygame.K_LSHIFT] else 1)
        dx = 0.0
        dy = 0.0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += speed
        if dx or dy:
            self.world_player_manager.move_player(self.mmo_player_id, dx, dy)

    def _mmo_sync_region(self) -> None:
        """Sync data about the nearest region into storage."""
        pos = self.world_player_manager.get_position(self.mmo_player_id)
        region = self._mmo_nearest_region(pos)
        if not region:
            self.mmo_message = "No region data available."
            return
        self.mmo_backend.upsert_regions([region])
        self.mmo_message = f"Synced {region.get('name', 'region')}."

    def _mmo_spawn_region(self) -> None:
        """Generate a new region if the player is near the frontier."""
        regions = self.world_generation_manager.region_manager.get_regions()
        max_radius = max((r.get("radius", 0) for r in regions), default=0)
        pos = self.world_player_manager.get_position(self.mmo_player_id)
        if max_radius <= 0:
            return
        distance = (pos[0] ** 2 + pos[1] ** 2) ** 0.5
        if distance < max_radius * 0.85:
            self.mmo_message = "Push further out to discover a new region."
            return
        seed = f"{random.getrandbits(128):032x}"
        self.world_generation_manager.seed_manager.add_seed(seed)
        region = self.world_generation_manager.generate_region_from_seed(
            seed,
            self.mmo_player_id,
        )
        self.mmo_backend.upsert_regions([region])
        self.mmo_message = f"Discovered {region.get('name', 'region')}!"

    def _bump_ai_progression(self) -> None:
        """Increase AI progression after a playthrough ends."""
        self.ai_playthroughs += 1
        if self.ai_playthroughs % 2 == 0:
            self.mmo_ai_level = min(10, self.mmo_ai_level + 1)
        self.ai_progression = {
            "playthroughs": self.ai_playthroughs,
            "mmo_level": self.mmo_ai_level,
        }
        self.ai_experience_manager.set_experience_level(
            max(1, self.ai_playthroughs + 1)
        )
        self._log_ai_experience(final=True)

    def _log_ai_experience(self, *, final: bool = False) -> None:
        """Persist AI experience snapshots for analysis."""
        if not self.enemies:
            return
        now = pygame.time.get_ticks()
        if not final and now - self.ai_experience_last_log < self.ai_experience_interval:
            return
        self.ai_experience_last_log = now
        snapshot = self.ai_experience_manager.snapshot(list(self.enemies))
        entry = self.ai_experience_store.build_snapshot(
            mode=self.selected_mode or "unknown",
            difficulty=self.difficulty_levels[self.difficulty_index],
            playthrough=self.ai_playthroughs,
            level_index=self.autoplay_level_index,
            ai_level=self.mmo_ai_level,
            agents=snapshot,
        )
        self.ai_experience_store.append_snapshot(entry, keep=200)

    def _setup_mmo_agents(self) -> None:
        """Seed roaming MMO agents for background exploration."""
        rng = random.Random(self.mmo_ai_seed)
        agents: list[dict[str, object]] = []
        for idx in range(max(0, self.mmo_ai_count)):
            agents.append(
                {
                    "id": f"agent_{idx + 1}",
                    "pos": [rng.uniform(-0.6, 0.6), rng.uniform(-0.6, 0.6)],
                    "dir": [rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0)],
                    "cooldown": rng.randint(80, 200),
                }
            )
        self.mmo_auto_agents = agents

    def _update_mmo_agents(self) -> None:
        """Update roaming MMO agents and allow exploration."""
        if not self.mmo_auto_agents:
            return
        regions = self.world_generation_manager.region_manager.get_regions()
        max_radius = max((r.get("radius", 0) for r in regions), default=1)
        level_boost = 1.0 + (self.mmo_ai_level - 1) * 0.06
        rng = random.Random(
            self.mmo_ai_seed + int(pygame.time.get_ticks() / 1200)
        )
        for agent in self.mmo_auto_agents:
            pos = agent["pos"]
            direction = agent["dir"]
            cooldown = int(agent.get("cooldown", 0))
            target = agent.get("target")
            if isinstance(target, (list, tuple)) and len(target) == 2:
                dx = float(target[0]) - float(pos[0])
                dy = float(target[1]) - float(pos[1])
                dist = (dx * dx + dy * dy) ** 0.5
                if dist > 0.01:
                    direction[0] = dx / dist
                    direction[1] = dy / dist
                if dist < max_radius * 0.1:
                    agent.pop("target", None)
            if cooldown <= 0:
                direction[0] = rng.uniform(-1.0, 1.0)
                direction[1] = rng.uniform(-1.0, 1.0)
                agent["cooldown"] = rng.randint(90, 220)
            else:
                agent["cooldown"] = cooldown - 1
            speed = self.mmo_ai_radius * level_boost
            speed *= 1.2 if rng.random() > 0.8 else 0.7
            pos[0] += float(direction[0]) * speed
            pos[1] += float(direction[1]) * speed
            distance = (pos[0] ** 2 + pos[1] ** 2) ** 0.5
            if distance > max_radius:
                pos[0] *= (max_radius * 0.98) / max(0.01, distance)
                pos[1] *= (max_radius * 0.98) / max(0.01, distance)
            discovery_chance = 0.985 - min(0.08, self.mmo_ai_level * 0.01)
            if distance > max_radius * 0.88 and rng.random() > discovery_chance:
                seed = f"{rng.getrandbits(128):032x}"
                self.world_generation_manager.seed_manager.add_seed(seed)
                region = self.world_generation_manager.generate_region_from_seed(
                    seed,
                    str(agent.get("id")),
                )
                self.mmo_backend.upsert_regions([region])

    def _victory_report_lines(self) -> list[str]:
        focus = self.post_victory_focus or {}
        plan = self.post_victory_plan or {}
        boss_plan = plan.get("boss_plan", {}) if isinstance(plan, dict) else {}
        lines = ["Auto-Dev Summary"]
        if focus:
            hazard = focus.get("trending_hazard", "n/a")
            favorite = focus.get("favorite_character", "n/a")
            lines.append(f"Trending Hazard: {hazard}")
            lines.append(f"Favorite Character: {favorite}")
            avg_score = focus.get("average_score")
            avg_time = focus.get("average_time")
            if avg_score is not None:
                lines.append(f"Avg Score: {int(avg_score)}")
            if avg_time is not None:
                lines.append(f"Avg Time: {int(avg_time)}s")
        if boss_plan:
            boss_name = boss_plan.get("name", "Unknown")
            threat = boss_plan.get("threat", 0)
            lines.append(f"Target Boss: {boss_name}")
            lines.append(f"Threat Rating: {round(float(threat), 2)}")
        quests = plan.get("quests") if isinstance(plan, dict) else None
        if isinstance(quests, (list, tuple)):
            lines.append(f"Quest Seeds: {len(quests)}")
        security_score = plan.get("network_security_score") if isinstance(plan, dict) else None
        if security_score is not None:
            lines.append(f"Net Security: {round(float(security_score), 2)}")
        lines.append("Back")
        return lines

    def _victory_briefing_lines(self) -> list[str]:
        regions = self.world_generation_manager.region_manager.get_regions()
        unlocked = "Yes" if self.mmo_unlocked or self.mmo_pending else "No"
        lines = [
            f"MMO Unlock: {unlocked}",
            f"AI Level: {self.mmo_ai_level}",
            f"Arena Wins: {self.arena_wins}",
            f"Regions Online: {len(regions)}",
        ]
        if self.mmo_plan_summary:
            lines.append(self.mmo_plan_summary)
        lines.append("Back")
        return lines

    def _draw_victory_report(self) -> None:
        self._draw_background()
        self._draw_title("Auto-Dev Report", (self.width // 2, 40))
        lines = self._victory_report_lines()
        for i, line in enumerate(lines):
            self._draw_option_label(line, i, (self.width // 2, 140 + i * 30))
        self._draw_border()

    def _draw_victory_briefing(self) -> None:
        self._draw_background()
        self._draw_title("MMO Briefing", (self.width // 2, 40))
        lines = self._victory_briefing_lines()
        for i, line in enumerate(lines):
            self._draw_option_label(line, i, (self.width // 2, 150 + i * 34))
        self._draw_border()

    def _draw_victory_actions(self) -> None:
        self._draw_background()
        self._draw_title("MMO Launchpad", (self.width // 2, 40))
        options = self._victory_actions_options()
        for i, option in enumerate(options):
            self._draw_option_label(
                option,
                i,
                (self.width // 2, 150 + i * 32),
            )
        if self.victory_action_message:
            message = self.small_font.render(
                self.victory_action_message, True, (210, 220, 230)
            )
            self.screen.blit(
                message,
                message.get_rect(center=(self.width // 2, self.height - 70)),
            )
        self._draw_border()

    def _draw_mmo_world(self) -> None:
        """Render a lightweight MMO world hub."""
        draw_mmo_backdrop(self)
        debugger = getattr(self, "ui_debugger", None)
        if debugger is not None and debugger.is_active:
            screen_bounds = pygame.Rect(0, 0, self.width, self.height)
            gutter = int(getattr(getattr(self, "ui_metrics", None), "gutter", 12))
            safe_bounds = pygame.Rect(
                gutter,
                gutter,
                max(0, self.width - gutter * 2),
                max(0, self.height - gutter * 2),
            )
            debugger.collect_rect("mmo.screen_bounds", screen_bounds, "bounds")
            debugger.collect_rect(
                "mmo.safe_bounds",
                safe_bounds,
                "bounds",
                meta={"bounds": screen_bounds},
            )
        regions = self.world_generation_manager.region_manager.get_regions()
        self._mmo_draw_shard_widget()
        center = (self.width // 2, self.height // 2)
        max_radius = max((r.get("radius", 0) for r in regions), default=1)
        scale = min(self.width, self.height) / (2 * (max_radius + 1))
        scale *= self.mmo_zoom
        ring_color = (40, 60, 90)
        for radius in range(1, max(2, max_radius + 1)):
            ring = int(radius * scale)
            pygame.draw.circle(self.screen, ring_color, center, ring, 1)
        biome_colors = {
            "plains": (70, 140, 220),
            "forest": (80, 170, 120),
            "desert": (210, 170, 90),
            "tundra": (120, 180, 200),
        }
        if self.mmo_layers.get("routes", True):
            for route in self.mmo_trade_routes:
                origin = str(route.get("origin", ""))
                destination = str(route.get("destination", ""))
                origin_region = self._mmo_find_region(origin)
                dest_region = self._mmo_find_region(destination)
                if not origin_region or not dest_region:
                    continue
                opos = origin_region.get("position")
                dpos = dest_region.get("position")
                if not opos or not dpos:
                    continue
                ox = int(center[0] + float(opos[0]) * scale)
                oy = int(center[1] + float(opos[1]) * scale)
                dx = int(center[0] + float(dpos[0]) * scale)
                dy = int(center[1] + float(dpos[1]) * scale)
                pygame.draw.line(
                    self.screen,
                    (120, 200, 230),
                    (ox, oy),
                    (dx, dy),
                    1,
                )
        if self.mmo_layers.get("heatmap", True) and regions:
            threats = [self._mmo_heatmap_threat(r) for r in regions]
            min_threat = min(threats)
            max_threat = max(threats)
            spread = max(1.0, max_threat - min_threat)
            for region in regions:
                pos = region.get("position")
                if not pos or len(pos) != 2:
                    continue
                rx = int(center[0] + float(pos[0]) * scale)
                ry = int(center[1] + float(pos[1]) * scale)
                threat = self._mmo_heatmap_threat(region)
                intensity = int(80 + ((threat - min_threat) / spread) * 140)
                color = (intensity, 90, 90)
                pygame.draw.circle(self.screen, color, (rx, ry), 12, 1)
        severity_colors = {
            "low": (120, 200, 200),
            "medium": (255, 200, 120),
            "high": (255, 130, 130),
        }
        event_regions: dict[str, str] = {}
        if self.mmo_layers.get("events", True):
            for event in self.mmo_world_events:
                region_name = str(event.get("region", ""))
                if not region_name:
                    continue
                severity = str(event.get("severity", "low")).lower()
                event_regions[region_name] = severity
        influence_regions: set[str] = set()
        for region in regions:
            if self._mmo_influence_value(region) >= 70:
                influence_regions.add(str(region.get("name", "")))
        if event_regions or influence_regions:
            now = pygame.time.get_ticks()
            glow = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            for region in regions:
                pos = region.get("position")
                if not pos or len(pos) != 2:
                    continue
                rx = int(center[0] + float(pos[0]) * scale)
                ry = int(center[1] + float(pos[1]) * scale)
                name = str(region.get("name", ""))
                if name in influence_regions:
                    influence = self._mmo_influence_value(region)
                    intensity = max(0.0, min(1.0, (influence - 70) / 30))
                    base = self._mmo_pulse_color((120, 200, 255), now, 30)
                    alpha = 60 + int(90 * intensity)
                    pygame.draw.circle(glow, (*base, alpha), (rx, ry), 18)
                severity = event_regions.get(name)
                if severity:
                    base = severity_colors.get(severity, (120, 200, 200))
                    pulse = self._mmo_pulse_color(base, now, 25)
                    pygame.draw.circle(glow, (*pulse, 70), (rx, ry), 22, 2)
            self.screen.blit(glow, (0, 0))
        for region in regions:
            pos = region.get("position")
            if not pos or len(pos) != 2:
                continue
            rx = int(center[0] + float(pos[0]) * scale)
            ry = int(center[1] + float(pos[1]) * scale)
            biome = str(region.get("biome", "plains")).lower()
            color = biome_colors.get(biome, (70, 140, 220))
            if region == self._mmo_selected_region():
                color = (255, 210, 120)
            pygame.draw.circle(self.screen, color, (rx, ry), 6)
            name = str(region.get("name", ""))
            if name in self.mmo_favorites:
                pygame.draw.circle(self.screen, (255, 240, 180), (rx, ry), 10, 1)
        if self.mmo_layers.get("outposts", True):
            for outpost in self.mmo_outposts:
                region_name = str(outpost.get("region", ""))
                region = self._mmo_find_region(region_name)
                if not region:
                    continue
                pos = region.get("position")
                if not pos or len(pos) != 2:
                    continue
                ox = int(center[0] + float(pos[0]) * scale)
                oy = int(center[1] + float(pos[1]) * scale)
                rect = pygame.Rect(ox - 5, oy - 5, 10, 10)
                pygame.draw.rect(self.screen, (180, 220, 140), rect, 2)
        if self.mmo_layers.get("events", True):
            for event in self.mmo_world_events:
                region_name = str(event.get("region", ""))
                region = self._mmo_find_region(region_name)
                if not region:
                    continue
                pos = region.get("position")
                if not pos or len(pos) != 2:
                    continue
                ex = int(center[0] + float(pos[0]) * scale)
                ey = int(center[1] + float(pos[1]) * scale)
                severity = str(event.get("severity", "low")).lower()
                color = severity_colors.get(severity, (120, 200, 200))
                points = [(ex, ey - 8), (ex - 6, ey + 6), (ex + 6, ey + 6)]
                pygame.draw.polygon(self.screen, color, points, 1)
        if self.mmo_layers.get("contracts", True):
            for contract in self.mmo_contracts:
                if contract.get("status") != "active":
                    continue
                region_name = str(contract.get("region", ""))
                region = self._mmo_find_region(region_name)
                if not region:
                    continue
                pos = region.get("position")
                if not pos or len(pos) != 2:
                    continue
                cx = int(center[0] + float(pos[0]) * scale)
                cy = int(center[1] + float(pos[1]) * scale)
                diamond = [
                    (cx, cy - 6),
                    (cx - 6, cy),
                    (cx, cy + 6),
                    (cx + 6, cy),
                ]
                pygame.draw.polygon(self.screen, (160, 210, 255), diamond, 1)   
        if self.mmo_layers.get("expeditions", True):
            for expedition in self.mmo_expeditions:
                status = str(expedition.get("status", "idle"))
                if status in {"complete", "idle"}:
                    continue
                region_name = str(expedition.get("region", ""))
                region = self._mmo_find_region(region_name)
                if not region:
                    continue
                pos = region.get("position")
                if not pos or len(pos) != 2:
                    continue
                ex = int(center[0] + float(pos[0]) * scale)
                ey = int(center[1] + float(pos[1]) * scale)
                color = (140, 200, 255)
                if status == "exploring":
                    color = (170, 240, 180)
                elif status == "returning":
                    color = (255, 200, 140)
                pygame.draw.circle(self.screen, color, (ex, ey), 6, 1)
                pygame.draw.line(
                    self.screen,
                    color,
                    (ex - 4, ey),
                    (ex + 4, ey),
                    1,
                )
        if self.mmo_layers.get("bounties", True):
            for bounty in self.mmo_bounties:
                status = str(bounty.get("status", "open"))
                if status == "complete":
                    continue
                region_name = str(bounty.get("region", ""))
                region = self._mmo_find_region(region_name)
                if not region:
                    continue
                pos = region.get("position")
                if not pos or len(pos) != 2:
                    continue
                bx = int(center[0] + float(pos[0]) * scale)
                by = int(center[1] + float(pos[1]) * scale)
                color = (255, 170, 170)
                pygame.draw.circle(self.screen, color, (bx, by), 6, 1)
                pygame.draw.line(
                    self.screen,
                    color,
                    (bx - 4, by - 4),
                    (bx + 4, by + 4),
                    1,
                )
                pygame.draw.line(
                    self.screen,
                    color,
                    (bx - 4, by + 4),
                    (bx + 4, by - 4),
                    1,
                )
        if self.mmo_layers.get("resources", True):
            resource_colors = {
                "Aether Ore": (160, 200, 255),
                "Sunsteel": (255, 200, 120),
                "Crystal": (180, 140, 255),
                "Runic Wood": (120, 200, 140),
                "Tide Salt": (120, 180, 230),
            }
            for region in regions:
                pos = region.get("position")
                if not pos or len(pos) != 2:
                    continue
                rx = int(center[0] + float(pos[0]) * scale)
                ry = int(center[1] + float(pos[1]) * scale)
                resource, richness = self._mmo_region_resources(region)
                color = resource_colors.get(resource, (180, 200, 220))
                size = max(2, min(6, int(richness)))
                pygame.draw.circle(self.screen, color, (rx, ry), size, 1)
        if self.mmo_layers.get("agents", True):
            for agent in self.mmo_auto_agents:
                pos = agent.get("pos") or [0.0, 0.0]
                rx = int(center[0] + float(pos[0]) * scale)
                ry = int(center[1] + float(pos[1]) * scale)
                pygame.draw.circle(self.screen, (130, 210, 180), (rx, ry), 5)
        if self.mmo_layers.get("remotes", True):
            for player_id, pos in self.mmo_remote_positions.items():
                rx = int(center[0] + pos[0] * scale)
                ry = int(center[1] + pos[1] * scale)
                pygame.draw.circle(self.screen, (120, 200, 255), (rx, ry), 6)
        player_pos = self.world_player_manager.get_position(self.mmo_player_id)
        px = int(center[0] + player_pos[0] * scale)
        py = int(center[1] + player_pos[1] * scale)
        pygame.draw.circle(self.screen, (255, 220, 120), (px, py), 8)
        if self.mmo_waypoint:
            wpos = self.mmo_waypoint.get("position")
            if isinstance(wpos, (list, tuple)) and len(wpos) == 2:
                wx = int(center[0] + float(wpos[0]) * scale)
                wy = int(center[1] + float(wpos[1]) * scale)
                pygame.draw.line(self.screen, (255, 230, 150), (px, py), (wx, wy), 1)
                pygame.draw.circle(self.screen, (255, 230, 150), (wx, wy), 7, 2)
        nearest = self._mmo_nearest_region(player_pos)
        palette = mmo_palette()
        overlay_label = self.mmo_overlay_mode.title()
        subtitle = f"Overlay {overlay_label}"
        if nearest:
            name = nearest.get("name", "region")
            biome = nearest.get("biome", "")
            subtitle = f"{name}  |  {biome}  |  Overlay {overlay_label}"
        status_lines = [
            f"Regions: {len(regions)}",
            f"Credits: {self.mmo_credits}",
            f"Account: {self.account_id}",
        ]
        match_line = self._mmo_header_match_line()
        if match_line:
            status_lines.append(match_line)
        draw_mmo_header(
            self,
            title="MMO Command Hub",
            subtitle=subtitle,
            status_lines=status_lines,
        )
        sections = [
            (
                "Navigation",
                [
                    "Move: WASD/Arrows",
                    "Select: Left/Right",
                    "Focus: F  Filter: G",
                    "Zoom: +/-  Panel: Tab",
                ],
            ),
            (
                "Operations",
                [
                    "Sync: E  Discover: R",
                    "Auto-dev: P  Waypoint: W",
                    "Favorite: B  Clear: C",
                ],
            ),
            (
                "Intel & Panels",
                [
                    "Details: I  Help: H",
                    "Quests: L  Growth: Y",
                    "Party: U  Network: N",
                    "Alerts: O  Minimap: M",
                ],
            ),
            (
                "Overlays",
                [
                    f"Overlay: {overlay_label} (F1-F12)",
                    "Shift+Key: Advanced Ops",
                    "Esc: Main Menu",
                ],
            ),
        ]
        account_data = self.accounts_manager.get(self.account_id) or {}
        account_level = account_data.get("level", "guest")
        key_status = "On File" if account_data.get("public_key") else "None"
        sections.append(
            (
                "Account",
                [
                    f"ID: {self.account_id}",
                    f"Tier: {account_level}",
                    f"Key: {key_status}",
                ],
            ),
        )
        if self.mmo_message or self.mmo_plan_summary:
            notes = []
            if self.mmo_message:
                notes.append(self.mmo_message)
            if self.mmo_plan_summary:
                notes.append(self.mmo_plan_summary)
            sections.append(("Status", notes))
        draw_mmo_command_panel(
            self,
            rect=pygame.Rect(18, 86, 360, 250),
            sections=sections,
        )
        active_contracts = len(
            [c for c in self.mmo_contracts if c.get("status") == "active"]
        )
        active_expeditions = len(
            [
                e
                for e in self.mmo_expeditions
                if str(e.get("status", "idle")) not in {"idle", "complete"}
            ]
        )
        active_bounties = len(
            [b for b in self.mmo_bounties if b.get("status") != "complete"]
        )
        influence_values = [self._mmo_influence_value(r) for r in regions]
        avg_influence = (
            sum(influence_values) / len(influence_values) if influence_values else 0.0
        )
        shard_summary = self._mmo_shard_summary()
        status_rows = [
            ("Account", str(self.account_id)),
            ("Regions", f"{len(regions)} online"),
            ("Outposts", str(len(self.mmo_outposts))),
            ("Events", str(len(self.mmo_world_events))),
            ("Contracts", str(active_contracts)),
            ("Expeditions", str(active_expeditions)),
            ("Bounties", str(active_bounties)),
            ("Auto Agents", str(len(self.mmo_auto_agents))),
            ("Remote Links", str(len(self.mmo_remote_positions))),
            ("Match", self._mmo_match_label()),
            ("Shard Health", shard_summary),
            ("Influence Avg", f"{avg_influence:.1f}%"),
            ("Favorites", str(len(self.mmo_favorites))),
        ]
        draw_mmo_status_panel(
            self,
            rect=pygame.Rect(self.width - 328, 86, 300, 250),
            title="Operations Status",
            rows=status_rows,
        )
        legend_rect = pygame.Rect(self.width - 328, 350, 300, 200)
        legend_panel = pygame.Surface(legend_rect.size, pygame.SRCALPHA)
        legend_panel.fill((*palette["panel_alt"], 220))
        pygame.draw.rect(legend_panel, palette["border"], legend_panel.get_rect(), 2)
        legend_title = self.small_font.render("Legend", True, palette["accent"])
        legend_panel.blit(legend_title, (16, 10))
        legend_lines = [
            ("Player", (255, 220, 120)),
            ("Region", (70, 140, 220)),
            ("Outpost", (180, 220, 140)),
            ("Event", (120, 200, 200)),
            ("Contract", (160, 210, 255)),
            ("Expedition", (140, 200, 255)),
            ("Bounty", (255, 170, 170)),
            ("Route", (120, 200, 230)),
            ("Influence", (120, 200, 255)),
        ]
        for idx, (label, color) in enumerate(legend_lines):
            column = 0 if idx < 5 else 1
            row = idx if idx < 5 else idx - 5
            x = 22 + column * 140
            y = 34 + row * 18
            pygame.draw.circle(legend_panel, color, (x, y + 6), 4)
            text = self.small_font.render(label, True, palette["text_dim"])
            legend_panel.blit(text, (x + 12, y))
        focus = self.mmo_focus_region_name or "n/a"
        focus_line = self.small_font.render(f"Focus: {focus}", True, palette["text"])
        legend_panel.blit(focus_line, (16, 132))
        threat = max(0.0, min(10.0, float(self.mmo_focus_region_threat or 0.0)))
        threat_ratio = min(1.0, threat / 10.0)
        bar_rect = pygame.Rect(16, 168, 180, 8)
        pygame.draw.rect(legend_panel, (25, 35, 50), bar_rect)
        bar_color = (
            int(120 + 100 * threat_ratio),
            int(200 - 120 * threat_ratio),
            90,
        )
        pygame.draw.rect(
            legend_panel,
            bar_color,
            pygame.Rect(bar_rect.x, bar_rect.y, int(bar_rect.width * threat_ratio), 8),
        )
        pygame.draw.rect(legend_panel, palette["border"], bar_rect, 1)
        target_text = "Patrol Target: n/a"
        patrol_entries = self._mmo_patrol_entries()
        if patrol_entries:
            entry = patrol_entries[self.mmo_patrol_index % len(patrol_entries)]
            target = entry.get("target")
            if isinstance(target, (list, tuple)) and len(target) == 2:
                target_text = f"Patrol Target: {target[0]:.2f},{target[1]:.2f}"
        target_line = self.small_font.render(target_text, True, palette["text_dim"])
        legend_panel.blit(target_line, (16, 150))
        self.screen.blit(legend_panel, legend_rect.topleft)
        if nearest:
            quest = nearest.get("quest", {})
            if isinstance(quest, dict):
                summary = quest.get("summary") or quest.get("name")
                if summary:
                    label = self.small_font.render(
                        f"Quest: {summary}", True, palette["accent_warm"]
                    )
                    self.screen.blit(label, (24, 352))
        footer_text = "MMO Hub Online"
        if self.mmo_plan_summary:
            footer_text = self.mmo_plan_summary
        if self.mmo_message:
            footer_text = self.mmo_message
        draw_mmo_footer(self, footer_text)
        if self.mmo_ui_show_panel:
            self._mmo_draw_overview_panel(self._mmo_regions())
        if self.mmo_overlay_mode == "details" or self.mmo_show_details:
            region = self._mmo_selected_region()
            if region:
                self._mmo_draw_details(region)
        if self.mmo_overlay_mode == "favorites" or self.mmo_show_favorites:
            self._mmo_draw_favorites()
        if self.mmo_overlay_mode == "quests" or self.mmo_show_quest_log:
            self._mmo_draw_quest_log()
        if self.mmo_overlay_mode == "growth" or self.mmo_show_growth:
            self._mmo_draw_growth_report()
        if self.mmo_overlay_mode == "party" or self.mmo_show_party:
            self._mmo_draw_party()
        if self.mmo_overlay_mode == "network" or self.mmo_show_network:
            self._mmo_draw_network_status()
        if self.mmo_overlay_mode == "help" or self.mmo_show_help:
            self._mmo_draw_help()
        if self.mmo_overlay_mode == "notifications" or self.mmo_show_notifications:
            self._mmo_draw_notifications()
        if self.mmo_overlay_mode == "market" or self.mmo_show_market:
            self._mmo_draw_market()
        if self.mmo_overlay_mode == "factions" or self.mmo_show_factions:
            self._mmo_draw_factions()
        if self.mmo_overlay_mode == "operations" or self.mmo_show_operations:
            self._mmo_draw_operations()
        if self.mmo_overlay_mode == "hub_settings" or self.mmo_show_hub_settings:
            self._mmo_draw_hub_settings()
        if self.mmo_overlay_mode == "guilds" or self.mmo_show_guilds:
            self._mmo_draw_guilds()
        if self.mmo_overlay_mode == "events" or self.mmo_show_events:
            self._mmo_draw_events()
        if self.mmo_overlay_mode == "contracts" or self.mmo_show_contracts:     
            self._mmo_draw_contracts()
        if self.mmo_overlay_mode == "intel" or self.mmo_show_intel:
            self._mmo_draw_intel()
        if self.mmo_overlay_mode == "infrastructure" or self.mmo_show_infrastructure:
            self._mmo_draw_infrastructure()
        if self.mmo_overlay_mode == "patrols" or self.mmo_show_patrols:
            self._mmo_draw_patrols()
        if self.mmo_overlay_mode == "timeline" or self.mmo_show_timeline:
            self._mmo_draw_timeline()
        if self.mmo_overlay_mode == "logistics" or self.mmo_show_logistics:
            self._mmo_draw_logistics()
        if self.mmo_overlay_mode == "survey" or self.mmo_show_survey:
            self._mmo_draw_survey()
        if self.mmo_overlay_mode == "diplomacy" or self.mmo_show_diplomacy:
            self._mmo_draw_diplomacy()
        if self.mmo_overlay_mode == "research" or self.mmo_show_research:
            self._mmo_draw_research()
        if self.mmo_overlay_mode == "crafting" or self.mmo_show_crafting:
            self._mmo_draw_crafting()
        if self.mmo_overlay_mode == "market_orders" or self.mmo_show_market_orders:
            self._mmo_draw_market_orders()
        if self.mmo_overlay_mode == "strategy" or self.mmo_show_strategy:
            self._mmo_draw_strategy()
        if self.mmo_overlay_mode == "campaign" or self.mmo_show_campaign:
            self._mmo_draw_campaign()
        if self.mmo_overlay_mode == "expeditions" or self.mmo_show_expeditions:
            self._mmo_draw_expeditions()
        if self.mmo_overlay_mode == "roster" or self.mmo_show_roster:
            self._mmo_draw_roster()
        if self.mmo_overlay_mode == "alerts" or self.mmo_show_alerts:
            self._mmo_draw_alerts()
        if self.mmo_overlay_mode == "command" or self.mmo_show_command:
            self._mmo_draw_command()
        if self.mmo_overlay_mode == "bounties" or self.mmo_show_bounties:
            self._mmo_draw_bounties()
        if self.mmo_overlay_mode == "influence" or self.mmo_show_influence:
            self._mmo_draw_influence()
        if self.mmo_overlay_mode == "fleet" or self.mmo_show_fleet:
            self._mmo_draw_fleet()
        if self.mmo_overlay_mode == "projects" or self.mmo_show_projects:
            self._mmo_draw_projects()
        if self.mmo_overlay_mode == "academy" or self.mmo_show_academy:
            self._mmo_draw_academy()
        if self.mmo_overlay_mode == "account" or self.mmo_show_account:
            self._mmo_draw_account()
        if self.mmo_overlay_mode == "account_audit" or self.mmo_show_account_audit:
            self._mmo_draw_account_audit()
        if self.mmo_show_minimap:
            self._mmo_draw_minimap(self._mmo_regions())
        self._mmo_draw_overlay_footer()
        self._mmo_draw_match_overlay()
        self._mmo_draw_flash_messages()
        self._mmo_draw_event_log()
        self._mmo_draw_floating_messages()
        self._mmo_draw_tab_bar()
        self._mmo_draw_tour()

    def _autoplay_menu_flow(self, now: int) -> None:
        """Automatically step through menus before starting a match."""
        if not self.autoplay_flow or self.state == "playing":
            return
        if self.autoplay_menu_state != self.state:
            self.autoplay_menu_state = self.state
            self.autoplay_menu_stage = 0
            self.autoplay_preview_index = 0
            self.autoplay_preview_count = 0
            self.autoplay_preview_wait_start = now
            self.autoplay_preview_pause_logged = False
            self.autoplay_last_menu_step = now
            return
        if now - self.autoplay_last_menu_step < self.autoplay_menu_delay:       
            return
        self.autoplay_last_menu_step = now
        if (
            self.autoplay_menu_budget > 0
            and now - self.autoplay_flow_start >= self.autoplay_menu_budget
        ):
            options = self._menu_options_for_state("main_menu") or []
            if self.state != "main_menu":
                self._set_state("main_menu")
                return
            if "Quick Start" in options:
                self.menu_index = options.index("Quick Start")
                self.menu_manager.index = self.menu_index
                self._autoplay_trace("Menu budget hit -> Quick Start", now=now)
                self._handle_menu_selection(options)
                return
            if "New Game" in options:
                self.menu_index = options.index("New Game")
                self.menu_manager.index = self.menu_index
                self._autoplay_trace("Menu budget hit -> New Game", now=now)
                self._handle_menu_selection(options)
                return
        if self.state == "splash":
            self._set_state("main_menu")
            return
        if self.state in {"rebind", "rebind_controller"}:
            self._autoplay_complete_rebind()
            return
        if (
            self.state == "mmo"
            and self.autoplay_menu_resume_state == "main_menu"
            and now >= self.autoplay_menu_resume_time
        ):
            self.autoplay_menu_resume_state = None
            self._set_state("main_menu")
            return
        if self.state in {"victory", "game_over"} and not self.show_end_options:
            self.show_end_options = True
        if self.state == "main_menu" and self.autoplay_pending_results:
            seen = self.autoplay_menu_seen.get("main_menu", set())
            options = self._menu_options_for_state("main_menu") or []
            required = [opt for opt in options if opt != "Exit"]
            if all(opt in seen for opt in required) and self._autoplay_vote_complete():
                next_state = self.autoplay_pending_results.pop(0)
                self.show_end_options = True
                self._set_state(next_state)
                return
        options = self._menu_options_for_state()
        if not options:
            return
        seen = self.autoplay_menu_seen.setdefault(self.state, set())
        if self.state == "settings_system" and not self.autoplay_allow_system_actions:
            seen.update({"Reset Records", "Wipe Saves"})
        preview_items = self._autoplay_preview_items()
        if preview_items and self.autoplay_menu_stage == 0:
            if now - self.autoplay_preview_wait_start < self.autoplay_preview_delay:
                if not self.autoplay_preview_pause_logged:
                    self.autoplay_preview_pause_logged = True
                    self._autoplay_trace(
                        f"Preview pause {self.state}", now=now
                    )
                return
            if self.autoplay_preview_count >= len(preview_items):
                self.autoplay_menu_stage = 1
            else:
                idx = self.autoplay_preview_index % len(preview_items)
                self.menu_index = idx
                self.menu_manager.index = idx
                self.autoplay_preview_index += 1
                self.autoplay_preview_count += 1
                self._autoplay_trace(
                    f"Preview {self.state}: {preview_items[idx]}", now=now
                )
                return
        ordered = self._autoplay_menu_choice_order(options)
        choice = None
        page_options = self._page_option_labels()
        char_filter_label = self._character_filter_label()
        map_filter_label = self._map_filter_label()
        for opt in ordered:
            if (
                self.state == "settings_system"
                and not self.autoplay_allow_system_actions
                and opt in {"Reset Records", "Wipe Saves"}
            ):
                continue
            if self.state == "char" and opt == "Continue":
                if not self._autoplay_collection_complete(
                    "char",
                    exclude={
                        "Add AI Player",
                        "Difficulty",
                        "Continue",
                        "Back",
                        char_filter_label,
                        *page_options,
                    },
                    required=list(self.characters),
                ):
                    continue
            if self.state == "char" and opt == "Back":
                if not self._autoplay_collection_complete(
                    "char",
                    exclude={
                        "Add AI Player",
                        "Difficulty",
                        "Continue",
                        "Back",
                        char_filter_label,
                        *page_options,
                    },
                    required=list(self.characters),
                ):
                    continue
            if self.state == "char" and opt in page_options:
                if self._autoplay_collection_complete(
                    "char",
                    exclude={
                        "Add AI Player",
                        "Difficulty",
                        "Continue",
                        "Back",
                        char_filter_label,
                        *page_options,
                    },
                    required=list(self.characters),
                ):
                    continue
            if self.state == "map" and opt == "Back":
                if not self._autoplay_collection_complete(
                    "map",
                    exclude={"Back", map_filter_label, *page_options},
                    required=list(self.map_manager.maps.keys()),
                ):
                    continue
            if self.state == "map" and opt in page_options:
                if self._autoplay_collection_complete(
                    "map",
                    exclude={"Back", map_filter_label, *page_options},
                    required=list(self.map_manager.maps.keys()),
                ):
                    continue
            if self.state == "chapter" and opt == "Back":
                if not self._autoplay_collection_complete(
                    "chapter",
                    exclude={"Back"},
                    required=list(self.chapters),
                ):
                    continue
            if self.state == "main_menu" and opt == "Vote":
                if not self._autoplay_vote_complete():
                    choice = opt
                    break
            if self.state == "main_menu" and opt == "Exit":
                if self.autoplay_pending_results:
                    continue
            if self.state == "vote_category" and opt in {"Character", "Biome"}:
                if not self._autoplay_vote_category_complete(opt):
                    choice = opt
                    break
            if self.state == "vote_category" and opt == "Back":
                if not self._autoplay_vote_complete():
                    continue
            if opt not in seen:
                choice = opt
                break
        if choice is None:
            return
        current_state = self.state
        self.menu_index = options.index(choice)
        self.menu_manager.index = self.menu_index
        if choice not in page_options:
            seen.add(choice)
        self._autoplay_trace(f"Menu {current_state}: {choice}", now=now)
        if self.state == "vote" and self.autoplay_vote_category:
            category_seen = self.autoplay_vote_seen.setdefault(
                self.autoplay_vote_category, set()
            )
            category_seen.add(choice)
        self._handle_menu_selection(options)
        if current_state == "main_menu" and choice == "MMO":
            self.autoplay_menu_resume_state = None
            self.autoplay_menu_resume_time = 0
            self.autoplay_mmo_state = None
        if current_state == "map" and choice != "Back":
            self.autoplay_menu_resume_state = "map"
            self.autoplay_menu_resume_time = now + self.autoplay_menu_delay     
        if current_state == "chapter" and choice != "Back":
            self.autoplay_menu_resume_state = "chapter"
            self.autoplay_menu_resume_time = now + self.autoplay_menu_delay

    def apply_vote_balancing(self, character_name: str, character) -> None:
        """Adjust stats for ``character`` based on recent community votes."""

        if not character_name:
            return
        counts = self.voting_manager.get_vote_counts(self.characters)
        if not counts:
            self.vote_adjustments[character_name] = 0
            return
        max_votes = max(counts.values())
        min_votes = min(counts.values())
        if max_votes == 0 or max_votes == min_votes:
            self.vote_adjustments[character_name] = 0
            return
        char_votes = counts.get(character_name, 0)
        popularity = char_votes / max_votes
        modifier = round((0.5 - popularity) * 4)
        self.vote_adjustments[character_name] = modifier
        if modifier == 0:
            return
        for stat in ("attack", "defense"):
            character.stats.apply_modifier(stat, modifier)
        health_delta = modifier * 5
        if health_delta:
            character.stats.apply_modifier("max_health", health_delta)
        character.max_health = character.stats.get("max_health")
        character.health_manager.max_health = character.max_health
        if modifier > 0:
            character.health_manager.health = character.max_health
        else:
            character.health_manager.health = min(
                character.health_manager.health,
                character.max_health,
            )
        character.health = character.health_manager.health

    def _quick_start(self) -> None:
        """Start a default single-player story match immediately."""
        self.selected_mode = "Story"
        self.multiplayer = False
        self.online_multiplayer = False
        self.human_players = 1
        self.ai_players = 0
        if self.characters:
            self.selected_character = self.characters[0]
        self.selected_chapter = self.chapters[0]
        self._setup_level()
        self._set_state("playing")
        self.level_start_time = pygame.time.get_ticks()

    def _goals_menu_options(self) -> list[str]:
        """Build the Goals menu entries to align input navigation."""
        goals: list[str] = []
        try:
            base_dir = os.path.dirname(__file__)
            path = os.path.join(base_dir, "..", "docs", "GOALS.md")
            with open(path, "r", encoding="utf-8") as fh:
                for line in fh:
                    if line.startswith("- "):
                        goals.append(line[2:].strip())
                    if len(goals) == 5:
                        break
        except OSError:
            pass
        goals.append("Back")
        return goals

    def _info_menu_options(self, state: str) -> list[str]:
        """Return menu options for informational screens."""
        if state == "howto":
            return [
                "Move: Arrow keys or WASD",
                "Jump: Space",
                "Shoot: Z",
                "Melee: X",
                "Block: Shift | Parry: C",
                "Special: V",
                "Back",
            ]
        if state == "credits":
            return [
                "Prototype by Hololive Fans",
                "Powered by Pygame",
                "Back",
            ]
        if state == "scoreboard":
            lines = [
                f"Best Time: {self.best_time}s",
                f"High Score: {self.best_score}",
            ]
            if getattr(self, "reputation_manager", None):
                top = self.reputation_manager.top(3)
                if top:
                    faction_summary = ", ".join(
                        f"{name} ({value})" for name, value in top
                    )
                    lines.append(f"Top Factions: {faction_summary}")
                else:
                    lines.append("Top Factions: None yet")
            lines.append("Back")
            return lines
        if state == "achievements":
            if self.achievement_manager.unlocked:
                lines = sorted(self.achievement_manager.unlocked)
            else:
                lines = ["No achievements yet"]
            lines.append("Back")
            return lines
        if state == "goals":
            return self._goals_menu_options()
        return ["Back"]

    def _page_option_labels(self) -> set[str]:
        return {"Next Page", "Prev Page"}

    def _page_count(self, total: int, page_size: int) -> int:
        if page_size <= 0:
            return 1
        return max(1, (total + page_size - 1) // page_size)

    def _character_filter_label(self) -> str:
        return f"Filter: {self.character_filter}"

    def _map_filter_label(self) -> str:
        return f"Filter: {self.map_filter}"

    def _character_preview_data(self, name: str) -> dict[str, object]:
        cached = self.character_preview_cache.get(name)
        if cached:
            return cached
        cls = get_player_class(name)
        instance = cls(0, 0, None)
        attack = int(instance.stats.get("attack"))
        defense = int(instance.stats.get("defense"))
        health = int(instance.stats.get("max_health"))
        mana = int(getattr(instance, "max_mana", 100))
        speed = float(getattr(instance, "speed_factor", 1.0))
        role = self._character_role_from_stats(attack, defense, mana, speed)
        summary = {
            "attack": attack,
            "defense": defense,
            "health": health,
            "mana": mana,
            "speed": round(speed, 2),
            "role": role,
        }
        self.character_preview_cache[name] = summary
        return summary

    def _character_role_from_stats(
        self, attack: int, defense: int, mana: int, speed: float
    ) -> str:
        if attack >= 12:
            return "Striker"
        if defense >= 7:
            return "Guardian"
        if mana >= 120:
            return "Caster"
        if speed >= 1.2:
            return "Skirmisher"
        return "Skirmisher"

    def _filtered_characters(self) -> list[str]:
        if self.character_filter == "All":
            return list(self.characters)
        filtered = []
        for name in self.characters:
            preview = self._character_preview_data(name)
            if preview.get("role") == self.character_filter:
                filtered.append(name)
        return filtered

    def _cycle_character_filter(self) -> None:
        idx = self.character_filters.index(self.character_filter)
        self.character_filter = self.character_filters[
            (idx + 1) % len(self.character_filters)
        ]
        self.character_page = 0
        self.menu_index = 0
        self.menu_manager.index = 0

    def _map_preview_data(self, name: str) -> dict[str, object]:
        cached = self.map_preview_cache.get(name)
        if cached:
            return cached
        data = self.map_manager.maps.get(name, {}) or {}
        hazards = data.get("hazards", []) or []
        hazard_types = sorted(
            {
                str(entry.get("type", "")).title()
                for entry in hazards
                if entry.get("type")
            }
        )
        platforms = data.get("platforms", []) or []
        moving = data.get("moving_platforms", []) or []
        crumbling = data.get("crumbling_platforms", []) or []
        gravity = data.get("gravity_zones", []) or []
        summary = {
            "hazards": len(hazards),
            "hazard_types": hazard_types,
            "platforms": len(platforms),
            "moving": len(moving),
            "crumbling": len(crumbling),
            "gravity": len(gravity),
            "minions": int(data.get("minions", 0) or 0),
            "boss": data.get("boss"),
        }
        summary["threat"] = (
            summary["hazards"] * 2
            + summary["minions"]
            + (2 if summary.get("boss") else 0)
            + summary["moving"]
        )
        self.map_preview_cache[name] = summary
        return summary

    def _chapter_preview_data(self, name: str) -> dict[str, object]:
        cached = self.chapter_preview_cache.get(name)
        if cached:
            return cached
        summary = self._map_preview_data(name)
        self.chapter_preview_cache[name] = summary
        return summary

    def _map_matches_filter(self, name: str, data: dict[str, object]) -> bool:
        if self.map_filter == "All":
            return True
        is_story = name.startswith("Chapter")
        if self.map_filter == "Story":
            return is_story
        if self.map_filter == "Arena":
            return not is_story
        hazards = len(data.get("hazards", []) or [])
        if self.map_filter == "Low Hazards":
            return hazards <= 1
        if self.map_filter == "High Hazards":
            return hazards >= 3
        if self.map_filter == "Boss":
            return bool(data.get("boss"))
        return True

    def _filtered_maps(self) -> list[str]:
        if self.map_filter == "All":
            return list(self.maps)
        filtered = []
        for name in self.maps:
            data = self.map_manager.maps.get(name, {}) or {}
            if self._map_matches_filter(name, data):
                filtered.append(name)
        return filtered

    def _cycle_map_filter(self) -> None:
        idx = self.map_filters.index(self.map_filter)
        self.map_filter = self.map_filters[(idx + 1) % len(self.map_filters)]
        self.map_page = 0
        self.menu_index = 0
        self.menu_manager.index = 0

    def _paged_characters(self) -> list[str]:
        characters = self._filtered_characters()
        total = self._page_count(len(characters), self.character_page_size)
        self.character_page = max(0, min(self.character_page, total - 1))       
        start = self.character_page * self.character_page_size
        end = start + self.character_page_size
        return characters[start:end]

    def _paged_maps(self) -> list[str]:
        maps = self._filtered_maps()
        total = self._page_count(len(maps), self.map_page_size)
        self.map_page = max(0, min(self.map_page, total - 1))
        start = self.map_page * self.map_page_size
        end = start + self.map_page_size
        return maps[start:end]

    def _character_menu_options(self) -> list[str]:
        options = list(self._paged_characters())
        total = self._page_count(
            len(self._filtered_characters()),
            self.character_page_size,
        )
        if total > 1 and self.character_page > 0:
            options.append("Prev Page")
        if total > 1 and self.character_page < total - 1:
            options.append("Next Page")
        options.append(self._character_filter_label())
        options.extend(["Add AI Player", "Difficulty", "Continue", "Back"])     
        return options

    def _map_menu_options(self) -> list[str]:
        options = list(self._paged_maps())
        total = self._page_count(len(self._filtered_maps()), self.map_page_size)
        if total > 1 and self.map_page > 0:
            options.append("Prev Page")
        if total > 1 and self.map_page < total - 1:
            options.append("Next Page")
        options.append("Random")
        options.append(self._map_filter_label())
        options.append("Back")
        return options

    def _victory_menu_options(self) -> list[str]:
        options = ["Auto-Dev Report", "MMO Briefing", "MMO Launchpad"]
        if self.mmo_unlocked or self.mmo_pending:
            options.append("MMO Hub")
        options.extend(["Play Again", "Main Menu"])
        return options

    def _victory_actions_options(self) -> list[str]:
        options = [
            "Generate Auto-Dev Plan",
            "Issue Arena Grant",
            "Sync Nearby Region",
            "Seed Frontier Region",
            "Stage Campaign",
            "Enter MMO Hub",
        ]
        options.append("Back")
        return options

    def _menu_options_for_state(self, state: str | None = None) -> list[str] | None:
        """Map the current menu state to its navigable options."""
        current = state or self.state
        if current == "inventory" and getattr(self, "player", None):
            return list(self.player.inventory.items.keys()) + ["Back"]
        if current == "equipment" and getattr(self, "player", None):
            return self.player.equipment.order + ["Back"]
        if current in {"howto", "credits", "scoreboard", "achievements", "goals"}:
            return self._info_menu_options(current)
        options = {
            "main_menu": self.main_menu_options,
            "mode": self.mode_options,
            "solo_multi": self.solo_multi_options,
            "mp_type": self.mp_type_options,
            "match_options": self.match_options,
            "settings": self.settings_options,
            "settings_controls": self.settings_controls_options,
            "settings_display": self.settings_display_options,
            "settings_audio": self.settings_audio_options,
            "settings_system": self.settings_system_options,
            "accessibility": self.accessibility_options,
            "node_settings": self.node_options,
            "accounts": self.account_options,
            "key_bindings": self.key_options,
            "controller_bindings": self.controller_options,
            "char": self._character_menu_options(),
            "map": self._map_menu_options(),
            "chapter": self.chapter_menu_options,
            "vote_category": self.vote_categories,
            "vote": self.vote_options,
            "lobby": self.lobby_options,
            "paused": self.pause_options,
            "victory": self._victory_menu_options(),
            "victory_report": ["Back"],
            "victory_briefing": ["Back"],
            "victory_actions": self._victory_actions_options(),
            "game_over": self.game_over_options,
        }
        return options.get(current)

    def _handle_menu_selection(self, options: list[str]) -> None:
        """Handle a menu selection without relying on a key event."""
        if not options:
            return
        choice = options[self.menu_index]
        if self.autoplay:
            self._autoplay_record_feature(f"menu:{self.state}:{choice}")
        if self.state == "key_bindings":
            if choice == "Back":
                self._set_state("settings_controls")
                self.menu_index = 0
            else:
                self.rebind_action = choice
                self._set_state("rebind")
            return
        if self.state == "controller_bindings":
            if choice == "Back":
                self._set_state("settings_controls")
                self.menu_index = 0
            else:
                self.rebind_action = choice
                self._set_state("rebind_controller")
            return
        if self.state == "main_menu":
            if choice == "Quick Start":
                self._quick_start()
            elif choice == "New Game":
                self._set_state("mode")
                self.menu_index = 0
            elif choice == "Character Select":
                self.multiplayer = False
                self.selected_mode = "Arena"
                self.character_page = 0
                self._set_state("char")
                self.menu_index = 0
            elif choice == "Map Select":
                self.multiplayer = False
                self.selected_mode = "Arena"
                self.map_page = 0
                self._set_state("map")
                self.menu_index = 0
            elif choice == "Match Options":
                self._set_state("match_options")
                self.menu_index = 0
            elif choice == "MMO":
                self._enter_mmo_mode()
            elif choice == "Settings":
                self._set_state("settings")
                self.menu_index = 0
            elif choice == "Accounts":
                self.return_state = "main_menu"
                self._set_state("accounts")
                self.menu_index = 0
            elif choice == "How to Play":
                self.return_state = "main_menu"
                self._set_state("howto")
                self.menu_index = 0
            elif choice == "Credits":
                self.return_state = "main_menu"
                self._set_state("credits")
                self.menu_index = 0
            elif choice == "Achievements":
                self.return_state = "main_menu"
                self._set_state("achievements")
                self.menu_index = 0
            elif choice == "Records":
                self.return_state = "main_menu"
                self._set_state("scoreboard")
                self.menu_index = 0
            elif choice == "Goals":
                self.return_state = "main_menu"
                self._set_state("goals")
                self.menu_index = 0
            elif choice == "Vote":
                self.open_vote_menu()
            elif choice == "Exit":
                self.running = False
            return
        if self.state == "mode":
            if choice == "Back":
                self._set_state("main_menu")
                self.menu_index = 0
            else:
                self.selected_mode = choice
                self.human_players = 1
                self.ai_players = 0
                self._set_state("solo_multi")
                self.menu_index = 0
            return
        if self.state == "solo_multi":
            if choice == "Back":
                self._set_state("mode")
                self.menu_index = 0
            else:
                self.multiplayer = choice == "Multiplayer"
                if choice == "Solo":
                    self.character_page = 0
                    self._set_state("char")
                else:
                    self._set_state("mp_type")
                self.menu_index = 0
            return
        if self.state == "mp_type":
            if choice == "Back":
                self._set_state("solo_multi")
                self.menu_index = 0
            else:
                self.online_multiplayer = choice == "Online"
                self.character_page = 0
                self._set_state("char")
                self.menu_index = 0
            return
        if self.state == "match_options":
            if choice == "Back":
                self._set_state("main_menu")
                self.menu_index = 0
            elif choice == "Lives":
                options = [1, 2, 3, 5, 7, 9]
                current = self.match_lives if not self.autoplay else self.autoplay_lives
                idx = (options.index(current) + 1) % len(options) if current in options else 0
                self.match_lives = options[idx]
            elif choice == "Allies":
                max_allies = 3
                value = self.match_allies + 1
                if value > max_allies:
                    value = 0
                self.match_allies = value
            elif choice == "AI Players":
                max_ai = 3
                value = self.ai_players + 1
                if value > max_ai:
                    value = 0
                self.ai_players = value
            elif choice == "Mob Waves":
                self.match_mobs = not self.match_mobs
            elif choice == "Mob Interval":
                options = [2200, 3000, 3800, 4500, 5200]
                idx = options.index(self.match_mob_interval) + 1 if self.match_mob_interval in options else 0
                self.match_mob_interval = options[idx % len(options)]
            elif choice == "Mob Wave":
                options = [1, 2, 3, 4]
                idx = options.index(self.match_mob_wave) + 1 if self.match_mob_wave in options else 0
                self.match_mob_wave = options[idx % len(options)]
            elif choice == "Mob Cap":
                options = [4, 6, 8, 10, 12, 14, 16]
                idx = options.index(self.match_mob_max) + 1 if self.match_mob_max in options else 0
                self.match_mob_max = options[idx % len(options)]
            return
        if self.state == "char":
            if choice == self._character_filter_label():
                self._cycle_character_filter()
            elif choice == "Prev Page":
                self.character_page = max(0, self.character_page - 1)
                self.menu_index = 0
                self.menu_manager.index = 0
            elif choice == "Next Page":
                self.character_page += 1
                self.menu_index = 0
                self.menu_manager.index = 0
            elif choice == "Add AI Player":
                if self.ai_players < 4 - self.human_players:
                    self.ai_players += 1
            elif choice == "Difficulty":
                self.difficulty_index = (
                    self.difficulty_index + 1
                ) % len(self.difficulty_levels)
            elif choice == "Continue":
                if self.selected_character is None and self.characters:
                    self.selected_character = self.characters[0]
                if self.multiplayer:
                    self.player_names = [
                        f"Player {i+1}" for i in range(self.human_players)
                    ]
                    self.player_names += [
                        f"AI {i+1}" for i in range(self.ai_players)
                    ]
                    self._set_state("lobby")
                elif self.selected_mode == "Story":
                    self._set_state("chapter")
                else:
                    self._set_state("map")
                self.menu_index = 0
            elif choice == "Back":
                self.state = "mp_type" if self.multiplayer else "solo_multi"
                self.menu_index = 0
            else:
                if self.multiplayer and self.human_players > 1:
                    self._sync_player_selection_lists()
                    idx = self.character_select_index
                    self.character_selections[idx] = choice
                    self.character_select_index = (
                        (idx + 1) % len(self.character_selections)
                    )
                    self.selected_character = self.character_selections[0]
                else:
                    self.selected_character = choice
            return
        if self.state == "lobby":
            if choice == "Back":
                self._set_state("char")
                self.menu_index = 0
            elif choice == "Start Game":
                if self.selected_mode == "Story":
                    self._set_state("chapter")
                else:
                    self._set_state("map")
                self.menu_index = 0
            return
        if self.state == "map":
            if choice == self._map_filter_label():
                self._cycle_map_filter()
            elif choice == "Prev Page":
                self.map_page = max(0, self.map_page - 1)
                self.menu_index = 0
                self.menu_manager.index = 0
            elif choice == "Next Page":
                self.map_page += 1
                self.menu_index = 0
                self.menu_manager.index = 0
            elif choice == "Random":
                pool = self._filtered_maps()
                if not pool:
                    pool = list(self.map_manager.maps.keys())
                if self.multiplayer and self.human_players > 1:
                    self._sync_player_selection_lists()
                    idx = self.map_select_index
                    if pool:
                        chosen = random.choice(pool)
                        self.map_selections[idx] = chosen
                        self.map_select_message = (
                            f"P{idx + 1} rolled {chosen}"
                        )
                    self.map_select_index = (
                        (idx + 1) % len(self.map_selections)
                    )
                    if all(self.map_selections):
                        self.selected_map = random.choice(
                            [m for m in self.map_selections if m]
                        )
                        self._setup_level()
                        self._set_state("playing")
                        self.level_start_time = pygame.time.get_ticks()
                else:
                    if pool:
                        self.selected_map = random.choice(pool)
                        self._setup_level()
                        self._set_state("playing")
                        self.level_start_time = pygame.time.get_ticks()
            elif choice == "Back":
                if self.multiplayer:
                    self._set_state("lobby")
                else:
                    self._set_state("char")
                self.menu_index = 0
            else:
                if self.multiplayer and self.human_players > 1:
                    self._sync_player_selection_lists()
                    idx = self.map_select_index
                    self.map_selections[idx] = choice
                    self.map_select_message = f"P{idx + 1} chose {choice}"
                    self.map_select_index = (
                        (idx + 1) % len(self.map_selections)
                    )
                    if all(self.map_selections):
                        self.selected_map = random.choice(
                            [m for m in self.map_selections if m]
                        )
                        self._setup_level()
                        self._set_state("playing")
                        self.level_start_time = pygame.time.get_ticks()
                else:
                    self.selected_map = choice
                    self._setup_level()
                    self._set_state("playing")
                    self.level_start_time = pygame.time.get_ticks()
            return
        if self.state == "chapter":
            if choice == "Back":
                if self.multiplayer:
                    self._set_state("lobby")
                else:
                    self._set_state("char")
                self.menu_index = 0
            else:
                self.selected_chapter = choice
                self._setup_level()
                self._set_state("playing")
                self.level_start_time = pygame.time.get_ticks()
            return
        if self.state == "vote_category":
            if choice == "Back":
                self._set_state("main_menu")
                self.menu_index = 0
            else:
                self.active_vote_manager = (
                    self.voting_manager
                    if choice == "Character"
                    else self.biome_voting_manager
                )
                self.vote_options = (
                    self.active_vote_manager.get_options() + ["Back"]
                )
                self.autoplay_vote_category = choice
                self._set_state("vote")
                self.menu_index = 0
            return
        if self.state == "vote":
            if choice == "Back":
                self._set_state("vote_category")
                self.menu_index = 0
            else:
                try:
                    if self.active_vote_manager:
                        self.active_vote_manager.cast_vote(
                            self.account_id, choice
                        )
                except ValueError:
                    pass
                self._set_state("main_menu")
                self.menu_index = 0
            return
        if self.state == "settings":
            if choice == "Back":
                self._set_state("main_menu")
                self.menu_index = 0
            elif choice == "Controls":
                self._set_state("settings_controls")
                self.menu_index = 0
            elif choice == "Display":
                self._set_state("settings_display")
                self.menu_index = 0
            elif choice == "Audio":
                self._set_state("settings_audio")
                self.menu_index = 0
            elif choice == "System":
                self._set_state("settings_system")
                self.menu_index = 0
            return
        if self.state == "settings_controls":
            if choice == "Back":
                self._set_state("settings")
                self.menu_index = 0
            elif choice == "Key Bindings":
                self._set_state("key_bindings")
                self.menu_index = 0
            elif choice == "Controller Bindings":
                self._set_state("controller_bindings")
                self.menu_index = 0
            elif choice == "Input Method":
                methods = ["auto", "keyboard", "controller"]
                idx = methods.index(self.input_method)
                self.input_method = methods[(idx + 1) % len(methods)]
                self.input_manager.set_mode(self.input_method)
            return
        if self.state == "settings_display":
            if choice == "Back":
                self._set_state("settings")
                self.menu_index = 0
            elif choice == "Window Size":
                self._cycle_window_size()
            elif choice == "Display Mode":
                self._cycle_display_mode()
            elif choice == "HUD Size":
                self._cycle_hud_size()
            elif choice == "Show FPS":
                self.show_fps = not self.show_fps
            return
        if self.state == "settings_audio":
            if choice == "Back":
                self._set_state("settings")
                self.menu_index = 0
            elif choice == "Volume":
                self._cycle_volume()
            elif choice == "SFX Profile":
                self._cycle_sfx_profile()
            elif choice == "SFX Debug":
                self.debug_sfx = not self.debug_sfx
            return
        if self.state == "settings_system":
            if choice == "Back":
                self._set_state("settings")
                self.menu_index = 0
            elif choice == "Reset Records":
                self.best_time = 0
                self.best_score = 0
            elif choice == "Wipe Saves":
                wipe_saves()
            elif choice == "Accessibility":
                self._set_state("accessibility")
                self.menu_index = 0
            elif choice == "Node Settings":
                self._set_state("node_settings")
                self.menu_index = 0
            elif choice == "Accounts":
                self.return_state = "settings_system"
                self._set_state("accounts")
                self.menu_index = 0
            return
        if self.state == "node_settings":
            if choice == "Back":
                self._set_state("settings_system")
                self.menu_index = 0
            elif choice == "Start Node":
                self.start_node()
            elif choice == "Stop Node":
                self.stop_node()
            elif choice == "Latency Helper":
                self.latency_helper = not self.latency_helper
                if self.network_manager is not None:
                    self.network_manager.relay_mode = self.latency_helper
                    if self.latency_helper:
                        self.network_manager.offer_relay(load_nodes())
            elif choice == "Background Mining":
                self.mining_enabled = not self.mining_enabled
                if self.mining_enabled:
                    self.mining_manager.start()
                else:
                    self.mining_manager.stop()
            return
        if self.state == "accessibility":
            if choice == "Back":
                self._set_state("settings_system")
                self.menu_index = 0
            elif choice == "Font Scale":
                current = float(
                    self.accessibility_manager.options.get("font_scale", 1.0)
                )
                if current not in self.font_scale_options:
                    current = 1.0
                idx = self.font_scale_options.index(current)
                next_scale = self.font_scale_options[
                    (idx + 1) % len(self.font_scale_options)
                ]
                self.accessibility_manager.options["font_scale"] = next_scale
                self._apply_font_scale()
            elif choice == "High Contrast":
                self.accessibility_manager.toggle("high_contrast")
            elif choice == "Input Prompts":
                self.accessibility_manager.toggle("input_prompts")
            elif choice == "Colorblind Mode":
                self.accessibility_manager.toggle("colorblind")
            return
        if self.state == "accounts":
            if choice == "Back":
                self._set_state(self.return_state or "settings_system")
                self.menu_index = 0
            elif choice == "Register Account":
                self.execute_account_option("Register Account")
            elif choice == "Delete Account":
                self.execute_account_option("Delete Account")
            elif choice == "Renew Key":
                self.execute_account_option("Renew Key")
            return
        if self.state in {"howto", "credits", "scoreboard", "achievements", "goals"}:
            if choice == "Back":
                self._set_state(self.return_state)
                self.menu_index = 0
            return
        if self.state == "paused":
            if choice == "Resume":
                self._set_state("playing")
            elif choice == "Inventory":
                self._set_state("inventory")
                self.menu_index = 0
            elif choice == "Equipment":
                self._set_state("equipment")
                self.menu_index = 0
            elif choice == "Achievements":
                self.return_state = "paused"
                self._set_state("achievements")
                self.menu_index = 0
            elif choice == "Main Menu":
                self._set_state("main_menu")
                self.menu_index = 0
            return
        if self.state == "inventory":
            if choice == "Back":
                self._set_state("paused")
                self.menu_index = 0
            else:
                item = self.item_manager.get(choice)
                if item and self.player.inventory.remove(choice):
                    self.player.equipment.equip(item.slot, choice)
                    if self.menu_index >= len(self.player.inventory.items):
                        self.menu_index = max(
                            0, len(self.player.inventory.items) - 1
                        )
                        self.menu_manager.index = self.menu_index
            return
        if self.state == "equipment":
            if choice == "Back":
                self._set_state("paused")
                self.menu_index = 0
            else:
                item = self.player.equipment.get(choice)
                if item:
                    self.player.equipment.unequip(choice)
                    self.player.inventory.add(item)
            return
        if self.state == "game_over":
            if choice == "Play Again":
                self._set_state("char")
                self.menu_index = 0
            elif choice == "Main Menu":
                self._set_state("main_menu")
                self.menu_index = 0
            return
        if self.state == "victory":
            if choice == "Auto-Dev Report":
                self._set_state("victory_report")
                self.menu_index = 0
            elif choice == "MMO Briefing":
                self._set_state("victory_briefing")
                self.menu_index = 0
            elif choice == "MMO Launchpad":
                self._set_state("victory_actions")
                self.menu_index = 0
            elif choice == "MMO Hub":
                self.mmo_pending = False
                self._enter_mmo_mode()
            elif choice == "Play Again":
                self._set_state("char")
                self.menu_index = 0
            elif choice == "Main Menu":
                self._set_state("main_menu")
                self.menu_index = 0
            return
        if self.state == "victory_actions":
            now = pygame.time.get_ticks()
            if choice == "Generate Auto-Dev Plan":
                self._mmo_generate_plan(now)
                self.victory_action_message = "Auto-dev plan generated."
            elif choice == "Issue Arena Grant":
                self.victory_action_message = self._mmo_award_arena_grant()
            elif choice == "Sync Nearby Region":
                self._mmo_sync_region()
                self.victory_action_message = "Nearby region synced."
            elif choice == "Seed Frontier Region":
                self._mmo_spawn_region()
                self.victory_action_message = "Frontier region scouting started."
            elif choice == "Stage Campaign":
                self.victory_action_message = self._mmo_extend_pipeline(
                    now, source="Launchpad"
                )
            elif choice == "Enter MMO Hub":
                if self.mmo_unlocked or self.mmo_pending:
                    self.mmo_pending = False
                    self._enter_mmo_mode()
                else:
                    self.victory_action_message = (
                        "MMO locked. Clear the final chapter to unlock."
                    )
            elif choice == "Back":
                self._set_state("victory")
                self.menu_index = 0
            return
        if self.state in {"victory_report", "victory_briefing"}:
            if choice == "Back":
                self._set_state("victory")
                self.menu_index = 0
            return

    def _autoplay_complete_rebind(self) -> None:
        """Complete a rebind step during autoplay."""
        if not self.rebind_action:
            self._set_state("key_bindings")
            return
        if self.state == "rebind":
            key = self.keybind_manager.get(self.rebind_action) or pygame.K_SPACE
            self.keybind_manager.set(self.rebind_action, key)
            self.input_manager.set(self.rebind_action, key)
            self._set_state("key_bindings")
        elif self.state == "rebind_controller":
            button = self.controller_bindings.get(self.rebind_action, 0)
            self.controller_bindings[self.rebind_action] = button
            self.input_manager.set_button(self.rebind_action, button)
            self._set_state("controller_bindings")

    def _autoplay_menu_choice_order(self, options: list[str]) -> list[str]:
        """Determine autoplay ordering for menu options."""
        options = [opt for opt in options if not opt.startswith("Filter:")]
        if self.state == "main_menu":
            preferred = [
                "Settings",
                "Match Options",
                "Accounts",
                "How to Play",
                "Credits",
                "Achievements",
                "Records",
                "Goals",
                "Vote",
                "Character Select",
                "Map Select",
                "MMO",
                "Quick Start",
                "New Game",
                "Exit",
            ]
            return [opt for opt in preferred if opt in options] + [
                opt for opt in options if opt not in preferred
            ]
        if "Back" in options:
            return [opt for opt in options if opt != "Back"] + ["Back"]
        return list(options)

    def _autoplay_preview_items(self) -> list[str]:
        """Return items to preview before selecting in the current menu."""
        if self.state == "char":
            if hasattr(self, "_paged_characters"):
                return list(self._paged_characters())
            return list(self.characters)
        if self.state == "map":
            if hasattr(self, "_paged_maps"):
                return list(self._paged_maps())
            return list(self.maps)
        if self.state == "chapter":
            return list(self.chapters)
        return []

    def _autoplay_state_complete(self, state: str) -> bool:
        """Return True when autoplay has selected every option for a state."""  
        options = self._menu_options_for_state(state)
        if not options:
            return False
        seen = self.autoplay_menu_seen.get(state, set())
        return all(opt in seen for opt in options)

    def _autoplay_collection_complete(
        self,
        state: str,
        *,
        exclude: set[str],
        required: list[str],
    ) -> bool:
        options = self._menu_options_for_state(state) or []
        candidates = [opt for opt in options if opt not in exclude]
        required = [opt for opt in required if opt not in exclude]
        if not candidates and not required:
            return False
        seen = self.autoplay_menu_seen.get(state, set())
        return all(opt in seen for opt in candidates) and all(
            opt in seen for opt in required
        )

    def _autoplay_vote_category_complete(self, category: str) -> bool:
        """Return True when a vote category has no remaining choices."""        
        if category == "Character":
            options = self.voting_manager.get_options()
        else:
            options = self.biome_voting_manager.get_options()
        seen = self.autoplay_vote_seen.get(category, set())
        seen_count = len([opt for opt in seen if opt != "Back"])
        if self.autoplay_menu_quick and self.autoplay_vote_limit > 0:
            return seen_count >= min(self.autoplay_vote_limit, len(options))
        return all(opt in seen for opt in options + ["Back"])

    def _autoplay_vote_complete(self) -> bool:
        """Return True once every vote option has been exercised."""
        return all(
            self._autoplay_vote_category_complete(category)
            for category in ("Character", "Biome")
        )

    def _autoplay_menu_playing(self, now: int) -> bool:
        """Exit gameplay quickly during menu traversal."""
        if self.autoplay_menu_resume_state and now >= self.autoplay_menu_resume_time:
            self._set_state(self.autoplay_menu_resume_state)
            self.autoplay_menu_resume_state = None
            return True
        if not self.autoplay_pause_tested and now - self.level_start_time >= 600:
            self._set_state("paused")
            self.autoplay_pause_tested = True
            return True
        return False

    def _autoplay_update_learning(self, now: int) -> None:
        """Feed recent combat outcomes back into autoplay tuning."""
        if not self.autoplay or not self.autoplayer:
            return
        player = getattr(self, "player", None)
        if player is None:
            return
        if self.autoplay_last_health is None:
            self.autoplay_last_health = float(player.health)
            self.autoplay_last_kills = self.kills
            self.autoplay_last_feedback = now
            return
        if now - self.autoplay_last_feedback < self.autoplay_learning_interval:
            return
        damage_taken = max(0.0, self.autoplay_last_health - float(player.health))
        kills = max(0, self.kills - self.autoplay_last_kills)
        health_ratio = float(player.health) / max(1.0, float(player.max_health))
        self.autoplayer.update_feedback(
            damage_taken,
            kills,
            health_ratio,
            now - self.autoplay_last_feedback,
        )
        self.autoplay_last_health = float(player.health)
        self.autoplay_last_kills = self.kills
        self.autoplay_last_feedback = now
        snapshot = self.autoplayer.tuning_snapshot()
        self._autoplay_trace(
            (
                "Learn tuning "
                f"agg={snapshot.get('aggression'):.2f} "
                f"caution={snapshot.get('caution'):.2f} "
                f"special={snapshot.get('special_chance'):.2f}"
            ),
            now=now,
        )

    def _autoplay_monitor(self, now: int) -> None:
        """Emit periodic autoplay telemetry for monitoring."""
        if not self.autoplay_monitor or not self.autoplay or not self.autoplayer:
            return
        if now - self.autoplay_monitor_last < self.autoplay_monitor_interval:
            return
        self.autoplay_monitor_last = now
        player = getattr(self, "player", None)
        if player is None:
            return
        goal = getattr(self.autoplayer, "last_goal", "idle")
        target = getattr(self.autoplayer, "last_target_name", "None")
        dist = getattr(self.autoplayer, "last_target_distance", 0)
        pos = int(player.rect.centerx)
        world = int(getattr(self, "world_width", self.width))
        map_name = self.map_manager.current or self.selected_map
        threat = 0.0
        if map_name:
            threat = float(self._map_preview_data(map_name).get("threat", 0))
        hp = player.health / max(1, player.max_health)
        mp = player.mana / max(1, player.max_mana)
        st = player.stamina / max(1, player.max_stamina)
        self._autoplay_trace(
            f"MON goal={goal} tgt={target} d={dist} pos={pos}/{world}",
            now=now,
        )
        self._autoplay_trace(
            f"MON hp={hp:.2f} mp={mp:.2f} st={st:.2f} thr={threat:.1f}",
            now=now,
        )
        snapshot = self.autoplayer.tuning_snapshot()
        self._autoplay_trace(
            "MON tune "
            f"a={snapshot.get('aggression', 0):.2f} "
            f"c={snapshot.get('caution', 0):.2f} "
            f"sp={snapshot.get('special_chance', 0):.2f} "
            f"dd={snapshot.get('dodge_bias', 0):.2f}",
            now=now,
        )
        if self.autoplay_feature_counts:
            summary = sorted(
                self.autoplay_feature_counts.items(),
                key=lambda item: item[1],
                reverse=True,
            )[:4]
            packed = " ".join(f"{name}={count}" for name, count in summary)
            self._autoplay_trace(f"MON features {packed}", now=now)

    def _autoplay_trace(self, message: str, *, now: int | None = None) -> None: 
        """Record autoplay actions to the HUD and console."""
        if now is None:
            now = pygame.time.get_ticks()
        stamp = f"{now / 1000:6.1f}s"
        line = f"{stamp} {message}"
        if self.autoplay_trace:
            self.autoplay_trace_lines.append(line)
            if len(self.autoplay_trace_lines) > max(1, self.autoplay_trace_limit):
                self.autoplay_trace_lines = self.autoplay_trace_lines[
                    -self.autoplay_trace_limit :
                ]
            if self.autoplay_trace_console:
                print(line)
        self._autoplay_log(line)

    def _autoplay_log(self, line: str) -> None:
        if not self.autoplay_log_enabled:
            return
        try:
            os.makedirs(os.path.dirname(self.autoplay_log_path), exist_ok=True)
            with open(self.autoplay_log_path, "a", encoding="utf-8") as handle:
                handle.write(line + "\n")
        except OSError:
            return

    def _autoplay_record_feature(self, name: str) -> None:
        if not self.autoplay:
            return
        current = self.autoplay_feature_counts.get(name, 0)
        self.autoplay_feature_counts[name] = current + 1

    def _autoplay_current_character_name(self) -> str:
        name = str(getattr(self, "selected_character", "") or "")
        if name:
            return name
        player = getattr(self, "player", None)
        if player is not None:
            return player.__class__.__name__.replace("Player", "") or "Player"
        return "Player"

    def _autoplay_required_actions(self) -> tuple[str, ...]:
        actions: set[str] = set()
        input_manager = getattr(self, "input_manager", None)
        if input_manager is not None:
            actions.update(str(name) for name in input_manager.key_bindings.keys())
        player = getattr(self, "player", None)
        if player is not None:
            skill_manager = getattr(player, "skill_manager", None)
            skill_names = getattr(skill_manager, "_skills", None)
            if isinstance(skill_names, dict):
                actions.update(str(name) for name in skill_names.keys())
        actions.discard("Back")
        if not actions:
            actions.update(
                {
                    "jump",
                    "block",
                    "parry",
                    "dodge",
                    "sprint",
                    "shoot",
                    "melee",
                    "special",
                    "use_item",
                    "use_mana",
                }
            )
        return tuple(sorted(actions))

    def _autoplay_record_character_action(self, action: str) -> None:
        if not self.autoplay_skill_audit:
            return
        if action not in self._autoplay_required_actions():
            return
        character = self._autoplay_current_character_name()
        counts = self.autoplay_character_action_counts.setdefault(character, {})
        counts[action] = counts.get(action, 0) + 1

    def _autoplay_reset_character_audit(self, character: str | None = None) -> None:
        if not self.autoplay_skill_audit:
            return
        if character is None:
            character = self._autoplay_current_character_name()
        self.autoplay_character_action_counts[character] = {}
        self.autoplay_character_action_missing[character] = set(
            self._autoplay_required_actions()
        )
        self.autoplay_skill_audit_completed.discard(character)

    def _autoplay_character_missing_actions(
        self, character: str | None = None
    ) -> list[str]:
        if character is None:
            character = self._autoplay_current_character_name()
        seen = self.autoplay_character_action_counts.get(character, {})
        required = self._autoplay_required_actions()
        missing = [name for name in required if name not in seen]
        self.autoplay_character_action_missing[character] = set(missing)
        return missing

    def _autoplay_audit_character_actions(self, now: int) -> None:
        if not self.autoplay_skill_audit or self.state != "playing":
            return
        if now - self.autoplay_skill_audit_last < self.autoplay_skill_audit_interval:
            return
        self.autoplay_skill_audit_last = now
        character = self._autoplay_current_character_name()
        missing = self._autoplay_character_missing_actions(character)
        if not missing:
            if character not in self.autoplay_skill_audit_completed:
                self.autoplay_skill_audit_completed.add(character)
                self._autoplay_dump_skill_audit_report(
                    character=character,
                    now=now,
                )
                self._autoplay_trace(
                    f"AUDIT {character}: all actions verified",
                    now=now,
                )
            return
        missing_text = ", ".join(missing)
        self._autoplay_trace(
            f"AUDIT {character}: missing {missing_text}",
            now=now,
        )

    def _autoplay_dump_skill_audit_report(
        self, *, character: str | None = None, now: int | None = None
    ) -> None:
        if not self.autoplay_skill_audit_report:
            return
        if character is None:
            character = self._autoplay_current_character_name()
        if now is None:
            now = pygame.time.get_ticks()
        counts = self.autoplay_character_action_counts.get(character, {})
        missing = self._autoplay_character_missing_actions(character)
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "elapsed_ms": int(now),
            "character": character,
            "completed": not missing,
            "missing": missing,
            "counts": dict(counts),
            "map": getattr(self, "selected_map", None),
            "mode": getattr(self, "selected_mode", None),
            "playthrough": int(getattr(self, "ai_playthroughs", 0)),
        }
        try:
            os.makedirs(
                os.path.dirname(self.autoplay_skill_audit_report_path),
                exist_ok=True,
            )
            report = []
            if os.path.exists(self.autoplay_skill_audit_report_path):
                with open(
                    self.autoplay_skill_audit_report_path,
                    "r",
                    encoding="utf-8",
                ) as handle:
                    report = json.load(handle) or []
            report.append(entry)
            with open(
                self.autoplay_skill_audit_report_path,
                "w",
                encoding="utf-8",
            ) as handle:
                json.dump(report, handle, indent=2)
        except (OSError, json.JSONDecodeError):
            return

    def _autoplay_next_audit_character(self) -> str | None:
        if not self.autoplay_skill_audit_runner:
            return None
        characters = list(getattr(self, "characters", []) or [])
        if not characters:
            return None
        remaining = [
            name for name in characters if name not in self.autoplay_skill_audit_completed
        ]
        if not remaining:
            return None
        start = self.autoplay_skill_audit_runner_index % len(remaining)
        name = remaining[start]
        self.autoplay_skill_audit_runner_index += 1
        return name

    def _autoplay_run_skill_audit_cycle(self, now: int) -> bool:
        if not self.autoplay_skill_audit_runner:
            return False
        current = self._autoplay_current_character_name()
        if current not in self.autoplay_skill_audit_completed:
            return False
        next_name = self._autoplay_next_audit_character()
        if next_name is None:
            self._autoplay_trace(
                "AUDIT runner complete: all characters verified",
                now=now,
            )
            self.autoplay_agent_enabled = False
            self.autoplay_menu_resume_state = "main_menu"
            self.autoplay_menu_resume_time = now + self.autoplay_menu_delay
            return True
        self.selected_character = next_name
        self._autoplay_trace(
            f"AUDIT runner -> {next_name}",
            now=now,
        )
        self._setup_level()
        self.level_start_time = pygame.time.get_ticks()
        self._set_state("playing")
        return True

    def _autoplay_trace_inputs(
        self,
        pressed_keys: set[int],
        actions: set[str],
        now: int,
    ) -> None:
        """Log input decisions made during autoplay."""
        for action in actions:
            self._autoplay_record_feature(f"action:{action}")
            self._autoplay_record_character_action(action)
        if not self.autoplay_trace:
            return
        if now - self.autoplay_input_trace_last < self.autoplay_trace_interval: 
            return
        self.autoplay_input_trace_last = now
        key_names = [pygame.key.name(key) for key in sorted(pressed_keys)]      
        action_names = sorted(actions)
        keys_text = ", ".join(key_names) if key_names else "-"
        actions_text = ", ".join(action_names) if action_names else "-"
        self._autoplay_trace(f"Input keys=[{keys_text}] actions=[{actions_text}]", now=now)

    def _draw_autoplay_trace(self) -> None:
        """Draw recent autoplay decisions on screen."""
        if not self.autoplay_trace_overlay:
            return
        if not self.autoplay_trace_lines:
            return
        font = self.autoplay_trace_font
        lines = self.autoplay_trace_lines[-self.autoplay_trace_limit :]
        line_h = font.get_linesize()
        width = max(font.size(line)[0] for line in lines) + 12
        height = line_h * len(lines) + 10
        panel = pygame.Surface((width, height), pygame.SRCALPHA)
        panel.fill((10, 12, 16, 170))
        self.screen.blit(panel, (10, 10))
        for i, line in enumerate(lines):
            label = font.render(line, True, (230, 240, 250))
            self.screen.blit(label, (16, 14 + i * line_h))

    def execute_account_option(self, option: str) -> None:
        """Handle account actions for tests and menus."""
        if option == "Register Account":
            self.accounts_manager.register(self.account_id, "user", "PUBKEY")
        elif option == "Delete Account":
            self.accounts_manager.delete(self.account_id)
        elif option == "Renew Key":
            priv = self.accounts_manager.renew_key(self.account_id)
            if self.network_manager is not None:
                key = serialization.load_pem_private_key(priv, password=None)
                self.network_manager.security.tx.sign_key = key

    def start_node(self) -> None:
        """Begin hosting a blockchain node."""
        if self.network_manager is None:
            priv = load_private_key(self.account_id)
            sign_key = None
            if priv is not None:
                sign_key = serialization.load_pem_private_key(priv, password=None)
            self.network_manager = NetworkManager(
                host=True,
                relay_mode=self.latency_helper,
                sign_key=sign_key,
                client_id=self.account_id or "node",
            )
            self.network_manager.broadcast_announce(load_nodes())
            if self.latency_helper:
                self.network_manager.offer_relay(load_nodes())
            self.node_hosting = True

    def stop_node(self) -> None:
        """Stop hosting the blockchain node."""
        if self.network_manager is not None:
            try:
                self.network_manager.sock.close()
            except OSError:
                pass
            self.network_manager = None
        self.node_hosting = False

    def _poll_network(self) -> None:
        if self.network_manager is not None:
            now = pygame.time.get_ticks()
            for _addr, data in self.network_manager.poll():
                if data.get("type") == "chat":
                    user = data.get("user", "Remote")
                    msg = data.get("msg", "")
                    self.chat_manager.send(user, msg)
                elif data.get("type") == "mmo_shard_announce":
                    shard = data.get("shard")
                    load = data.get("load")
                    if isinstance(shard, str) and isinstance(load, int):
                        self.mmo_shard_stats[shard] = max(1, load)
                elif data.get("type") == "mmo_join":
                    if not self._mmo_shard_ok(data):
                        continue
                    player_id = str(data.get("player_id") or "remote")
                    if player_id != self.mmo_player_id:
                        pos = self._mmo_pos_from_payload(data)
                        if pos is not None:
                            self.mmo_presence.seen(player_id, pos, now)
                        self._send_mmo_snapshot(_addr)
                elif data.get("type") == "mmo_leave":
                    if not self._mmo_shard_ok(data):
                        continue
                    player_id = str(data.get("player_id") or "remote")
                    self._drop_mmo_peer(player_id)
                elif data.get("type") == "mmo_snapshot_request":
                    if not self._mmo_shard_ok(data):
                        continue
                    self._send_mmo_snapshot(_addr)
                elif data.get("type") == "mmo_snapshot":
                    if not self._mmo_shard_ok(data):
                        continue
                    player_id = str(data.get("player_id") or "remote")
                    if player_id == self.mmo_player_id:
                        continue
                    snapshot = data.get("state")
                    if not isinstance(snapshot, dict):
                        continue
                    seq = data.get("seq")
                    verify = data.get("verify")
                    if verify and not self.mmo_verifier.verify(snapshot, verify):
                        continue
                    manager = self._mmo_remote_state(player_id)
                    manager.load_snapshot(snapshot, sequence=seq)
                    pos = self._mmo_pos_from_payload(snapshot)
                    if pos is not None:
                        self.mmo_presence.seen(player_id, pos, now)
                elif data.get("type") == "mmo_world_request":
                    if not self._mmo_shard_ok(data):
                        continue
                    self._send_mmo_world_snapshot(_addr)
                elif data.get("type") == "mmo_world_snapshot":
                    if not self._mmo_shard_ok(data):
                        continue
                    snapshot = data.get("state")
                    if not isinstance(snapshot, dict):
                        continue
                    seq = data.get("seq")
                    verify = data.get("verify")
                    try:
                        state = self.mmo_world_state.load_snapshot(
                            snapshot,
                            sequence=seq,
                            verify=verify if isinstance(verify, dict) else None,
                        )
                    except ValueError:
                        continue
                    self._apply_mmo_world_state(state)
                elif data.get("type") == "mmo_world_delta":
                    if not self._mmo_shard_ok(data):
                        continue
                    delta = data.get("delta")
                    if not isinstance(delta, dict):
                        continue
                    try:
                        state = self.mmo_world_state.apply_delta(delta)
                    except ValueError:
                        continue
                    self._apply_mmo_world_state(state)
                elif data.get("type") == "match_found":
                    if not self._mmo_shard_ok(data):
                        continue
                    players = data.get("players")
                    if not isinstance(players, list):
                        continue
                    self.mmo_match_group = [str(p) for p in players]
                    self.mmo_match_id = str(data.get("match_id", ""))
                    self.mmo_match_status = "found"
                    self.mmo_match_found_at = pygame.time.get_ticks()
                    self.mmo_match_ready_at = None
                    self.mmo_message = "Match found."
                elif data.get("type") == "match_ready":
                    if not self._mmo_shard_ok(data):
                        continue
                    self.mmo_match_status = "ready"
                    self.mmo_match_ready_at = pygame.time.get_ticks()
                    self.mmo_message = "Match ready."
                elif data.get("type") == "match_cancel":
                    if not self._mmo_shard_ok(data):
                        continue
                    self.mmo_match_status = "idle"
                    self.mmo_match_group = None
                    self.mmo_match_id = None
                    self.mmo_match_found_at = None
                    self.mmo_match_ready_at = None
                    self.mmo_message = "Match canceled."
                elif data.get("type") == "mmo_state":
                    if not self._mmo_shard_ok(data):
                        continue
                    player_id = str(data.get("player_id") or "remote")
                    delta = data.get("delta")
                    if not isinstance(delta, dict):
                        continue
                    if player_id == self.mmo_player_id:
                        continue
                    try:
                        state = self._mmo_remote_state(player_id).apply(delta)
                    except ValueError:
                        continue
                    pos = (
                        float(state.get("pos_x", 0.0)),
                        float(state.get("pos_y", 0.0)),
                    )
                    self.mmo_presence.seen(player_id, pos, now)
            self.network_manager.process_reliable()
            self._prune_mmo_presence(now)

    def _prune_mmo_presence(self, now: int) -> None:
        removed = self.mmo_presence.prune(now)
        for player_id in removed:
            self.mmo_remote_states.pop(player_id, None)

    def _drop_mmo_peer(self, player_id: str) -> None:
        if not player_id or player_id == self.mmo_player_id:
            return
        self.mmo_presence.drop(player_id)
        self.mmo_remote_states.pop(player_id, None)

    def _mmo_shard_ok(self, payload: dict[str, object]) -> bool:
        shard = payload.get("shard")
        if shard is None:
            return self.mmo_shard_id == "public"
        return str(shard) == self.mmo_shard_id

    def _mmo_match_label(self) -> str:
        status = self.mmo_match_status
        if self.mmo_match_group:
            return f"{status} ({len(self.mmo_match_group)})"
        return status

    def _mmo_shard_summary(self) -> str:
        if not self.mmo_shard_stats:
            return "n/a"
        best = min(self.mmo_shard_stats.items(), key=lambda item: (item[1], item[0]))
        best_name, best_load = best
        current_load = self.mmo_shard_stats.get(self.mmo_shard_id, best_load)
        if best_name == self.mmo_shard_id:
            return f"{current_load} (optimal)"
        return f"{current_load} | best {best_load}"

    def _mmo_draw_shard_widget(self) -> None:
        palette = mmo_palette()
        rect = pygame.Rect(24, 86, 220, 96)
        panel = pygame.Surface(rect.size, pygame.SRCALPHA)
        panel.fill((*palette["panel_alt"], 228))
        pygame.draw.rect(panel, palette["border"], panel.get_rect(), 2)
        now = pygame.time.get_ticks()
        sweep = pygame.Surface(rect.size, pygame.SRCALPHA)
        offset = (now // 18) % (rect.width + rect.height)
        pygame.draw.line(
            sweep,
            (*palette["accent"], 35),
            (offset - rect.height, 0),
            (offset, rect.height),
            2,
        )
        panel.blit(sweep, (0, 0))
        header = self.small_font.render("Shard Status", True, palette["accent"])
        panel.blit(header, (12, 10))
        shard_line = self.small_font.render(
            f"{self.mmo_shard_id} | {self._mmo_shard_summary()}",
            True,
            palette["text"],
        )
        panel.blit(shard_line, (12, 34))
        mode = "Auto" if self.mmo_shard_mode == "auto" else "Fixed"
        mode_line = self.small_font.render(
            f"Mode: {mode}", True, palette["text_dim"]
        )
        panel.blit(mode_line, (12, 56))
        self.screen.blit(panel, rect.topleft)

    def _mmo_header_match_line(self) -> str | None:
        status = self.mmo_match_status
        if status == "idle":
            return None
        if status == "found" and self.mmo_match_found_at is not None:
            now = pygame.time.get_ticks()
            deadline = self.mmo_match_found_at + self.mmo_match_timeout_ms
            remaining = max(0, int((deadline - now) / 1000))
            return f"Match: Found ({remaining}s)"
        if status == "ready":
            if self.mmo_match_ready_at is None:
                return "Match: Ready"
            now = pygame.time.get_ticks()
            deadline = self.mmo_match_ready_at + self.mmo_match_ready_timeout_ms
            remaining = max(0, int((deadline - now) / 1000))
            return f"Match: Ready (launch in {remaining}s)"
        if status == "launching":
            return "Match: Launching"
        return f"Match: {status.title()}"

    def _mmo_pos_from_payload(
        self, payload: dict[str, object]
    ) -> tuple[float, float] | None:
        if "pos_x" not in payload or "pos_y" not in payload:
            return None
        return (
            float(payload.get("pos_x", 0.0)),
            float(payload.get("pos_y", 0.0)),
        )

    def _mmo_network_join(self) -> None:
        if self.network_manager is None:
            return
        pos = self.world_player_manager.get_position(self.mmo_player_id)
        region = self._mmo_nearest_region(pos)
        payload = {
            "type": "mmo_join",
            "player_id": self.mmo_player_id,
            "shard": self.mmo_shard_id,
            "pos_x": round(pos[0], 3),
            "pos_y": round(pos[1], 3),
            "region": region.get("name") if region else None,
            "biome": region.get("biome") if region else None,
        }
        self.network_manager.send_reliable(payload, importance=2)

    def _mmo_network_leave(self) -> None:
        if self.network_manager is None:
            return
        payload = {
            "type": "mmo_leave",
            "player_id": self.mmo_player_id,
            "shard": self.mmo_shard_id,
        }
        self.network_manager.send_reliable(payload, importance=2)

    def _request_mmo_snapshot(self) -> None:
        if self.network_manager is None:
            return
        payload = {
            "type": "mmo_snapshot_request",
            "player_id": self.mmo_player_id,
            "shard": self.mmo_shard_id,
        }
        self.network_manager.send_reliable(payload, importance=2)

    def _send_mmo_snapshot(self, addr: tuple[str, int]) -> None:
        if self.network_manager is None:
            return
        now = pygame.time.get_ticks()
        if not self.mmo_shared_state.state:
            self._mmo_sync_state(now, force=True)
        seq = self.mmo_shared_state.current_sequence()
        state = dict(self.mmo_shared_state.state)
        verify = self.mmo_verifier.compute(state)
        payload = {
            "type": "mmo_snapshot",
            "player_id": self.mmo_player_id,
            "shard": self.mmo_shard_id,
            "seq": seq,
            "state": state,
            "verify": verify,
        }
        self.network_manager.send_reliable(payload, addr=addr, importance=2)

    def _request_mmo_world_snapshot(self) -> None:
        if self.network_manager is None:
            return
        payload = {
            "type": "mmo_world_request",
            "player_id": self.mmo_player_id,
            "shard": self.mmo_shard_id,
        }
        self.network_manager.send_reliable(payload, importance=2)

    def _send_mmo_world_snapshot(self, addr: tuple[str, int]) -> None:
        if self.network_manager is None:
            return
        now = pygame.time.get_ticks()
        if not self.mmo_world_state.state:
            self._mmo_sync_world_state(now, force=True)
        seq = self.mmo_world_state.current_sequence()
        state = dict(self.mmo_world_state.state)
        verify = self.mmo_verifier.compute(state)
        payload = {
            "type": "mmo_world_snapshot",
            "player_id": self.mmo_player_id,
            "shard": self.mmo_shard_id,
            "seq": seq,
            "state": state,
            "verify": verify,
        }
        self.network_manager.send_reliable(payload, addr=addr, importance=2)

    def _trigger_holo_hype(self, now: int) -> None:
        """Boost the arena momentum during hot streaks."""
        if self.holo_hype_active:
            self.holo_hype_until = max(self.holo_hype_until, now + 4000)
            return
        self.holo_hype_active = True
        self.holo_hype_until = now + 4000
        self.player.stats.apply_modifier("attack", self.holo_hype_attack_bonus)
        self.player.speed_factor += self.holo_hype_speed_bonus
        self._spawn_holo_cheer("Holo Hype!", (self.player.rect.centerx, self.player.rect.top - 30))

    def _end_holo_hype(self) -> None:
        if not self.holo_hype_active:
            return
        self.holo_hype_active = False
        self.player.stats.remove_modifier(
            "attack", self.holo_hype_attack_bonus
        )
        self.player.speed_factor = max(
            0.1, self.player.speed_factor - self.holo_hype_speed_bonus
        )

    def _draw_holo_hype_banner(self, now: int) -> None:
        if not self.holo_hype_active:
            return
        remaining = max(0, int((self.holo_hype_until - now) / 1000))
        banner = pygame.Surface((self.width, 48), pygame.SRCALPHA)
        banner.fill((250, 180, 80, 140))
        self.screen.blit(banner, (0, 80))
        label = self.menu_font.render(
            f"Holo Hype! {remaining}s", True, (255, 255, 255)
        )
        self.screen.blit(
            label, label.get_rect(center=(self.width // 2, 104))
        )

    def _spawn_holo_cheer(self, text: str, pos: tuple[int, int]) -> None:
        color = self.holo_cheer_colors[
            self.holo_cheer_color_idx % len(self.holo_cheer_colors)
        ]
        self.holo_cheer_color_idx += 1
        self.damage_numbers.add(CheerText(text, pos, color=color))

    def _draw_stage_ribbons(self, now: int) -> None:
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        center_x = self.width // 2
        base_y = int(self.height * 0.12)
        wave = math.sin(now / 700) * 6
        colors = [
            (120, 210, 255, 90),
            (255, 180, 220, 90),
            (255, 220, 160, 90),
        ]
        for idx, color in enumerate(colors):
            offset = idx * 12
            points = [
                (center_x - 240, base_y + offset),
                (center_x - 80, base_y + 20 + wave + offset),
                (center_x + 80, base_y + 10 - wave + offset),
                (center_x + 240, base_y + offset),
            ]
            pygame.draw.lines(overlay, color, False, points, 4)
        self.screen.blit(overlay, (0, 0))

    def _draw_holo_spotlight(self, now: int) -> None:
        if not self.holo_hype_active and now >= self.holo_spotlight_swap_until:
            return
        pulse = (math.sin(now / 200) + 1) * 0.5
        radius = 90 + int(10 * pulse)
        center = (self.player.rect.centerx, self.player.rect.centery)
        if now < self.holo_spotlight_swap_until and self.enemies:
            target = max(self.enemies, key=lambda e: getattr(e, "health", 0))
            center = (target.rect.centerx, target.rect.centery)
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        pygame.draw.circle(overlay, (255, 220, 120, 40), center, radius)
        pygame.draw.circle(overlay, (255, 240, 200, 90), center, radius, 2)
        self.screen.blit(overlay, (0, 0))

    def _draw_stage_lights(self, now: int) -> None:
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        pulse = (math.sin(now / 900) + 1) * 0.5
        left = [(0, 0), (self.width * 0.35, 0), (self.width * 0.5, self.height)]
        right = [
            (self.width, 0),
            (self.width * 0.65, 0),
            (self.width * 0.5, self.height),
        ]
        alpha = 40 + int(30 * pulse)
        pygame.draw.polygon(overlay, (120, 200, 255, alpha), left)
        pygame.draw.polygon(overlay, (255, 180, 220, alpha), right)
        for idx in range(6):
            x = int(self.width * 0.2 + idx * self.width * 0.12)
            y = int(40 + 10 * math.sin((now / 500) + idx))
            pygame.draw.circle(overlay, (255, 240, 200, 80), (x, y), 4)
        self.screen.blit(overlay, (0, 0))

    def _draw_holo_sparkles(self, now: int) -> None:
        if not self.holo_hype_active:
            return
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        center = (self.player.rect.centerx, self.player.rect.centery)
        for idx in range(8):
            angle = (now / 200) + idx * (math.pi / 4)
            radius = 36 + int(6 * math.sin((now / 150) + idx))
            x = int(center[0] + math.cos(angle) * radius)
            y = int(center[1] + math.sin(angle) * radius)
            pygame.draw.circle(overlay, (255, 230, 180, 180), (x, y), 3)
        self.screen.blit(overlay, (0, 0))

    def _draw_holo_confetti(self, now: int) -> None:
        if not self.holo_hype_active:
            return
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        colors = [
            (120, 220, 255, 140),
            (255, 180, 220, 140),
            (255, 220, 160, 140),
            (180, 255, 210, 140),
        ]
        for idx in range(16):
            drift = math.sin((now / 400) + idx) * 20
            x = int((idx * 90 + now / 6) % (self.width + 40) - 20)
            y = int((idx * 40 + now / 10) % 160)
            color = colors[idx % len(colors)]
            pygame.draw.circle(overlay, color, (x, y + int(drift)), 3)
        self.screen.blit(overlay, (0, 0))

    def _draw_fan_glow(self, now: int) -> None:
        if not self.holo_hype_active:
            return
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        pulse = (math.sin(now / 300) + 1) * 0.5
        bar_width = 18
        for idx in range(10):
            x = int(self.width * 0.1 + idx * self.width * 0.08)
            height = 26 + int(8 * math.sin((now / 200) + idx))
            color = (120, 210, 255, int(120 + 60 * pulse))
            pygame.draw.rect(
                overlay,
                color,
                pygame.Rect(x, self.height - height - 12, bar_width, height),
            )
        self.screen.blit(overlay, (0, 0))

    def _draw_holo_highlight(self, now: int) -> None:
        if now >= self.holo_highlight_until:
            return
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        pulse = (math.sin(now / 180) + 1) * 0.5
        alpha = 80 + int(80 * pulse)
        overlay.fill((255, 220, 160, alpha))
        self.screen.blit(overlay, (0, 0))

    def _draw_arena_intro(self, now: int) -> None:
        if now >= self.arena_intro_until:
            return
        remaining = self.arena_intro_until - now
        alpha = 180 if remaining > 600 else max(60, int(180 * remaining / 600))
        banner = pygame.Surface((self.width, 70), pygame.SRCALPHA)
        banner.fill((20, 30, 45, alpha))
        self.screen.blit(banner, (0, int(self.height * 0.25)))
        title = self.menu_font.render(self.arena_intro_title, True, (255, 255, 255))
        subtitle = self.small_font.render(
            self.arena_intro_subtitle, True, (220, 240, 255)
        )
        self.screen.blit(
            title,
            title.get_rect(center=(self.width // 2, int(self.height * 0.25) + 22)),
        )
        self.screen.blit(
            subtitle,
            subtitle.get_rect(center=(self.width // 2, int(self.height * 0.25) + 46)),
        )

    def _draw_fan_sign_wave(self, now: int) -> None:
        if now >= self.holo_sign_until:
            return
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        wave = math.sin(now / 200) * 6
        signs = [
            (int(self.width * 0.15), int(self.height * 0.78)),
            (int(self.width * 0.3), int(self.height * 0.8)),
            (int(self.width * 0.7), int(self.height * 0.8)),
            (int(self.width * 0.85), int(self.height * 0.78)),
        ]
        for idx, (x, y) in enumerate(signs):
            offset = int(wave + idx * 2)
            rect = pygame.Rect(x, y + offset, 60, 28)
            pygame.draw.rect(overlay, (255, 220, 160, 160), rect, 0, 6)
            pygame.draw.rect(overlay, (255, 240, 220, 220), rect, 2, 6)
        self.screen.blit(overlay, (0, 0))

    def _draw_audience_wave(self, now: int) -> None:
        if now >= self.holo_audience_until:
            return
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        base_y = int(self.height * 0.82)
        for idx in range(16):
            x = int(self.width * 0.08 + idx * self.width * 0.055)
            bob = int(6 * math.sin((now / 180) + idx))
            color = (120, 220, 255, 120 + (idx % 3) * 30)
            pygame.draw.circle(overlay, color, (x, base_y + bob), 6)
            pygame.draw.circle(overlay, (255, 230, 180, 200), (x, base_y + bob), 2)
        self.screen.blit(overlay, (0, 0))

    def _draw_arena_corner_badge(self, now: int) -> None:
        label = "Hololive Live Arena"
        map_name = (
            self.selected_map
            or self.selected_chapter
            or self.map_manager.current
            or "Arena"
        )
        badge = pygame.Surface((240, 46), pygame.SRCALPHA)
        badge.fill((10, 20, 30, 170))
        pygame.draw.rect(badge, (0, 180, 200), badge.get_rect(), 2)
        text = self.small_font.render(label, True, (220, 240, 255))
        badge.blit(text, (12, 6))
        sub = self.small_font.render(str(map_name), True, (170, 210, 230))
        badge.blit(sub, (12, 24))
        pulse = (math.sin(now / 500) + 1) * 0.5
        dot = pygame.Surface((6, 6), pygame.SRCALPHA)
        dot.fill((255, 220, 140, 100 + int(80 * pulse)))
        badge.blit(dot, (210, 18))
        self.screen.blit(badge, (14, 12))

    def _xp_for_enemy(self, enemy) -> int:
        """Return XP reward for a single enemy based on stats and difficulty."""
        multiplier = max(0.1, float(getattr(self, "xp_multiplier", 1.0)))
        base = 10.0 * multiplier
        stats = getattr(enemy, "stats", None)
        attack = int(stats.get("attack")) if stats else 0
        defense = int(stats.get("defense")) if stats else 0
        max_hp = int(getattr(enemy, "max_health", 0) or 0)
        rating = base + (attack * 0.6) + (defense * 0.4) + (max_hp * 0.08)
        rating = max(base, min(45.0 * multiplier, rating))
        diff = str(getattr(enemy, "difficulty", "Normal"))
        diff_mult = {
            "Easy": 0.85,
            "Normal": 1.0,
            "Hard": 1.15,
            "Elite": 1.3,
            "Adaptive": 1.2,
        }.get(diff, 1.0)
        return max(1, int(rating * diff_mult))

    def _handle_collisions(self) -> None:
        """Delegate collision handling to :class:`CombatManager`."""       
        now = pygame.time.get_ticks()
        killed = self.combat_manager.handle_collisions(
            self.player,
            self.enemies,
            self.projectiles,
            self.melee_attacks,
            now,
            allies=self.allies,
            damage_numbers=self.damage_numbers,
        )
        if killed:
            count = len(killed)
            self._autoplay_record_feature("kill")
            if self.autoplay_log_enabled:
                self._autoplay_log(f"Kills +{count}")
            for _ in range(count):
                self.score_manager.record_kill(now / 1000.0)
            combo = self.score_manager.combo
            thresholds = [3, 5, 8, 12]
            for idx, threshold in enumerate(thresholds):
                if combo >= threshold and self.combo_cheer_level < threshold:
                    phrase_idx = min(idx, len(self.holo_cheer_phrases) - 1)
                    text = self.holo_cheer_phrases[phrase_idx]
                    self._spawn_holo_cheer(
                        text,
                        (self.player.rect.centerx, self.player.rect.top - 20),
                    )
                    self.combo_cheer_level = threshold
                    self.holo_highlight_until = now + 400
            self.score += count
            if self.holo_hype_active:
                self.score_manager.add(5 * count)
            self.player.currency_manager.add(count)
            self.kills += count
            rewards = []
            if count:
                rewards.extend(
                    self.objective_manager.record_event(
                        "enemy_defeated", count
                    )
                )
                rewards.extend(
                    self.objective_manager.record_event(
                        "coin_collected", count
                    )
                )
            for enemy in killed:
                loot = self.loot_manager.roll_loot(enemy.__class__.__name__)
                if loot:
                    self.player.inventory.add(loot)
                self.reputation_manager.modify(
                    getattr(enemy, "faction", "Arena"),
                    getattr(enemy, "reputation_reward", 5),
                )
            xp_gain = max(1, int(sum(self._xp_for_enemy(enemy) for enemy in killed)))
            self.player.gain_xp(xp_gain)
            if rewards:
                self._apply_objective_rewards(rewards)
            if (
                self.kills >= 1
                and not self.achievement_manager.is_unlocked("First Blood")
            ):
                self.achievement_manager.unlock("First Blood")
            if self.kills == 5:
                self.holo_sign_until = now + 1800
                self.holo_audience_until = now + 2000
                self._spawn_holo_cheer(
                    "Fan Sign Wave!",
                    (self.width // 2, int(self.height * 0.2)),
                )
            if (
                self.score_manager.combo >= self.holo_hype_trigger
                and not self.holo_hype_active
            ):
                self._trigger_holo_hype(now)

    def _handle_powerup_collision(self) -> None:
        """Apply power-up effects when the player touches one."""
        if getattr(self.player, "dodging", False):
            return
        for p in list(self.powerups):
            if not self.player.rect.colliderect(p.rect):
                continue
            self._autoplay_record_feature(f"powerup:{p.effect}")
            if p.effect == "heal":
                hp_before = float(getattr(self.player, "health", 0))
                self.player.health = self.player.max_health
                self.emit_event(
                    {
                        "type": "heal",
                        "source": "powerup:heal",
                        "target_id": self._event_target_id(self.player),
                        "amount": max(0.0, float(self.player.health) - hp_before),
                        "hp_before": hp_before,
                        "hp_after": float(getattr(self.player, "health", 0)),
                    }
                )
            elif p.effect == "mana":
                self.player.mana = self.player.max_mana
            elif p.effect == "stamina":
                self.player.stamina_manager.stamina = (
                    self.player.stamina_manager.max_stamina
                )
            elif p.effect == "speed":
                self.status_manager.add_effect(self.player, SpeedEffect())
            elif p.effect == "shield":
                self.status_manager.add_effect(self.player, ShieldEffect())
            elif p.effect == "attack":
                self.status_manager.add_effect(self.player, AttackEffect())
            elif p.effect == "defense":
                self.status_manager.add_effect(self.player, DefenseEffect())
            elif p.effect == "xp":
                self.player.gain_xp(50)
            elif p.effect == "life":
                self.player.lives += 1
            cheer_map = {
                "heal": "Idol Heal!",
                "mana": "Mana Wave!",
                "stamina": "Stamina Pop!",
                "speed": "Speed Step!",
                "shield": "Stage Shield!",
                "attack": "Power Up!",
                "defense": "Guard Up!",
                "xp": "XP Spark!",
                "life": "Encore Life!",
            }
            cheer_text = cheer_map.get(p.effect)
            if cheer_text:
                self._spawn_holo_cheer(
                    cheer_text,
                    (self.player.rect.centerx, self.player.rect.top - 24),
                )
            self.event_manager.trigger(f"pickup_{p.effect}")
            rewards = self.objective_manager.record_event("powerup_collected")
            if rewards:
                self._apply_objective_rewards(rewards)
            p.kill()

    def _apply_objective_rewards(self, rewards: list[dict[str, int]]) -> None:
        """Grant coins or experience from newly completed objectives."""

        player = getattr(self, "player", None)
        if not rewards or player is None:
            return
        for reward in rewards:
            coins = int(reward.get("coins", 0))
            xp = int(reward.get("xp", 0))
            if coins:
                player.currency_manager.add(coins)
            if xp:
                player.gain_xp(xp)

    def _bootstrap_profile_from_legacy_settings(self) -> None:
        """Seed an empty profile from legacy settings/inventory files."""

        items = self.profile.inventory.get("items", {})
        balances = self.profile.economy.get("balances", {})
        unlocks = self.profile.progression.get("unlocks", {})
        has_progress = bool(
            items
            or self.profile.achievements.get("unlocked_ids")
            or self.profile.reputation.get("factions")
            or (isinstance(balances, dict) and int(balances.get("coins", 0)) > 0)
            or (isinstance(unlocks, dict) and unlocks.get("mmo_unlocked"))
        )
        if has_progress:
            return
        legacy_inventory = load_inventory()
        if isinstance(legacy_inventory, dict) and legacy_inventory:
            self.profile.inventory["items"] = {
                str(k): max(0, int(v))
                for k, v in legacy_inventory.items()
                if isinstance(k, str)
            }
        legacy_coins = self.settings.get("coins")
        if legacy_coins is not None:
            self.profile.economy.setdefault("balances", {})
            self.profile.economy["balances"]["coins"] = max(0, int(legacy_coins))
        legacy_achievements = self.settings.get("achievements", [])
        if isinstance(legacy_achievements, list) and legacy_achievements:
            self.profile.achievements["unlocked_ids"] = sorted(
                {str(item) for item in legacy_achievements if str(item)}
            )
        legacy_reputation = self.settings.get("reputation", {})
        if isinstance(legacy_reputation, dict) and legacy_reputation:
            self.profile.reputation["factions"] = {
                str(k): int(v)
                for k, v in legacy_reputation.items()
                if isinstance(k, str)
            }
        if self.settings.get("mmo_unlocked"):
            self.profile.progression.setdefault("unlocks", {})
            self.profile.progression["unlocks"]["mmo_unlocked"] = True
        self.profile_store.save(self.profile)

    def _apply_profile_to_global_progression(self) -> None:
        """Apply profile-level progression to runtime defaults."""

        balances = self.profile.economy.get("balances", {})
        if isinstance(balances, dict):
            profile_coins = max(0, int(balances.get("coins", 0)))
            self.coins = max(int(self.coins), profile_coins)
        unlocks = self.profile.progression.get("unlocks", {})
        if isinstance(unlocks, dict):
            self.mmo_unlocked = bool(unlocks.get("mmo_unlocked", False))

    def _apply_profile_meta_selection(self) -> None:
        """Restore last character selection from profile metadata."""

        meta = self.profile.meta if isinstance(self.profile.meta, dict) else {}
        last_character = str(meta.get("last_played_character", "") or "")
        if last_character and last_character in self.characters and not self.autoplay:
            self.selected_character = last_character

    def _hydrate_player_from_profile(self, player: PlayerCharacter) -> None:
        """Hydrate inventory/currency/XP state for a new player instance."""

        inventory = self.profile.inventory if isinstance(self.profile.inventory, dict) else {}
        items = inventory.get("items", {})
        if isinstance(items, dict):
            player.inventory.load_from_dict(
                {str(k): max(0, int(v)) for k, v in items.items() if isinstance(k, str)}
            )
        capacity = inventory.get("capacity")
        player.inventory.capacity = None if capacity is None else max(0, int(capacity))
        economy = self.profile.economy if isinstance(self.profile.economy, dict) else {}
        balances = economy.get("balances", {}) if isinstance(economy.get("balances", {}), dict) else {}
        profile_coins = max(0, int(balances.get("coins", 0)))
        player.currency_manager.balance = max(profile_coins, int(getattr(self, "coins", 0)))
        progression = self.profile.progression if isinstance(self.profile.progression, dict) else {}
        player.experience_manager.level = max(1, int(progression.get("level", 1)))
        player.experience_manager.xp = max(0, int(progression.get("xp", 0)))
        player.experience_manager.threshold = max(1, int(progression.get("threshold", 100)))
        player.experience_manager.growth = max(
            1.0,
            float(progression.get("growth", player.experience_manager.growth)),
        )
        max_threshold = progression.get("max_threshold")
        if max_threshold is None:
            player.experience_manager.max_threshold = None
        else:
            player.experience_manager.max_threshold = max(1, int(max_threshold))

    def _build_profile_snapshot(self) -> Profile:
        """Build a profile snapshot from runtime progression managers."""

        player = getattr(self, "player", None)
        progression = dict(self.profile.progression)
        inventory = dict(self.profile.inventory)
        economy = dict(self.profile.economy)
        achievements = dict(self.profile.achievements)
        reputation = dict(self.profile.reputation)
        meta = dict(self.profile.meta)
        if player is not None:
            inventory["items"] = player.inventory.to_dict()
            inventory["capacity"] = player.inventory.capacity
            economy.setdefault("balances", {})
            economy["balances"] = dict(economy.get("balances", {}))
            economy["balances"]["coins"] = player.currency_manager.get_balance()
            progression["level"] = int(player.experience_manager.level)
            progression["xp"] = int(player.experience_manager.xp)
            progression["threshold"] = int(player.experience_manager.threshold)
            progression["growth"] = float(player.experience_manager.growth)
            progression["max_threshold"] = player.experience_manager.max_threshold
        progression.setdefault("unlocks", {})
        progression["unlocks"] = dict(progression.get("unlocks", {}))
        progression["unlocks"]["mmo_unlocked"] = bool(self.mmo_unlocked)
        achievements["unlocked_ids"] = sorted(self.achievement_manager.unlocked)
        reputation["factions"] = self.reputation_manager.to_dict()
        meta["last_played_character"] = str(self.selected_character or "")
        meta["last_played_utc"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        meta["session_count"] = int(meta.get("session_count", 0)) + 1
        return Profile(
            schema_version=self.profile.schema_version,
            created_utc=self.profile.created_utc,
            updated_utc=self.profile.updated_utc,
            profile_id=self.profile.profile_id,
            progression=progression,
            inventory=inventory,
            economy=economy,
            achievements=achievements,
            reputation=reputation,
            meta=meta,
            validation_warnings=[],
            raw_payload=dict(self.profile.raw_payload),
        )

    def _save_profile_checkpoint(self) -> None:
        """Persist profile state for exit/checkpoint saves."""

        snapshot = self._build_profile_snapshot()
        self.profile_store.save(snapshot)
        self.profile = snapshot

    def run(self):
        """Start the main game loop."""
        self.running = True
        frame_index = 0
        while self.running:
            self._event_frame = int(frame_index)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type in (
                    pygame.VIDEORESIZE,
                    getattr(pygame, "WINDOWSIZECHANGED", pygame.NOEVENT),
                ):
                    next_w = int(getattr(event, "w", self.width) or self.width)
                    next_h = int(getattr(event, "h", self.height) or self.height)
                    min_w, min_h = 800, 450
                    next_w = max(min_w, next_w)
                    next_h = max(min_h, next_h)
                    if (next_w, next_h) != (self.width, self.height):
                        self.width, self.height = next_w, next_h
                        if self.state != "playing":
                            self.world_width = self.width
                            self.world_height = self.height
                        self.ground_y = self.height - 50
                        self.screen = self._apply_display_mode()
                        self._apply_font_scale()
                elif (
                    event.type == pygame.KEYDOWN
                    and event.key == pygame.K_F3
                    and (self.state != "mmo" or event.mod & pygame.KMOD_CTRL)
                ):
                    if self.ui_debugger is not None:
                        state = self.ui_debugger.toggle()
                        self._autoplay_trace(
                            f"UI debug overlay -> {'on' if state else 'off'}",
                        )
                elif self.state == "splash" and event.type in (
                    pygame.KEYDOWN,
                    pygame.MOUSEBUTTONDOWN,
                    pygame.JOYBUTTONDOWN,
                ):
                    self._set_state("main_menu")
                    self.menu_index = 0
                elif (
                    self.state == "playing"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                ):
                    self._set_state("paused")
                    self.menu_index = 0
                elif (
                    self.state == "playing"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_F10
                ):
                    self.autoplay_agent_enabled = not self.autoplay_agent_enabled
                    state = "on" if self.autoplay_agent_enabled else "off"
                    self._autoplay_trace(f"Agent toggle -> {state}")
                elif (
                    self.state == "paused"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                ):
                    self._set_state("playing")
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                ):
                    if self.mmo_show_tour:
                        self.mmo_show_tour = False
                        self.mmo_seen_tour = True
                        continue
                    self._set_state("main_menu")
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_e
                    and event.mod & pygame.KMOD_SHIFT
                ):
                    self.mmo_overlay_mode = "expeditions"
                    self._clear_mmo_toggles()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_e
                ):
                    self._mmo_sync_region()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_TAB
                ):
                    self.mmo_ui_show_panel = not self.mmo_ui_show_panel
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and self.mmo_show_tour
                    and event.key in (
                        pygame.K_RETURN,
                        pygame.K_KP_ENTER,
                        pygame.K_SPACE,
                    )
                ):
                    self.mmo_tour_step += 1
                    if self.mmo_tour_step >= 5:
                        self.mmo_show_tour = False
                        self.mmo_seen_tour = True
                    continue
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_g
                ):
                    if event.mod & pygame.KMOD_SHIFT:
                        self.mmo_overlay_mode = "strategy"
                        self._clear_mmo_toggles()
                    else:
                        self._mmo_cycle_filter()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_h
                ):
                    if event.mod & pygame.KMOD_SHIFT:
                        self.mmo_overlay_mode = "projects"
                        self._clear_mmo_toggles()
                    else:
                        self.mmo_show_help = not self.mmo_show_help
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_i
                ):
                    self.mmo_show_details = not self.mmo_show_details
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_v
                ):
                    self.mmo_show_favorites = not self.mmo_show_favorites
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_l
                ):
                    if event.mod & pygame.KMOD_SHIFT:
                        self.mmo_overlay_mode = "logistics"
                        self._clear_mmo_toggles()
                    else:
                        self.mmo_show_quest_log = not self.mmo_show_quest_log
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_y
                ):
                    if event.mod & pygame.KMOD_SHIFT:
                        self.mmo_overlay_mode = "campaign"
                        self._clear_mmo_toggles()
                    else:
                        self.mmo_show_growth = not self.mmo_show_growth
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_u
                ):
                    if event.mod & pygame.KMOD_SHIFT:
                        self.mmo_overlay_mode = "fleet"
                        self._clear_mmo_toggles()
                    else:
                        self.mmo_show_party = not self.mmo_show_party
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_n
                ):
                    if event.mod & pygame.KMOD_SHIFT:
                        self.mmo_overlay_mode = "influence"
                        self._clear_mmo_toggles()
                    else:
                        self.mmo_show_network = not self.mmo_show_network
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_o
                ):
                    if event.mod & pygame.KMOD_SHIFT:
                        self.mmo_overlay_mode = "roster"
                        self._clear_mmo_toggles()
                    else:
                        self.mmo_show_notifications = (
                            not self.mmo_show_notifications
                        )
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_s
                ):
                    if event.mod & pygame.KMOD_SHIFT:
                        self.mmo_overlay_mode = "survey"
                        self._clear_mmo_toggles()
                    else:
                        self._mmo_cycle_sort()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_a
                    and event.mod & pygame.KMOD_SHIFT
                ):
                    self.mmo_overlay_mode = "alerts"
                    self._clear_mmo_toggles()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_z
                ):
                    self.mmo_overlay_mode = "intel"
                    self._clear_mmo_toggles()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_d
                ):
                    if event.mod & pygame.KMOD_SHIFT:
                        self.mmo_overlay_mode = "infrastructure"
                        self._clear_mmo_toggles()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_k
                ):
                    if event.mod & pygame.KMOD_SHIFT:
                        self.mmo_overlay_mode = "academy"
                        self._clear_mmo_toggles()
                    else:
                        self.mmo_overlay_mode = "market"
                        self._clear_mmo_toggles()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_a
                    and event.mod & pygame.KMOD_CTRL
                ):
                    self.mmo_overlay_mode = "account"
                    self._clear_mmo_toggles()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_l
                    and event.mod & pygame.KMOD_CTRL
                ):
                    self.mmo_overlay_mode = "account_audit"
                    self._clear_mmo_toggles()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and self.mmo_overlay_mode == "account"
                ):
                    if event.key == pygame.K_r:
                        self._mmo_account_action("register")
                    elif event.key == pygame.K_k:
                        self._mmo_account_action("renew")
                    elif event.key == pygame.K_u:
                        self._mmo_account_action("upgrade")
                    elif event.key in (pygame.K_DELETE, pygame.K_BACKSPACE):
                        self._mmo_account_action("delete")
                    elif event.key == pygame.K_PAGEUP:
                        self._mmo_cycle_account(-1)
                    elif event.key == pygame.K_PAGEDOWN:
                        self._mmo_cycle_account(1)
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and self.mmo_overlay_mode == "account_audit"
                ):
                    if event.key == pygame.K_f:
                        self._mmo_cycle_account_audit_filter()
                    elif event.key == pygame.K_u:
                        self.mmo_account_audit_upgrades_only = (
                            not self.mmo_account_audit_upgrades_only
                        )
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_q
                ):
                    self.mmo_overlay_mode = "factions"
                    self._clear_mmo_toggles()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_j
                ):
                    self.mmo_overlay_mode = "operations"
                    self._clear_mmo_toggles()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_t
                ):
                    if event.mod & pygame.KMOD_SHIFT:
                        self.mmo_overlay_mode = "timeline"
                        self._clear_mmo_toggles()
                    else:
                        self.mmo_overlay_mode = "hub_settings"
                        self._clear_mmo_toggles()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_l
                ):
                    if event.mod & pygame.KMOD_SHIFT:
                        self.mmo_overlay_mode = "logistics"
                        self._clear_mmo_toggles()
                    else:
                        self.mmo_show_quest_log = not self.mmo_show_quest_log
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_r
                ):
                    if event.mod & pygame.KMOD_SHIFT:
                        self.mmo_overlay_mode = "research"
                        self._clear_mmo_toggles()
                    else:
                        self._mmo_spawn_region()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_f
                ):
                    if event.mod & pygame.KMOD_SHIFT:
                        self.mmo_overlay_mode = "diplomacy"
                        self._clear_mmo_toggles()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_x
                ):
                    if event.mod & pygame.KMOD_SHIFT:
                        self.mmo_overlay_mode = "command"
                        self._clear_mmo_toggles()
                    else:
                        self.mmo_show_event_log = not self.mmo_show_event_log
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_1
                ):
                    self.mmo_layers["routes"] = not self.mmo_layers.get("routes", True)
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_2
                ):
                    self.mmo_layers["outposts"] = not self.mmo_layers.get("outposts", True)
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_3
                ):
                    self.mmo_layers["events"] = not self.mmo_layers.get("events", True)
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_4
                ):
                    self.mmo_layers["contracts"] = not self.mmo_layers.get("contracts", True)
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_5
                ):
                    self.mmo_layers["agents"] = not self.mmo_layers.get("agents", True)
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_6
                ):
                    self.mmo_layers["remotes"] = not self.mmo_layers.get("remotes", True)
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_7
                ):
                    self.mmo_layers["heatmap"] = not self.mmo_layers.get("heatmap", True)
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_8
                ):
                    self.mmo_layers["resources"] = not self.mmo_layers.get(     
                        "resources",
                        True,
                    )
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_9
                ):
                    self.mmo_layers["expeditions"] = not self.mmo_layers.get(
                        "expeditions",
                        True,
                    )
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_0
                ):
                    self.mmo_layers["bounties"] = not self.mmo_layers.get(
                        "bounties",
                        True,
                    )
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_F1
                ):
                    self.mmo_overlay_mode = "overview"
                    self._clear_mmo_toggles()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_F2
                ):
                    self.mmo_overlay_mode = "details"
                    self._clear_mmo_toggles()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_F3
                ):
                    self.mmo_overlay_mode = "favorites"
                    self._clear_mmo_toggles()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_F4
                ):
                    self.mmo_overlay_mode = "quests"
                    self._clear_mmo_toggles()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_F5
                ):
                    self.mmo_overlay_mode = "growth"
                    self._clear_mmo_toggles()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_F6
                ):
                    self.mmo_overlay_mode = "party"
                    self._clear_mmo_toggles()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_F7
                ):
                    self.mmo_overlay_mode = "network"
                    self._clear_mmo_toggles()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_F8
                ):
                    self.mmo_overlay_mode = "help"
                    self._clear_mmo_toggles()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_F9
                ):
                    self.mmo_overlay_mode = "notifications"
                    self._clear_mmo_toggles()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_F10
                ):
                    self.mmo_overlay_mode = "guilds"
                    self._clear_mmo_toggles()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_F11
                ):
                    self.mmo_overlay_mode = "events"
                    self._clear_mmo_toggles()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_F12
                ):
                    self.mmo_overlay_mode = "contracts"
                    self._clear_mmo_toggles()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_m
                ):
                    if event.mod & pygame.KMOD_SHIFT:
                        self.mmo_overlay_mode = "market_orders"
                        self._clear_mmo_toggles()
                    else:
                        self.mmo_show_minimap = not self.mmo_show_minimap
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_UP
                ):
                    self.mmo_action_index = max(0, self.mmo_action_index - 1)
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_DOWN
                ):
                    self.mmo_action_index = min(
                        len(self.mmo_region_actions) - 1, self.mmo_action_index + 1
                    )
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_PAGEUP
                ):
                    if self.mmo_overlay_mode == "help" or self.mmo_show_help:
                        self.mmo_help_page = max(0, self.mmo_help_page - 1)
                        continue
                    if self.mmo_overlay_mode == "contracts":
                        self.mmo_contract_index = max(
                            0,
                            self.mmo_contract_index - 1,
                        )
                    elif self.mmo_overlay_mode == "events":
                        self.mmo_event_index = max(0, self.mmo_event_index - 1) 
                    elif self.mmo_overlay_mode == "operations":
                        self.mmo_operation_index = max(
                            0,
                            self.mmo_operation_index - 1,
                        )
                    elif self.mmo_overlay_mode == "infrastructure":
                        self.mmo_infra_index = max(0, self.mmo_infra_index - 1)
                    elif self.mmo_overlay_mode == "patrols":
                        self.mmo_patrol_index = max(0, self.mmo_patrol_index - 1)
                    elif self.mmo_overlay_mode == "timeline":
                        self.mmo_timeline_index = max(0, self.mmo_timeline_index - 1)
                    elif self.mmo_overlay_mode == "survey":
                        self.mmo_survey_index = max(0, self.mmo_survey_index - 1)
                    elif self.mmo_overlay_mode == "logistics":
                        self.mmo_logistics_index = max(0, self.mmo_logistics_index - 1)
                    elif self.mmo_overlay_mode == "crafting":
                        self.mmo_crafting_index = max(0, self.mmo_crafting_index - 1)
                    elif self.mmo_overlay_mode == "market_orders":
                        self.mmo_market_index = max(0, self.mmo_market_index - 1)
                    elif self.mmo_overlay_mode == "expeditions":
                        self.mmo_expedition_index = max(
                            0, self.mmo_expedition_index - 1
                        )
                    elif self.mmo_overlay_mode == "roster":
                        self.mmo_roster_index = max(0, self.mmo_roster_index - 1)
                    elif self.mmo_overlay_mode == "alerts":
                        self.mmo_alert_index = max(0, self.mmo_alert_index - 1)
                    elif self.mmo_overlay_mode == "command":
                        self.mmo_directive_index = max(
                            0, self.mmo_directive_index - 1
                        )
                    elif self.mmo_overlay_mode == "bounties":
                        self.mmo_bounty_index = max(0, self.mmo_bounty_index - 1)
                    elif self.mmo_overlay_mode == "influence":
                        self.mmo_influence_index = max(
                            0, self.mmo_influence_index - 1
                        )
                    elif self.mmo_overlay_mode == "fleet":
                        self.mmo_fleet_index = max(0, self.mmo_fleet_index - 1)
                    elif self.mmo_overlay_mode == "projects":
                        self.mmo_project_index = max(0, self.mmo_project_index - 1)
                    elif self.mmo_overlay_mode == "academy":
                        self.mmo_training_index = max(0, self.mmo_training_index - 1)
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_PAGEDOWN
                ):
                    if self.mmo_overlay_mode == "help" or self.mmo_show_help:
                        pages = len(self._mmo_help_pages())
                        self.mmo_help_page = min(
                            pages - 1, self.mmo_help_page + 1
                        )
                        continue
                    if self.mmo_overlay_mode == "contracts":
                        max_idx = max(0, len(self.mmo_contracts) - 1)
                        self.mmo_contract_index = min(
                            max_idx,
                            self.mmo_contract_index + 1,
                        )
                    elif self.mmo_overlay_mode == "events":
                        max_idx = max(0, len(self.mmo_world_events) - 1)        
                        self.mmo_event_index = min(
                            max_idx,
                            self.mmo_event_index + 1,
                        )
                    elif self.mmo_overlay_mode == "operations":
                        max_idx = max(0, len(self.mmo_operations) - 1)
                        self.mmo_operation_index = min(
                            max_idx,
                            self.mmo_operation_index + 1,
                        )
                    elif self.mmo_overlay_mode == "infrastructure":
                        max_idx = max(0, len(self._mmo_infra_items()) - 1)
                        self.mmo_infra_index = min(max_idx, self.mmo_infra_index + 1)
                    elif self.mmo_overlay_mode == "patrols":
                        max_idx = max(0, len(self._mmo_patrol_entries()) - 1)
                        self.mmo_patrol_index = min(max_idx, self.mmo_patrol_index + 1)
                    elif self.mmo_overlay_mode == "timeline":
                        max_idx = max(
                            0,
                            len(self._mmo_timeline_items(pygame.time.get_ticks())) - 1,
                        )
                        self.mmo_timeline_index = min(
                            max_idx,
                            self.mmo_timeline_index + 1,
                        )
                    elif self.mmo_overlay_mode == "survey":
                        max_idx = max(0, len(self._mmo_survey_items()) - 1)
                        self.mmo_survey_index = min(max_idx, self.mmo_survey_index + 1)
                    elif self.mmo_overlay_mode == "logistics":
                        max_idx = max(0, len(self.mmo_stockpile) - 1)
                        self.mmo_logistics_index = min(
                            max_idx,
                            self.mmo_logistics_index + 1,
                        )
                    elif self.mmo_overlay_mode == "crafting":
                        max_idx = max(0, len(self._mmo_recipes()) - 1)
                        self.mmo_crafting_index = min(max_idx, self.mmo_crafting_index + 1)
                    elif self.mmo_overlay_mode == "market_orders":
                        max_idx = max(0, len(self.mmo_stockpile) - 1)
                        self.mmo_market_index = min(max_idx, self.mmo_market_index + 1)
                    elif self.mmo_overlay_mode == "expeditions":
                        max_idx = max(0, len(self.mmo_expeditions) - 1)
                        self.mmo_expedition_index = min(
                            max_idx,
                            self.mmo_expedition_index + 1,
                        )
                    elif self.mmo_overlay_mode == "roster":
                        max_idx = max(0, len(self._mmo_roster_entries()) - 1)
                        self.mmo_roster_index = min(
                            max_idx,
                            self.mmo_roster_index + 1,
                        )
                    elif self.mmo_overlay_mode == "alerts":
                        max_idx = max(0, len(self.mmo_alerts) - 1)
                        self.mmo_alert_index = min(
                            max_idx,
                            self.mmo_alert_index + 1,
                        )
                    elif self.mmo_overlay_mode == "command":
                        max_idx = max(0, len(self.mmo_directives) - 1)
                        self.mmo_directive_index = min(
                            max_idx,
                            self.mmo_directive_index + 1,
                        )
                    elif self.mmo_overlay_mode == "bounties":
                        max_idx = max(0, len(self.mmo_bounties) - 1)
                        self.mmo_bounty_index = min(
                            max_idx,
                            self.mmo_bounty_index + 1,
                        )
                    elif self.mmo_overlay_mode == "influence":
                        max_idx = max(0, len(self._mmo_influence_entries()) - 1)
                        self.mmo_influence_index = min(
                            max_idx,
                            self.mmo_influence_index + 1,
                        )
                    elif self.mmo_overlay_mode == "fleet":
                        max_idx = max(0, len(self.mmo_shipments) - 1)
                        self.mmo_fleet_index = min(
                            max_idx,
                            self.mmo_fleet_index + 1,
                        )
                    elif self.mmo_overlay_mode == "projects":
                        max_idx = max(0, len(self.mmo_projects) - 1)
                        self.mmo_project_index = min(
                            max_idx,
                            self.mmo_project_index + 1,
                        )
                    elif self.mmo_overlay_mode == "academy":
                        max_idx = max(0, len(self.mmo_training_queue) - 1)
                        self.mmo_training_index = min(
                            max_idx,
                            self.mmo_training_index + 1,
                        )
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER)
                ):
                    if self.mmo_overlay_mode == "details":
                        self._mmo_apply_action()
                    elif self.mmo_overlay_mode == "contracts":
                        if self.mmo_contracts:
                            idx = self.mmo_contract_index % len(self.mmo_contracts)
                            contract = self.mmo_contracts[idx]
                            if contract.get("status") == "active":
                                contract["status"] = "accepted"
                                contract["eta"] = max(
                                    1,
                                    int(contract.get("eta", 2)),
                                )
                                self._mmo_log_event(
                                    f"Accepted {contract.get('name', 'Contract')}."
                                )
                                self._mmo_record_stat("contracts_accepted")
                    elif self.mmo_overlay_mode == "events":
                        if self.mmo_world_events:
                            idx = self.mmo_event_index % len(self.mmo_world_events)
                            event = self.mmo_world_events[idx]
                            event["severity"] = "Low"
                            self._mmo_log_event(
                                f"Responded to {event.get('name', 'Event')}."
                            )
                            self._mmo_record_stat("events_responded")
                    elif self.mmo_overlay_mode == "operations":
                        if self.mmo_operations:
                            idx = self.mmo_operation_index % len(self.mmo_operations)
                            op = self.mmo_operations[idx]
                            if op.get("status") == "active":
                                op["eta"] = max(
                                    0,
                                    int(op.get("eta", 0)) - 1,
                                )
                                self._mmo_log_event(
                                    f"Boosted {op.get('name', 'Operation')}."
                                )
                    elif self.mmo_overlay_mode == "infrastructure":
                        items = self._mmo_infra_items()
                        if items:
                            idx = self.mmo_infra_index % len(items)
                            item = items[idx]
                            if item["kind"] == "outpost":
                                outpost = item["data"]
                                level = int(outpost.get("level", 1))
                                if level < 5:
                                    outpost["level"] = level + 1
                                    self.mmo_backend.upsert_outpost(outpost)
                                    self._mmo_log_event(
                                        f"Upgraded outpost at {outpost.get('region')}."
                                    )
                                else:
                                    self.mmo_message = "Outpost already maxed."
                            else:
                                route = item["data"]
                                status = route.get("status", "active")
                                route["status"] = "paused" if status == "active" else "active"
                                self._mmo_log_event(
                                    f"Route {route.get('origin')} -> {route.get('destination')}"
                                    f" set to {route.get('status')}."
                                )
                    elif self.mmo_overlay_mode == "patrols":
                        entries = self._mmo_patrol_entries()
                        if entries:
                            idx = self.mmo_patrol_index % len(entries)
                            entry = entries[idx]
                            label = entry.get("id", "patrol")
                            self.mmo_message = f"Tracking {label}."
                            self._mmo_log_event(f"Tracking {label}.")
                    elif self.mmo_overlay_mode == "timeline":
                        items = self._mmo_timeline_items(pygame.time.get_ticks())
                        if items:
                            idx = self.mmo_timeline_index % len(items)
                            item = items[idx]
                            region = str(item.get("region", ""))
                            if region:
                                self._mmo_set_waypoint_for_region(region)
                    elif self.mmo_overlay_mode == "survey":
                        items = self._mmo_survey_items()
                        if items:
                            idx = self.mmo_survey_index % len(items)
                            item = items[idx]
                            region = str(item.get("region", ""))
                            if region:
                                self._mmo_set_waypoint_for_region(region)
                    elif self.mmo_overlay_mode == "logistics":
                        stockpile = sorted(
                            self.mmo_stockpile.items(),
                            key=lambda item: item[1],
                            reverse=True,
                        )
                        if stockpile:
                            resource, _amount = stockpile[
                                self.mmo_logistics_index % len(stockpile)
                            ]
                            self.mmo_message = f"Prioritizing {resource}."
                            self._mmo_log_event(f"Prioritized {resource}.")
                            available = int(self.mmo_stockpile.get(resource, 0))
                            if available > 0:
                                amount = min(available, 5)
                                self.mmo_stockpile[resource] = available - amount
                                self._mmo_add_shipment(resource, amount)
                    elif self.mmo_overlay_mode == "crafting":
                        recipes = self._mmo_recipes()
                        if recipes:
                            idx = self.mmo_crafting_index % len(recipes)
                            self._mmo_start_craft(recipes[idx])
                    elif self.mmo_overlay_mode == "market_orders":
                        resources = list(self.mmo_stockpile.keys())
                        if event.mod & pygame.KMOD_SHIFT:
                            self._mmo_cancel_open_order()
                        elif resources:
                            idx = self.mmo_market_index % len(resources)
                            resource = resources[idx]
                            self._mmo_post_order(resource, kind="sell")
                    elif self.mmo_overlay_mode == "strategy":
                        focus = self.mmo_strategy.get("focus", "resources")
                        idx = self.mmo_strategy_options.index(focus)
                        next_focus = self.mmo_strategy_options[
                            (idx + 1) % len(self.mmo_strategy_options)
                        ]
                        self.mmo_strategy["focus"] = next_focus
                        self.mmo_message = f"Strategy focus: {next_focus.title()}."
                        self._mmo_log_event(self.mmo_message)
                    elif self.mmo_overlay_mode == "expeditions":
                        if self.mmo_expeditions:
                            idx = self.mmo_expedition_index % len(
                                self.mmo_expeditions
                            )
                            expedition = self.mmo_expeditions[idx]
                            status = expedition.get("status", "idle")
                            now = pygame.time.get_ticks()
                            if status in {"complete", "idle"}:
                                self._mmo_redeploy_expedition(expedition, now)
                            else:
                                expedition["eta"] = max(
                                    0, int(expedition.get("eta", 0)) - 1
                                )
                                self._mmo_log_event(
                                    f"Boosted {expedition.get('name', 'Expedition')}."
                                )
                    elif self.mmo_overlay_mode == "roster":
                        entries = self._mmo_roster_entries()
                        if entries:
                            idx = self.mmo_roster_index % len(entries)
                            entry = entries[idx]
                            pos = entry.get("pos")
                            if isinstance(pos, (list, tuple)) and len(pos) == 2:
                                nearest = self._mmo_nearest_region(
                                    (float(pos[0]), float(pos[1]))
                                )
                                if nearest:
                                    self._mmo_set_waypoint_for_region(
                                        str(nearest.get("name", "region"))
                                    )
                            else:
                                self.mmo_message = "Roster entry unavailable."
                    elif self.mmo_overlay_mode == "alerts":
                        if self.mmo_alerts:
                            idx = self.mmo_alert_index % len(self.mmo_alerts)
                            alert = self.mmo_alerts.pop(idx)
                            message = alert.get("text", "Alert cleared.")
                            self._mmo_log_event(f"Cleared alert: {message}")
                    elif self.mmo_overlay_mode == "command":
                        if self.mmo_directives:
                            idx = self.mmo_directive_index % len(
                                self.mmo_directives
                            )
                            directive = self.mmo_directives[idx]
                            status = directive.get("status", "open")
                            if status == "open":
                                self._mmo_assign_directive(directive)
                            elif status == "complete":
                                directive_id = directive.get("id", "Directive")
                                self.mmo_directives.pop(idx)
                                self._mmo_log_event(
                                    f"{directive_id} archived."
                                )
                    elif self.mmo_overlay_mode == "bounties":
                        if self.mmo_bounties:
                            idx = self.mmo_bounty_index % len(self.mmo_bounties)
                            bounty = self.mmo_bounties[idx]
                            status = bounty.get("status", "open")
                            if status == "open":
                                self._mmo_assign_bounty(bounty)
                            elif status == "complete":
                                bounty_id = bounty.get("id", "Bounty")
                                self.mmo_bounties.pop(idx)
                                self._mmo_log_event(
                                    f"{bounty_id} archived."
                                )
                    elif self.mmo_overlay_mode == "influence":
                        entries = self._mmo_influence_entries()
                        if entries:
                            idx = min(
                                self.mmo_influence_index, len(entries) - 1
                            )
                            region = entries[idx]
                            name = str(region.get("name", "region"))
                            cost = 25
                            if self.mmo_credits < cost:
                                self.mmo_message = "Insufficient credits."
                            else:
                                self.mmo_credits -= cost
                                self._mmo_adjust_influence(name, 5)
                                self._mmo_log_event(
                                    f"Invested in {name} (+5 influence)."
                                )
                                self._mmo_record_stat("influence_invested")
                    elif self.mmo_overlay_mode == "fleet":
                        if self.mmo_shipments:
                            idx = self.mmo_fleet_index % len(self.mmo_shipments)
                            shipment = self.mmo_shipments[idx]
                            self._mmo_toggle_shipment_escort(shipment)
                    elif self.mmo_overlay_mode == "projects":
                        if self.mmo_projects:
                            idx = self.mmo_project_index % len(self.mmo_projects)
                            project = self.mmo_projects[idx]
                            status = project.get("status", "open")
                            if status == "open":
                                self._mmo_start_project(project)
                            elif status == "complete":
                                project_id = project.get("id", "Project")
                                self.mmo_projects.pop(idx)
                                self._mmo_log_event(
                                    f"{project_id} archived."
                                )
                    elif self.mmo_overlay_mode == "academy":
                        if self.mmo_training_queue:
                            idx = self.mmo_training_index % len(
                                self.mmo_training_queue
                            )
                            training = self.mmo_training_queue[idx]
                            status = training.get("status", "open")
                            if status == "open":
                                self._mmo_start_training(training)
                            elif status == "complete":
                                training_id = training.get("id", "Training")
                                self.mmo_training_queue.pop(idx)
                                self._mmo_log_event(
                                    f"{training_id} archived."
                                )
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_b
                ):
                    if event.mod & pygame.KMOD_SHIFT:
                        self.mmo_overlay_mode = "bounties"
                        self._clear_mmo_toggles()
                    else:
                        self._mmo_toggle_favorite()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_w
                ):
                    self._mmo_set_waypoint()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_c
                ):
                    if event.mod & pygame.KMOD_SHIFT:
                        self.mmo_overlay_mode = "crafting"
                        self._clear_mmo_toggles()
                    else:
                        self._mmo_clear_waypoint()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key in (pygame.K_EQUALS, pygame.K_KP_PLUS)
                ):
                    self.mmo_zoom = min(2.0, self.mmo_zoom + 0.1)
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key in (pygame.K_MINUS, pygame.K_KP_MINUS)
                ):
                    self.mmo_zoom = max(0.5, self.mmo_zoom - 0.1)
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_LEFT
                ):
                    self.mmo_region_index = max(0, self.mmo_region_index - 1)
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_RIGHT
                ):
                    regions = self._mmo_regions()
                    if regions:
                        self.mmo_region_index = min(
                            len(regions) - 1, self.mmo_region_index + 1
                        )
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_f
                ):
                    if event.mod & pygame.KMOD_SHIFT:
                        self.mmo_overlay_mode = "diplomacy"
                        self._clear_mmo_toggles()
                    else:
                        self._mmo_focus_selected()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_r
                ):
                    if event.mod & pygame.KMOD_SHIFT:
                        self.mmo_overlay_mode = "research"
                        self._clear_mmo_toggles()
                    else:
                        self._mmo_spawn_region()
                elif (
                    self.state == "mmo"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_p
                ):
                    if event.mod & pygame.KMOD_SHIFT:
                        self.mmo_overlay_mode = "patrols"
                        self._clear_mmo_toggles()
                    else:
                        self._mmo_generate_plan(pygame.time.get_ticks())
                elif (
                    self.state in ("inventory", "equipment")   
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                ):
                    self._set_state("paused")
                elif (
                    self.state == "playing"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_F12
                ):
                    self.screenshot_manager.capture(self.screen)
                    continue
                elif (
                    self.state == "playing"
                    and event.type == pygame.KEYDOWN
                    and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER)
                ):
                    if self.chat_manager.open:
                        if self.chat_input.strip():
                            sender = self.player_names[0] if self.player_names else "Player"
                            self.chat_manager.send(sender, self.chat_input)
                            if self.network_manager is not None:
                                self.network_manager.send_chat(
                                    sender, self.chat_input, reliable=True
                                )
                        self.chat_input = ""
                        self.chat_manager.hide()
                    else:
                        self.chat_manager.show()
                    continue
                elif (
                    self.state == "playing"
                    and self.chat_manager.open
                    and event.type == pygame.KEYDOWN
                ):
                    if event.key == pygame.K_BACKSPACE:
                        self.chat_input = self.chat_input[:-1]
                    elif event.unicode and event.unicode.isprintable():
                        self.chat_input += event.unicode
                    continue
                elif (
                    event.type == pygame.KEYDOWN
                    and self._menu_options_for_state() is not None
                    and (
                        self.state not in {"victory", "game_over"}
                        or self.show_end_options
                    )
                ):
                    options = self._menu_options_for_state()
                    if (
                        self.state == "char"
                        and event.key == pygame.K_j
                        and self.multiplayer
                        and not self.online_multiplayer
                    ):
                        if self.human_players < 4:
                            self.human_players += 1
                            self.player_names.append(
                                f"Player {self.human_players}"
                            )
                        continue
                    if event.key == pygame.K_UP:
                        self.menu_manager.move(-1, len(options))
                        self.menu_index = self.menu_manager.index
                    elif event.key == pygame.K_DOWN:
                        self.menu_manager.move(1, len(options))
                        self.menu_index = self.menu_manager.index
                    elif (
                        self.state == "char"
                        and options[self.menu_index] == "Difficulty"
                        and event.key in (pygame.K_LEFT, pygame.K_RIGHT)
                    ):
                        if event.key == pygame.K_LEFT:
                            self.difficulty_index = (
                                self.difficulty_index - 1
                            ) % len(self.difficulty_levels)
                        else:
                            self.difficulty_index = (
                                self.difficulty_index + 1
                            ) % len(self.difficulty_levels)
                    elif (
                        self.state == "settings"
                        and options[self.menu_index] == "Volume"
                        and event.key in (pygame.K_LEFT, pygame.K_RIGHT)
                    ):
                        if event.key == pygame.K_LEFT:
                            self.volume = self.sound_manager.adjust_volume(-0.1)
                        else:
                            self.volume = self.sound_manager.adjust_volume(0.1)
                    elif event.key in (
                        pygame.K_RETURN,
                        pygame.K_KP_ENTER,
                        pygame.K_SPACE,
                    ):
                        self._handle_menu_selection(options)
                elif self.state == "rebind" and event.type == pygame.KEYDOWN:
                    self.keybind_manager.set(self.rebind_action, event.key)
                    self.input_manager.set(self.rebind_action, event.key)
                    self._set_state("key_bindings")
                elif (
                    self.state == "rebind_controller"
                    and event.type == pygame.JOYBUTTONDOWN
                ):
                    self.controller_bindings[self.rebind_action] = event.button
                    self.input_manager.set_button(
                        self.rebind_action,
                        event.button,
                    )
                    self._set_state("controller_bindings")
            now = pygame.time.get_ticks()
            if self.autoplay and self.autoplay_deadline:
                if now >= self.autoplay_deadline:
                    self.running = False
                    continue
            if self.autoplay_mining and not self.mining_enabled:
                self.mining_manager.start(self.autoplay_mining_intensity)
                self.mining_enabled = True
            self.status_manager.update(now)
            self.environment_manager.update(now)
            if (
                self.state in {"victory", "game_over"}
                and not self.show_end_options
                and now - self.end_time >= 3000
            ):
                self.show_end_options = True
            if (
                self.state == "victory"
                and self.mmo_pending
                and now - self.end_time >= 1500
            ):
                self._enter_mmo_mode()
            if self.autoplay and self.state in {"victory", "game_over"}:
                if (
                    now - self.end_time >= 500
                    and self.autoplay_level_index < self.autoplay_levels_target
                ):
                    self.autoplay_level_index += 1
                    if self.selected_mode == "Story" and self.chapters:
                        next_idx = min(
                            self.autoplay_level_index, len(self.chapters) - 1
                        )
                        self.selected_chapter = self.chapters[next_idx]
                    self._setup_level()
                    self.level_start_time = pygame.time.get_ticks()
                    self._set_state("playing")

            if self.ui_debugger is not None and self.ui_debugger.is_active:
                self.ui_debugger.begin_frame(
                    mode=self._ui_debug_mode(),
                    state_name=self.state,
                    resolution=(self.width, self.height),
                    ui_scale=float(getattr(self.ui_metrics, "ui_scale", 1.0)),
                    effective_font_scale=float(getattr(self, "effective_font_scale", 1.0)),
                    fps=float(self.clock.get_fps()),
                )
            drawer = self.menu_drawers.get(self.state)
            if drawer is not None:
                if self.state == "mmo":
                    self._update_mmo_controls()
                    self._update_mmo_agents()
                    self._update_mmo_world(now)
                    self._mmo_sync_state(now)
                    self._mmo_sync_world_state(now)
                    self._mmo_update_matchmaking(now)
                    self._autoplay_mmo(now)
                drawer()
                if self.autoplay and self.autoplay_flow:
                    self._autoplay_menu_flow(now)
            else:
                if self.autoplay and self.autoplay_flow:
                    if self._autoplay_menu_playing(now):
                        continue
                if self.autoplay and self.autoplay_agent_enabled and self.autoplayer:
                    keys, action_pressed = self.autoplayer.inputs(now)
                else:
                    keys = pygame.key.get_pressed()

                    def action_pressed(action: str) -> bool:
                        return self.input_manager.pressed(action, keys)

                self.player.handle_input(
                    keys,
                    now,
                    self.input_manager.key_bindings,
                    action_pressed,
                )
                if self.autoplay:
                    self._autoplay_generation(now)
                if action_pressed("special"):
                    proj = self.player.special_attack(now)
                    if isinstance(proj, HealingZone):
                        self.healing_zones.add(proj)      
                        self.all_sprites.add(proj)        
                    elif proj:
                        self.projectiles.add(proj)        
                        self.all_sprites.add(proj)
                    if proj:
                        self._spawn_holo_cheer(
                            "Special Stage!",
                            (self.player.rect.centerx, self.player.rect.top - 30),
                        )
                        self.holo_highlight_until = max(
                            self.holo_highlight_until, now + 300
                        )
                if action_pressed("shoot"):
                    target = pygame.mouse.get_pos()
                    if self.autoplay:
                        target = None
                    proj = self.player.shoot(now, target)
                    if proj:
                        self.projectiles.add(proj)
                        self.all_sprites.add(proj)
                if action_pressed("melee"):
                    melee = self.player.melee_attack(now)
                    if melee:
                        self.melee_attacks.add(melee)
                        self.all_sprites.add(melee)
                zone = pygame.sprite.spritecollideany(self.player, self.gravity_zones)
                if zone:
                    self.player.set_gravity_multiplier(zone.multiplier)
                else:
                    self.player.set_gravity_multiplier(1.0)
                self.hazard_manager.apply_to_player(self.player, now)
                self.platforms.update()
                if self.player.current_platform:
                    self.player.pos += self.player.current_platform.velocity    
                    self.player.rect.topleft = (
                        int(self.player.pos.x), int(self.player.pos.y)
                    )
                for enemy in self.enemies:
                    if enemy.current_platform:
                        enemy.pos += enemy.current_platform.velocity
                        enemy.rect.topleft = (
                            int(enemy.pos.x), int(enemy.pos.y)
                        )
                extra = self.player.update(self.ground_y, now)
                self._apply_pending_respawn(now)
                self._handle_fall_deaths(now)
                self.camera_manager.follow_bounds(
                    self.player.rect,
                    (self.width, self.height),
                    (self.world_width, self.world_height),
                    smoothing=0.18,
                    lock_y=True,
                )
                self.camera_manager.update()
                if isinstance(extra, pygame.sprite.Sprite):
                    self.projectiles.add(extra)
                    self.all_sprites.add(extra)
                if self.autoplay and self.autoplay_deadline:
                    if now >= self.autoplay_deadline:
                        self.running = False
                map_name = self.map_manager.current or self.selected_map
                threat_rating = None
                if map_name:
                    threat_rating = float(
                        self._map_preview_data(map_name).get("threat", 0)
                    )
                self.ai_experience_manager.update_context(
                    self.player,
                    list(self.enemies),
                    now,
                    hazards=self.hazards,
                    threat_level=threat_rating,
                )
                self._log_ai_experience()
                self._maybe_spawn_mobs(now)
                new_projs, new_melees = self.ai_manager.update(
                    self.player,
                    now,
                    self.hazards,
                    self.projectiles,
                    targets=self._ai_targets(),
                )
                for enemy, proj in new_projs:
                    self.projectiles.add(proj)
                    self.all_sprites.add(proj)
                    action = "special" if getattr(proj, "is_special", False) else "shoot"
                    self.ai_experience_manager.record_action(enemy, action)
                for enemy, melee in new_melees:
                    self.melee_attacks.add(melee)
                    self.all_sprites.add(melee)
                    self.ai_experience_manager.record_action(enemy, "melee")
                for enemy in list(self.enemies):
                    zone = pygame.sprite.spritecollideany(enemy, self.gravity_zones)
                    if zone:
                        enemy.set_gravity_multiplier(zone.multiplier)
                    else:
                        enemy.set_gravity_multiplier(1.0)
                    if self.hazard_manager.apply_to_enemy(enemy, now):
                        self.score += 1
                    enemy.update(self.ground_y, now)
                ally_projs, ally_melees, ally_zones, ally_messages = self.ally_manager.update(
                    self.player,
                    list(self.enemies),
                    self.hazards,
                    self.projectiles,
                    self.ground_y,
                    now,
                    status_manager=self.status_manager,
                )
                for ally, proj in ally_projs:
                    self.projectiles.add(proj)
                    self.all_sprites.add(proj)
                for ally, melee in ally_melees:
                    self.melee_attacks.add(melee)
                    self.all_sprites.add(melee)
                for zone in ally_zones:
                    self.healing_zones.add(zone)
                    self.all_sprites.add(zone)
                for text, pos in ally_messages:
                    self.damage_numbers.add(CheerText(text, pos))
                if self.ai_interaction_enabled:
                    callouts = self.ai_interaction_manager.update(
                        self.player,
                        list(self.enemies),
                        list(self.allies),
                        now,
                    )
                    for callout in callouts:
                        text = str(callout.get("text", ""))
                        pos = callout.get("pos", (0, 0))
                        color = callout.get("color", (255, 220, 120))
                        if text:
                            self.damage_numbers.add(
                                CheerText(text, pos, color=color)
                            )
                self.projectiles.update()
                self.melee_attacks.update()
                self.healing_zones.update()
                self.damage_numbers.update(now)
                self.score_manager.update(now / 1000.0)
                if self.score_manager.combo == 0:
                    self.combo_cheer_level = 0
                self._handle_collisions()
                if self.holo_hype_active and now >= self.holo_hype_until:
                    self._end_holo_hype()
                self.powerups.update()
                for item in self.spawn_manager.get_ready(now):
                    center_x = self.world_width // 2
                    if item == "heal":
                        x = center_x
                        p = PowerUp(x, self.ground_y - 20, "heal")
                        self.powerups.add(p)
                        self.all_sprites.add(p)
                        self.spawn_manager.schedule("heal", now + 5000)
                    elif item == "mana":
                        x = center_x - 80
                        p = PowerUp(x, self.ground_y - 20, "mana")
                        self.powerups.add(p)
                        self.all_sprites.add(p)
                        self.spawn_manager.schedule("mana", now + 6000)
                    elif item == "speed":
                        x = center_x + 40
                        p = PowerUp(x, self.ground_y - 20, "speed")
                        self.powerups.add(p)
                        self.all_sprites.add(p)
                        self.spawn_manager.schedule("speed", now + 7000)
                    elif item == "stamina":
                        x = center_x + 120
                        p = PowerUp(x, self.ground_y - 20, "stamina")
                        self.powerups.add(p)
                        self.all_sprites.add(p)
                        self.spawn_manager.schedule("stamina", now + 8000)
                    elif item == "shield":
                        x = center_x - 40
                        p = PowerUp(x, self.ground_y - 20, "shield")
                        self.powerups.add(p)
                        self.all_sprites.add(p)
                        self.spawn_manager.schedule("shield", now + 9000)
                    elif item == "life":
                        x = center_x + 80
                        p = PowerUp(x, self.ground_y - 20, "life")
                        self.powerups.add(p)
                        self.all_sprites.add(p)
                        self.spawn_manager.schedule("life", now + 11000)
                    elif item == "attack":
                        x = center_x - 160
                        p = PowerUp(x, self.ground_y - 20, "attack")
                        self.powerups.add(p)
                        self.all_sprites.add(p)
                        self.spawn_manager.schedule("attack", now + 10000)
                    elif item == "defense":
                        x = center_x + 160
                        p = PowerUp(x, self.ground_y - 20, "defense")
                        self.powerups.add(p)
                        self.all_sprites.add(p)
                        self.spawn_manager.schedule("defense", now + 10500)
                    elif item == "xp":
                        x = center_x - 200
                        p = PowerUp(x, self.ground_y - 20, "xp")
                        self.powerups.add(p)
                        self.all_sprites.add(p)
                        self.spawn_manager.schedule("xp", now + 11500)
                for zone in self.healing_zones:
                    if zone.rect.colliderect(self.player.rect):
                        hp_before = float(getattr(self.player, "health", 0))
                        self.player.health = min(
                            self.player.max_health,
                            self.player.health + zone.heal_rate,
                        )
                        self.emit_event(
                            {
                                "type": "heal",
                                "source": "zone:healing",
                                "target_id": self._event_target_id(self.player),
                                "amount": max(0.0, float(self.player.health) - hp_before),
                                "hp_before": hp_before,
                                "hp_after": float(getattr(self.player, "health", 0)),
                            }
                        )
                self._handle_powerup_collision()
                self._autoplay_update_learning(now)
                self._autoplay_audit_character_actions(now)
                self._autoplay_monitor(now)
                for proj in list(self.projectiles):
                    if proj.rect.right < 0 or proj.rect.left > self.world_width:
                        proj.kill()
                if self.player.lives == 0:
                    self.final_time = (now - self.level_start_time) // 1000
                    if self.final_time > self.best_time:
                        self.best_time = self.final_time
                    self.score_manager.finalize()
                    self._autoplay_log(
                        "Match end game_over "
                        f"time={self.final_time}s score={self.score_manager.score}"
                    )
                    self._autoplay_dump_skill_audit_report(now=now)
                    self.auto_dev_manager.finalize(
                        "game_over",
                        self.score_manager.score,
                        self.final_time,
                        self.account_id,
                    )
                    self.iteration_manager.save(
                        {
                            "result": "game_over",
                            "time": self.final_time,
                            "score": self.score_manager.score,
                            "character": self.selected_character,
                            "map": self.selected_map,
                            "account": self.account_id,
                        }
                    )
                    self._bump_ai_progression()
                    self.game_over_flash_until = now + 1800
                    self._set_state("game_over")
                    self.end_time = now
                    self.show_end_options = False
                    self.menu_index = 0
                    continue
                boss_present = any(
                    isinstance(enemy, BossEnemy) for enemy in self.enemies 
                )
                if boss_present and not self.boss_present_last:
                    self.boss_banner_until = now + 2500
                    self._spawn_holo_cheer(
                        "Boss Encore!",
                        (self.width // 2, int(self.height * 0.18)),
                    )
                    self.holo_highlight_until = now + 600
                    self.holo_spotlight_swap_until = now + 1500
                self.boss_present_last = boss_present
                self.screen.blit(self._get_arena_backdrop(), (0, 0))
                haze_alpha = int(
                    18 + 18 * (math.sin(now / 1200) + 1) * 0.5
                )
                haze = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
                haze.fill((18, 30, 48, haze_alpha))
                self.screen.blit(haze, (0, 0))
                self._draw_stage_lights(now)
                self._draw_stage_ribbons(now)
                self._draw_arena_corner_badge(now)
                ground = self._get_ground_surface(self.world_width)
                ground_rect = pygame.Rect(
                    0, self.ground_y, ground.get_width(), ground.get_height()
                )
                self.screen.blit(ground, self.camera_manager.apply(ground_rect))
                self._draw_stage_barriers()
                self._draw_world_sprites(self.all_sprites)
                self._draw_holo_spotlight(now)
                self._draw_holo_sparkles(now)
                self._draw_holo_confetti(now)
                self._draw_fan_glow(now)
                self._draw_holo_highlight(now)
                self._draw_arena_intro(now)
                self._draw_fan_sign_wave(now)
                self._draw_audience_wave(now)
                for enemy in self.enemies:
                    enemy.draw_health_bar(self.screen, self.camera_manager)
                self._draw_revive_glow(now)
                self._draw_world_sprites(self.damage_numbers)
                overlay_rgba = self.environment_manager.ambient_overlay()
                if overlay_rgba[3] > 0:
                    ambient = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
                    ambient.fill(overlay_rgba)
                    self.screen.blit(ambient, (0, 0))
                health_ratio = self.player.health / max(1, self.player.max_health)
                if health_ratio <= 0.25:
                    pulse = (math.sin(now / 180) + 1) * 0.5
                    intensity = (0.25 - health_ratio) / 0.25
                    alpha = int(60 + 140 * intensity * (0.6 + 0.4 * pulse))
                    vignette = pygame.Surface(
                        self.screen.get_size(), pygame.SRCALPHA
                    )
                    vignette.fill((120, 20, 20, alpha))
                    self.screen.blit(vignette, (0, 0))
                elapsed = (now - self.level_start_time) // 1000
                objective_lines = self.objective_manager.summary()
                resource_summary = self._hud_resource_summary()
                status_effects = self._hud_status_effects(now)
                insights = self._hud_insights()
                auto_dev_summary = self._hud_auto_dev_summary()
                world_activity = self._hud_world_activity()
                minimap = self._hud_minimap_data()
                hype_meter = min(1.0, self.score_manager.combo / 12)
                hype_label = "Holo Hype" if self.holo_hype_active else "Crowd"  
                map_name = self.map_manager.current or self.selected_map
                threat_rating = None
                if map_name:
                    threat_rating = float(
                        self._map_preview_data(map_name).get("threat", 0)
                    )
                self.hud_manager.draw(
                    self.screen,
                    self.player,
                    self.score,
                    elapsed,
                    self.score_manager.combo,
                    allies=list(self.allies),
                    objectives=objective_lines,
                    resource_summary=resource_summary,
                    status_effects=status_effects,
                    insights=insights,
                    auto_dev_summary=auto_dev_summary,
                    world_activity=world_activity,
                    minimap=minimap,
                    hype_meter=hype_meter,
                    hype_label=hype_label,
                    threat_rating=threat_rating,
                    threat_label=map_name,
                    sfx_debug=(
                        self.sound_manager.last_played
                        if self.debug_sfx
                        else None
                    ),
                    sfx_profile=(
                        self.sound_manager.profile
                        if self.debug_sfx
                        else None
                    ),
                    impact_scale=(
                        float(getattr(self.player, "last_hit_difficulty_scale", 1.0))
                        if self.debug_sfx
                        else None
                    ),
                )
                self._draw_holo_hype_banner(now)
                if self.chat_manager.open:
                    chat_rect = pygame.Rect(10, self.height - 40, 300, 30)
                    pygame.draw.rect(self.screen, (50, 50, 50), chat_rect)
                    txt = self.menu_font.render(self.chat_input, True, (255, 255, 255))
                    self.screen.blit(txt, (chat_rect.x + 5, chat_rect.y + 5))
                if self.boss_banner_until > now:
                    banner = pygame.Surface((self.width, 70), pygame.SRCALPHA)
                    banner.fill((90, 25, 25, 180))
                    title = self.title_font.render(
                        "Boss Incoming!", True, (255, 230, 200)
                    )
                    banner.blit(
                        title,
                        title.get_rect(center=(self.width // 2, 35)),
                    )
                    self.screen.blit(banner, (0, 20))
                if elapsed >= self.level_limit or len(self.enemies) == 0:
                    self.final_time = elapsed
                    if self.final_time > self.best_time:
                        self.best_time = self.final_time
                    self.score_manager.finalize()
                    self._autoplay_log(
                        "Match end victory "
                        f"time={self.final_time}s score={self.score_manager.score}"
                    )
                    self._autoplay_dump_skill_audit_report(now=now)
                    self.auto_dev_manager.finalize(
                        "victory",
                        self.score_manager.score,
                        self.final_time,
                        self.account_id,
                    )
                    self.iteration_manager.save(
                        {
                            "result": "victory",
                            "time": self.final_time,
                            "score": self.score_manager.score,
                            "character": self.selected_character,
                            "map": self.selected_map,
                            "account": self.account_id,
                        }
                    )
                    victory_rewards = self.objective_manager.record_event(
                        "match_victory"
                    )
                    if victory_rewards:
                        self._apply_objective_rewards(victory_rewards)
                    self._bump_ai_progression()
                    self.arena_wins += 1
                    final_chapter = self.chapters[-1] if self.chapters else None
                    self.last_victory_final = bool(
                        self.selected_mode == "Story"
                        and self.selected_chapter == final_chapter
                    )
                    if self.last_victory_final:
                        self._unlock_mmo()
                        self.mmo_pending = True
                    self._build_post_victory_report(now)
                    self.victory_action_message = self._mmo_extend_pipeline(
                        now, source="Arena"
                    )
                    self.victory_flash_until = now + 1800
                    self._set_state("victory")
                    self.end_time = now
                    self.show_end_options = False
                    self.menu_index = 0
                    continue

            if self.autoplay_trace_overlay:
                self._draw_autoplay_trace()
            if self.ui_debugger is not None and self.ui_debugger.is_active:
                self.ui_debugger.render_overlay(
                    self.screen,
                    getattr(self, "ui_metrics", None),
                    float(self.clock.get_fps()),
                    self.state,
                )
                self.ui_debugger.flush_frame(frame_index)
            self._poll_network()

            pygame.display.flip()
            self.clock.tick(60)
            frame_index += 1
        if self.ui_debugger is not None and self.ui_debugger.log_enabled:
            summary_path = self.ui_debugger.finalize_run()
            self.ui_debug_summary_path = str(summary_path) if summary_path else None
        player = getattr(self, "player", None)
        coins = self.coins
        inventory: dict[str, int] | None = None
        if player is not None:
            coins = player.currency_manager.get_balance()
            inventory = player.inventory.to_dict()
        self._save_profile_checkpoint()
        mmo_position = self.world_player_manager.get_position(self.mmo_player_id)
        save_settings(
            {
                "width": self.width,
                "height": self.height,
                "volume": self.volume,
                "sfx_profile": self.sfx_profile,
                "debug_sfx": self.debug_sfx,
                "best_time": self.best_time,
                "best_score": self.best_score,
                "coins": coins,
                "show_fps": self.show_fps,
                "hud_font_size": self.hud_font_size,
                "accessibility": dict(self.accessibility_manager.options),
                "key_bindings": self.keybind_manager.to_dict(),
                "controller_bindings": self.controller_bindings,
                "mining": self.mining_enabled,
                "achievements": list(self.achievement_manager.unlocked),
                "input_method": self.input_method,
                "account_id": self.account_id,
                "fullscreen": self.fullscreen,
                "display_mode": self.display_mode,
                "mmo_unlocked": self.mmo_unlocked,
                "mmo_position": list(mmo_position),
                "mmo_zoom": self.mmo_zoom,
                "mmo_favorites": sorted(self.mmo_favorites),
                "mmo_show_panel": self.mmo_ui_show_panel,
                "mmo_show_minimap": self.mmo_show_minimap,
                "mmo_show_event_log": self.mmo_show_event_log,
                "arena_wins": self.arena_wins,
                "account_log": self.mmo_account_log,
                "match_lives": self.match_lives,
                "match_allies": self.match_allies,
                "match_mobs": self.match_mobs,
                "match_mob_interval": self.match_mob_interval,
                "match_mob_wave": self.match_mob_wave,
                "match_mob_max": self.match_mob_max,
                "mmo_outposts": self.mmo_outposts,
                "mmo_trade_routes": self.mmo_trade_routes,
                "mmo_operations": self.mmo_operations,
                "mmo_world_events": self.mmo_world_events,
                "mmo_world_tombstones": self.mmo_world_tombstones,
                "mmo_contracts": self.mmo_contracts,
                "mmo_sort_mode": self.mmo_sort_mode,
                "mmo_layers": self.mmo_layers,
                "mmo_stockpile": self.mmo_stockpile,
                "mmo_shipments": self.mmo_shipments,
                "mmo_credits": self.mmo_credits,
                "mmo_market_orders": self.mmo_market_orders,
                "mmo_crafting_queue": self.mmo_crafting_queue,
                "mmo_strategy": self.mmo_strategy,
                "mmo_stats": self.mmo_stats,
                "mmo_campaign_status": self.mmo_campaign_status,
                "mmo_expeditions": self.mmo_expeditions,
                "mmo_alerts": self.mmo_alerts,
                "mmo_directives": self.mmo_directives,
                "mmo_bounties": self.mmo_bounties,
                "mmo_influence": self.mmo_influence,
                "mmo_projects": self.mmo_projects,
                "mmo_training_queue": self.mmo_training_queue,
                "mmo_threat_history": self.mmo_threat_history,
                "mmo_threat_history_window": self.mmo_threat_history_window,
                "mmo_seen_tour": self.mmo_seen_tour,
                "mmo_shard": self.mmo_shard_id,
                "ai_progression": self.ai_progression,
                "autoplay_tuning": (
                    self.autoplayer.tuning_snapshot()
                    if self.autoplayer
                    else self.autoplay_tuning
                ),
                "reputation": self.reputation_manager.to_dict(),
                "objectives": self.objective_manager.to_dict(),
            }
        )
        if inventory is not None:
            save_inventory(inventory)
        if self.mining_enabled:
            self.mining_manager.stop()
        self.mmo_backend.close()
        pygame.quit()

    def _hud_resource_summary(self) -> list[tuple[str, object]]:
        """Return ordered resource data for the HUD side panel."""

        player = getattr(self, "player", None)
        if player is None:
            return []
        summary: list[tuple[str, object]] = []
        summary.append(("Coins", player.currency_manager.get_balance()))
        total_items = player.inventory.total_items()
        capacity = player.inventory.capacity
        inventory_line: str
        if capacity is None:
            inventory_line = str(total_items)
        else:
            inventory_line = f"{total_items}/{capacity}"
        summary.append(("Inventory", inventory_line))
        summary.append(("Level", player.experience_manager.level))
        summary.append(("XP", player.experience_manager.xp))
        if hasattr(player, "stats"):
            attack = player.stats.get("attack")
            defense = player.stats.get("defense")
            summary.append(("ATK", attack))
            summary.append(("DEF", defense))
        return summary

    def _hud_status_effects(self, now: int) -> list[dict[str, object]]:
        """Return status effects affecting the player for HUD rendering."""

        player = getattr(self, "player", None)
        if player is None:
            return []
        return self.status_manager.active_effects(player, now)

    def _hud_insights(self) -> list[str]:
        """Summarise difficulty, modifiers and support plans for the HUD."""

        lines: list[str] = []
        if self.difficulty_levels:
            difficulty = self.difficulty_levels[self.difficulty_index]
            lines.append(f"Difficulty: {difficulty}")
        active_mods: list[str] = []
        for key, value in self.match_modifiers.items():
            if not value:
                continue
            label = key.replace("_", " ").title()
            if isinstance(value, bool):
                active_mods.append(label)
            else:
                active_mods.append(f"{label}: {value}")
        if active_mods:
            lines.append("Modifiers: " + ", ".join(active_mods[:2]))
        support_plan = self.auto_dev_support_plan or {}
        hazard = support_plan.get("hazard")
        if hazard:
            lines.append(f"Support: {hazard}")
        projection = self.auto_dev_projection_summary or {}
        focus = projection.get("focus") or []
        if focus:
            focus_hazard = focus[0].get("hazard")
            if focus_hazard:
                lines.append(f"Focus Hazard: {focus_hazard}")
        network_line = self._hud_network_line()
        if network_line:
            lines.append(network_line)
        return lines[:4]

    def _hud_network_line(self) -> str | None:
        """Describe the current networking state for HUD insights."""

        if self.network_manager is None:
            return None
        manager = self.network_manager
        if getattr(manager, "host", False):
            client_count = len(getattr(manager, "clients", []))
            return f"Hosting: {client_count} clients"
        peer_count = len(getattr(manager, "peers", []))
        if peer_count:
            return f"Peers: {peer_count}"
        return "Online"

    def _hud_auto_dev_summary(self) -> list[tuple[str, object]]:
        """Return condensed auto-dev telemetry for the HUD panel."""

        manager = getattr(self, "auto_dev_manager", None)
        if manager is None:
            return []
        summary: list[tuple[str, object]] = []
        try:
            feedback = manager.region_insight()
        except Exception:  # pragma: no cover - defensive safety
            feedback = {}
        if isinstance(feedback, dict):
            hazard = feedback.get("trending_hazard")
            if hazard:
                summary.append(("Trend", hazard))
            favorite = feedback.get("favorite_character")
            if favorite:
                summary.append(("Favorite", favorite))
            avg_score = feedback.get("average_score")
            if isinstance(avg_score, (int, float)) and avg_score > 0:
                summary.append(("Avg Score", round(avg_score)))
            avg_time = feedback.get("average_time")
            if isinstance(avg_time, (int, float)) and avg_time > 0:
                summary.append(("Avg Time", f"{int(round(avg_time))}s"))
            challenge = feedback.get("hazard_challenge")
            if isinstance(challenge, dict):
                hazard_name = challenge.get("hazard")
                target = challenge.get("target")
                if hazard_name:
                    label = str(hazard_name)
                    if isinstance(target, (int, float)) and target:
                        label = f"{label} x{int(target)}"
                    summary.append(("Challenge", label))
        base_level = 1
        player = getattr(self, "player", None)
        if player is not None and hasattr(player, "experience_manager"):
            base_level = int(getattr(player.experience_manager, "level", 1)) or 1
        try:
            recommended = manager.estimate_recommended_level(base_level)
        except Exception:  # pragma: no cover - defensive safety
            recommended = None
        if isinstance(recommended, (int, float)) and recommended > 0:
            summary.append(("Rec Lv", int(recommended)))
        support_hazard = (self.auto_dev_support_plan or {}).get("hazard")
        if support_hazard:
            summary.append(("Support", support_hazard))
        focus = (self.auto_dev_projection_summary or {}).get("focus") or []     
        for entry in focus:
            if not isinstance(entry, dict):
                continue
            hazard = entry.get("hazard") or entry.get("track")
            if hazard:
                summary.append(("Focus", hazard))
                break
        return summary[:8]

    def _hud_minimap_data(self) -> dict[str, object] | None:
        """Return normalized points for the arena minimap."""
        if not getattr(self, "player", None):
            return None
        points_x: list[float] = []
        points_y: list[float] = []
        for platform in getattr(self, "platforms", []):
            rect = getattr(platform, "rect", None)
            if rect is None:
                continue
            points_x.extend([rect.left, rect.right])
            points_y.extend([rect.top, rect.bottom])
        player_pos = (self.player.rect.centerx, self.player.rect.centery)
        points_x.append(player_pos[0])
        points_y.append(player_pos[1])
        enemies = []
        for enemy in self.enemies:
            pos = (enemy.rect.centerx, enemy.rect.centery)
            enemies.append(
                {"pos": pos, "boss": bool(getattr(enemy, "is_boss", False))}
            )
            points_x.append(pos[0])
            points_y.append(pos[1])
        allies = []
        for ally in self.allies:
            pos = (ally.rect.centerx, ally.rect.centery)
            allies.append({"pos": pos})
            points_x.append(pos[0])
            points_y.append(pos[1])
        if not points_x or not points_y:
            return None
        min_x = min(points_x)
        max_x = max(points_x)
        min_y = min(points_y + [0])
        max_y = max(points_y + [self.ground_y])
        if min_x == max_x:
            max_x += 1
        if min_y == max_y:
            max_y += 1
        return {
            "bounds": (min_x, max_x, min_y, max_y),
            "player": player_pos,
            "enemies": enemies,
            "allies": allies,
        }

    def _hud_world_activity(self) -> list[str]:
        """Return world-generation updates for the HUD ticker."""

        manager = getattr(self, "world_generation_manager", None)
        region_manager = getattr(manager, "region_manager", None) if manager else None
        if region_manager is None:
            return []
        try:
            regions = region_manager.get_regions()
        except Exception:  # pragma: no cover - defensive safety
            return []
        if not regions:
            return []
        lines: list[str] = [f"Regions: {len(regions)}"]
        latest = regions[-1] or {}
        name = latest.get("name")
        if name:
            lines.append(f"Latest: {name}")
        recommended = latest.get("recommended_level")
        if isinstance(recommended, (int, float)) and recommended > 0:
            lines.append(f"Req Lv: {int(recommended)}")
        quest_info = latest.get("quest")
        quest_text: str | None = None
        if isinstance(quest_info, dict):
            quest_text = (
                str(
                    quest_info.get("name")
                    or quest_info.get("title")
                    or quest_info.get("objective")
                    or quest_info.get("description")
                    or ""
                ).strip()
            )
        elif isinstance(quest_info, str):
            quest_text = quest_info.strip()
        auto_dev = latest.get("auto_dev")
        support_hazard = None
        backlog_count = 0
        if isinstance(auto_dev, dict):
            support_plan = auto_dev.get("support_plan")
            if isinstance(support_plan, dict):
                support_hazard = support_plan.get("hazard")
            backlog = auto_dev.get("network_upgrade_backlog")
            if isinstance(backlog, dict):
                backlog_count = len(backlog)
            elif isinstance(backlog, (list, tuple, set)):
                backlog_count = len(backlog)
            elif backlog:
                backlog_count = 1
        if backlog_count:
            lines.append(f"Upgrades: {backlog_count}")
        if quest_text:
            lines.append(f"Quest: {quest_text[:32]}")
        if support_hazard:
            lines.append(f"Support: {support_hazard}")
        return lines[:5]


def main():
    """Entry point for running the game via `python -m hololive_coliseum`."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
