"""Projectile sprite behaviors and collisions."""

import math
import pygame

PROJECTILE_SPEED = 10
EXPLODE_TIME = 30

class Projectile(pygame.sprite.Sprite):
    """Simple projectile moving in a given direction."""

    def __init__(
        self,
        x: int,
        y: int,
        direction: pygame.math.Vector2,
        from_enemy: bool = False,
        owner: object | None = None,
    ) -> None:
        super().__init__()
        self.image = pygame.Surface((10, 4))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.from_enemy = from_enemy
        self.owner = owner
        self.anim_style: str | None = None
        self.anim_color: tuple[int, int, int] | None = None
        self.anim_speed = 1.0
        self.anim_phase = (x + y) % 360
        self.base_image: pygame.Surface | None = None
        self.frame_images: list[pygame.Surface] | None = None
        self.frame_index = 0
        self.frame_next = 0
        self.frame_ms = 90
        self.frame_loop = True
        self.knockback = 1.0
        self.vfx_intensity = 1.0
        if direction.length_squared() == 0:
            direction = pygame.math.Vector2(1, 0)
        self.velocity = direction.normalize() * PROJECTILE_SPEED

    def set_animation(
        self,
        style: str,
        color: tuple[int, int, int] | None = None,
        speed: float = 1.0,
    ) -> None:
        self.anim_style = style
        self.anim_color = color
        self.anim_speed = speed
        self.base_image = self.image.copy()

    def set_frame_animation(
        self,
        frames: list[pygame.Surface],
        *,
        frame_ms: int = 90,
        loop: bool = True,
    ) -> None:
        if not frames:
            return
        self.frame_images = [frame.copy() for frame in frames]
        self.frame_index = 0
        self.frame_ms = max(1, frame_ms)
        self.frame_next = pygame.time.get_ticks() + self.frame_ms
        self.frame_loop = loop
        self._apply_image(self.frame_images[0])

    def _apply_image(self, image: pygame.Surface) -> None:
        center = self.rect.center
        self.image = image
        self.rect = self.image.get_rect(center=center)

    def _animate(self) -> None:
        style = self.anim_style
        now = pygame.time.get_ticks()
        frame = None
        if self.frame_images:
            if now >= self.frame_next:
                self.frame_index += 1
                if self.frame_index >= len(self.frame_images):
                    if self.frame_loop:
                        self.frame_index = 0
                    else:
                        self.frame_index = len(self.frame_images) - 1
                self.frame_next = now + self.frame_ms
            frame = self.frame_images[self.frame_index]
            self.base_image = frame.copy()
            if not style:
                self._apply_image(frame)
                return
        if not style:
            return
        if self.base_image is None:
            self.base_image = self.image.copy()
        base = self.base_image
        phase = (now / 180.0) * self.anim_speed + self.anim_phase
        color = self.anim_color or (255, 255, 255)
        width, height = base.get_size()
        if style in {"pulse_ring", "time_dash", "time_guard", "crystal_shield"}:
            image = base.copy()
            alpha = 80 + int(60 * math.sin(phase))
            alpha = max(40, min(220, int(alpha * self.vfx_intensity)))
            radius = max(3, min(width, height) // 2 - 1)
            overlay = pygame.Surface(image.get_size(), pygame.SRCALPHA)
            pygame.draw.circle(
                overlay,
                (*color, max(60, alpha)),
                (width // 2, height // 2),
                radius,
                2,
            )
            image.blit(overlay, (0, 0))
            self._apply_image(image)
        elif style == "ripple":
            image = base.copy()
            overlay = pygame.Surface(image.get_size(), pygame.SRCALPHA)
            pulse = (math.sin(phase) + 1) * 0.5
            radius = max(3, int((min(width, height) / 2) * (0.7 + pulse * 0.4)))
            pygame.draw.circle(
                overlay,
                (*color, max(50, min(220, int((100 + 80 * pulse) * self.vfx_intensity)))),
                (width // 2, height // 2),
                radius,
                2,
            )
            image.blit(overlay, (0, 0))
            self._apply_image(image)
        elif style in {"scythe_spin", "anchor_swing", "carrot_wiggle", "oni_slash"}:
            if style == "anchor_swing":
                angle = math.sin(phase) * 20
            elif style == "carrot_wiggle":
                angle = math.sin(phase * 1.4) * 25
            elif style == "oni_slash":
                angle = math.sin(phase * 1.8) * 30
            else:
                angle = (phase * 22) % 360
            image = pygame.transform.rotozoom(base, angle, 1.0)
            self._apply_image(image)
        elif style == "flock_flutter":
            scale = 0.85 + 0.2 * (math.sin(phase) + 1) * 0.5
            new_h = max(2, int(height * scale))
            image = pygame.transform.smoothscale(base, (width, new_h))
            self._apply_image(image)
        elif style in {"frost_glint", "star_twinkle"}:
            image = base.copy()
            overlay = pygame.Surface(image.get_size(), pygame.SRCALPHA)
            pulse = (math.sin(phase * 1.6) + 1) * 0.5
            alpha = 60 + int(120 * pulse)
            alpha = max(40, min(220, int(alpha * self.vfx_intensity)))
            pygame.draw.rect(
                overlay,
                (*color, alpha),
                overlay.get_rect(),
                2,
            )
            image.blit(overlay, (0, 0))
            self._apply_image(image)
        elif style in {"festival_burst", "phoenix_flare", "shockwave_expand"}:
            scale = 1.0 + 0.15 * math.sin(phase)
            scale = max(0.7, min(1.4, scale * (0.9 + 0.25 * self.vfx_intensity)))
            image = pygame.transform.rotozoom(base, 0, scale)
            self._apply_image(image)
        elif style == "shrine_beam":
            image = base.copy()
            overlay = pygame.Surface(image.get_size(), pygame.SRCALPHA)
            alpha = 80 + int(80 * (math.sin(phase * 2) + 1) * 0.5)
            alpha = max(40, min(220, int(alpha * self.vfx_intensity)))
            pygame.draw.line(
                overlay,
                (*color, alpha),
                (0, height // 2),
                (width, height // 2),
                2,
            )
            image.blit(overlay, (0, 0))
            self._apply_image(image)
        elif style == "water_bubble":
            scale = 0.95 + 0.08 * math.sin(phase)
            scale = max(0.75, min(1.3, scale * (0.9 + 0.2 * self.vfx_intensity)))
            image = pygame.transform.rotozoom(base, 0, scale)
            self._apply_image(image)
        elif style == "flame_flicker":
            image = base.copy()
            overlay = pygame.Surface(image.get_size(), pygame.SRCALPHA)
            alpha = 90 + int(80 * (math.sin(phase * 2.4) + 1) * 0.5)
            alpha = max(50, min(230, int(alpha * self.vfx_intensity)))
            pygame.draw.rect(overlay, (*color, alpha), overlay.get_rect())
            image.blit(overlay, (0, 0))
            self._apply_image(image)
        elif style == "stun_zap":
            image = base.copy()
            overlay = pygame.Surface(image.get_size(), pygame.SRCALPHA)
            pulse = (math.sin(phase * 3) + 1) * 0.5
            pygame.draw.rect(
                overlay,
                (*color, max(50, min(230, int((80 + 120 * pulse) * self.vfx_intensity)))),
                overlay.get_rect(),
            )
            image.blit(overlay, (0, 0))
            self._apply_image(image)
        elif style == "melody_wave":
            image = base.copy()
            overlay = pygame.Surface(image.get_size(), pygame.SRCALPHA)
            pulse = (math.sin(phase) + 1) * 0.5
            pygame.draw.circle(
                overlay,
                (*color, max(40, min(220, int((70 + 80 * pulse) * self.vfx_intensity)))),
                (width // 2, height // 2),
                max(2, width // 4),
            )
            image.blit(overlay, (0, 0))
            self._apply_image(image)
        elif style == "chaos_glitch":
            image = pygame.Surface(base.get_size(), pygame.SRCALPHA)
            offset = int(2 * math.sin(phase * 3))
            image.blit(base, (offset, 0))
            overlay = pygame.Surface(image.get_size(), pygame.SRCALPHA)
            pygame.draw.rect(
                overlay,
                (*color, 60),
                pygame.Rect(0, height // 3, width, 2),
            )
            image.blit(overlay, (0, 0))
            self._apply_image(image)

    def update(self) -> None:
        self._animate()
        self.rect.move_ip(self.velocity.x, self.velocity.y)


class VisualEffect(Projectile):
    """Short-lived visual-only sprite for special attacks."""

    def __init__(
        self,
        x: int,
        y: int,
        size: int,
        color: tuple[int, int, int],
        duration: int = 20,
        follow: object | None = None,
        style: str = "pulse_ring",
        image: pygame.Surface | None = None,
        frames: list[pygame.Surface] | None = None,
        frame_ms: int = 90,
    ) -> None:
        super().__init__(x, y, pygame.math.Vector2(1, 0))
        self.velocity.update(0, 0)
        self.timer = duration
        self.follow_target = follow
        self.visual_only = True
        if image is not None:
            self.image = image
        else:
            self.image = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(
                self.image,
                (*color, 140),
                (size // 2, size // 2),
                size // 2,
                2,
            )
        self.rect = self.image.get_rect(center=(x, y))
        if frames:
            self.set_frame_animation(frames, frame_ms=frame_ms)
        self.set_animation(style, color=color, speed=1.2)

    def update(self) -> None:
        if self.follow_target is not None and hasattr(self.follow_target, "rect"):
            self.rect.center = self.follow_target.rect.center
        self._animate()
        self.timer -= 1
        if self.timer <= 0:
            self.kill()


class ExplodingProjectile(Projectile):
    """Projectile that disappears after a short duration."""

    def __init__(self, x: int, y: int, direction: pygame.math.Vector2) -> None:
        super().__init__(x, y, direction)
        self.knockback = 2.0
        self.timer = EXPLODE_TIME

    def update(self) -> None:
        super().update()
        self.timer -= 1
        if self.timer <= 0:
            self.kill()


class GrappleProjectile(Projectile):
    """Projectile that pulls enemies toward the shooter on contact."""

    def __init__(self, x: int, y: int, direction: pygame.math.Vector2) -> None:
        super().__init__(x, y, direction)
        self.grapple = True


class BoomerangProjectile(Projectile):
    """Projectile that returns to the shooter after a short delay."""

    def __init__(self, x: int, y: int, direction: pygame.math.Vector2, owner) -> None:
        super().__init__(x, y, direction)
        self.owner = owner
        self.timer = 15

    def update(self) -> None:
        if self.timer > 0:
            self.timer -= 1
        else:
            to_owner = pygame.math.Vector2(
                self.owner.rect.centerx - self.rect.centerx,
                self.owner.rect.centery - self.rect.centery,
            )
            if to_owner.length_squared() > 0:
                self.velocity = to_owner.normalize() * PROJECTILE_SPEED
        super().update()
        if self.rect.colliderect(self.owner.rect):
            self.kill()


class ExplosionProjectile(Projectile):
    """Short-lived projectile that damages enemies in an area."""

    def __init__(self, x: int, y: int, radius: int = 30) -> None:
        super().__init__(x, y, pygame.math.Vector2(0, 0))
        self.velocity.update(0, 0)
        self.radius = radius
        self.timer = 5
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 128, 0), (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self) -> None:
        super().update()
        self.timer -= 1
        if self.timer <= 0:
            self.kill()


class FreezingProjectile(Projectile):
    """Projectile that slows enemies on hit."""

    def __init__(self, x: int, y: int, direction: pygame.math.Vector2) -> None:
        super().__init__(x, y, direction)
        self.freeze = True
        self.knockback = 0.0
        self.image.fill((200, 255, 255))


class FlockProjectile(Projectile):
    """Projectile that slows enemies by summoning a flock."""

    def __init__(self, x: int, y: int, direction: pygame.math.Vector2) -> None:
        super().__init__(x, y, direction)
        self.slow = True
        self.knockback = 0.0
        self.image.fill((150, 150, 255))


class PiercingProjectile(Projectile):
    """Projectile that passes through enemies instead of disappearing."""

    def __init__(self, x: int, y: int, direction: pygame.math.Vector2) -> None:
        super().__init__(x, y, direction)
        self.pierce = True
        self.knockback = 0.9
        self.image.fill((255, 105, 180))


class PoisonProjectile(Projectile):
    """Projectile that poisons enemies on hit."""

    def __init__(self, x: int, y: int, direction: pygame.math.Vector2) -> None:
        super().__init__(x, y, direction)
        self.poison = True
        self.knockback = 0.9
        self.image.fill((0, 200, 0))


class BurningProjectile(ExplodingProjectile):
    """Projectile that ignites enemies causing burn damage."""

    def __init__(self, x: int, y: int, direction: pygame.math.Vector2) -> None:
        super().__init__(x, y, direction)
        self.burn = True
        self.knockback = 1.6
        self.image.fill((255, 120, 0))


class StunningProjectile(ExplodingProjectile):
    """Projectile that stuns enemies on hit."""

    def __init__(self, x: int, y: int, direction: pygame.math.Vector2) -> None:
        super().__init__(x, y, direction)
        self.stun = True
        self.knockback = 1.4
        self.image.fill((255, 255, 0))


class WaterProjectile(ExplodingProjectile):
    """Water blast that slows enemies before dissipating."""

    def __init__(self, x: int, y: int, direction: pygame.math.Vector2) -> None:
        super().__init__(x, y, direction)
        self.slow = True
        self.knockback = 0.0
        self.image.fill((0, 100, 255))


class BouncyProjectile(ExplodingProjectile):
    """Projectile that arcs upward then drops like a bouncing bomb."""

    def __init__(self, x: int, y: int, direction: pygame.math.Vector2) -> None:
        super().__init__(x, y, direction)
        self.knockback = 1.8
        self.velocity.y = -5
        self._bounced = False

    def update(self) -> None:
        super().update()
        if not self._bounced and self.timer <= EXPLODE_TIME // 2:
            self.velocity.y = abs(self.velocity.y)
            self._bounced = True


class FireworkProjectile(ExplodingProjectile):
    """Projectile that rises then bursts into an explosion."""

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, pygame.math.Vector2(0, -1))
        self.knockback = 2.2
        self.image.fill((255, 215, 0))

    def update(self) -> None:
        super().update()
        if self.timer <= 0:
            self.kill()


class ShockwaveProjectile(ExplodingProjectile):
    """Ground-level wave that slides horizontally."""

    def __init__(self, x: int, y: int, direction: pygame.math.Vector2) -> None:
        super().__init__(x, y, direction)
        self.knockback = 2.4
        self.image = pygame.Surface((20, 6))
        self.image.fill((200, 200, 200))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity.y = 0


class MelodyProjectile(ExplodingProjectile):
    """Projectile that oscillates vertically like a musical note."""

    def __init__(self, x: int, y: int, direction: pygame.math.Vector2) -> None:
        super().__init__(x, y, direction)
        self.knockback = 1.3
        self.image.fill((150, 200, 255))
        self.start_y = y
        self.phase = 0.0

    def update(self) -> None:
        super().update()
        self.phase += 0.2
        self.rect.y = self.start_y + int(5 * math.sin(self.phase))
