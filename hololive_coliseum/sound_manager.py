"""Sound effect and music playback helpers."""

import os
import math
import array
import pygame


class SoundManager:
    """Manage mixer volume and track the last played sound."""

    SFX_PROFILES = {
        "Default": {
            "hit_light": "hit_light",
            "hit_heavy": "hit_heavy",
            "hit_crit": "hit_crit",
            "melee_swing": "melee_swing",
            "special_cast": "special_cast",
        },
        "Arcade": {
            "hit_light": "hit_heavy",
            "hit_heavy": "hit_crit",
            "hit_crit": "hit_crit",
            "melee_swing": "hit_light",
            "special_cast": "hit_heavy",
        },
        "Muted": {
            "hit_light": None,
            "hit_heavy": None,
            "hit_crit": None,
            "melee_swing": None,
            "special_cast": None,
        },
    }
    WEAPON_SFX = {
        "Default": {
            "sword": "melee_swing",
            "axe": "hit_heavy",
            "spear": "melee_swing",
            "bow": "hit_light",
            "wand": "special_cast",
            "weapon": "melee_swing",
        },
        "Arcade": {
            "sword": "hit_heavy",
            "axe": "hit_crit",
            "spear": "hit_heavy",
            "bow": "hit_light",
            "wand": "special_cast",
            "weapon": "hit_heavy",
        },
        "Muted": {
            "sword": None,
            "axe": None,
            "spear": None,
            "bow": None,
            "wand": None,
            "weapon": None,
        },
    }

    def __init__(
        self,
        volume: float = 1.0,
        *,
        base_dir: str | None = None,
        profile: str = "Default",
    ):
        os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
        self.volume = volume
        self.last_played = None
        self.last_event = None
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        self.base_dir = base_dir or os.path.join(
            os.path.dirname(__file__),
            "..",
            "sounds",
        )
        self.profile = profile if profile in self.SFX_PROFILES else "Default"
        self.mixer_ready = False
        try:
            pygame.mixer.init()
            pygame.mixer.music.set_volume(self.volume)
            self.mixer_ready = True
        except pygame.error:
            self.mixer_ready = False
        self._load_default_sounds()

    def play(self, name: str) -> None:
        self.last_played = name
        if not self.mixer_ready:
            return
        sound = self.sounds.get(name)
        if sound:
            sound.set_volume(self.volume)
            sound.play()

    def play_event(self, event: str) -> None:
        self.last_event = event
        mapping = self.SFX_PROFILES.get(self.profile, {})
        cue = mapping.get(event)
        if cue is None and event.startswith("melee_swing:"):
            parts = event.split(":")
            weapon = parts[2] if len(parts) > 2 else ""
            weapon_map = self.WEAPON_SFX.get(self.profile, {})
            cue = weapon_map.get(weapon) or weapon_map.get("weapon")
        if cue is None and ":" in event:
            cue = mapping.get(event.split(":", 1)[0])
        if cue is None:
            cue = mapping.get(event, event)
        if not cue:
            return
        self.play(cue)

    def stop(self) -> None:
        self.last_played = None

    def cycle_volume(self) -> float:
        """Cycle master volume between 0%, 50% and 100%."""
        steps = [0.0, 0.5, 1.0]
        current = min(steps, key=lambda v: abs(v - self.volume))
        idx = steps.index(current)
        self.volume = steps[(idx + 1) % len(steps)]
        if self.mixer_ready:
            pygame.mixer.music.set_volume(self.volume)
        return self.volume

    def set_profile(self, profile: str) -> None:
        if profile in self.SFX_PROFILES:
            self.profile = profile

    def register_sound(self, name: str, filename: str) -> None:
        if not self.mixer_ready:
            return
        path = filename
        if not os.path.isabs(filename):
            path = os.path.join(self.base_dir, filename)
        if not os.path.exists(path):
            return
        try:
            self.sounds[name] = pygame.mixer.Sound(path)
        except pygame.error:
            return

    def _load_default_sounds(self) -> None:
        default_names = (
            "hit_light",
            "hit_heavy",
            "hit_crit",
            "melee_swing",
            "special_cast",
        )
        for name in default_names:
            for ext in (".wav", ".ogg"):
                filename = f"{name}{ext}"
                path = os.path.join(self.base_dir, filename)
                if os.path.exists(path):
                    self.register_sound(name, filename)
                    break
            if name not in self.sounds:
                self._register_synth_sound(name)

    def _register_synth_sound(self, name: str) -> None:
        if not self.mixer_ready:
            return
        sound = self._synth_tone(name)
        if sound is not None:
            self.sounds[name] = sound

    def _synth_tone(self, name: str) -> pygame.mixer.Sound | None:
        if not self.mixer_ready:
            return None
        init = pygame.mixer.get_init()
        if not init:
            return None
        freq, _format, channels = init
        length_ms = 120
        tone = 440.0
        volume = 0.6
        if name == "hit_light":
            tone, length_ms, volume = 520.0, 90, 0.45
        elif name == "hit_heavy":
            tone, length_ms, volume = 280.0, 160, 0.65
        elif name == "hit_crit":
            tone, length_ms, volume = 760.0, 180, 0.7
        elif name == "melee_swing":
            tone, length_ms, volume = 620.0, 110, 0.5
        elif name == "special_cast":
            tone, length_ms, volume = 680.0, 200, 0.55
        sample_count = max(1, int(freq * (length_ms / 1000.0)))
        amplitude = int(32767 * volume)
        buf = array.array("h")
        for idx in range(sample_count):
            env = 1.0
            if idx < sample_count * 0.15:
                env = idx / max(1, int(sample_count * 0.15))
            elif idx > sample_count * 0.8:
                env = (sample_count - idx) / max(1, int(sample_count * 0.2))
            sample = int(amplitude * env * math.sin(2.0 * math.pi * tone * idx / freq))
            buf.append(sample)
            if channels == 2:
                buf.append(sample)
        try:
            return pygame.mixer.Sound(buffer=buf.tobytes())
        except pygame.error:
            return None

    def adjust_volume(self, delta: float) -> float:
        """Increment volume by *delta* within 0..1."""
        self.volume = max(0.0, min(1.0, self.volume + delta))
        if self.mixer_ready:
            pygame.mixer.music.set_volume(self.volume)
        return self.volume
