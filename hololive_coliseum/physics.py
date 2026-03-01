"""Physics helpers for collisions and movement."""

GRAVITY = 0.5
MAX_FALL_SPEED = 15
MOVE_ACCEL = 0.4
MAX_MOVE_SPEED = 5
GROUND_FRICTION = 0.3
AIR_FRICTION = 0.05


def apply_gravity(vy: float, multiplier: float = 1.0) -> float:
    """Apply gravity and limit to MAX_FALL_SPEED."""
    vy += GRAVITY * multiplier
    if vy > MAX_FALL_SPEED:
        vy = MAX_FALL_SPEED
    return vy


def accelerate(vx: float, direction: int) -> float:
    """Accelerate horizontally up to MAX_MOVE_SPEED."""
    vx += MOVE_ACCEL * direction
    if vx > MAX_MOVE_SPEED:
        vx = MAX_MOVE_SPEED
    elif vx < -MAX_MOVE_SPEED:
        vx = -MAX_MOVE_SPEED
    return vx


def apply_friction(vx: float, on_ground: bool, multiplier: float = 1.0) -> float:
    """Apply friction to slow down when no input.

    The ``multiplier`` allows surfaces like ice to modify friction strength.
    """
    friction = (GROUND_FRICTION if on_ground else AIR_FRICTION) * multiplier
    if vx > 0:
        vx = max(0, vx - friction)
    elif vx < 0:
        vx = min(0, vx + friction)
    return vx
