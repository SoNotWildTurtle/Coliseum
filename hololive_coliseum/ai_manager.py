"""Coordinate AI behavior for NPCs and combatants."""

class AIManager:
    """Coordinate AI updates for enemy sprites."""

    def __init__(self, enemies) -> None:
        self.enemies = enemies
        self._squad_special_last_ms = -99999
        self._squad_special_gap_ms = 900
        self._squad_focus_target = None
        self._squad_focus_time = 0
        self._squad_focus_hold_ms = 1100
        self._squad_focus_switch_margin = 0.2
        self._squad_focus_min_score = 0.6
        self._squad_focus_hold_floor = 0.45

    def update(self, player, now, hazards=None, projectiles=None, targets=None):
        """Run AI logic for all enemies and return actions."""
        hazards = hazards or []
        projectiles = projectiles or []
        candidates = list(targets) if targets else ([player] if player else [])
        new_projectiles = []
        new_melees = []
        focus_scores: dict[object, float] = {}
        if candidates:
            focus_scores = self._focus_scores(
                candidates,
                hazards,
                list(self.enemies),
                now=now,
            )
            self._squad_focus_target = self._resolve_squad_focus(
                candidates,
                focus_scores,
                now=now,
            )
        special_gap_ms = self._special_gap_ms(focus_scores)
        fired_special = False
        for enemy in list(self.enemies):
            allow_special = (
                now - self._squad_special_last_ms >= special_gap_ms
            ) and not fired_special
            target = (
                self._select_target(
                    enemy,
                    candidates,
                    now,
                    focus_scores,
                    squad_focus_target=self._squad_focus_target,
                ) if candidates else player
            )
            if target is None:
                continue
            proj, melee = enemy.handle_ai(
                target,
                now,
                hazards,
                projectiles,
                squad_focus=focus_scores,
                allow_special=allow_special,
            )
            if proj:
                new_projectiles.append((enemy, proj))
                if getattr(proj, "is_special", False):
                    fired_special = True
                    self._squad_special_last_ms = now
            if melee:
                new_melees.append((enemy, melee))
        return new_projectiles, new_melees

    def _special_gap_ms(self, focus_scores: dict[object, float] | None = None) -> int:
        """Return the squad special cooldown adjusted for pressure."""
        gap = int(self._squad_special_gap_ms)
        enemy_count = len(list(self.enemies))
        if enemy_count >= 4:
            gap -= 180
        elif enemy_count == 3:
            gap -= 100
        if focus_scores:
            peak_focus = max(float(v) for v in focus_scores.values())
            if peak_focus >= 1.25:
                gap -= 140
            elif peak_focus >= 0.95:
                gap -= 70
        return max(420, gap)

    def _resolve_squad_focus(self, candidates, focus_scores, *, now: int) -> object | None:
        """Choose a squad focus target with a short hold window to avoid thrash."""
        if not candidates or not focus_scores:
            self._squad_focus_target = None
            return None
        best_target = max(focus_scores, key=focus_scores.get)
        best_score = float(focus_scores.get(best_target, 0.0))
        current_target = self._squad_focus_target
        if (
            current_target in candidates
            and now - int(self._squad_focus_time) < self._squad_focus_hold_ms
        ):
            current_score = float(focus_scores.get(current_target, 0.0))
            within_margin = (best_score - current_score) <= self._squad_focus_switch_margin
            if current_score >= self._squad_focus_hold_floor and within_margin:
                return current_target
        if best_score < self._squad_focus_min_score:
            self._squad_focus_target = None
            return None
        self._squad_focus_time = int(now)
        return best_target

    @staticmethod
    def _select_target(
        enemy,
        candidates,
        now: int | None = None,
        focus_scores: dict[object, float] | None = None,
        squad_focus_target: object | None = None,
    ):
        if not candidates:
            return None
        preferred = getattr(enemy, "preferred_target", None)
        if preferred in candidates:
            return preferred
        cc_targets = [
            target
            for target in candidates
            if AIManager._crowd_control_score(target, now=now)
        ]
        if cc_targets:
            return min(
                cc_targets,
                key=lambda target: abs(target.rect.centerx - enemy.rect.centerx),
            )
        focus_low = getattr(enemy, "focus_low_health", False)
        if focus_low:
            threshold = float(getattr(enemy, "focus_threshold", 0.35))
            focus_range = float(getattr(enemy, "focus_range", 260))
            low_targets = []
            for target in candidates:
                max_health = getattr(target, "max_health", 0)
                if not max_health:
                    continue
                ratio = getattr(target, "health", 0) / max_health
                dist = abs(target.rect.centerx - enemy.rect.centerx)
                if ratio <= threshold and dist <= focus_range:
                    low_targets.append(target)
            if low_targets:
                return min(
                    low_targets,
                    key=lambda target: abs(target.rect.centerx - enemy.rect.centerx),
                )
        now = 0 if now is None else int(now)

        def _score(target) -> float:
            dist = abs(target.rect.centerx - enemy.rect.centerx)
            max_health = getattr(target, "max_health", 0) or 1
            health_ratio = getattr(target, "health", max_health) / max_health
            recent = getattr(target, "last_hit_time", None)
            recent_bonus = 0.0
            if isinstance(recent, (int, float)) and now - recent < 1200:
                recent_bonus = 30.0
            crowd_bonus = 0.0
            crowd_score = AIManager._crowd_control_score(target, now=now)
            if crowd_score:
                crowd_bonus = 40.0 * crowd_score
            health_weight = 200.0
            if getattr(enemy, "focus_low_health", False):
                health_weight = 260.0
            focus_bonus = 0.0
            if focus_scores and target in focus_scores:
                focus_bonus = 38.0 * focus_scores[target]
            squad_bonus = 0.0
            if squad_focus_target is target and focus_scores:
                squad_bonus = 45.0 * focus_scores.get(target, 0.0)
            return (
                dist
                + health_ratio * health_weight
                - recent_bonus
                - focus_bonus
                - crowd_bonus
                - squad_bonus
            )

        return min(candidates, key=_score)

    @staticmethod
    def _focus_scores(
        candidates,
        hazards,
        enemies=None,
        *,
        now: int | None = None,
    ) -> dict[object, float]:
        scores: dict[object, float] = {}
        enemies = enemies or []
        for target in candidates:
            score = 0.0
            recent = getattr(target, "last_hit_time", None)
            if isinstance(recent, (int, float)):
                score += 0.5
            max_health = getattr(target, "max_health", 0) or 1
            health_ratio = getattr(target, "health", max_health) / max_health
            if health_ratio < 0.5:
                score += 0.6
            score += 0.7 * AIManager._crowd_control_score(target, now=now)
            for hz in hazards or []:
                if not getattr(hz, "avoid", False):
                    continue
                if hz.rect.colliderect(target.rect.inflate(12, 12)):
                    score += 0.4
            if enemies:
                heat = 0.0
                for enemy in enemies:
                    dist = abs(enemy.rect.centerx - target.rect.centerx)
                    if dist < 220:
                        heat += 0.15
                    elif dist < 360:
                        heat += 0.08
                score += min(0.9, heat)
            scores[target] = score
        return scores

    @staticmethod
    def _crowd_control_score(target, *, now: int | None = None) -> float:
        if getattr(target, "stunned", False):
            return 1.0
        if getattr(target, "silenced", False):
            return 0.5
        if now is not None:
            stagger_until = getattr(target, "stagger_until", 0) or 0
            if now < stagger_until:
                return 0.7
        speed_factor = float(getattr(target, "speed_factor", 1.0) or 1.0)
        if speed_factor < 0.75:
            return 0.4
        return 0.0
