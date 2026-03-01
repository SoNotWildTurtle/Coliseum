"""Player character implementations with movement and combat helpers."""

from __future__ import annotations
import os
import random
import pygame
from . import physics
from .skill_manager import SkillManager
from .platform import Platform, CrumblingPlatform
from .health_manager import HealthManager
from .mana_manager import ManaManager
from .stamina_manager import StaminaManager
from .equipment_manager import EquipmentManager
from .inventory_manager import InventoryManager
from .currency_manager import CurrencyManager
from .stats_manager import StatsManager
from .experience_manager import ExperienceManager
JUMP_VELOCITY = -10
MAX_JUMPS = 2
MOVE_SPEED = physics.MAX_MOVE_SPEED
PROJECTILE_COOLDOWN = 250  # milliseconds
MELEE_COOLDOWN = 500  # milliseconds
PARRY_COOLDOWN = 1000  # milliseconds
PARRY_DURATION = 200  # milliseconds
SPECIAL_COOLDOWN = 1000  # milliseconds
DODGE_COOLDOWN = 800  # milliseconds
DODGE_DURATION = 200  # milliseconds
DODGE_SPEED = 8
STAMINA_COST_DODGE = 20
STAMINA_COST_ATTACK = 10
STAMINA_COST_BLOCK = 2
SPRINT_MULTIPLIER = 1.5
STAMINA_COST_SPRINT = 5
VFX_DIR = os.path.join(os.path.dirname(__file__), "..", "Images", "vfx")
_VFX_CACHE: dict[tuple[str, tuple[int, int]], pygame.Surface] = {}
_VFX_FRAME_CACHE: dict[tuple[str, tuple[int, int], int], list[pygame.Surface]] = (
    {}
)
MELEE_VFX_PALETTES = {
    "gura": (0, 235, 235),
    "watson": (120, 200, 255),
    "ina": (150, 90, 210),
    "kiara": (255, 140, 60),
    "calliope": (200, 200, 220),
    "fauna": (140, 255, 190),
    "kronii": (170, 200, 255),
    "irys": (210, 170, 255),
    "mumei": (180, 180, 240),
    "baelz": (255, 160, 210),
    "fubuki": (200, 240, 255),
    "matsuri": (255, 210, 120),
    "miko": (255, 90, 120),
    "aqua": (80, 150, 255),
    "pekora": (250, 150, 70),
    "marine": (210, 120, 160),
    "suisei": (120, 210, 255),
    "ayame": (200, 90, 90),
    "noel": (190, 190, 210),
    "flare": (255, 140, 60),
    "subaru": (255, 230, 120),
    "sora": (160, 210, 255),
    "enemy": (255, 170, 120),
}


def _load_vfx_surface(
    name: str,
    size: tuple[int, int],
    draw_fn,
) -> pygame.Surface:
    key = (name, size)
    cached = _VFX_CACHE.get(key)
    if cached is None:
        path = os.path.join(VFX_DIR, f"{name}.png")
        if os.path.exists(path):
            surf = pygame.image.load(path).convert_alpha()
            if surf.get_size() != size:
                surf = pygame.transform.smoothscale(surf, size)
        else:
            surf = pygame.Surface(size, pygame.SRCALPHA)
            draw_fn(surf)
        _VFX_CACHE[key] = surf
    return _VFX_CACHE[key].copy()


def _load_vfx_frames(
    name: str,
    size: tuple[int, int],
    draw_fn,
    frame_count: int = 6,
) -> list[pygame.Surface]:
    key = (name, size, frame_count)
    cached = _VFX_FRAME_CACHE.get(key)
    if cached is None:
        frames: list[pygame.Surface] = []
        for idx in range(frame_count):
            path = os.path.join(VFX_DIR, f"{name}_{idx}.png")
            if not os.path.exists(path):
                frames = []
                break
            surf = pygame.image.load(path).convert_alpha()
            if surf.get_size() != size:
                surf = pygame.transform.smoothscale(surf, size)
            frames.append(surf)
        if not frames:
            frames = [_load_vfx_surface(name, size, draw_fn)]
        _VFX_FRAME_CACHE[key] = frames
    return [frame.copy() for frame in _VFX_FRAME_CACHE[key]]


def _load_vfx_frameset(
    name: str,
    size: tuple[int, int],
    draw_fn,
    frame_count: int = 6,
) -> tuple[pygame.Surface, list[pygame.Surface]]:
    frames = _load_vfx_frames(name, size, draw_fn, frame_count=frame_count)
    return frames[0], frames


def _apply_vfx_sequence(
    sprite: pygame.sprite.Sprite,
    name: str,
    size: tuple[int, int],
    draw_fn,
    *,
    center: tuple[int, int] | None = None,
    frame_ms: int = 90,
    frame_count: int = 6,
) -> None:
    image, frames = _load_vfx_frameset(name, size, draw_fn, frame_count=frame_count)
    sprite.image = image
    if center is not None:
        sprite.rect = sprite.image.get_rect(center=center)
    if len(frames) > 1 and hasattr(sprite, "set_frame_animation"):
        sprite.set_frame_animation(frames, frame_ms=frame_ms)


class PlayerCharacter(pygame.sprite.Sprite):
    """Base controllable character sprite.

    Provides movement, combat mechanics and resource tracking. Subclasses
    override :py:meth:`special_attack` to implement unique abilities.
    """

    def __init__(
        self, x: int, y: int, image_path: str | None = None, color=(255, 255, 255)
    ) -> None:
        super().__init__()
        if image_path:
            if os.path.exists(image_path):
                self.image = pygame.image.load(image_path).convert_alpha()
            else:
                self.image = pygame.Surface((64, 64))
                self.image.fill(color)
        else:
            self.image = pygame.Surface((40, 60))
            self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.max_jumps = MAX_JUMPS
        self.jump_count = 0
        self.direction = 1  # 1 for right, -1 for left
        self.last_shot = -PROJECTILE_COOLDOWN
        self.last_melee = -MELEE_COOLDOWN
        self.last_parry = -PARRY_COOLDOWN
        self.parrying = False
        self.last_dodge = -DODGE_COOLDOWN
        self.dodging = False
        self.dodge_end = 0
        self.skill_manager = SkillManager()
        self.gravity_multiplier = 1.0
        self.friction_multiplier = 1.0
        self.speed_factor = 1.0
        self.stats = StatsManager({"attack": 10, "defense": 5, "max_health": 100})
        self.max_health = self.stats.get("max_health")
        self.health_manager = HealthManager(self.max_health)
        self.health = self.health_manager.health
        self.max_mana = 100
        self.mana_manager = ManaManager(self.max_mana)
        self.mana = self.mana_manager.mana
        self.max_stamina = 100
        self.stamina_manager = StaminaManager(self.max_stamina)
        self.stamina = self.stamina_manager.stamina
        self.equipment = EquipmentManager()
        # Limit capacity to encourage inventory upgrades in later MMO modes.
        self.inventory = InventoryManager(capacity=30)
        self.currency_manager = CurrencyManager()
        self.experience_manager = ExperienceManager(growth=1.12, max_threshold=1200)
        self.invincible = False
        self.invincible_until = 0
        self.revive_until = 0
        self.revive_flash_until = 0
        self.pending_respawn = False
        self.stunned = False
        self.silenced = False
        self.hitstop_until = 0
        self.last_hit_critical = False
        self.stagger_until = 0
        self.sound_manager = None
        self.special_sfx_event = "special_cast"
        self.melee_sfx_event = "melee_swing"
        self.last_hit_difficulty_scale = 1.0
        self.weapon_sfx_event = None
        self.melee_vfx_style = "slash_arc"
        self.melee_vfx_color = (255, 220, 120)
        # Platforms the character can stand on
        self.platforms: pygame.sprite.Group = pygame.sprite.Group()
        self.current_platform: Platform | None = None
        self.blocking = False
        self.lives = 3
        self.last_hit_time = -1000
        self.spawn_point = pygame.math.Vector2(x, y)
        self.ground_gaps: list[tuple[int, int]] = []
        self.skill_manager.register("special", SPECIAL_COOLDOWN, self._special_impl)

    def handle_input(
        self,
        keys,
        now: int | None = None,
        key_bindings: dict[str, int] | None = None,
        action_pressed=None,
    ) -> None:
        if now is None:
            now = pygame.time.get_ticks()
        if key_bindings is None:
            key_bindings = {
                "block": pygame.K_LSHIFT,
                "parry": pygame.K_c,
                "jump": pygame.K_SPACE,
            }
        if action_pressed is None:
            action_pressed = lambda act: keys[key_bindings.get(act, 0)]
        if getattr(self, "stunned", False):
            return
        if now < getattr(self, "stagger_until", 0):
            return
        speed = self.speed_factor
        if action_pressed("sprint") and self.stamina > 0:
            if self.use_stamina(STAMINA_COST_SPRINT):
                speed *= SPRINT_MULTIPLIER
        if self.dodging:
            pass
        else:
            if keys[pygame.K_LEFT]:
                self.velocity.x = physics.accelerate(self.velocity.x, -1) * speed
                self.direction = -1
            elif keys[pygame.K_RIGHT]:
                self.velocity.x = physics.accelerate(self.velocity.x, 1) * speed
                self.direction = 1
            else:
                self.velocity.x = (
                    physics.apply_friction(
                        self.velocity.x, self.on_ground, self.friction_multiplier
                    )
                    * speed
                )

        self.blocking = action_pressed("block") and self.stamina > 0
        if action_pressed("parry"):
            self.parry(now)
        if action_pressed("dodge"):
            direction = (
                -1
                if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]
                else 1
                if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]
                else self.direction
            )
            self.dodge(now, direction)
        if action_pressed("jump"):
            if self.on_ground:
                self.velocity.y = JUMP_VELOCITY
                self.on_ground = False
                self.jump_count = 1
            elif self.jump_count < self.max_jumps:
                self.velocity.y = JUMP_VELOCITY
                self.jump_count += 1
        if action_pressed("use_item"):
            self.use_item("potion")
        if action_pressed("use_mana"):
            self.use_item("mana_potion")

    def shoot(self, now: int, target: tuple[int, int] | None = None):
        """Return a projectile if the cooldown has elapsed."""
        from .projectile import Projectile

        if (
            now - self.last_shot >= PROJECTILE_COOLDOWN
            and self.use_mana(10)
            and self.use_stamina(STAMINA_COST_ATTACK)
        ):
            self.last_shot = now
            x = self.rect.centerx
            y = self.rect.centery
            if target:
                direction = pygame.math.Vector2(target[0] - x, target[1] - y)
            else:
                direction = pygame.math.Vector2(self.direction, 0)
            proj = Projectile(x, y, direction, owner=self)
            proj.attack = self.stats.get("attack")
            proj.crit_chance = self.stats.get("crit_chance")
            proj.crit_multiplier = self.stats.get("crit_multiplier")
            proj.knockback = 1.1
            return proj
        return None

    def melee_attack(self, now: int):
        """Return a melee attack sprite if cooldown allows."""
        from .melee_attack import MeleeAttack

        if now - self.last_melee >= MELEE_COOLDOWN and self.use_stamina(
            STAMINA_COST_ATTACK
        ):
            self.last_melee = now
            x = self.rect.centerx + self.direction * 20
            y = self.rect.centery
            attack = MeleeAttack(x, y, self.direction, owner=self)
            attack.attack = self.stats.get("attack") + 5
            attack.crit_chance = self.stats.get("crit_chance")
            attack.crit_multiplier = self.stats.get("crit_multiplier")
            attack.knockback = 2.8
            attack.vfx_style = self._melee_vfx_style()
            attack.vfx_color = self.melee_vfx_color
            attack.vfx_intensity = self._vfx_scale_for_vfx()
            event = self.melee_sfx_event
            if self.weapon_sfx_event:
                event = f"{event}:{self.weapon_sfx_event}"
            self._play_sfx(event)
            return attack
        return None

    def _special_impl(self, now: int):
        """Default special does nothing."""
        return None

    def special_attack(self, now: int):
        """Use the registered special skill if available and not silenced."""
        if self.silenced:
            return None
        skill = self.skill_manager._skills.get("special")
        last_used = skill.last_used if skill else None
        result = self.skill_manager.use("special", now)
        if skill and last_used != skill.last_used:
            self._play_sfx(self.special_sfx_event)
        return result

    def _play_sfx(self, name: str) -> None:
        sound_manager = getattr(self, "sound_manager", None)
        if sound_manager is not None:
            if hasattr(sound_manager, "play_event"):
                sound_manager.play_event(name)
            else:
                sound_manager.play(name)

    def _melee_vfx_style(self) -> str:
        weapon = self.weapon_sfx_event or ""
        mapping = {
            "sword": "slash_arc",
            "axe": "slash_spike",
            "spear": "slash_thrust",
            "bow": "slash_wave",
            "wand": "slash_wave",
        }
        return mapping.get(weapon, self.melee_vfx_style)

    def _apply_melee_palette(self, tag: str) -> None:
        color = MELEE_VFX_PALETTES.get(tag)
        if color is not None:
            self.melee_vfx_color = color

    def _special_vfx_style(
        self,
        base_style: str,
        hard_style: str,
        *,
        easy_style: str | None = None,
    ) -> str:
        difficulty = str(getattr(self, "difficulty", "Normal"))
        if difficulty == "Easy" and easy_style:
            return easy_style
        if difficulty in {"Hard", "Elite", "Adaptive"}:
            return hard_style
        return base_style

    def _vfx_scale_for_vfx(self) -> float:
        difficulty = str(getattr(self, "difficulty", "Normal"))
        scale = {
            "Easy": 0.85,
            "Normal": 1.0,
            "Hard": 1.1,
            "Elite": 1.2,
            "Adaptive": 1.15,
        }.get(difficulty, 1.0)
        return max(0.8, min(1.35, 0.9 + (scale - 1.0) * 1.4))

    def parry(self, now: int) -> bool:
        """Start a parry if cooldown allows."""
        if now - self.last_parry >= PARRY_COOLDOWN:
            self.last_parry = now
            self.parrying = True
            return True
        return False

    def dodge(self, now: int, direction: int) -> bool:
        """Perform a quick dodge movement if cooldown allows."""
        if now - self.last_dodge >= DODGE_COOLDOWN and self.use_stamina(
            STAMINA_COST_DODGE
        ):
            self.last_dodge = now
            self.dodging = True
            self.dodge_end = now + DODGE_DURATION
            self.velocity.x = DODGE_SPEED * direction
            return True
        return False

    def apply_gravity(self) -> None:
        self.velocity.y = physics.apply_gravity(self.velocity.y, self.gravity_multiplier)

    def _is_invincible(self, now: int) -> bool:
        return (
            getattr(self, "invincible", False)
            or self.dodging
            or now < getattr(self, "invincible_until", 0)
        )

    def take_damage(self, amount: int) -> None:
        """Reduce health by the given amount, considering block/parry."""
        now = pygame.time.get_ticks()
        if self._is_invincible(now):
            return
        self.health = self.health_manager.take_damage(
            amount, self.blocking, self.parrying
        )
        self.last_hit_time = pygame.time.get_ticks()
        critical = bool(getattr(self, "last_hit_critical", False))
        self._apply_hitstop(amount, critical=critical)
        cam = getattr(self, "camera_manager", None)
        if cam:
            scale = float(getattr(self, "last_hit_difficulty_scale", 1.0) or 1.0)
            base_dur = 240 if critical else 200
            base_mag = 7 if critical else 5
            cam.shake(int(base_dur * scale), int(base_mag * scale))
        if self.health == 0 and self.lives > 0:
            self.lives -= 1
            self.health_manager.health = self.health_manager.max_health
            self.health = self.health_manager.health
            self.pending_respawn = True
            self.revive_until = max(self.revive_until, now + 3000)
            self.invincible_until = max(self.invincible_until, self.revive_until)

    def _apply_hitstop(self, amount: int, *, critical: bool = False) -> None:
        if amount <= 0:
            return
        now = pygame.time.get_ticks()
        duration = 50 + int(amount * 1.4)
        if critical:
            duration += 30
        scale = float(getattr(self, "last_hit_difficulty_scale", 1.0) or 1.0)
        duration = int(duration * scale)
        duration = min(140, duration)
        self.hitstop_until = max(self.hitstop_until, now + duration)

    def use_mana(self, amount: int) -> bool:
        """Spend mana if available. Returns True if successful."""
        if self.mana_manager.use(amount):
            self.mana = self.mana_manager.mana
            return True
        return False

    def use_stamina(self, amount: int) -> bool:
        """Spend stamina if available. Returns True if successful."""
        if self.stamina_manager.use(amount):
            self.stamina = self.stamina_manager.stamina
            return True
        return False

    def regen_mana(self, amount: int) -> None:
        """Regenerate mana up to max_mana."""
        self.mana_manager.regen(amount)
        self.mana = self.mana_manager.mana

    def use_item(self, name: str) -> bool:
        """Consume an item from the inventory and apply its effect."""
        if name == "potion" and self.inventory.remove("potion"):
            self.health_manager.heal(20)
            return True
        if name == "mana_potion" and self.inventory.remove("mana_potion"):
            self.mana_manager.regen(20)
            self.mana = self.mana_manager.mana
            return True
        return False

    # Properties keep manager values in sync when tests assign directly
    @property
    def health(self) -> int:
        return self.health_manager.health

    @health.setter
    def health(self, value: int) -> None:
        self.health_manager.health = max(0, min(self.health_manager.max_health, value))

    @property
    def mana(self) -> int:
        return self.mana_manager.mana

    @mana.setter
    def mana(self, value: int) -> None:
        self.mana_manager.mana = max(0, min(self.mana_manager.max_mana, value))

    def draw_status(self, surface: pygame.Surface, x: int = 10, y: int = 10) -> None:
        """Draw health and mana bars on the given surface."""
        bar_width = 100
        # Health bar (red)
        health_ratio = self.health / self.max_health
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(x, y, bar_width, 10))
        pygame.draw.rect(
            surface,
            (0, 255, 0),
            pygame.Rect(x, y, int(bar_width * health_ratio), 10),
        )
        # Mana bar (blue)
        mana_ratio = self.mana / self.max_mana
        pygame.draw.rect(surface, (50, 50, 50), pygame.Rect(x, y + 15, bar_width, 10))
        pygame.draw.rect(
            surface,
            (0, 0, 255),
            pygame.Rect(x, y + 15, int(bar_width * mana_ratio), 10),
        )
        # Stamina bar (yellow)
        stamina_ratio = self.stamina / self.max_stamina
        pygame.draw.rect(surface, (50, 50, 50), pygame.Rect(x, y + 30, bar_width, 10))
        pygame.draw.rect(
            surface,
            (255, 255, 0),
            pygame.Rect(x, y + 30, int(bar_width * stamina_ratio), 10),
        )
        font = pygame.font.SysFont(None, 16)
        lives_text = font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        surface.blit(lives_text, (x, y + 45))
        level = self.experience_manager.level
        xp = self.experience_manager.xp
        lvl_text = font.render(f"Lvl: {level} XP: {xp}", True, (255, 255, 255))
        surface.blit(lvl_text, (x, y + 60))

    def draw_health_bar(self, surface: pygame.Surface, camera=None) -> None:
        """Draw a small health bar above the character sprite."""
        rect = self.rect
        if camera is not None and hasattr(camera, "apply"):
            rect = camera.apply(rect)
        bar_width = rect.width
        ratio = self.health / self.max_health
        bar_rect = pygame.Rect(rect.x, rect.y - 6, bar_width, 5)
        pygame.draw.rect(surface, (255, 0, 0), bar_rect)
        pygame.draw.rect(
            surface,
            (0, 255, 0),
            pygame.Rect(bar_rect.x, bar_rect.y, int(bar_width * ratio), 5),
        )

    def cooldown_status(self, now: int) -> list[dict[str, object]]:
        """Return cooldown timers for the HUD."""
        specials = []
        skill = self.skill_manager._skills.get("special")
        if skill:
            remaining = max(0, int(skill.cooldown - (now - skill.last_used)))
            specials.append(
                {
                    "name": "Special",
                    "remaining_ms": remaining,
                    "total_ms": int(skill.cooldown),
                }
            )
        return [
            {
                "name": "Shoot",
                "remaining_ms": max(0, PROJECTILE_COOLDOWN - (now - self.last_shot)),
                "total_ms": PROJECTILE_COOLDOWN,
            },
            {
                "name": "Melee",
                "remaining_ms": max(0, MELEE_COOLDOWN - (now - self.last_melee)),
                "total_ms": MELEE_COOLDOWN,
            },
            {
                "name": "Parry",
                "remaining_ms": max(0, PARRY_COOLDOWN - (now - self.last_parry)),
                "total_ms": PARRY_COOLDOWN,
            },
            {
                "name": "Dodge",
                "remaining_ms": max(0, DODGE_COOLDOWN - (now - self.last_dodge)),
                "total_ms": DODGE_COOLDOWN,
            },
            *specials,
        ]

    def gain_xp(self, amount: int) -> bool:
        """Add experience and return True if a level up occurred."""
        leveled = self.experience_manager.add_xp(amount)
        if leveled:
            # grow stronger each level to support long-term MMO progression
            self.stats.base["attack"] = self.stats.base.get("attack", 0) + 1
            self.stats.base["defense"] = self.stats.base.get("defense", 0) + 1
            self.stats.base["max_health"] = self.stats.base.get("max_health", 0) + 5
            self.health_manager.max_health += 5
            self.health_manager.health = min(
                self.health_manager.max_health, self.health_manager.health + 5
            )
            self.max_health = self.health_manager.max_health
            self.health = self.health_manager.health
            self.max_mana = min(200, self.max_mana + 5)
            self.mana_manager.max_mana = self.max_mana
            self.mana_manager.mana = min(self.max_mana, self.mana_manager.mana + 5)
            self.mana = self.mana_manager.mana
            self.max_stamina = min(200, self.max_stamina + 4)
            self.stamina_manager.max_stamina = self.max_stamina
            self.stamina_manager.stamina = min(
                self.max_stamina,
                self.stamina_manager.stamina + 4,
            )
            self.stamina = self.stamina_manager.stamina
        return leveled

    def set_gravity_multiplier(self, multiplier: float) -> None:
        """Adjust the gravity multiplier affecting this player."""
        self.gravity_multiplier = multiplier

    def set_friction_multiplier(self, multiplier: float) -> None:
        """Adjust horizontal friction when on special surfaces."""
        self.friction_multiplier = multiplier

    def update(self, ground_y: int, now: int | None = None) -> None:
        if now is None:
            now = pygame.time.get_ticks()
        if self.invincible_until and now >= self.invincible_until:
            self.invincible_until = 0
        self.stamina = self.stamina_manager.regen(1)
        self.health = self.health_manager.update(now)
        if self.blocking and not self.use_stamina(STAMINA_COST_BLOCK):
            self.blocking = False
        if now < self.hitstop_until:
            return
        self.apply_gravity()
        self.pos += self.velocity
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))
        if self.dodging and now >= self.dodge_end:
            self.dodging = False
        if self.parrying and now - self.last_parry >= PARRY_DURATION:
            self.parrying = False
        landed = False
        self.current_platform = None
        for plat in getattr(self, "platforms", []):
            if (
                self.velocity.y >= 0
                and self.rect.bottom <= plat.rect.top + self.velocity.y
                and self.rect.colliderect(plat.rect)
            ):
                self.rect.bottom = plat.rect.top
                self.pos.y = self.rect.top
                self.velocity.y = 0
                landed = True
                self.current_platform = plat
                if isinstance(plat, CrumblingPlatform):
                    plat.start_crumble()
                break
        if not landed and self.rect.bottom >= ground_y:
            gap_hit = False
            for gap in self.ground_gaps:
                if gap[0] <= self.rect.centerx <= gap[1]:
                    gap_hit = True
                    break
            if not gap_hit:
                self.rect.bottom = ground_y
                self.pos.y = self.rect.top
                self.velocity.y = 0
                landed = True
        if landed:
            if not self.on_ground:
                self.jump_count = 0
            self.on_ground = True
        else:
            self.on_ground = False
            self.current_platform = None

    def begin_revive(self, spawn: tuple[int, int], now: int | None = None) -> None:
        """Reset the player to a spawn point with brief invulnerability."""
        if now is None:
            now = pygame.time.get_ticks()
        self.pending_respawn = False
        self.revive_until = max(self.revive_until, now + 3000)
        self.revive_flash_until = max(self.revive_flash_until, now + 900)
        self.invincible_until = max(self.invincible_until, self.revive_until)
        self.health_manager.health = self.health_manager.max_health
        self.health = self.health_manager.health
        self.stunned = False
        self.silenced = False
        self.blocking = False
        self.velocity.update(0, 0)
        self.pos.update(spawn)
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))
        self.on_ground = False
        self.jump_count = 0


class GuraPlayer(PlayerCharacter):
    """Player subclass implementing Gura's special trident attack."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        # Gura favors offense at the cost of durability.
        self.stats = StatsManager({"attack": 14, "defense": 3, "max_health": 90})
        self.max_health = self.stats.get("max_health")
        self.health_manager = HealthManager(self.max_health)
        self.health = self.health_manager.health
        self.special_sfx_event = "special_cast:gura"
        self.melee_sfx_event = "melee_swing:gura"
        self._apply_melee_palette("gura")
        self.skill_manager.register("special", SPECIAL_COOLDOWN, self._special_impl)

    def _special_impl(self, now: int):
        from .projectile import ExplodingProjectile

        if self.use_mana(20):
            x = self.rect.centerx
            y = self.rect.centery
            direction = pygame.math.Vector2(self.direction, 0)
            proj = ExplodingProjectile(x, y, direction)
            def _draw(surface: pygame.Surface) -> None:
                pygame.draw.line(surface, (0, 235, 235), (0, 4), (20, 4), 3)
                pygame.draw.line(surface, (0, 235, 235), (14, 1), (20, 4), 2)
                pygame.draw.line(surface, (0, 235, 235), (14, 7), (20, 4), 2)

            _apply_vfx_sequence(
                proj,
                "special_gura_trident",
                (20, 8),
                _draw,
                center=(x, y),
            )
            proj.knockback = 2.8
            proj.vfx_intensity = self._vfx_scale_for_vfx()
            proj.velocity *= 1.6
            proj.slow = True
            style = self._special_vfx_style("pulse_ring", "star_twinkle")
            proj.set_animation(style, (0, 235, 235), 1.2)
            return proj
        return None


class WatsonPlayer(PlayerCharacter):
    """Watson Amelia with a time-dash special attack."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        # Watson favors speed over resilience.
        self.speed_factor = 1.2
        self.stats = StatsManager({"attack": 8, "defense": 4, "max_health": 80})
        self.max_health = self.stats.get("max_health")
        self.health_manager = HealthManager(self.max_health)
        self.health = self.health_manager.health
        self.dashing = False
        self.dash_end = 0
        self.dash_invincible_until = 0
        self.special_sfx_event = "special_cast:watson"
        self.melee_sfx_event = "melee_swing:watson"
        self._apply_melee_palette("watson")
        self.skill_manager.register("special", SPECIAL_COOLDOWN, self._special_impl)

    def _special_impl(self, now: int):
        if self.use_mana(15):
            self.dashing = True
            self.dash_end = now + 350
            self.dash_invincible_until = self.dash_end
            self.invincible = True
            self.velocity.x = 15 * self.direction
            from .projectile import VisualEffect

            def _draw(surface: pygame.Surface) -> None:
                pygame.draw.circle(
                    surface, (120, 200, 255), (16, 16), 12, 2
                )
                pygame.draw.line(surface, (120, 200, 255), (6, 16), (26, 16), 2)

            image, frames = _load_vfx_frameset(
                "special_watson_dash", (32, 32), _draw
            )
            effect = VisualEffect(
                self.rect.centerx,
                self.rect.centery,
                32,
                (120, 200, 255),
                duration=18,
                follow=self,
                style=self._special_vfx_style("time_dash", "time_guard"),
                image=image,
                frames=frames,
            )
            effect.vfx_intensity = self._vfx_scale_for_vfx()
            return effect
        return None

    def update(self, ground_y: int, now: int | None = None) -> None:
        if now is None:
            now = pygame.time.get_ticks()
        if self.dashing and now >= self.dash_end:
            self.dashing = False
        if self.invincible and now >= self.dash_invincible_until:
            self.invincible = False
        super().update(ground_y, now)


class InaPlayer(PlayerCharacter):
    """Ninomae Ina'nis with a tentacle grapple special attack."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        # Ina draws from a deep mana pool and sturdy defenses.
        self.stats = StatsManager({"attack": 9, "defense": 6, "max_health": 110})
        self.max_health = self.stats.get("max_health")
        self.health_manager = HealthManager(self.max_health)
        self.health = self.health_manager.health
        self.max_mana = 150
        self.mana_manager = ManaManager(self.max_mana)
        self.mana = self.mana_manager.mana
        self.special_sfx_event = "special_cast:ina"
        self.melee_sfx_event = "melee_swing:ina"
        self._apply_melee_palette("ina")
        self.skill_manager.register("special", SPECIAL_COOLDOWN, self._special_impl)

    def _special_impl(self, now: int):
        from .projectile import GrappleProjectile

        if self.use_mana(15):
            x = self.rect.centerx
            y = self.rect.centery
            direction = pygame.math.Vector2(self.direction, 0)
            proj = GrappleProjectile(x, y, direction)
            def _draw(surface: pygame.Surface) -> None:
                pygame.draw.line(
                    surface, (150, 90, 210), (0, 3), (18, 3), 3
                )

            _apply_vfx_sequence(
                proj,
                "special_ina_tentacle",
                (18, 6),
                _draw,
                center=(x, y),
            )
            proj.knockback = 0.0
            proj.vfx_intensity = self._vfx_scale_for_vfx()
            proj.slow = True
            style = self._special_vfx_style("ripple", "pulse_ring")
            proj.set_animation(style, (150, 90, 210), 1.1)
            return proj
        return None


class KiaraPlayer(PlayerCharacter):
    """Takanashi Kiara's fiery leap that explodes on landing."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        self.stats = StatsManager({"attack": 12, "defense": 5, "max_health": 100})
        self.max_health = self.stats.get("max_health")
        self.health_manager = HealthManager(self.max_health)
        self.health = self.health_manager.health
        self.diving = False
        self.special_sfx_event = "special_cast:kiara"
        self.melee_sfx_event = "melee_swing:kiara"
        self._apply_melee_palette("kiara")
        self.skill_manager.register("special", SPECIAL_COOLDOWN, self._special_impl)

    def _special_impl(self, now: int):
        if not self.diving and self.use_mana(20):
            self.velocity.y = JUMP_VELOCITY * 1.5
            self.diving = True
        return None

    def update(self, ground_y: int, now: int | None = None) -> None:
        super().update(ground_y, now)
        if self.diving and self.on_ground:
            self.diving = False
            from .projectile import ExplosionProjectile
            radius = 42
            blast = ExplosionProjectile(
                self.rect.centerx,
                self.rect.bottom - 10,
                radius=radius,
            )
            blast.burn = True
            def _draw(surface: pygame.Surface) -> None:
                pygame.draw.circle(
                    surface,
                    (255, 130, 50, 160),
                    (radius, radius),
                    radius,
                )

            _apply_vfx_sequence(
                blast,
                "special_kiara_blast",
                (radius * 2, radius * 2),
                _draw,
                center=(self.rect.centerx, self.rect.bottom - 10),
            )
            blast.knockback = 3.2
            blast.vfx_intensity = self._vfx_scale_for_vfx()
            style = self._special_vfx_style("phoenix_flare", "shockwave_expand")
            blast.set_animation(style, (255, 140, 60), 1.0)
            return blast
        return None


class CalliopePlayer(PlayerCharacter):
    """Mori Calliope's returning scythe projectile."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        self.stats = StatsManager({"attack": 13, "defense": 4, "max_health": 85})
        self.max_health = self.stats.get("max_health")
        self.health_manager = HealthManager(self.max_health)
        self.health = self.health_manager.health
        self.special_sfx_event = "special_cast:calliope"
        self.melee_sfx_event = "melee_swing:calliope"
        self._apply_melee_palette("calliope")
        self.skill_manager.register("special", SPECIAL_COOLDOWN, self._special_impl)

    def _special_impl(self, now: int):
        from .projectile import BoomerangProjectile

        if self.use_mana(20):
            proj = BoomerangProjectile(
                self.rect.centerx,
                self.rect.centery,
                pygame.math.Vector2(self.direction, 0),
                self,
            )
            def _draw(surface: pygame.Surface) -> None:
                pygame.draw.arc(
                    surface,
                    (200, 200, 220),
                    pygame.Rect(2, 2, 14, 14),
                    0.6,
                    2.6,
                    3,
                )

            _apply_vfx_sequence(
                proj,
                "special_calliope_scythe",
                (18, 18),
                _draw,
                center=(self.rect.centerx, self.rect.centery),
            )
            proj.knockback = 2.2
            proj.vfx_intensity = self._vfx_scale_for_vfx()
            style = self._special_vfx_style("scythe_spin", "oni_slash")
            proj.set_animation(style, (200, 200, 220), 1.3)
            return proj
        return None


class FaunaPlayer(PlayerCharacter):
    """Ceres Fauna creates a healing field to restore health."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        # Fauna trades attack power for durability and healing.
        self.stats = StatsManager({"attack": 8, "defense": 7, "max_health": 110})
        self.max_health = self.stats.get("max_health")
        self.health_manager = HealthManager(self.max_health)
        self.health = self.health_manager.health
        self.special_sfx_event = "special_cast:fauna"
        self.melee_sfx_event = "melee_swing:fauna"
        self._apply_melee_palette("fauna")
        self.skill_manager.register("special", SPECIAL_COOLDOWN, self._special_impl)

    def _special_impl(self, now: int):
        from .healing_zone import HealingZone

        if self.use_mana(15):
            zone_rect = self.rect.inflate(100, 60)
            zone_rect.center = self.rect.center
            zone = HealingZone(
                zone_rect,
                heal_rate=2,
                duration=90,
                base_color=(90, 220, 140),
                pulse_style=self._special_vfx_style("grove", "bloom"),
            )
            def _draw(surface: pygame.Surface) -> None:
                surface.fill((0, 0, 0, 0))
                pygame.draw.ellipse(
                    surface,
                    (90, 220, 140, 110),
                    surface.get_rect(),
                    0,
                )
                pygame.draw.ellipse(
                    surface,
                    (140, 255, 190, 120),
                    surface.get_rect().inflate(-20, -14),
                    2,
                )

            _apply_vfx_sequence(
                zone,
                "special_fauna_grove",
                (zone_rect.width, zone_rect.height),
                _draw,
            )
            return zone
        return None


class KroniiPlayer(PlayerCharacter):
    """Ouro Kronii parry lasts longer as a special."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        # Kronii leans on defense with a modest health pool.
        self.stats = StatsManager({"attack": 11, "defense": 6, "max_health": 95})
        self.max_health = self.stats.get("max_health")
        self.health_manager = HealthManager(self.max_health)
        self.health = self.health_manager.health
        self.time_guard_end = 0
        self.special_sfx_event = "special_cast:kronii"
        self.melee_sfx_event = "melee_swing:kronii"
        self._apply_melee_palette("kronii")
        self.skill_manager.register("special", SPECIAL_COOLDOWN, self._special_impl)

    def _special_impl(self, now: int):
        if self.use_mana(15):
            self.parry(now)
            self.last_parry -= 400  # extend duration
            self.invincible = True
            self.time_guard_end = now + 250
            from .projectile import VisualEffect

            def _draw(surface: pygame.Surface) -> None:
                pygame.draw.circle(
                    surface, (170, 200, 255), (18, 18), 14, 2
                )
                pygame.draw.circle(
                    surface, (80, 110, 160), (18, 18), 6, 2
                )

            image, frames = _load_vfx_frameset(
                "special_kronii_guard", (36, 36), _draw
            )
            effect = VisualEffect(
                self.rect.centerx,
                self.rect.centery,
                36,
                (170, 200, 255),
                duration=22,
                follow=self,
                style=self._special_vfx_style("time_guard", "crystal_shield"),
                image=image,
                frames=frames,
            )
            effect.vfx_intensity = self._vfx_scale_for_vfx()
            return effect
        return None

    def update(self, ground_y: int, now: int | None = None) -> None:
        if now is None:
            now = pygame.time.get_ticks()
        super().update(ground_y, now)
        if self.invincible and now >= self.time_guard_end:
            self.invincible = False


class IRySPlayer(PlayerCharacter):
    """IRyS deploys a shield that blocks projectiles."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        # IRyS favors defense to reinforce her crystal shield.
        self.stats = StatsManager({"attack": 9, "defense": 8, "max_health": 105})
        self.max_health = self.stats.get("max_health")
        self.health_manager = HealthManager(self.max_health)
        self.health = self.health_manager.health
        self.shield_active = False
        self.shield_end = 0
        self.special_sfx_event = "special_cast:irys"
        self.melee_sfx_event = "melee_swing:irys"
        self._apply_melee_palette("irys")
        self.skill_manager.register("special", SPECIAL_COOLDOWN, self._special_impl)

    def _special_impl(self, now: int):
        if self.use_mana(15):
            self.shield_active = True
            self.shield_end = now + 1200
            self.health_manager.heal(5)
            self.health = self.health_manager.health
            from .projectile import VisualEffect

            def _draw(surface: pygame.Surface) -> None:
                pygame.draw.circle(
                    surface, (210, 170, 255), (20, 20), 16, 2
                )
                pygame.draw.circle(
                    surface, (240, 220, 255), (20, 20), 8, 2
                )

            image, frames = _load_vfx_frameset(
                "special_irys_shield", (40, 40), _draw
            )
            effect = VisualEffect(
                self.rect.centerx,
                self.rect.centery,
                40,
                (210, 170, 255),
                duration=72,
                follow=self,
                style=self._special_vfx_style("crystal_shield", "star_twinkle"),
                image=image,
                frames=frames,
            )
            effect.vfx_intensity = self._vfx_scale_for_vfx()
            return effect
        return None

    def update(self, ground_y: int, now: int | None = None) -> None:
        super().update(ground_y, now)
        if self.shield_active and now is not None and now >= self.shield_end:
            self.shield_active = False


class MumeiPlayer(PlayerCharacter):
    """Nanashi Mumei summons a slowing flock."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        # Mumei strikes hard but can't take many hits.
        self.stats = StatsManager({"attack": 12, "defense": 4, "max_health": 90})
        self.max_health = self.stats.get("max_health")
        self.health_manager = HealthManager(self.max_health)
        self.health = self.health_manager.health
        self.special_sfx_event = "special_cast:mumei"
        self.melee_sfx_event = "melee_swing:mumei"
        self._apply_melee_palette("mumei")
        self.skill_manager.register("special", SPECIAL_COOLDOWN, self._special_impl)

    def _special_impl(self, now: int):
        from .projectile import FlockProjectile

        if self.use_mana(15):
            proj = FlockProjectile(
                self.rect.centerx,
                self.rect.centery,
                pygame.math.Vector2(self.direction, 0),
            )
            def _draw(surface: pygame.Surface) -> None:
                pygame.draw.polygon(
                    surface,
                    (180, 180, 240),
                    [(0, 5), (8, 0), (15, 5), (8, 9)],
                )

            _apply_vfx_sequence(
                proj,
                "special_mumei_flock",
                (16, 10),
                _draw,
                center=(self.rect.centerx, self.rect.centery),
            )
            proj.knockback = 0.0
            proj.vfx_intensity = self._vfx_scale_for_vfx()
            proj.velocity *= 0.9
            style = self._special_vfx_style("flock_flutter", "star_twinkle")
            proj.set_animation(style, (180, 180, 240), 1.2)
            return proj
        return None


class BaelzPlayer(PlayerCharacter):
    """Hakos Baelz triggers random chaos effects."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        # Baelz mixes agility with chaotic power.
        self.stats = StatsManager({"attack": 9, "defense": 8, "max_health": 110})
        self.max_health = self.stats.get("max_health")
        self.health_manager = HealthManager(self.max_health)
        self.health = self.health_manager.health
        self.chaos_end = 0
        self.chaos_gravity_restore = self.gravity_multiplier
        self.special_sfx_event = "special_cast:baelz"
        self.melee_sfx_event = "melee_swing:baelz"
        self._apply_melee_palette("baelz")
        self.skill_manager.register("special", SPECIAL_COOLDOWN, self._special_impl)

    def _special_impl(self, now: int):
        if self.use_mana(20):
            effect = random.choice(["invert", "low_gravity", "chaos_burst"])
            if effect == "invert":
                self.direction *= -1
                self.velocity.x *= -1
                from .projectile import VisualEffect

                def _draw(surface: pygame.Surface) -> None:
                    pygame.draw.circle(
                        surface, (255, 160, 210), (14, 14), 10, 2
                    )
                    pygame.draw.line(
                        surface, (255, 160, 210), (6, 14), (22, 14), 2
                    )

                image, frames = _load_vfx_frameset(
                    "special_baelz_glitch", (28, 28), _draw
                )
                effect = VisualEffect(
                    self.rect.centerx,
                    self.rect.centery,
                    28,
                    (255, 160, 210),
                    duration=14,
                    follow=self,
                    style=self._special_vfx_style("chaos_glitch", "festival_burst"),
                    image=image,
                    frames=frames,
                )
                effect.vfx_intensity = self._vfx_scale_for_vfx()
                return effect
            elif effect == "low_gravity":
                self.chaos_gravity_restore = self.gravity_multiplier
                self.set_gravity_multiplier(0.6)
                self.chaos_end = now + 800
                from .projectile import VisualEffect

                def _draw(surface: pygame.Surface) -> None:
                    pygame.draw.circle(
                        surface, (200, 120, 255), (15, 15), 11, 2
                    )
                    pygame.draw.circle(
                        surface, (80, 40, 120), (15, 15), 5, 2
                    )

                image, frames = _load_vfx_frameset(
                    "special_baelz_glitch", (30, 30), _draw
                )
                effect = VisualEffect(
                    self.rect.centerx,
                    self.rect.centery,
                    30,
                    (200, 120, 255),
                    duration=16,
                    follow=self,
                    style=self._special_vfx_style("chaos_glitch", "festival_burst"),
                    image=image,
                    frames=frames,
                )
                effect.vfx_intensity = self._vfx_scale_for_vfx()
                return effect
            else:
                from .projectile import PoisonProjectile

                direction = pygame.math.Vector2(self.direction, 0)
                direction = direction.rotate(random.randint(-20, 20))
                proj = PoisonProjectile(
                    self.rect.centerx,
                    self.rect.centery,
                    direction,
                )
                def _draw(surface: pygame.Surface) -> None:
                    pygame.draw.circle(surface, (255, 120, 200), (6, 6), 6)

                _apply_vfx_sequence(
                    proj,
                    "special_baelz_burst",
                    (12, 12),
                    _draw,
                    center=(self.rect.centerx, self.rect.centery),
                )
                proj.knockback = 1.2
                proj.vfx_intensity = self._vfx_scale_for_vfx()
                style = self._special_vfx_style("chaos_glitch", "festival_burst")
                proj.set_animation(style, (255, 120, 200), 1.4)
                return proj
        return None

    def update(self, ground_y: int, now: int | None = None) -> None:
        if now is None:
            now = pygame.time.get_ticks()
        super().update(ground_y, now)
        if self.chaos_end and now >= self.chaos_end:
            self.set_gravity_multiplier(self.chaos_gravity_restore)
            self.chaos_end = 0


class FubukiPlayer(PlayerCharacter):
    """Shirakami Fubuki fires an ice shard that slows enemies."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        # Fubuki is swift but slightly frailer than average.
        self.speed_factor = 1.15
        self.stats = StatsManager({"attack": 9, "defense": 5, "max_health": 95})
        self.max_health = self.stats.get("max_health")
        self.health_manager = HealthManager(self.max_health)
        self.health = self.health_manager.health
        self.special_sfx_event = "special_cast:fubuki"
        self.melee_sfx_event = "melee_swing:fubuki"
        self._apply_melee_palette("fubuki")
        self.skill_manager.register("special", SPECIAL_COOLDOWN, self._special_impl)

    def _special_impl(self, now: int):
        from .projectile import FreezingProjectile

        if self.use_mana(15):
            proj = FreezingProjectile(
                self.rect.centerx,
                self.rect.centery,
                pygame.math.Vector2(self.direction, 0),
            )
            def _draw(surface: pygame.Surface) -> None:
                pygame.draw.polygon(
                    surface,
                    (200, 240, 255),
                    [(0, 3), (10, 0), (15, 3), (10, 6)],
                )

            _apply_vfx_sequence(
                proj,
                "special_fubuki_shard",
                (16, 6),
                _draw,
                center=(self.rect.centerx, self.rect.centery),
            )
            proj.knockback = 0.0
            proj.vfx_intensity = self._vfx_scale_for_vfx()
            proj.velocity *= 1.1
            style = self._special_vfx_style("frost_glint", "star_twinkle")
            proj.set_animation(style, (200, 240, 255), 1.2)
            return proj
        return None


class MatsuriPlayer(PlayerCharacter):
    """Natsuiro Matsuri launches a firework that explodes overhead."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        # Matsuri leans slightly into offense.
        self.stats = StatsManager({"attack": 11, "defense": 5, "max_health": 100})
        self.max_health = self.stats.get("max_health")
        self.health_manager = HealthManager(self.max_health)
        self.health = self.health_manager.health
        self.special_sfx_event = "special_cast:matsuri"
        self.melee_sfx_event = "melee_swing:matsuri"
        self._apply_melee_palette("matsuri")
        self.skill_manager.register("special", SPECIAL_COOLDOWN, self._special_impl)

    def _special_impl(self, now: int):
        from .projectile import FireworkProjectile

        if self.use_mana(20):
            proj = FireworkProjectile(self.rect.centerx, self.rect.centery)
            proj.burn = True
            def _draw(surface: pygame.Surface) -> None:
                pygame.draw.circle(surface, (255, 210, 120), (5, 5), 5)

            _apply_vfx_sequence(
                proj,
                "special_matsuri_firework",
                (10, 10),
                _draw,
                center=(self.rect.centerx, self.rect.centery),
            )
            proj.knockback = 2.6
            proj.vfx_intensity = self._vfx_scale_for_vfx()
            style = self._special_vfx_style("festival_burst", "phoenix_flare")
            proj.set_animation(style, (255, 210, 120), 1.4)
            return proj
        return None


class MikoPlayer(PlayerCharacter):
    """Sakura Miko fires a piercing beam that passes through enemies."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        # Miko hits hard but has light defenses and health.
        self.stats = StatsManager({"attack": 12, "defense": 3, "max_health": 85})
        self.max_health = self.stats.get("max_health")
        self.health_manager = HealthManager(self.max_health)
        self.health = self.health_manager.health
        self.special_sfx_event = "special_cast:miko"
        self.melee_sfx_event = "melee_swing:miko"
        self._apply_melee_palette("miko")
        self.skill_manager.register("special", SPECIAL_COOLDOWN, self._special_impl)

    def _special_impl(self, now: int):
        from .projectile import PiercingProjectile

        if self.use_mana(20):
            proj = PiercingProjectile(
                self.rect.centerx,
                self.rect.centery,
                pygame.math.Vector2(self.direction, 0),
            )
            def _draw(surface: pygame.Surface) -> None:
                pygame.draw.line(surface, (255, 90, 120), (0, 2), (18, 2), 3)

            _apply_vfx_sequence(
                proj,
                "special_miko_beam",
                (18, 4),
                _draw,
                center=(self.rect.centerx, self.rect.centery),
            )
            proj.knockback = 1.5
            proj.vfx_intensity = self._vfx_scale_for_vfx()
            style = self._special_vfx_style("shrine_beam", "shockwave_expand")
            proj.set_animation(style, (255, 90, 120), 1.1)
            return proj
        return None


class AquaPlayer(PlayerCharacter):
    """Minato Aqua fires a water blast that explodes."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        # Aqua favors defense over raw damage.
        self.stats = StatsManager({"attack": 9, "defense": 7, "max_health": 100})
        self.max_health = self.stats.get("max_health")
        self.health_manager = HealthManager(self.max_health)
        self.health = self.health_manager.health
        self.special_sfx_event = "special_cast:aqua"
        self.melee_sfx_event = "melee_swing:aqua"
        self._apply_melee_palette("aqua")
        self.skill_manager.register("special", SPECIAL_COOLDOWN, self._special_impl)

    def _special_impl(self, now: int):
        from .projectile import WaterProjectile

        if self.use_mana(20):
            proj = WaterProjectile(
                self.rect.centerx,
                self.rect.centery,
                pygame.math.Vector2(self.direction, 0),
            )
            def _draw(surface: pygame.Surface) -> None:
                pygame.draw.circle(surface, (80, 150, 255), (8, 5), 5)

            _apply_vfx_sequence(
                proj,
                "special_aqua_bubble",
                (16, 10),
                _draw,
                center=(self.rect.centerx, self.rect.centery),
            )
            proj.knockback = 0.0
            proj.vfx_intensity = self._vfx_scale_for_vfx()
            proj.velocity *= 1.1
            style = self._special_vfx_style("water_bubble", "ripple")
            proj.set_animation(style, (80, 150, 255), 1.1)
            return proj
        return None


class PekoraPlayer(PlayerCharacter):
    """Usada Pekora tosses an explosive carrot."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        # Pekora mixes steady attack with modest defenses.
        self.stats = StatsManager({"attack": 11, "defense": 5, "max_health": 95})
        self.max_health = self.stats.get("max_health")
        self.health_manager = HealthManager(self.max_health)
        self.health = self.health_manager.health
        self.special_sfx_event = "special_cast:pekora"
        self.melee_sfx_event = "melee_swing:pekora"
        self._apply_melee_palette("pekora")
        self.skill_manager.register("special", SPECIAL_COOLDOWN, self._special_impl)

    def _special_impl(self, now: int):
        from .projectile import BouncyProjectile

        if self.use_mana(20):
            proj = BouncyProjectile(
                self.rect.centerx,
                self.rect.centery,
                pygame.math.Vector2(self.direction, 0),
            )
            def _draw(surface: pygame.Surface) -> None:
                pygame.draw.polygon(
                    surface,
                    (250, 150, 70),
                    [(6, 0), (0, 12), (12, 12)],
                )
                pygame.draw.line(surface, (90, 170, 90), (6, 0), (6, -4), 2)

            _apply_vfx_sequence(
                proj,
                "special_pekora_carrot",
                (12, 12),
                _draw,
                center=(self.rect.centerx, self.rect.centery),
            )
            proj.knockback = 2.4
            proj.vfx_intensity = self._vfx_scale_for_vfx()
            style = self._special_vfx_style("carrot_wiggle", "scythe_spin")
            proj.set_animation(style, (250, 150, 70), 1.3)
            return proj
        return None


class MarinePlayer(PlayerCharacter):
    """Houshou Marine's anchor boomerang."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        # Marine hits hard but carries a lighter health pool.
        self.stats = StatsManager({"attack": 13, "defense": 5, "max_health": 90})
        self.max_health = self.stats.get("max_health")
        self.health_manager = HealthManager(self.max_health)
        self.health = self.health_manager.health
        self.special_sfx_event = "special_cast:marine"
        self.melee_sfx_event = "melee_swing:marine"
        self._apply_melee_palette("marine")
        self.skill_manager.register("special", SPECIAL_COOLDOWN, self._special_impl)

    def _special_impl(self, now: int):
        from .projectile import BoomerangProjectile

        if self.use_mana(20):
            proj = BoomerangProjectile(
                self.rect.centerx,
                self.rect.centery,
                pygame.math.Vector2(self.direction, 0),
                self,
            )
            def _draw(surface: pygame.Surface) -> None:
                pygame.draw.circle(surface, (210, 120, 160), (9, 9), 7, 2)
                pygame.draw.line(surface, (210, 120, 160), (9, 2), (9, 14), 2)

            _apply_vfx_sequence(
                proj,
                "special_marine_anchor",
                (18, 18),
                _draw,
                center=(self.rect.centerx, self.rect.centery),
            )
            proj.knockback = 2.1
            proj.vfx_intensity = self._vfx_scale_for_vfx()
            style = self._special_vfx_style("anchor_swing", "scythe_spin")
            proj.set_animation(style, (210, 120, 160), 1.1)
            return proj
        return None


class SuiseiPlayer(PlayerCharacter):
    """Hoshimachi Suisei shoots a piercing star."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        # Suisei mixes precise offense with sturdier defenses.
        self.stats = StatsManager({"attack": 12, "defense": 6, "max_health": 95})
        self.max_health = self.stats.get("max_health")
        self.health_manager = HealthManager(self.max_health)
        self.health = self.health_manager.health
        self.special_sfx_event = "special_cast:suisei"
        self.melee_sfx_event = "melee_swing:suisei"
        self._apply_melee_palette("suisei")
        self.skill_manager.register("special", SPECIAL_COOLDOWN, self._special_impl)

    def _special_impl(self, now: int):
        from .projectile import PiercingProjectile

        if self.use_mana(20):
            proj = PiercingProjectile(
                self.rect.centerx,
                self.rect.centery,
                pygame.math.Vector2(self.direction, 0),
            )
            def _draw(surface: pygame.Surface) -> None:
                pygame.draw.polygon(
                    surface,
                    (120, 210, 255),
                    [
                        (7, 0),
                        (9, 5),
                        (14, 7),
                        (9, 9),
                        (7, 14),
                        (5, 9),
                        (0, 7),
                        (5, 5),
                    ],
                )

            _apply_vfx_sequence(
                proj,
                "special_suisei_star",
                (14, 14),
                _draw,
                center=(self.rect.centerx, self.rect.centery),
            )
            proj.knockback = 1.7
            proj.vfx_intensity = self._vfx_scale_for_vfx()
            style = self._special_vfx_style("star_twinkle", "festival_burst")
            proj.set_animation(style, (120, 210, 255), 1.4)
            return proj
        return None


class AyamePlayer(PlayerCharacter):
    """Nakiri Ayame performs a swift dash."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        # Ayame strikes fast with modest defenses.
        self.stats = StatsManager({"attack": 11, "defense": 4, "max_health": 90})
        self.max_health = self.stats.get("max_health")
        self.health_manager = HealthManager(self.max_health)
        self.health = self.health_manager.health
        self.dashing = False
        self.dash_end = 0
        self.dash_invincible_until = 0
        self.special_sfx_event = "special_cast:ayame"
        self.melee_sfx_event = "melee_swing:ayame"
        self._apply_melee_palette("ayame")
        self.skill_manager.register("special", SPECIAL_COOLDOWN, self._special_impl)

    def _special_impl(self, now: int):
        if self.use_mana(15):
            self.dashing = True
            self.dash_end = now + 320
            self.dash_invincible_until = self.dash_end
            self.invincible = True
            self.velocity.x = 15 * self.direction
            from .projectile import VisualEffect

            def _draw(surface: pygame.Surface) -> None:
                pygame.draw.polygon(
                    surface,
                    (200, 90, 90),
                    [(2, 15), (15, 2), (28, 15), (15, 28)],
                    2,
                )

            image, frames = _load_vfx_frameset(
                "special_ayame_slash", (30, 30), _draw
            )
            return VisualEffect(
                self.rect.centerx,
                self.rect.centery,
                30,
                (200, 90, 90),
                duration=16,
                follow=self,
                style=self._special_vfx_style("oni_slash", "scythe_spin"),
                image=image,
                frames=frames,
            )
        return None

    def update(self, ground_y: int, now: int | None = None) -> None:
        if now is None:
            now = pygame.time.get_ticks()
        if self.dashing and now >= self.dash_end:
            self.dashing = False
        if self.invincible and now >= self.dash_invincible_until:
            self.invincible = False
        super().update(ground_y, now)


class NoelPlayer(PlayerCharacter):
    """Shirogane Noel smashes the ground sending a shockwave forward."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        # Noel leans into defense with a heavy armor build.
        self.stats = StatsManager({"attack": 9, "defense": 8, "max_health": 110})
        self.max_health = self.stats.get("max_health")
        self.health_manager = HealthManager(self.max_health)
        self.health = self.health_manager.health
        self.special_sfx_event = "special_cast:noel"
        self.melee_sfx_event = "melee_swing:noel"
        self._apply_melee_palette("noel")
        self.skill_manager.register("special", SPECIAL_COOLDOWN, self._special_impl)

    def _special_impl(self, now: int):
        from .projectile import ShockwaveProjectile

        if self.use_mana(20):
            proj = ShockwaveProjectile(
                self.rect.centerx,
                self.rect.bottom - 10,
                pygame.math.Vector2(self.direction, 0),
            )
            def _draw(surface: pygame.Surface) -> None:
                surface.fill((190, 190, 210))
                pygame.draw.rect(surface, (90, 90, 120), surface.get_rect(), 2)

            _apply_vfx_sequence(
                proj,
                "special_noel_shock",
                (28, 8),
                _draw,
                center=(self.rect.centerx, self.rect.bottom - 10),
            )
            proj.knockback = 3.0
            proj.vfx_intensity = self._vfx_scale_for_vfx()
            proj.slow = True
            style = self._special_vfx_style("shockwave_expand", "festival_burst")
            proj.set_animation(style, (190, 190, 210), 1.1)
            return proj
        return None


class FlarePlayer(PlayerCharacter):
    """Shiranui Flare fires a burning fireball."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        # Flare pushes offense at the cost of resilience.
        self.stats = StatsManager({"attack": 12, "defense": 4, "max_health": 95})
        self.max_health = self.stats.get("max_health")
        self.health_manager = HealthManager(self.max_health)
        self.health = self.health_manager.health
        self.special_sfx_event = "special_cast:flare"
        self.melee_sfx_event = "melee_swing:flare"
        self._apply_melee_palette("flare")
        self.skill_manager.register("special", SPECIAL_COOLDOWN, self._special_impl)

    def _special_impl(self, now: int):
        from .projectile import BurningProjectile

        if self.use_mana(20):
            proj = BurningProjectile(
                self.rect.centerx,
                self.rect.centery,
                pygame.math.Vector2(self.direction, 0),
            )
            def _draw(surface: pygame.Surface) -> None:
                pygame.draw.circle(surface, (255, 140, 60), (7, 5), 5)

            _apply_vfx_sequence(
                proj,
                "special_flare_fireball",
                (14, 10),
                _draw,
                center=(self.rect.centerx, self.rect.centery),
            )
            proj.knockback = 2.0
            proj.vfx_intensity = self._vfx_scale_for_vfx()
            proj.velocity *= 1.1
            style = self._special_vfx_style("flame_flicker", "phoenix_flare")
            proj.set_animation(style, (255, 140, 60), 1.3)
            return proj
        return None


class SubaruPlayer(PlayerCharacter):
    """Oozora Subaru launches a stunning blast."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        # Subaru's stamina grants balanced defense and a slightly larger health pool.
        self.stats = StatsManager({"attack": 10, "defense": 6, "max_health": 105})
        self.max_health = self.stats.get("max_health")
        self.health_manager = HealthManager(self.max_health)
        self.health = self.health_manager.health
        self.special_sfx_event = "special_cast:subaru"
        self.melee_sfx_event = "melee_swing:subaru"
        self._apply_melee_palette("subaru")
        self.skill_manager.register("special", SPECIAL_COOLDOWN, self._special_impl)

    def _special_impl(self, now: int):
        from .projectile import StunningProjectile

        if self.use_mana(20):
            proj = StunningProjectile(
                self.rect.centerx,
                self.rect.centery,
                pygame.math.Vector2(self.direction, 0),
            )
            def _draw(surface: pygame.Surface) -> None:
                pygame.draw.circle(surface, (255, 230, 120), (7, 4), 4)

            _apply_vfx_sequence(
                proj,
                "special_subaru_blast",
                (14, 8),
                _draw,
                center=(self.rect.centerx, self.rect.centery),
            )
            proj.knockback = 2.2
            proj.vfx_intensity = self._vfx_scale_for_vfx()
            style = self._special_vfx_style("stun_zap", "shockwave_expand")
            proj.set_animation(style, (255, 230, 120), 1.5)
            return proj
        return None


class SoraPlayer(PlayerCharacter):
    """Tokino Sora unleashes a melodic note that weaves upward."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        # Sora trades some attack for generous health, enduring longer in battle.
        self.stats = StatsManager({"attack": 9, "defense": 5, "max_health": 110})
        self.max_health = self.stats.get("max_health")
        self.health_manager = HealthManager(self.max_health)
        self.health = self.health_manager.health
        self.special_sfx_event = "special_cast:sora"
        self.melee_sfx_event = "melee_swing:sora"
        self._apply_melee_palette("sora")
        self.skill_manager.register("special", SPECIAL_COOLDOWN, self._special_impl)

    def _special_impl(self, now: int):
        from .projectile import MelodyProjectile

        if self.use_mana(20):
            proj = MelodyProjectile(
                self.rect.centerx,
                self.rect.centery,
                pygame.math.Vector2(self.direction, 0),
            )
            def _draw(surface: pygame.Surface) -> None:
                pygame.draw.circle(surface, (160, 210, 255), (6, 10), 4)
                pygame.draw.line(surface, (160, 210, 255), (6, 2), (6, 10), 2)
                pygame.draw.line(surface, (160, 210, 255), (6, 2), (12, 0), 2)

            _apply_vfx_sequence(
                proj,
                "special_sora_melody",
                (14, 14),
                _draw,
                center=(self.rect.centerx, self.rect.centery),
            )
            proj.knockback = 1.3
            proj.vfx_intensity = self._vfx_scale_for_vfx()
            style = self._special_vfx_style("melody_wave", "star_twinkle")
            proj.set_animation(style, (160, 210, 255), 1.0)
            return proj
        return None


class Enemy(PlayerCharacter):
    """AI controlled opponent sharing the player mechanics."""

    AI_LEVELS = {
        "Easy": {
            "react_ms": 600,
            "speed": 0.6,
            "shoot_prob": 1.0,
            "melee_prob": 1.0,
            "jump_prob": 0.1,
            "dodge_prob": 0.2,
            "block_prob": 0.1,
            "special_prob": 0.04,
            "dash_prob": 0.05,
            "feint_prob": 0.03,
            "strafe_prob": 0.08,
            "hold_distance": 90,
            "lead_frames": 0,
        },
        "Normal": {
            "react_ms": 300,
            "speed": 0.8,
            "shoot_prob": 1.0,
            "melee_prob": 1.0,
            "jump_prob": 0.2,
            "dodge_prob": 0.4,
            "block_prob": 0.2,
            "special_prob": 0.08,
            "dash_prob": 0.1,
            "feint_prob": 0.05,
            "strafe_prob": 0.12,
            "hold_distance": 105,
            "lead_frames": 0,
        },
        "Hard": {
            "react_ms": 100,
            "speed": 1.0,
            "shoot_prob": 1.0,
            "melee_prob": 1.0,
            "jump_prob": 0.4,
            "dodge_prob": 0.6,
            "block_prob": 0.4,
            "special_prob": 0.14,
            "dash_prob": 0.18,
            "feint_prob": 0.08,
            "strafe_prob": 0.2,
            "hold_distance": 120,
            "lead_frames": 10,
        },
        "Elite": {
            "react_ms": 70,
            "speed": 1.15,
            "shoot_prob": 1.0,
            "melee_prob": 1.0,
            "jump_prob": 0.5,
            "dodge_prob": 0.7,
            "block_prob": 0.5,
            "special_prob": 0.2,
            "dash_prob": 0.22,
            "feint_prob": 0.12,
            "strafe_prob": 0.25,
            "hold_distance": 130,
            "lead_frames": 14,
        },
        "Adaptive": {
            "react_ms": 85,
            "speed": 1.1,
            "shoot_prob": 1.0,
            "melee_prob": 1.0,
            "jump_prob": 0.45,
            "dodge_prob": 0.65,
            "block_prob": 0.5,
            "special_prob": 0.18,
            "dash_prob": 0.2,
            "feint_prob": 0.1,
            "strafe_prob": 0.22,
            "hold_distance": 125,
            "lead_frames": 12,
        },
    }

    def __init__(
        self,
        x: int,
        y: int,
        image_path: str | None = None,
        difficulty: str = "Normal",
        faction: str = "Arena",
        reputation_reward: int = 5,
    ) -> None:
        super().__init__(x, y, image_path)
        self.stats = StatsManager({"attack": 8, "defense": 2, "max_health": 50})
        self.max_health = self.stats.get("max_health")
        self.health_manager = HealthManager(self.max_health)
        self.health = self.health_manager.health
        self.difficulty = difficulty
        # Seed a short warmup window so AI can react soon after spawning
        # without bypassing the slower Easy cadence in tests and gameplay.
        self.last_ai_action = pygame.time.get_ticks() - 400
        self.lives = 1
        self.block_release = 0
        self.spawn_x = x
        self.patrol_dir = 1
        self.faction = faction
        self.reputation_reward = reputation_reward
        self.focus_low_health = self.difficulty in {"Hard", "Elite", "Adaptive"}
        self.focus_threshold = 0.35
        self.focus_range = 260
        self.special_sfx_event = "special_cast:enemy"
        self.melee_sfx_event = "melee_swing:enemy"
        self._apply_melee_palette("enemy")

    def _special_impl(self, now: int):
        from .projectile import Projectile, PROJECTILE_SPEED

        if not self.use_mana(15):
            return None
        x = self.rect.centerx
        y = self.rect.centery
        direction = pygame.math.Vector2(self.direction, 0)
        proj = Projectile(x, y, direction, from_enemy=True, owner=self)
        def _draw(surface: pygame.Surface) -> None:
            pygame.draw.rect(surface, (255, 170, 120), surface.get_rect(), 0)
            pygame.draw.rect(surface, (255, 210, 170), surface.get_rect(), 2)

        _apply_vfx_sequence(
            proj,
            "special_enemy_pulse",
            (16, 6),
            _draw,
            center=(x, y),
        )
        proj.knockback = 1.4
        proj.vfx_intensity = self._vfx_scale_for_vfx()
        proj.velocity = direction.normalize() * (PROJECTILE_SPEED * 0.75)
        proj.attack = self.stats.get("attack") + 8
        proj.crit_chance = self.stats.get("crit_chance")
        proj.crit_multiplier = self.stats.get("crit_multiplier")
        style = self._special_vfx_style("pulse_ring", "stun_zap")
        proj.set_animation(style, (255, 170, 120), 1.15)
        proj.is_special = True
        return proj

    def take_damage(self, amount: int) -> None:
        if self._is_invincible(pygame.time.get_ticks()):
            return
        critical = bool(getattr(self, "last_hit_critical", False))
        self.health = self.health_manager.take_damage(amount, self.blocking, False)
        self._apply_hitstop(amount, critical=critical)
        if self.health == 0:
            self.kill()

    def _patrol(self, settings: dict[str, float]) -> None:
        """Move back and forth around the spawn point when no target is nearby."""
        if self.rect.centerx > self.spawn_x + 100:
            self.patrol_dir = -1
        elif self.rect.centerx < self.spawn_x - 100:
            self.patrol_dir = 1
        self.velocity.x = (
            physics.accelerate(self.velocity.x, self.patrol_dir)
            * settings["speed"]
            * self.speed_factor
        )

    def _avoid_hazards(self, hazards) -> bool:
        """Jump to avoid nearby hazards when possible."""
        for hz in hazards or []:
            if not getattr(hz, "avoid", False):
                continue
            if hz.rect.colliderect(self.rect.move(self.direction * 5, 0)):
                if self.on_ground or self.jump_count < self.max_jumps:
                    self.velocity.y = JUMP_VELOCITY
                    if not self.on_ground:
                        self.jump_count += 1
                    else:
                        self.jump_count = 1
                    self.on_ground = False
                return True
        return False

    def _edge_risk(self, world_width: int) -> bool:
        if world_width <= 0:
            return False
        if self.rect.left < 50 or self.rect.right > world_width - 50:
            return True
        for gap in getattr(self, "ground_gaps", []) or []:
            if gap[0] <= self.rect.centerx <= gap[1]:
                return True
        return False

    def shoot(self, now: int, target: tuple[int, int] | None = None):
        proj = super().shoot(now, target)
        if proj:
            proj.from_enemy = True
            proj.attack = self.stats.get("attack")
            proj.crit_chance = self.stats.get("crit_chance")
            proj.crit_multiplier = self.stats.get("crit_multiplier")
            proj.knockback = 0.9
        return proj

    def melee_attack(self, now: int):
        attack = super().melee_attack(now)
        if attack:
            attack.from_enemy = True
            attack.attack = self.stats.get("attack") + 5
            attack.crit_chance = self.stats.get("crit_chance")
            attack.crit_multiplier = self.stats.get("crit_multiplier")
        return attack

    def handle_ai(
        self,
        target: PlayerCharacter,
        now: int,
        hazards=None,
        projectiles=None,
        *,
        squad_focus: dict[object, float] | None = None,
        allow_special: bool = True,
    ):
        """React to the player based on difficulty level."""
        if getattr(self, "stunned", False):
            return None, None
        settings = dict(
            self.AI_LEVELS.get(self.difficulty, self.AI_LEVELS["Normal"])       
        )
        bias = getattr(self, "ai_bias", None)
        if isinstance(bias, dict):
            for key in (
                "react_ms",
                "speed",
                "shoot_prob",
                "melee_prob",
                "jump_prob",
                "dodge_prob",
                "block_prob",
                "special_prob",
                "dash_prob",
                "feint_prob",
                "strafe_prob",
                "hold_distance",
                "lead_frames",
            ):
                if key in bias:
                    settings[key] = bias[key]
            retreat_threshold = float(bias.get("retreat_threshold", 0.3))
        else:
            retreat_threshold = 0.3
        hazards = hazards or []
        projectiles = projectiles or []
        self._avoid_hazards(hazards)
        world_width = int(getattr(self, "world_width", 0) or 0)
        if world_width and self._edge_risk(world_width):
            move_dir = -1 if self.rect.centerx > world_width / 2 else 1
            self.velocity.x = (
                physics.accelerate(self.velocity.x, move_dir)
                * settings["speed"]
                * self.speed_factor
            )
            self.direction = move_dir
            if self.on_ground and random.random() < settings["jump_prob"]:
                self.velocity.y = JUMP_VELOCITY
                self.jump_count = 1
                self.on_ground = False
            return None, None
        if self.difficulty == "Adaptive":
            player_health = target.health / max(1, target.max_health)
            if player_health > 0.7:
                settings["dodge_prob"] = settings.get("dodge_prob", 0.4) + 0.1
                settings["block_prob"] = settings.get("block_prob", 0.2) + 0.1
            elif player_health < 0.35:
                settings["melee_prob"] = 1.0
                settings["shoot_prob"] = 0.6
                settings["speed"] = settings.get("speed", 1.0) + 0.05
        if self.blocking and now > self.block_release:
            self.blocking = False
        if now - self.last_ai_action < settings["react_ms"]:
            return None, None
        self.last_ai_action = now
        dist_x = abs(target.rect.centerx - self.rect.centerx)
        hold_distance = settings.get("hold_distance", 110)
        if dist_x > 300:
            if self.difficulty in {"Hard", "Elite", "Adaptive"}:
                shoot_ready = now - self.last_shot >= PROJECTILE_COOLDOWN
                if shoot_ready and random.random() < 0.35:
                    lead = settings.get("lead_frames", 0)
                    aim = target.rect.center
                    if lead:
                        aim = (
                            int(target.rect.centerx + target.velocity.x * lead),
                            int(target.rect.centery + target.velocity.y * lead),
                        )
                    proj = self.shoot(now, aim)
                    if proj:
                        return proj, None
            move_dir = 1 if target.rect.centerx > self.rect.centerx else -1
            self.velocity.x = (
                physics.accelerate(self.velocity.x, move_dir)
                * settings["speed"]
                * self.speed_factor
            )
            self.direction = move_dir
            return None, None
        if dist_x > 180 and random.random() < settings.get("dash_prob", 0):
            dash_dir = 1 if target.rect.centerx > self.rect.centerx else -1
            self.dodge(now, dash_dir)
        if dist_x < hold_distance and random.random() < settings.get("feint_prob", 0):
            feint_dir = -1 if target.rect.centerx > self.rect.centerx else 1
            self.dodge(now, feint_dir)
            # Keep evaluating actions after a feint so hard/elite AI still pressures
            # the player instead of idling for the full reaction window.
        for p in projectiles:
            if getattr(p, "visual_only", False):
                continue
            if p.rect.colliderect(self.rect.inflate(30, 30)):
                roll = random.random()
                dodge_prob = settings["dodge_prob"]
                block_prob = settings.get("block_prob", 0)
                if roll < dodge_prob:
                    self.dodge(now, -self.direction)
                    return None, None
                if roll < dodge_prob + block_prob:
                    self.blocking = True
                    self.block_release = now + 500
                    return None, None
            dx = self.rect.centerx - p.rect.centerx
            closing = (p.velocity.x > 0 and dx < 0) or (p.velocity.x < 0 and dx > 0)
            if closing and abs(dx) < 180 and abs(p.rect.centery - self.rect.centery) < 40:
                roll = random.random()
                if roll < settings["dodge_prob"] * 0.8:
                    self.dodge(now, -self.direction)
                    return None, None
                if roll < settings["dodge_prob"] + settings.get("block_prob", 0):
                    self.blocking = True
                    self.block_release = now + 450
                    return None, None
        if (
            dist_x < 60
            and self.health / self.max_health >= 0.3
        ):
            roll = random.random()
            dodge_prob = settings["dodge_prob"]
            block_prob = settings.get("block_prob", 0)
            if roll < dodge_prob:
                self.dodge(now, -self.direction)
                return None, None
            if roll < dodge_prob + block_prob:
                self.blocking = True
                self.block_release = now + 500
                return None, None
        if self.health / self.max_health < retreat_threshold:
            if target.rect.centerx > self.rect.centerx:
                self.velocity.x = (
                    physics.accelerate(self.velocity.x, -1)
                    * settings["speed"]
                    * self.speed_factor
                )
                self.direction = -1
            else:
                self.velocity.x = (
                    physics.accelerate(self.velocity.x, 1)
                    * settings["speed"]
                    * self.speed_factor
                )
                self.direction = 1
            if (
                (self.on_ground or self.jump_count < self.max_jumps)
                and random.random() < settings["jump_prob"]
            ):
                self.velocity.y = JUMP_VELOCITY
                if not self.on_ground:
                    self.jump_count += 1
                else:
                    self.jump_count = 1
                self.on_ground = False
            return None, None
        used_positioning = False
        if self.difficulty in {"Elite", "Adaptive"}:
            next_action = getattr(self, "ai_next_action", "")
            desired_min = max(40, hold_distance - 40)
            desired_max = max(desired_min + 60, hold_distance + 90)
            if next_action == "melee":
                desired_min, desired_max = 30, 90
            elif next_action == "shoot":
                desired_min, desired_max = max(90, hold_distance), hold_distance + 120
            elif next_action in {"retreat", "avoid"}:
                desired_min, desired_max = 160, 280
            if dist_x < desired_min:
                sign = -1 if target.rect.centerx > self.rect.centerx else 1
                self.velocity.x = (
                    physics.accelerate(self.velocity.x, sign)
                    * settings["speed"]
                    * self.speed_factor
                )
                self.direction = 1 if sign > 0 else -1
                used_positioning = True
            elif dist_x > desired_max:
                sign = 1 if target.rect.centerx > self.rect.centerx else -1
                self.velocity.x = (
                    physics.accelerate(self.velocity.x, sign)
                    * settings["speed"]
                    * self.speed_factor
                )
                self.direction = 1 if sign > 0 else -1
                used_positioning = True
            elif next_action == "shoot":
                self.velocity.x *= 0.6
                used_positioning = True
        if not used_positioning:
            if target.rect.centerx > self.rect.centerx:
                self.velocity.x = (
                    physics.accelerate(self.velocity.x, 1)
                    * settings["speed"]
                    * self.speed_factor
                )
                self.direction = 1
            else:
                self.velocity.x = (
                    physics.accelerate(self.velocity.x, -1)
                    * settings["speed"]
                    * self.speed_factor
                )
                self.direction = -1
        if (
            hold_distance - 25 <= dist_x <= hold_distance + 25
            and random.random() < settings.get("strafe_prob", 0)
        ):
            strafe_dir = 1 if random.random() < 0.5 else -1
            self.velocity.x = (
                physics.accelerate(self.velocity.x, strafe_dir)
                * settings["speed"]
                * self.speed_factor
            )
        if (
            (self.on_ground or self.jump_count < self.max_jumps)
            and abs(target.rect.centery - self.rect.centery) > 20
            and random.random() < settings["jump_prob"]
        ):
            self.velocity.y = JUMP_VELOCITY
            if not self.on_ground:
                self.jump_count += 1
            else:
                self.jump_count = 1
            self.on_ground = False
        melee = None
        proj = None
        aim = target.rect.center
        lead = settings.get("lead_frames", 0)
        if lead:
            aim = (
                int(target.rect.centerx + target.velocity.x * lead),
                int(target.rect.centery + target.velocity.y * lead),
            )
        special_roll = random.random()
        if (
            settings.get("special_prob", 0)
            and 150 < dist_x < 260
            and special_roll < settings["special_prob"]
            and special_roll > 0.02
            and abs(target.velocity.y) < 1
            and allow_special
        ):
            special = self.special_attack(now)
            if special:
                return special, None
        melee_ready = now - self.last_melee >= MELEE_COOLDOWN
        shoot_ready = now - self.last_shot >= PROJECTILE_COOLDOWN
        if squad_focus:
            focus_value = squad_focus.get(target, 0.0)
            if focus_value >= 0.8:
                settings["melee_prob"] = max(settings.get("melee_prob", 1.0), 0.9)
                settings["shoot_prob"] = max(settings.get("shoot_prob", 1.0), 0.6)
        if self.difficulty in {"Hard", "Elite", "Adaptive"}:
            if dist_x < 40 and melee_ready:
                melee = self.melee_attack(now)
            elif dist_x < 250 and shoot_ready:
                proj = self.shoot(now, aim)
        else:
            if dist_x < 40 and melee_ready and (
                settings["melee_prob"] >= 1 or random.random() < settings["melee_prob"]
            ):
                melee = self.melee_attack(now)
            elif dist_x < 250 and shoot_ready and (
                settings["shoot_prob"] >= 1 or random.random() < settings["shoot_prob"]
            ):
                proj = self.shoot(now, aim)
        return proj, melee

# Alias for backward compatibility
Player = PlayerCharacter


class BossEnemy(Enemy):
    """Enemy variant used for boss fights with periodic special attacks."""

    def __init__(
        self,
        x: int,
        y: int,
        image_path: str | None = None,
        difficulty: str = "Hard",
        faction: str = "Arena",
        reputation_reward: int = 20,
    ) -> None:
        super().__init__(
            x,
            y,
            image_path,
            difficulty,
            faction=faction,
            reputation_reward=reputation_reward,
        )
        self.skill_manager.register("special", 2000, self._special_impl)

    def _special_impl(self, now: int):
        from .projectile import ExplodingProjectile

        x = self.rect.centerx
        y = self.rect.centery
        direction = pygame.math.Vector2(self.direction, 0)
        proj = ExplodingProjectile(x, y, direction)
        proj.from_enemy = True
        proj.attack = self.stats.get("attack") + 10
        return proj

    def handle_ai(self, target, now, hazards=None, projectiles=None):
        special = self.special_attack(now)
        if special:
            return special, None
        return super().handle_ai(target, now, hazards, projectiles)


# Mapping from character names to specialized player subclasses
CHARACTER_CLASSES = {
    "Gawr Gura": GuraPlayer,
    "Watson Amelia": WatsonPlayer,
    "Ninomae Ina'nis": InaPlayer,
    "Takanashi Kiara": KiaraPlayer,
    "Mori Calliope": CalliopePlayer,
    "Ceres Fauna": FaunaPlayer,
    "Ouro Kronii": KroniiPlayer,
    "IRyS": IRySPlayer,
    "Nanashi Mumei": MumeiPlayer,
    "Hakos Baelz": BaelzPlayer,
    "Shirakami Fubuki": FubukiPlayer,
    "Natsuiro Matsuri": MatsuriPlayer,
    "Sakura Miko": MikoPlayer,
    "Minato Aqua": AquaPlayer,
    "Usada Pekora": PekoraPlayer,
    "Houshou Marine": MarinePlayer,
    "Hoshimachi Suisei": SuiseiPlayer,
    "Nakiri Ayame": AyamePlayer,
    "Shirogane Noel": NoelPlayer,
    "Shiranui Flare": FlarePlayer,
    "Oozora Subaru": SubaruPlayer,
    "Tokino Sora": SoraPlayer,
}


def character_class_exists(name: str) -> bool:
    """Return ``True`` if ``name`` maps to a dedicated player subclass."""

    return name in CHARACTER_CLASSES


def get_player_class(name: str) -> type[PlayerCharacter]:
    """Return the subclass for ``name`` or fallback to ``PlayerCharacter``.

    Verification is performed via :func:`character_class_exists`.  When a
    dedicated subclass is missing the generic base class is returned so the
    game can continue running with a simplified moveset.
    """

    if character_class_exists(name):
        return CHARACTER_CLASSES[name]
    return PlayerCharacter
