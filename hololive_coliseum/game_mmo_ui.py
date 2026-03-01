"""MMO hub UI helpers extracted from the main game class."""

from __future__ import annotations

import math
import random

import pygame

from .mmo_ui import mmo_palette

PALETTE = mmo_palette()


class GameMMOUI:
    """UI helper mixin for MMO hub overlays and panels."""

    def _mmo_draw_panel(self, panel: pygame.Rect) -> dict[str, tuple[int, int, int]]:
        palette = PALETTE
        pygame.draw.rect(self.screen, palette["panel"], panel)
        pygame.draw.rect(self.screen, palette["border"], panel, 2)
        now = pygame.time.get_ticks()
        sweep = pygame.Surface(panel.size, pygame.SRCALPHA)
        offset = (now // 20) % (panel.width + panel.height)
        pygame.draw.line(
            sweep,
            (*palette["neon"], 22),
            (offset - panel.height, 0),
            (offset, panel.height),
            2,
        )
        self.screen.blit(sweep, panel.topleft)
        return palette

    def _mmo_draw_title(
        self,
        text: str,
        x: int,
        y: int,
        *,
        palette: dict[str, tuple[int, int, int]],
    ) -> None:
        shadow = self.menu_font.render(text, True, (10, 16, 24))
        self.screen.blit(shadow, (x + 2, y + 2))
        title = self.menu_font.render(text, True, palette["text"])
        self.screen.blit(title, (x, y))
        pygame.draw.line(
            self.screen,
            palette["idol_pink"],
            (x, y + 28),
            (x + min(260, title.get_width()), y + 28),
            2,
        )

    def _mmo_pulse_color(
        self, base: tuple[int, int, int], now: int, amount: int = 20
    ) -> tuple[int, int, int]:
        pulse = int((math.sin(now / 220) + 1) * 0.5 * amount)
        return (
            min(255, base[0] + pulse),
            min(255, base[1] + pulse),
            min(255, base[2] + pulse),
        )

    def _mmo_draw_row_highlight(
        self, panel: pygame.Rect, y: int, height: int, *, active: bool
    ) -> None:
        if not active:
            return
        palette = mmo_palette()
        now = pygame.time.get_ticks()
        color = self._mmo_pulse_color(palette["border"], now, 16)
        highlight = pygame.Rect(panel.x + 12, y - 2, panel.width - 24, height)
        pygame.draw.rect(self.screen, color, highlight, 0, border_radius=6)
        chip = pygame.Rect(panel.x + 16, y + 2, 10, height - 8)
        pygame.draw.rect(
            self.screen,
            palette["idol_pink"],
            chip,
            0,
            border_radius=4,
        )

    def _mmo_draw_status_badge(
        self,
        panel: pygame.Rect,
        y: int,
        status: str,
        *,
        offset: int = 8,
    ) -> None:
        if not status:
            return
        label = str(status).upper()
        palette = mmo_palette()
        badge_palette = {
            "OPEN": palette["accent"],
            "ACTIVE": palette["neon"],
            "COMPLETE": palette["accent_warm"],
            "IN_TRANSIT": (120, 180, 240),
            "DELIVERED": (180, 220, 160),
        }
        color = badge_palette.get(label, palette["border"])
        text = self.small_font.render(label, True, (12, 16, 22))
        badge = pygame.Rect(0, 0, text.get_width() + 16, text.get_height() + 6)
        badge.topright = (panel.right - offset, y - 4)
        pygame.draw.rect(self.screen, color, badge, 0, border_radius=6)
        pygame.draw.rect(
            self.screen,
            palette["border"],
            badge,
            1,
            border_radius=6,
        )
        self.screen.blit(text, (badge.x + 8, badge.y + 3))

    def _mmo_progress_ratio(self, item: dict[str, object]) -> float:
        eta = float(item.get("eta", 0) or 0)
        total = float(item.get("eta_total", eta) or eta)
        if total <= 0:
            return 0.0
        return max(0.0, min(1.0, 1.0 - eta / total))

    def _mmo_draw_progress_bar(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        ratio: float,
        *,
        color: tuple[int, int, int] = (140, 200, 220),
    ) -> None:
        ratio = max(0.0, min(1.0, ratio))
        palette = mmo_palette()
        outline = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, (50, 70, 90), outline, 1, border_radius=4)
        fill = pygame.Rect(x + 1, y + 1, int((width - 2) * ratio), height - 2)
        if fill.width > 0:
            pygame.draw.rect(self.screen, color, fill, 0, border_radius=4)
            sheen = pygame.Rect(x + 1, y + 1, fill.width, max(1, height // 2))
            pygame.draw.rect(
                self.screen,
                (*palette["accent"], 70),
                sheen,
                0,
                border_radius=4,
            )

    def _mmo_ensure_starfield(self) -> None:
        size = (self.width, self.height)
        if self.mmo_starfield and self.mmo_starfield_size == size:
            return
        rng = random.Random(self.mmo_ai_seed + 101)
        count = max(80, (self.width * self.height) // 9000)
        self.mmo_starfield = []
        for _ in range(count):
            self.mmo_starfield.append(
                {
                    "x": rng.random() * self.width,
                    "y": rng.random() * self.height,
                    "depth": rng.random(),
                    "twinkle": rng.randint(0, 1000),
                }
            )
        self.mmo_starfield_size = size

    def _mmo_draw_starfield(self) -> None:
        self._mmo_ensure_starfield()
        now = pygame.time.get_ticks()
        for star in self.mmo_starfield:
            depth = float(star["depth"])
            drift = now / (6000 + depth * 5000)
            sx = (float(star["x"]) + drift * (0.4 + depth)) % self.width
            sy = (float(star["y"]) + drift * (0.25 + depth)) % self.height
            twinkle = (math.sin((now + int(star["twinkle"])) / 500) + 1) * 0.5
            alpha = 80 + int(120 * twinkle)
            radius = 1 if depth < 0.6 else 2
            pygame.draw.circle(
                self.screen,
                (120, 170, 210, alpha),
                (int(sx), int(sy)),
                radius,
            )

    def _mmo_help_pages(self) -> list[list[str]]:
        return [
            [
                "MMO Hub Help (Core)",
                "Move: WASD/Arrows",
                "Sync: E  Discover: R  Auto-dev: P",
                "Select: Left/Right  Focus: F",
                "Filter: G  Favorite: B",
                "Waypoint: W  Clear: C",
                "Zoom: +/-  Panel: Tab",
                "Overlay Tabs: F1-F12",
                "PageUp/PageDown: Select Lists",
                "Enter: Act  Esc: Main Menu",
            ],
            [
                "MMO Hub Help (Operations)",
                "Events: F11  Contracts: F12",
                "Ops: J  Intel: Z  Guilds: F10",
                "Infrastructure: Shift+D",
                "Patrols: Shift+P  Timeline: Shift+T",
                "Bounties: Shift+B",
                "Influence: Shift+N",
            ],
            [
                "MMO Hub Help (Economy)",
                "Market: K  Orders: Shift+M",
                "Logistics: Shift+L  Survey: Shift+S",
                "Crafting: Shift+C",
                "Fleet: Shift+U",
                "Projects: Shift+H",
                "Academy: Shift+K",
            ],
            [
                "MMO Hub Help (Community)",
                "Favorites: V  Quests: L",
                "Growth: Y  Party: U",
                "Network: N  Notifications: O/F9",
                "Help: H  Settings: T",
            ],
        ]

    def _mmo_draw_overlay_footer(self) -> None:
        if self.mmo_show_tour:
            return
        mode = self.mmo_overlay_mode
        hints = {
            "fleet": "Enter: Assign escort | PageUp/Down: Select | Esc: Back",
            "projects": "Enter: Start/archive | PageUp/Down: Select | Esc: Back",
            "academy": "Enter: Start/archive | PageUp/Down: Select | Esc: Back",
            "bounties": "Enter: Assign/archive | PageUp/Down: Select | Esc: Back",
            "command": "Enter: Assign/archive | PageUp/Down: Select | Esc: Back",
            "contracts": "Enter: Accept | PageUp/Down: Select | Esc: Back",
            "events": "Enter: Respond | PageUp/Down: Select | Esc: Back",
            "logistics": "Enter: Dispatch | PageUp/Down: Select | Esc: Back",
            "crafting": "Enter: Start craft | PageUp/Down: Select | Esc: Back",
            "market_orders": "Enter: Post order | Shift+Enter: Cancel open",
            "influence": "Enter: Invest 25g | PageUp/Down: Select | Esc: Back",
            "expeditions": "Enter: Boost/redeploy | PageUp/Down: Select | Esc: Back",
        }
        text = hints.get(mode)
        if not text:
            return
        padding = 10
        render = self.small_font.render(text, True, (220, 235, 250))
        width = render.get_width() + padding * 2
        height = render.get_height() + 8
        rect = pygame.Rect(20, self.height - height - 18, width, height)
        pygame.draw.rect(self.screen, (18, 28, 42), rect, 0, border_radius=6)
        pygame.draw.rect(self.screen, (60, 90, 120), rect, 1, border_radius=6)
        self.screen.blit(render, (rect.x + padding, rect.y + 4))

    def _mmo_draw_tour(self) -> None:
        if not self.mmo_show_tour:
            return
        steps = [
            "Welcome to the MMO hub. Move with WASD/Arrows.",
            "Use Left/Right to select a region, F to focus.",
            "Press F11 for Events, F12 for Contracts.",
            "Try Shift+U for Fleet, Shift+H for Projects.",
            "Press H for help. Enter advances this tour.",
        ]
        step = min(self.mmo_tour_step, len(steps) - 1)
        panel = pygame.Rect(80, 80, self.width - 160, 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 16
        self._mmo_draw_title("MMO Tour", x, y, palette=palette)
        message = self.menu_font.render(steps[step], True, palette["text"])
        self.screen.blit(message, (x, panel.y + 56))
        footer = self.small_font.render(
            f"Step {step + 1}/{len(steps)}  Enter: Next  Esc: Close",
            True,
            palette["text_dim"],
        )
        self.screen.blit(footer, (x, panel.y + 100))

    def _mmo_set_waypoint(self) -> None:
        region = self._mmo_selected_region()
        if not region:
            self.mmo_message = "No region selected."
            return
        self.mmo_waypoint = {
            "name": region.get("name", "region"),
            "position": region.get("position"),
            "biome": region.get("biome", "n/a"),
        }
        self.mmo_message = f"Waypoint set: {self.mmo_waypoint['name']}."
        self._mmo_log_event(f"Waypoint set: {self.mmo_waypoint['name']}")

    def _mmo_clear_waypoint(self) -> None:
        self.mmo_waypoint = None
        self.mmo_message = "Waypoint cleared."
        self._mmo_log_event("Waypoint cleared.")

    def _mmo_log_event(self, message: str) -> None:
        self.mmo_event_log.append(message)
        if len(self.mmo_event_log) > self.mmo_event_log_limit:
            self.mmo_event_log = self.mmo_event_log[-self.mmo_event_log_limit :]
        self._mmo_floating_message(message)
        self._mmo_notify(message)

    def _mmo_floating_message(self, message: str) -> None:
        self.mmo_floating_messages.append(
            {"text": message, "time": pygame.time.get_ticks()}
        )
        if len(self.mmo_floating_messages) > 6:
            self.mmo_floating_messages = self.mmo_floating_messages[-6:]

    def _mmo_notify(self, message: str, *, level: str = "info") -> None:
        self.mmo_notifications.append(
            {
                "text": message,
                "time": pygame.time.get_ticks(),
                "level": level,
            }
        )
        if len(self.mmo_notifications) > 8:
            self.mmo_notifications = self.mmo_notifications[-8:]

    def _mmo_draw_help(self) -> None:
        panel = pygame.Rect(40, 40, self.width - 80, self.height - 80)
        palette = self._mmo_draw_panel(panel)
        pages = self._mmo_help_pages()
        self.mmo_help_page = max(0, min(self.mmo_help_page, len(pages) - 1))
        lines = pages[self.mmo_help_page]
        x = panel.x + 20
        y = panel.y + 20
        if lines:
            self._mmo_draw_title(lines[0], x, y, palette=palette)
            y += 36
        for line in lines[1:]:
            label = self.menu_font.render(line, True, palette["text"])
            self.screen.blit(label, (x, y))
            y += 28
        footer = self.small_font.render(
            f"Page {self.mmo_help_page + 1}/{len(pages)}  "
            "PageUp/PageDown to switch",
            True,
            palette["text_dim"],
        )
        self.screen.blit(footer, (x, panel.bottom - 32))

    def _mmo_draw_details(self, region: dict[str, object]) -> None:
        panel = pygame.Rect(60, 60, self.width - 120, self.height - 120)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        name = str(region.get("name", "region"))
        self._mmo_draw_title(f"Region: {name}", x, y, palette=palette)
        y += 36
        auto_dev = region.get("auto_dev", {}) if isinstance(region, dict) else {}
        plan_summary = auto_dev.get("auto_dev_plan_summary", {})
        lines = [
            f"Biome: {region.get('biome', 'n/a')}",
            f"Recommended Level: {region.get('recommended_level', 'n/a')}",
            f"Seed: {str(region.get('seed', ''))}",
            f"Focus: {plan_summary.get('hazards', 'n/a')}",
            f"Boss: {plan_summary.get('boss_name', 'n/a')}",
            f"Spawn Tempo: {plan_summary.get('spawn_tempo', 'n/a')}",
            f"Network Upgrades: {plan_summary.get('network_upgrades', 'n/a')}",
        ]
        outpost = next(
            (
                entry
                for entry in self.mmo_outposts
                if entry.get("region") == name
            ),
            None,
        )
        if outpost:
            lines.append(f"Outpost Level: {outpost.get('level', 1)}")
        route_count = sum(
            1
            for route in self.mmo_trade_routes
            if route.get("origin") == name or route.get("destination") == name
        )
        if route_count:
            lines.append(f"Trade Routes: {route_count}")
        op_count = sum(
            1 for op in self.mmo_operations if op.get("region") == name
        )
        if op_count:
            lines.append(f"Active Operations: {op_count}")
        region_events = self._mmo_region_events(name)
        if region_events:
            event = region_events[0]
            lines.append(
                f"Event: {event.get('name', 'Event')} ({event.get('severity', 'n/a')})"
            )
        region_contracts = self._mmo_region_contracts(name)
        if region_contracts:
            contract = region_contracts[0]
            lines.append(
                f"Contract: {contract.get('objective', 'Objective')}"
            )
        weather, upcoming = self._mmo_region_weather(region, pygame.time.get_ticks())
        lines.append(f"Weather: {weather}")
        if upcoming:
            lines.append("Next: " + ", ".join(upcoming))
        resource, richness = self._mmo_region_resources(region)
        lines.append(f"Resource: {resource} (Tier {richness})")
        for line in lines:
            label = self.menu_font.render(line, True, palette["text"])
            self.screen.blit(label, (x, y))
            y += 26
        y += 10
        action_title = self.menu_font.render("Actions", True, palette["text"])
        self.screen.blit(action_title, (x, y))
        y += 26
        for idx, action in enumerate(self.mmo_region_actions):
            color = (
                (255, 220, 140)
                if idx == self.mmo_action_index
                else palette["text"]
            )
            label = self.menu_font.render(action, True, color)
            self.screen.blit(label, (x, y))
            y += 24

    def _mmo_draw_minimap(self, regions: list[dict[str, object]]) -> None:
        size = min(self.width, self.height) // 5
        minimap = pygame.Rect(20, self.height - size - 20, size, size)
        self._mmo_draw_panel(minimap)
        center = minimap.center
        max_radius = max((r.get("radius", 0) for r in regions), default=1)
        scale = (size / 2 - 8) / max(1, max_radius)
        for region in regions:
            pos = region.get("position")
            if not pos or len(pos) != 2:
                continue
            rx = int(center[0] + float(pos[0]) * scale)
            ry = int(center[1] + float(pos[1]) * scale)
            pygame.draw.circle(self.screen, (80, 140, 200), (rx, ry), 2)
        player_pos = self.world_player_manager.get_position(self.mmo_player_id)
        px = int(center[0] + player_pos[0] * scale)
        py = int(center[1] + player_pos[1] * scale)
        pygame.draw.circle(self.screen, (255, 220, 120), (px, py), 3)

    def _mmo_apply_action(self) -> None:
        region = self._mmo_selected_region()
        if not region:
            self.mmo_message = "No region selected."
            return
        action = self.mmo_region_actions[self.mmo_action_index]
        if action == "Teleport":
            self._mmo_focus_selected()
            self._mmo_log_event(f"Teleported to {region.get('name', 'region')}.")
        elif action == "Pin Objective":
            quest = region.get("quest") or {}
            objective = quest.get("objective", "Objective")
            self.mmo_message = f"Pinned: {objective}"
            self._mmo_log_event(f"Objective pinned: {objective}")
        elif action == "Generate Plan":
            self._mmo_generate_plan(pygame.time.get_ticks())
        elif action == "Build Outpost":
            self._mmo_build_outpost(region)
        elif action == "Remove Outpost":
            self._mmo_remove_outpost(region)
        elif action == "Assign Patrol":
            self._mmo_assign_patrol(region)
        elif action == "Open Trade Route":
            self._mmo_open_trade_route(region)
        elif action == "Close Trade Route":
            self._mmo_close_trade_route(region)
        elif action == "Dispatch Operation":
            self._mmo_dispatch_operation(region)
        elif action == "Queue Match":
            self._mmo_queue_match()
        elif action == "Leave Match":
            self._mmo_leave_match()
        elif action == "Accept Match":
            self._mmo_accept_match()
        elif action == "Decline Match":
            self._mmo_decline_match()
        elif action == "Launch Match":
            self._mmo_launch_match()
        elif action == "Migrate Shard":
            self._mmo_migrate_shard()
        elif action == "Cycle Shard":
            self._mmo_cycle_shard_choice()
        elif action == "Confirm Shard":
            self._mmo_confirm_shard_choice()

    def _mmo_draw_event_log(self) -> None:
        if not self.mmo_show_event_log or not self.mmo_event_log:
            return
        palette = mmo_palette()
        panel = pygame.Rect(20, self.height - 156, 360, 128)
        self._mmo_draw_panel(panel)
        x = panel.x + 16
        y = panel.y + 12
        self._mmo_draw_title("Event Log", x, y, palette=palette)
        y += 32
        for entry in self.mmo_event_log[-6:]:
            text = self.menu_font.render(entry, True, palette["text_dim"])
            self.screen.blit(text, (x, y))
            y += 22

    def _mmo_draw_match_overlay(self) -> None:
        if self.mmo_match_status == "idle":
            return
        now = pygame.time.get_ticks()
        palette = mmo_palette()
        status = self.mmo_match_status
        label = f"Match {status.title()}"
        if self.mmo_match_group:
            label += f" ({len(self.mmo_match_group)})"
        sub = ""
        if status == "found" and self.mmo_match_found_at is not None:
            deadline = self.mmo_match_found_at + self.mmo_match_timeout_ms
            remaining = max(0, int((deadline - now) / 1000))
            sub = f"Respond within {remaining}s"
        elif status == "accepted":
            sub = "Awaiting squad confirmations"
        elif status == "ready":
            if self.mmo_match_ready_at is None:
                sub = "All players ready"
            else:
                deadline = (
                    self.mmo_match_ready_at
                    + self.mmo_match_ready_timeout_ms
                )
                remaining = max(0, int((deadline - now) / 1000))
                sub = f"Launch in {remaining}s"
        elif status == "launching":
            sub = "Launch sequence engaged"
        if status == "found":
            hint = "Actions: Accept Match / Decline Match"
        elif status == "ready":
            hint = "Action: Launch Match"
        elif status == "launching":
            hint = "Prepare loadout and launch"
        else:
            hint = "Stand by"
        width = max(280, self.menu_font.size(label)[0] + 60)
        height = 92 if sub else 72
        rect = pygame.Rect(0, 0, width, height)
        rect.centerx = self.width // 2
        rect.y = 76
        panel = pygame.Surface(rect.size, pygame.SRCALPHA)
        panel.fill((*palette["panel_alt"], 232))
        pygame.draw.rect(panel, palette["accent"], panel.get_rect(), 2)
        glow = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(glow, (*palette["accent"], 40), glow.get_rect(), 4)
        panel.blit(glow, (0, 0))
        title = self.menu_font.render(label, True, palette["text"])
        panel.blit(title, (20, 10))
        if sub:
            detail = self.small_font.render(sub, True, palette["text_dim"])
            panel.blit(detail, (20, 34))
            hint_y = 56
        else:
            hint_y = 40
        hint_label = self.small_font.render(hint, True, palette["text_dim"])
        panel.blit(hint_label, (20, hint_y))
        if status == "found" and self.mmo_match_found_at is not None:
            deadline = self.mmo_match_found_at + self.mmo_match_timeout_ms
            remaining = max(0, deadline - now)
            ratio = remaining / max(1, self.mmo_match_timeout_ms)
            bar_y = rect.height - 14
            bar_x = 20
            bar_w = rect.width - 40
            bar_h = 6
            track = pygame.Rect(bar_x, bar_y, bar_w, bar_h)
            pygame.draw.rect(panel, (30, 40, 60), track, 0, border_radius=4)
            fill = pygame.Rect(bar_x, bar_y, int(bar_w * ratio), bar_h)
            if fill.width > 0:
                pygame.draw.rect(
                    panel,
                    palette["accent_hot"],
                    fill,
                    0,
                    border_radius=4,
                )
        elif status == "ready" and self.mmo_match_ready_at is not None:
            deadline = (
                self.mmo_match_ready_at + self.mmo_match_ready_timeout_ms
            )
            remaining = max(0, deadline - now)
            ratio = remaining / max(1, self.mmo_match_ready_timeout_ms)
            bar_y = rect.height - 14
            bar_x = 20
            bar_w = rect.width - 40
            bar_h = 6
            track = pygame.Rect(bar_x, bar_y, bar_w, bar_h)
            pygame.draw.rect(panel, (30, 40, 60), track, 0, border_radius=4)
            fill = pygame.Rect(bar_x, bar_y, int(bar_w * ratio), bar_h)
            if fill.width > 0:
                pygame.draw.rect(
                    panel,
                    palette["accent"],
                    fill,
                    0,
                    border_radius=4,
                )
        self.screen.blit(panel, rect.topleft)

    def _mmo_draw_flash_messages(self) -> None:
        if not self.mmo_flash_messages:
            return
        now = pygame.time.get_ticks()
        self.mmo_flash_messages = [
            msg
            for msg in self.mmo_flash_messages
            if msg.get("expires_at", 0) > now
        ]
        if not self.mmo_flash_messages:
            return
        palette = mmo_palette()
        start_y = 84
        for msg in self.mmo_flash_messages[-3:]:
            text = str(msg.get("text", ""))
            color = msg.get("color", palette["text"])
            remaining = int(msg.get("expires_at", 0)) - now
            alpha = 220 if remaining > 600 else max(
                60, int(220 * remaining / 600)
            )
            label = self.menu_font.render(text, True, color)
            label.set_alpha(alpha)
            padding = 12
            panel = pygame.Rect(
                0,
                0,
                label.get_width() + padding * 2,
                label.get_height() + 8,
            )
            panel.centerx = self.width // 2
            panel.y = start_y
            backdrop = pygame.Surface(panel.size, pygame.SRCALPHA)
            backdrop.fill((*palette["panel"], min(210, alpha)))
            self.screen.blit(backdrop, panel.topleft)
            pygame.draw.rect(
                self.screen,
                palette["border"],
                panel,
                1,
                border_radius=6,
            )
            self.screen.blit(label, (panel.x + padding, panel.y + 4))
            start_y += panel.height + 8

    def _mmo_draw_floating_messages(self) -> None:
        now = pygame.time.get_ticks()
        x = self.width // 2
        y = 80
        for msg in list(self.mmo_floating_messages):
            age = now - int(msg["time"])
            if age > 3000:
                self.mmo_floating_messages.remove(msg)
                continue
            alpha = max(0, 255 - int(age / 3000 * 255))
            palette = mmo_palette()
            text = self.menu_font.render(
                msg["text"], True, palette["accent_warm"]
            )
            text.set_alpha(alpha)
            rect = text.get_rect(center=(x, y))
            panel_rect = rect.inflate(28, 14)
            panel = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
            panel.fill((*palette["panel_alt"], min(190, alpha)))
            pygame.draw.rect(
                panel,
                (*palette["border"], min(220, alpha)),
                panel.get_rect(),
                2,
            )
            pygame.draw.line(
                panel,
                (*palette["idol_pink"], min(220, alpha)),
                (10, panel_rect.height - 6),
                (panel_rect.width - 10, panel_rect.height - 6),
                2,
            )
            self.screen.blit(panel, panel_rect)
            self.screen.blit(text, rect)
            y += 26

    def _mmo_draw_notifications(self) -> None:
        palette = mmo_palette()
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Notifications", x, y, palette=palette)
        y += 32
        for note in self.mmo_notifications[-10:]:
            level = note.get("level", "info")
            color = palette["text"]
            if level == "warn":
                color = palette["accent_warm"]
            elif level == "error":
                color = palette["accent_hot"]
            text = self.menu_font.render(note.get("text", ""), True, color)
            self.screen.blit(text, (x, y))
            y += 24

    def _mmo_draw_market(self) -> None:
        palette = mmo_palette()
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Market Board", x, y, palette=palette)
        y += 32
        for item in getattr(self, "mmo_market_items", []):
            price = self.economy_manager.get_price(item)
            band = "High" if price >= 130 else "Mid" if price >= 70 else "Low"
            label = self.menu_font.render(
                f"{item}: {price}g ({band})", True, palette["text"]
            )
            self.screen.blit(label, (x, y))
            y += 24

    def _mmo_draw_factions(self) -> None:
        palette = mmo_palette()
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Faction Standing", x, y, palette=palette)
        y += 32
        for faction in self.mmo_factions:
            rep = self.reputation_manager.get(faction)
            if rep >= 40:
                status = "Allied"
            elif rep >= 0:
                status = "Neutral"
            else:
                status = "Hostile"
            label = self.menu_font.render(
                f"{faction}: {rep} ({status})", True, palette["text"]
            )
            self.screen.blit(label, (x, y))
            y += 24

    def _mmo_draw_operations(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Operations Board", x, y, palette=palette)
        y += 32
        if not self.mmo_operations:
            label = self.menu_font.render(
                "No active operations.", True, palette["text_dim"]
            )
            self.screen.blit(label, (x, y))
            return
        self.mmo_operation_index = min(
            self.mmo_operation_index,
            len(self.mmo_operations) - 1,
        )
        for idx, op in enumerate(self.mmo_operations[:12]):
            self._mmo_draw_row_highlight(panel, y, 22, active=idx == self.mmo_operation_index)
            name = op.get("name", "Operation")
            region = op.get("region", "region")
            status = op.get("status", "active")
            eta = op.get("eta", "?")
            priority = op.get("priority", "Medium")
            risk = op.get("risk", "Medium")
            color = (
                palette["accent_warm"]
                if idx == self.mmo_operation_index
                else palette["text"]
            )
            label = self.menu_font.render(
                f"{name} | {region} | {status} | ETA {eta}", True, color
            )
            self.screen.blit(label, (x, y))
            self._mmo_draw_status_badge(panel, y, status)
            y += 24
            detail = self.small_font.render(
                f"Priority: {priority} | Risk: {risk}", True, palette["text_dim"]
            )
            self.screen.blit(detail, (x + 16, y))
            y += 20

    def _mmo_draw_hub_settings(self) -> None:
        palette = mmo_palette()
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Hub Settings", x, y, palette=palette)
        y += 32
        lines = [
            f"Panel: {'On' if self.mmo_ui_show_panel else 'Off'} (Tab)",
            f"Minimap: {'On' if self.mmo_show_minimap else 'Off'} (M)",
            f"Event Log: {'On' if self.mmo_show_event_log else 'Off'} (X)",
            f"Notifications: {len(self.mmo_notifications)} (O/F9)",
            f"Guilds: {len(self.mmo_guilds)} (F10)",
            f"Events: {len(self.mmo_world_events)} (F11)",
            f"Contracts: {len(self.mmo_contracts)} (F12)",
            f"Sort Mode: {self.mmo_sort_mode.title()} (S)",
            f"Intel Overlay: {'On' if self.mmo_overlay_mode == 'intel' else 'Off'} (Z)",
            f"Infrastructure: {len(self.mmo_outposts)} (Shift+D)",
            f"Patrols: {len(self.mmo_auto_agents)} (Shift+P)",
            f"Timeline: {len(self.mmo_contracts) + len(self.mmo_operations)} (Shift+T)",
            f"Logistics: {sum(self.mmo_stockpile.values())} (Shift+L)",
            f"Survey: {len(self._mmo_survey_items())} (Shift+S)",
            f"Diplomacy: {len(self.mmo_factions)} (Shift+F)",
            f"Research: {self.mmo_ai_level} (Shift+R)",
            f"Crafting Queue: {len(self.mmo_crafting_queue)} (Shift+C)",
            f"Market Orders: {len(self.mmo_market_orders)} (Shift+M)",
            f"Strategy: {self.mmo_strategy.get('focus', 'resources')} (Shift+G)",
            f"Campaigns: {len(self.mmo_campaign_status)} (Shift+Y)",
            f"Expeditions: {len(self.mmo_expeditions)} (Shift+E)",
            f"Roster: {len(self._mmo_roster_entries())} (Shift+O)",
            f"Alerts: {len(self.mmo_alerts)} (Shift+A)",
            f"Command: {len(self.mmo_directives)} (Shift+X)",
            f"Bounties: {len(self.mmo_bounties)} (Shift+B)",
            f"Influence: {len(self.mmo_influence)} (Shift+N)",
            f"Fleet: {len(self.mmo_shipments)} (Shift+U)",
            f"Projects: {len(self.mmo_projects)} (Shift+H)",
            f"Academy: {len(self.mmo_training_queue)} (Shift+K)",
            "Account Center: Ctrl+A",
            "Account Audit: Ctrl+L",
            f"Routes: {'On' if self.mmo_layers.get('routes') else 'Off'} (1)",
            f"Outposts: {'On' if self.mmo_layers.get('outposts') else 'Off'} (2)",
            f"Event Markers: {'On' if self.mmo_layers.get('events') else 'Off'} (3)",
            f"Contract Markers: {'On' if self.mmo_layers.get('contracts') else 'Off'} (4)",
            f"Agents: {'On' if self.mmo_layers.get('agents') else 'Off'} (5)",
            f"Remotes: {'On' if self.mmo_layers.get('remotes') else 'Off'} (6)",
            f"Heatmap: {'On' if self.mmo_layers.get('heatmap') else 'Off'} (7)",
            f"Resources: {'On' if self.mmo_layers.get('resources') else 'Off'} (8)",
            f"Expeditions: {'On' if self.mmo_layers.get('expeditions') else 'Off'} (9)",
            f"Bounties: {'On' if self.mmo_layers.get('bounties') else 'Off'} (0)",
        ]
        for line in lines:
            label = self.menu_font.render(line, True, PALETTE["text"])
            self.screen.blit(label, (x, y))
            y += 24

    def _mmo_draw_guilds(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Guild Registry", x, y, palette=palette)
        y += 32
        for guild in self.mmo_guilds:
            name = guild.get("name", "Guild")
            focus = guild.get("focus", "Focus")
            rank = guild.get("rank", "Rank")
            rep = self.reputation_manager.get(str(name))
            line = f"{name} | {focus} | {rank} | REP {rep}"
            label = self.menu_font.render(line, True, PALETTE["text"])
            self.screen.blit(label, (x, y))
            y += 24

    def _mmo_draw_events(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("World Events", x, y, palette=palette)
        y += 32
        if not self.mmo_world_events:
            label = self.menu_font.render("No active events.", True, palette["text_dim"])
            self.screen.blit(label, (x, y))
            return
        self.mmo_event_index = min(
            self.mmo_event_index,
            len(self.mmo_world_events) - 1,
        )
        now = pygame.time.get_ticks()
        for idx, event in enumerate(self.mmo_world_events[:12]):
            self._mmo_draw_row_highlight(panel, y, 22, active=idx == self.mmo_event_index)
            name = event.get("name", "Event")
            region = event.get("region", "region")
            severity = event.get("severity", "n/a")
            remaining = max(0, int((event.get("expires_at", 0) - now) / 1000))
            line = f"{name} | {region} | {severity} | {remaining}s"
            color = (
                palette["accent_warm"]
                if idx == self.mmo_event_index
                else palette["text"]
            )
            label = self.menu_font.render(line, True, color)
            self.screen.blit(label, (x, y))
            self._mmo_draw_status_badge(panel, y, str(severity))
            y += 24

    def _mmo_draw_contracts(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Contracts Board", x, y, palette=palette)
        y += 32
        if not self.mmo_contracts:
            label = self.menu_font.render(
                "No active contracts.", True, palette["text_dim"]
            )
            self.screen.blit(label, (x, y))
            return
        self.mmo_contract_index = min(
            self.mmo_contract_index,
            len(self.mmo_contracts) - 1,
        )
        for idx, contract in enumerate(self.mmo_contracts[:12]):
            self._mmo_draw_row_highlight(panel, y, 22, active=idx == self.mmo_contract_index)
            name = contract.get("name", "Contract")
            region = contract.get("region", "region")
            status = contract.get("status", "active")
            reward = contract.get("reward", 0)
            objective = contract.get("objective", "Objective")
            difficulty = contract.get("difficulty", "Medium")
            line = f"{name} | {region} | {difficulty} | {status} | {reward}g"
            color = (
                palette["accent_warm"]
                if idx == self.mmo_contract_index
                else palette["text"]
            )
            label = self.menu_font.render(line, True, color)
            self.screen.blit(label, (x, y))
            self._mmo_draw_status_badge(panel, y, status)
            y += 24
            detail = self.small_font.render(
                f"Objective: {objective}", True, palette["text_dim"]
            )
            self.screen.blit(detail, (x + 16, y))
            y += 20

    def _mmo_draw_intel(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Regional Intel", x, y, palette=palette)
        y += 32
        regions = self._mmo_regions()
        if not regions:
            label = self.menu_font.render("No regions available.", True, PALETTE["text"])
            self.screen.blit(label, (x, y))
            return
        ranked = sorted(regions, key=self._mmo_region_threat, reverse=True)[:8]
        now = pygame.time.get_ticks()
        for region in ranked:
            name = region.get("name", "region")
            threat = self._mmo_region_threat(region)
            weather, upcoming = self._mmo_region_weather(region, now)
            next_weather = ", ".join(upcoming) if upcoming else "n/a"
            line = f"{name} | Threat {threat:.1f} | Weather {weather}"
            label = self.menu_font.render(line, True, PALETTE["text"])
            self.screen.blit(label, (x, y))
            y += 24
            detail = self.menu_font.render(
                f"Next: {next_weather}", True, PALETTE["text_dim"]
            )
            self.screen.blit(detail, (x + 16, y))
            y += 22
            trend = self._mmo_threat_trend(str(name))
            trend_label = self.small_font.render(
                f"Trend: {trend}", True, (160, 190, 220)
            )
            self.screen.blit(trend_label, (x + 16, y))
            y += 20

    def _mmo_draw_infrastructure(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        title = self.menu_font.render(
            "Infrastructure Overview", True, PALETTE["text"]
        )
        self.screen.blit(title, (x, y))
        y += 32
        items = self._mmo_infra_items()
        if not items:
            label = self.menu_font.render("No infrastructure yet.", True, PALETTE["text"])
            self.screen.blit(label, (x, y))
            return
        self.mmo_infra_index = min(self.mmo_infra_index, len(items) - 1)
        for idx, item in enumerate(items[:12]):
            if item["kind"] == "outpost":
                text = (
                    f"Outpost {item.get('region', 'region')} "
                    f"L{item['data'].get('level', 1)}"
                )
            else:
                text = (
                    f"Route {item.get('origin', '')} -> {item.get('destination', '')}"
                    f" ({item['data'].get('status', 'active')})"
                )
            color = (255, 220, 140) if idx == self.mmo_infra_index else PALETTE["text"]
            label = self.menu_font.render(text, True, color)
            self.screen.blit(label, (x, y))
            y += 24

    def _mmo_draw_patrols(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Patrol Monitor", x, y, palette=palette)
        y += 32
        focus_name = self.mmo_focus_region_name or "n/a"
        focus_line = self.small_font.render(
            f"Focus Region: {focus_name}", True, PALETTE["text_dim"]
        )
        self.screen.blit(focus_line, (x, y))
        y += 24
        entries = self._mmo_patrol_entries()
        if not entries:
            label = self.menu_font.render("No patrols active.", True, PALETTE["text"])
            self.screen.blit(label, (x, y))
            return
        self.mmo_patrol_index = min(self.mmo_patrol_index, len(entries) - 1)
        for idx, entry in enumerate(entries[:12]):
            target = entry.get("target")
            target_text = ""
            if isinstance(target, (list, tuple)) and len(target) == 2:
                target_text = f" -> {target[0]:.2f},{target[1]:.2f}"
            assignment = entry.get("assignment") or "Unassigned"
            text = (
                f"{entry.get('id')} | dist {entry.get('distance', 0):.2f}"
                f"{target_text}"
            )
            color = (255, 220, 140) if idx == self.mmo_patrol_index else PALETTE["text"]
            label = self.menu_font.render(text, True, color)
            self.screen.blit(label, (x, y))
            y += 24
            detail = self.small_font.render(
                f"Assignment: {assignment}", True, PALETTE["text_dim"]
            )
            self.screen.blit(detail, (x + 16, y))
            y += 20

    def _mmo_draw_timeline(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Operations Timeline", x, y, palette=palette)
        y += 32
        items = self._mmo_timeline_items(pygame.time.get_ticks())
        if not items:
            label = self.menu_font.render("No upcoming tasks.", True, PALETTE["text"])
            self.screen.blit(label, (x, y))
            return
        self.mmo_timeline_index = min(self.mmo_timeline_index, len(items) - 1)
        for idx, item in enumerate(items[:12]):
            line = (
                f"{item['type']} | {item.get('name')} | "
                f"{item.get('region')} | {item.get('remaining', 0)}s"
            )
            color = (255, 220, 140) if idx == self.mmo_timeline_index else PALETTE["text"]
            label = self.menu_font.render(line, True, color)
            self.screen.blit(label, (x, y))
            y += 24

    def _mmo_draw_logistics(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Logistics Ledger", x, y, palette=palette)
        y += 32
        stockpile = sorted(
            self.mmo_stockpile.items(),
            key=lambda item: item[1],
            reverse=True,
        )
        if not stockpile:
            label = self.menu_font.render("No stockpile yet.", True, PALETTE["text"])
            self.screen.blit(label, (x, y))
            return
        route_active = sum(
            1 for route in self.mmo_trade_routes
            if route.get("status", "active") == "active"
        )
        label = self.menu_font.render(
            f"Active Routes: {route_active}", True, PALETTE["text_dim"]
        )
        self.screen.blit(label, (x, y))
        y += 26
        self.mmo_logistics_index = min(self.mmo_logistics_index, len(stockpile) - 1)
        for idx, (resource, amount) in enumerate(stockpile[:12]):
            color = (255, 220, 140) if idx == self.mmo_logistics_index else PALETTE["text"]
            label = self.menu_font.render(
                f"{resource}: {amount}", True, color
            )
            self.screen.blit(label, (x, y))
            y += 24
        if self.mmo_shipments:
            y += 12
            label = self.menu_font.render("Shipments", True, PALETTE["text"])
            self.screen.blit(label, (x, y))
            y += 26
            for shipment in self.mmo_shipments[:6]:
                line = (
                    f"{shipment.get('resource')} -> {shipment.get('destination')}"
                    f" ({shipment.get('eta')}s)"
                )
                label = self.menu_font.render(line, True, PALETTE["text_dim"])
                self.screen.blit(label, (x, y))
                y += 22

    def _mmo_draw_survey(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Resource Survey", x, y, palette=palette)
        y += 32
        items = self._mmo_survey_items()
        if not items:
            label = self.menu_font.render("No survey data.", True, PALETTE["text"])
            self.screen.blit(label, (x, y))
            return
        self.mmo_survey_index = min(self.mmo_survey_index, len(items) - 1)
        for idx, item in enumerate(items[:12]):
            line = (
                f"{item['region']} | {item['resource']} | Tier {item['richness']}"
            )
            color = (255, 220, 140) if idx == self.mmo_survey_index else PALETTE["text"]
            label = self.menu_font.render(line, True, color)
            self.screen.blit(label, (x, y))
            y += 24

    def _mmo_draw_diplomacy(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Diplomacy Board", x, y, palette=palette)
        y += 32
        for faction in self.mmo_factions:
            rep = self.reputation_manager.get(faction)
            label = self.menu_font.render(
                f"{faction}: {rep}", True, PALETTE["text"]
            )
            self.screen.blit(label, (x, y))
            y += 24
        y += 8
        regions = sorted(
            self._mmo_regions(),
            key=lambda r: self._mmo_region_influence(r)[1],
            reverse=True,
        )
        for region in regions[:6]:
            faction, influence = self._mmo_region_influence(region)
            line = f"{region.get('name', 'region')} | {faction} | {influence}"
            label = self.menu_font.render(line, True, PALETTE["text_dim"])
            self.screen.blit(label, (x, y))
            y += 22

    def _mmo_draw_research(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Research Console", x, y, palette=palette)
        y += 32
        lines = [
            f"Mining Seeds: {self.mining_manager.mined}",
            f"AI Playthroughs: {self.ai_playthroughs}",
            f"AI Level: {self.mmo_ai_level}",
        ]
        focus = {}
        try:
            focus = self.auto_dev_manager.region_insight()
        except Exception:
            focus = {}
        if isinstance(focus, dict):
            hazard = focus.get("trending_hazard")
            if hazard:
                lines.append(f"Trending Hazard: {hazard}")
            favorite = focus.get("favorite_character")
            if favorite:
                lines.append(f"Favorite Fighter: {favorite}")
        plan = self.mmo_backend.latest_plan() or {}
        summary = plan.get("summary", {}) if isinstance(plan, dict) else {}
        if summary:
            lines.append(f"Plan Focus: {summary.get('focus', 'n/a')}")
            lines.append(f"Boss: {summary.get('boss', 'n/a')}")
            lines.append(f"Security: {summary.get('network_security_score', 'n/a')}")
        for line in lines:
            label = self.menu_font.render(line, True, PALETTE["text"])
            self.screen.blit(label, (x, y))
            y += 24

    def _mmo_draw_crafting(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Crafting Lab", x, y, palette=palette)
        y += 32
        recipes = self._mmo_recipes()
        if not recipes:
            label = self.menu_font.render("No recipes available.", True, PALETTE["text"])
            self.screen.blit(label, (x, y))
            return
        self.mmo_crafting_index = min(self.mmo_crafting_index, len(recipes) - 1)
        for idx, recipe in enumerate(recipes[:8]):
            can_craft = self._mmo_can_craft(recipe)
            color = (255, 220, 140) if idx == self.mmo_crafting_index else PALETTE["text"]
            if not can_craft:
                color = (160, 170, 190)
            label = self.menu_font.render(recipe.get("name", "Craft"), True, color)
            self.screen.blit(label, (x, y))
            y += 24
        y += 10
        if self.mmo_crafting_queue:
            queue_label = self.menu_font.render("Queue", True, PALETTE["text"])
            self.screen.blit(queue_label, (x, y))
            y += 26
            for entry in self.mmo_crafting_queue[:6]:
                line = (
                    f"{entry.get('name', 'Craft')} | {entry.get('status')} | "
                    f"{entry.get('eta', 0)}s"
                )
                label = self.menu_font.render(line, True, PALETTE["text_dim"])
                self.screen.blit(label, (x, y))
                y += 22

    def _mmo_draw_market_orders(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Market Orders", x, y, palette=palette)
        y += 32
        label = self.menu_font.render(
            f"Credits: {self.mmo_credits}", True, PALETTE["text"]
        )
        self.screen.blit(label, (x, y))
        y += 26
        resources = sorted(self.mmo_stockpile.keys())
        if not resources:
            label = self.menu_font.render("No stock to trade.", True, PALETTE["text"])
            self.screen.blit(label, (x, y))
            return
        self.mmo_market_index = min(self.mmo_market_index, len(resources) - 1)
        for idx, resource in enumerate(resources[:8]):
            color = (255, 220, 140) if idx == self.mmo_market_index else PALETTE["text"]
            price = self.economy_manager.get_price(resource)
            label = self.menu_font.render(f"{resource} | {price}g", True, color)
            self.screen.blit(label, (x, y))
            y += 24
        y += 10
        if self.mmo_market_orders:
            orders_label = self.menu_font.render("Orders", True, PALETTE["text"])
            self.screen.blit(orders_label, (x, y))
            y += 26
            for order in self.mmo_market_orders[:6]:
                status = order.get("status", "open")
                eta = order.get("eta", 0)
                expires = order.get("expires_in", 0)
                line = (
                    f"{order.get('kind')} {order.get('quantity')} "
                    f"{order.get('resource')} | {status} | "
                    f"ETA {eta}s | EXP {expires}s"
                )
                label = self.menu_font.render(line, True, PALETTE["text_dim"])
                self.screen.blit(label, (x, y))
                y += 22

    def _mmo_draw_strategy(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Strategy Console", x, y, palette=palette)
        y += 32
        focus = self.mmo_strategy.get("focus", "resources")
        mode = self.mmo_strategy.get("mode", "balanced")
        lines = [
            f"Focus: {focus.title()}",
            f"Mode: {mode.title()}",
            "Enter: Cycle Focus",
        ]
        for line in lines:
            label = self.menu_font.render(line, True, PALETTE["text"])
            self.screen.blit(label, (x, y))
            y += 24

    def _mmo_draw_campaign(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Campaign Board", x, y, palette=palette)
        y += 32
        for campaign in self._mmo_campaigns():
            name = str(campaign.get("name", "Campaign"))
            stat_key = str(campaign.get("stat", ""))
            target = int(campaign.get("target", 0))
            current = int(self.mmo_stats.get(stat_key, 0))
            reward = int(campaign.get("reward", 0))
            status = "Complete" if self.mmo_campaign_status.get(name) else "Active"
            line = f"{name} | {current}/{target} | {reward}g | {status}"
            label = self.menu_font.render(line, True, PALETTE["text"])
            self.screen.blit(label, (x, y))
            y += 24

    def _mmo_tab_layout(self) -> tuple[list[list[tuple[str, str, str]]], int]:
        tabs = [
            ("F1", "Overview", "overview"),
            ("F2", "Details", "details"),
            ("F3", "Favorites", "favorites"),
            ("F4", "Quests", "quests"),
            ("F5", "Growth", "growth"),
            ("F6", "Party", "party"),
            ("F7", "Network", "network"),
            ("F8", "Help", "help"),
            ("F9", "Notifications", "notifications"),
            ("F10", "Guilds", "guilds"),
            ("F11", "Events", "events"),
            ("F12", "Contracts", "contracts"),
            ("Z", "Intel", "intel"),
            ("Shift+D", "Infra", "infrastructure"),
            ("Shift+P", "Patrols", "patrols"),
            ("Shift+T", "Timeline", "timeline"),
            ("Shift+L", "Logistics", "logistics"),
            ("Shift+S", "Survey", "survey"),
            ("Shift+F", "Diplomacy", "diplomacy"),
            ("Shift+R", "Research", "research"),
            ("Shift+C", "Crafting", "crafting"),
            ("Shift+M", "Orders", "market_orders"),
            ("Shift+G", "Strategy", "strategy"),
            ("Shift+Y", "Campaign", "campaign"),
            ("Shift+E", "Expeditions", "expeditions"),
            ("Shift+O", "Roster", "roster"),
            ("Shift+A", "Alerts", "alerts"),
            ("Shift+X", "Command", "command"),
            ("Shift+B", "Bounties", "bounties"),
            ("Shift+N", "Influence", "influence"),
            ("Shift+U", "Fleet", "fleet"),
            ("Shift+H", "Projects", "projects"),
            ("Shift+K", "Academy", "academy"),
            ("K", "Market", "market"),
            ("Q", "Factions", "factions"),
            ("J", "Ops", "operations"),
            ("T", "Settings", "hub_settings"),
        ]
        max_width = self.width - 40
        rows: list[list[tuple[str, str, str]]] = [[]]
        row_width = 0
        for key, label, mode in tabs:
            text = f"{key}:{label}"
            entry_width = self.menu_font.size(text)[0] + 16
            if rows[-1] and row_width + entry_width > max_width:
                rows.append([])
                row_width = 0
            rows[-1].append((key, label, mode))
            row_width += entry_width
        bar_height = 8 + 24 * len(rows)
        return rows, bar_height

    def _mmo_draw_tab_bar(self) -> None:
        rows, bar_height = self._mmo_tab_layout()
        bar_rect = pygame.Rect(10, 10, self.width - 20, bar_height)
        palette = self._mmo_draw_panel(bar_rect)
        y = bar_rect.y + 4
        for row in rows:
            x = bar_rect.x + 10
            for key, label, mode in row:
                active = self.mmo_overlay_mode == mode
                text = f"{key}:{label}"
                color = palette["accent_warm"] if active else palette["text_dim"]
                render = self.menu_font.render(text, True, color)
                self.screen.blit(render, (x, y))
                x += render.get_width() + 16
            y += 24

    def _mmo_draw_favorites(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Favorite Regions", x, y, palette=palette)
        y += 32
        favorites = sorted(self.mmo_favorites)
        if not favorites:
            label = self.menu_font.render("No favorites yet.", True, palette["text"])
            self.screen.blit(label, (x, y))
            return
        for name in favorites:
            label = self.menu_font.render(name, True, palette["text"])
            self.screen.blit(label, (x, y))
            y += 24

    def _clear_mmo_toggles(self) -> None:
        self.mmo_show_details = False
        self.mmo_show_help = False
        self.mmo_show_favorites = False
        self.mmo_show_quest_log = False
        self.mmo_show_growth = False
        self.mmo_show_party = False
        self.mmo_show_network = False
        self.mmo_show_notifications = False
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

    def _mmo_draw_quest_log(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Quest Log", x, y, palette=palette)
        y += 32
        regions = self._mmo_regions()
        quests = []
        for region in regions:
            quest = region.get("quest") or {}
            if isinstance(quest, dict) and quest:
                quests.append((region.get("name", "region"), quest))
        if not quests:
            label = self.menu_font.render("No quests found.", True, PALETTE["text"])
            self.screen.blit(label, (x, y))
            return
        for name, quest in quests[:12]:
            qname = quest.get("name", "Quest")
            objective = quest.get("objective", "Objective")
            label = self.menu_font.render(f"{name}: {qname}", True, PALETTE["text"])
            self.screen.blit(label, (x, y))
            y += 24
            detail = self.menu_font.render(f"- {objective}", True, PALETTE["text_dim"])
            self.screen.blit(detail, (x + 16, y))
            y += 22

    def _mmo_draw_growth_report(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Growth Report", x, y, palette=palette)
        y += 32
        regions = self.world_generation_manager.region_manager.get_regions()
        auto_dev_count = sum(
            1 for region in regions if isinstance(region.get("auto_dev"), dict)
        )
        lines = [
            f"Regions Generated: {len(regions)}",
            f"Auto-dev Regions: {auto_dev_count}",
            f"Mining Seeds: {self.mining_manager.mined}",
            f"AI Playthroughs: {self.ai_playthroughs}",
            f"AI Level: {self.mmo_ai_level}",
        ]
        for line in lines:
            label = self.menu_font.render(line, True, PALETTE["text"])
            self.screen.blit(label, (x, y))
            y += 24

    def _mmo_draw_party(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Party Status", x, y, palette=palette)
        y += 32
        roster = [self.mmo_player_id]
        roster += sorted(self.mmo_remote_positions.keys())
        for name in roster:
            label = self.menu_font.render(name, True, PALETTE["text"])
            self.screen.blit(label, (x, y))
            y += 24
        if self.mmo_auto_agents:
            y += 12
            agents_label = self.menu_font.render(
                f"Agents: {len(self.mmo_auto_agents)}", True, PALETTE["text_dim"]
            )
            self.screen.blit(agents_label, (x, y))

    def _mmo_draw_network_status(self) -> None:
        palette = mmo_palette()
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Network & Shards", x, y, palette=palette)
        y += 32
        if self.network_manager is None:
            label = self.menu_font.render("Offline", True, palette["text_dim"])
            self.screen.blit(label, (x, y))
            return
        nodes = getattr(self.network_manager.node_manager, "load_nodes", lambda: [])()
        label = self.menu_font.render(
            f"Nodes: {len(nodes)}", True, palette["text"]
        )
        self.screen.blit(label, (x, y))
        y += 26
        label = self.menu_font.render(
            f"Peers: {len(self.mmo_remote_positions)}", True, palette["text"]
        )
        self.screen.blit(label, (x, y))
        y += 26
        mode = "Auto" if self.mmo_shard_mode == "auto" else "Fixed"
        mode_label = self.menu_font.render(
            f"Shard Mode: {mode}", True, palette["text"]
        )
        self.screen.blit(mode_label, (x, y))
        y += 26
        shard_line = self.menu_font.render(
            f"Active Shard: {self.mmo_shard_id}", True, palette["text"]
        )
        self.screen.blit(shard_line, (x, y))
        y += 28
        shard_title = self.menu_font.render("Shard Health", True, palette["accent"])
        self.screen.blit(shard_title, (x, y))
        y += 26
        shards = [f"shard-{idx + 1}" for idx in range(self.mmo_shard_count)]
        shard_loads = [
            (name, self.mmo_shard_stats.get(name, 0)) for name in shards
        ]
        selected = (
            shards[self.mmo_shard_choice_index % len(shards)]
            if shards
            else None
        )
        shard_loads.sort(key=lambda item: (item[1] or 10 ** 9, item[0]))
        suggested = shard_loads[0][0] if shard_loads else "n/a"
        for idx, (name, load) in enumerate(shard_loads[:6]):
            tag = []
            if name == self.mmo_shard_id:
                tag.append("active")
            if selected and name == selected:
                tag.append("selected")
            suffix = f" ({', '.join(tag)})" if tag else ""
            load_text = "n/a" if not load else str(load)
            line = f"{name}: {load_text}{suffix}"
            color = palette["accent_warm"] if "selected" in tag else palette["text"]
            label = self.menu_font.render(line, True, color)
            self.screen.blit(label, (x, y))
            y += 22
        y += 6
        rec = self.small_font.render(
            f"Suggested: {suggested}", True, palette["text_dim"]
        )
        self.screen.blit(rec, (x, y))
        y += 22
        hints = [
            "Actions: Cycle Shard / Confirm Shard",
            "Auto mode migrates on load delta threshold",
        ]
        for line in hints:
            hint = self.small_font.render(line, True, palette["text_dim"])
            self.screen.blit(hint, (x, y))
            y += 18

    def _mmo_draw_expeditions(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Expeditions", x, y, palette=palette)
        y += 32
        if not self.mmo_expeditions:
            label = self.menu_font.render(
                "No expeditions queued.", True, PALETTE["text"]
            )
            self.screen.blit(label, (x, y))
            return
        self.mmo_expedition_index = min(
            self.mmo_expedition_index,
            len(self.mmo_expeditions) - 1,
        )
        for idx, expedition in enumerate(self.mmo_expeditions[:10]):
            self._mmo_draw_row_highlight(panel, y, 22, active=idx == self.mmo_expedition_index)
            name = expedition.get("name", "Expedition")
            region = expedition.get("region", "region")
            status = expedition.get("status", "idle")
            eta = expedition.get("eta", "?")
            risk = expedition.get("risk", "n/a")
            color = (
                (255, 220, 140)
                if idx == self.mmo_expedition_index
                else PALETTE["text"]
            )
            line = f"{name} | {region} | {status} | ETA {eta} | {risk}"
            label = self.menu_font.render(line, True, color)
            self.screen.blit(label, (x, y))
            self._mmo_draw_status_badge(panel, y, status)
            ratio = self._mmo_progress_ratio(expedition)
            self._mmo_draw_progress_bar(
                panel.x + 24, y + 22, panel.width - 60, 6, ratio
            )
            y += 24
            team = expedition.get("team", [])
            if team:
                team_line = f"Team: {', '.join(team)}"
                detail = self.menu_font.render(
                    team_line, True, PALETTE["text_dim"]
                )
                self.screen.blit(detail, (x + 16, y))
                y += 22

    def _mmo_draw_roster(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Roster", x, y, palette=palette)
        y += 32
        entries = self._mmo_roster_entries()
        if not entries:
            label = self.menu_font.render("No roster entries.", True, PALETTE["text"])
            self.screen.blit(label, (x, y))
            return
        self.mmo_roster_index = min(
            self.mmo_roster_index,
            len(entries) - 1,
        )
        for idx, entry in enumerate(entries[:12]):
            self._mmo_draw_row_highlight(panel, y, 22, active=idx == self.mmo_roster_index)
            name = entry.get("name", "member")
            role = entry.get("role", "role")
            status = entry.get("status", "active")
            color = (
                (255, 220, 140)
                if idx == self.mmo_roster_index
                else PALETTE["text"]
            )
            label = self.menu_font.render(
                f"{name} | {role} | {status}", True, color
            )
            self.screen.blit(label, (x, y))
            self._mmo_draw_status_badge(panel, y, status)
            y += 24
            pos = entry.get("pos")
            if isinstance(pos, (list, tuple)) and len(pos) == 2:
                pos_line = f"Pos: {pos[0]:.2f}, {pos[1]:.2f}"
                detail = self.menu_font.render(
                    pos_line, True, PALETTE["text_dim"]
                )
                self.screen.blit(detail, (x + 16, y))
                y += 22

    def _mmo_draw_command(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Command Deck", x, y, palette=palette)
        y += 32
        if not self.mmo_directives:
            label = self.menu_font.render(
                "No directives available.", True, PALETTE["text"]
            )
            self.screen.blit(label, (x, y))
            return
        self.mmo_directive_index = min(
            self.mmo_directive_index,
            len(self.mmo_directives) - 1,
        )
        for idx, directive in enumerate(self.mmo_directives[:10]):
            self._mmo_draw_row_highlight(panel, y, 22, active=idx == self.mmo_directive_index)
            entry = directive.get("id", "Directive")
            kind = directive.get("kind", "Task")
            region = directive.get("region", "region")
            status = directive.get("status", "open")
            eta = directive.get("eta", "?")
            assignee = directive.get("assignee") or "unassigned"
            color = (
                (255, 220, 140)
                if idx == self.mmo_directive_index
                else PALETTE["text"]
            )
            line = f"{entry} | {kind} | {region} | {status} | ETA {eta}"
            label = self.menu_font.render(line, True, color)
            self.screen.blit(label, (x, y))
            self._mmo_draw_status_badge(panel, y, status)
            ratio = self._mmo_progress_ratio(directive)
            self._mmo_draw_progress_bar(
                panel.x + 24, y + 22, panel.width - 60, 6, ratio
            )
            y += 24
            detail = self.menu_font.render(
                f"Assignee: {assignee}", True, PALETTE["text_dim"]
            )
            self.screen.blit(detail, (x + 16, y))
            y += 22

    def _mmo_draw_bounties(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Bounties", x, y, palette=palette)
        y += 32
        if not self.mmo_bounties:
            label = self.menu_font.render(
                "No bounties available.", True, PALETTE["text"]
            )
            self.screen.blit(label, (x, y))
            return
        self.mmo_bounty_index = min(
            self.mmo_bounty_index,
            len(self.mmo_bounties) - 1,
        )
        for idx, bounty in enumerate(self.mmo_bounties[:10]):
            self._mmo_draw_row_highlight(panel, y, 22, active=idx == self.mmo_bounty_index)
            entry = bounty.get("id", "Bounty")
            name = bounty.get("name", "Target")
            region = bounty.get("region", "region")
            threat = bounty.get("threat", "n/a")
            status = bounty.get("status", "open")
            eta = bounty.get("eta", "?")
            reward = bounty.get("reward", 0)
            color = (
                (255, 220, 140)
                if idx == self.mmo_bounty_index
                else PALETTE["text"]
            )
            line = (
                f"{entry} | {name} | {region} | {status} | ETA {eta} | {threat}"
            )
            label = self.menu_font.render(line, True, color)
            self.screen.blit(label, (x, y))
            self._mmo_draw_status_badge(panel, y, status)
            ratio = self._mmo_progress_ratio(bounty)
            self._mmo_draw_progress_bar(
                panel.x + 24, y + 22, panel.width - 60, 6, ratio
            )
            y += 24
            detail = self.menu_font.render(
                f"Reward: {reward}g", True, PALETTE["text_dim"]
            )
            self.screen.blit(detail, (x + 16, y))
            y += 22

    def _mmo_draw_fleet(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Fleet Control", x, y, palette=palette)
        y += 32
        if not self.mmo_shipments:
            label = self.menu_font.render(
                "No active shipments.", True, PALETTE["text"]
            )
            self.screen.blit(label, (x, y))
            return
        self.mmo_fleet_index = min(
            self.mmo_fleet_index,
            len(self.mmo_shipments) - 1,
        )
        for idx, shipment in enumerate(self.mmo_shipments[:10]):
            self._mmo_draw_row_highlight(panel, y, 22, active=idx == self.mmo_fleet_index)
            resource = shipment.get("resource", "Cargo")
            destination = shipment.get("destination", "Frontier")
            status = shipment.get("status", "in_transit")
            eta = shipment.get("eta", "?")
            risk = shipment.get("risk", "n/a")
            escorted = "Yes" if shipment.get("escorted") else "No"
            color = (
                (255, 220, 140)
                if idx == self.mmo_fleet_index
                else PALETTE["text"]
            )
            line = (
                f"{resource} -> {destination} | {status} | ETA {eta} | {risk}"
            )
            label = self.menu_font.render(line, True, color)
            self.screen.blit(label, (x, y))
            self._mmo_draw_status_badge(panel, y, status)
            ratio = self._mmo_progress_ratio(shipment)
            self._mmo_draw_progress_bar(
                panel.x + 24, y + 22, panel.width - 60, 6, ratio
            )
            y += 24
            detail = self.menu_font.render(
                f"Escort: {escorted}", True, PALETTE["text_dim"]
            )
            self.screen.blit(detail, (x + 16, y))
            y += 22
        y += 8
        hint = self.menu_font.render(
            "Enter: Assign escort (-15g, -1 ETA).",
            True,
            PALETTE["text_dim"],
        )
        self.screen.blit(hint, (x, y))

    def _mmo_draw_projects(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Project Board", x, y, palette=palette)
        y += 32
        if not self.mmo_projects:
            label = self.menu_font.render(
                "No projects available.", True, PALETTE["text"]
            )
            self.screen.blit(label, (x, y))
            return
        self.mmo_project_index = min(
            self.mmo_project_index,
            len(self.mmo_projects) - 1,
        )
        for idx, project in enumerate(self.mmo_projects[:10]):
            self._mmo_draw_row_highlight(panel, y, 22, active=idx == self.mmo_project_index)
            entry = project.get("id", "Project")
            name = project.get("name", "Project")
            region = project.get("region", "region")
            status = project.get("status", "open")
            eta = project.get("eta", "?")
            credits = project.get("credits", 0)
            color = (
                (255, 220, 140)
                if idx == self.mmo_project_index
                else PALETTE["text"]
            )
            line = f"{entry} | {name} | {region} | {status} | ETA {eta}"
            label = self.menu_font.render(line, True, color)
            self.screen.blit(label, (x, y))
            self._mmo_draw_status_badge(panel, y, status)
            ratio = self._mmo_progress_ratio(project)
            self._mmo_draw_progress_bar(
                panel.x + 24, y + 22, panel.width - 60, 6, ratio
            )
            y += 24
            resources = project.get("resources", {})
            resource_line = ", ".join(
                f"{res}:{amt}" for res, amt in resources.items()
            )
            detail = self.menu_font.render(
                f"Cost: {credits}g | {resource_line}", True, PALETTE["text_dim"]
            )
            self.screen.blit(detail, (x + 16, y))
            y += 22
        y += 8
        hint = self.menu_font.render(
            "Enter: Start project or archive when complete.",
            True,
            PALETTE["text_dim"],
        )
        self.screen.blit(hint, (x, y))

    def _mmo_draw_academy(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Academy", x, y, palette=palette)
        y += 32
        if not self.mmo_training_queue:
            label = self.menu_font.render(
                "No training sessions queued.", True, PALETTE["text"]
            )
            self.screen.blit(label, (x, y))
            return
        self.mmo_training_index = min(
            self.mmo_training_index,
            len(self.mmo_training_queue) - 1,
        )
        for idx, training in enumerate(self.mmo_training_queue[:10]):
            self._mmo_draw_row_highlight(panel, y, 22, active=idx == self.mmo_training_index)
            entry = training.get("id", "Training")
            name = training.get("name", "Session")
            status = training.get("status", "open")
            eta = training.get("eta", "?")
            credits = training.get("credits", 0)
            color = (
                (255, 220, 140)
                if idx == self.mmo_training_index
                else PALETTE["text"]
            )
            line = f"{entry} | {name} | {status} | ETA {eta}"
            label = self.menu_font.render(line, True, color)
            self.screen.blit(label, (x, y))
            self._mmo_draw_status_badge(panel, y, status)
            ratio = self._mmo_progress_ratio(training)
            self._mmo_draw_progress_bar(
                panel.x + 24, y + 22, panel.width - 60, 6, ratio
            )
            y += 24
            detail = self.menu_font.render(
                f"Cost: {credits}g", True, PALETTE["text_dim"]
            )
            self.screen.blit(detail, (x + 16, y))
            y += 22
        y += 8
        hint = self.menu_font.render(
            "Enter: Start session or archive when complete.",
            True,
            PALETTE["text_dim"],
        )
        self.screen.blit(hint, (x, y))

    def _mmo_draw_account(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Account Center", x, y, palette=palette)
        y += 32
        account_id = str(self.account_id)
        account_data = self.accounts_manager.get(account_id) or {}
        level = account_data.get("level", "guest")
        public_key = account_data.get("public_key")
        private_key = load_private_key(account_id)
        if public_key and private_key:
            key_status = "Valid"
        elif public_key:
            key_status = "Missing Private"
        elif private_key:
            key_status = "Missing Public"
        else:
            key_status = "None"
        next_tier = self._mmo_next_account_tier(level)
        upgrade_cost = self.mmo_account_tier_costs.get(next_tier, 0)
        lines = [
            f"Account ID: {account_id}",
            f"Tier: {level}",
            f"Public Key: {key_status}",
            f"MMO Access: {'Unlocked' if self.mmo_unlocked else 'Locked'}",
            f"AI Level: {self.mmo_ai_level}",
            f"Arena Wins: {self.arena_wins}",
            f"Regions Online: {len(self._mmo_regions())}",
            f"Upgrade: {next_tier} ({upgrade_cost}g)",
        ]
        for line in lines:
            label = self.menu_font.render(line, True, PALETTE["text"])
            self.screen.blit(label, (x, y))
            y += 24
        y += 10
        actions = [
            "R: Register account",
            "K: Renew key",
            "U: Upgrade tier",
            "Del: Delete account",
            "PgUp/PgDn: Cycle accounts",
            "Esc: Return",
        ]
        for action in actions:
            label = self.small_font.render(action, True, PALETTE["text_dim"])
            self.screen.blit(label, (x, y))
            y += 20
        y += 6
        if self.mmo_account_log:
            log_label = self.small_font.render("Audit Log", True, (200, 220, 240))
            self.screen.blit(log_label, (x, y))
            y += 20
            for entry in self.mmo_account_log[-6:]:
                text = entry.get("text") if isinstance(entry, dict) else str(entry)
                label = self.small_font.render(str(text), True, (160, 190, 215))
                self.screen.blit(label, (x, y))
                y += 18

    def _mmo_account_action(self, action: str) -> None:
        account_id = str(self.account_id)
        if action == "register":
            self.accounts_manager.register(account_id, "user", "PUBKEY")
            self.mmo_message = f"Account {account_id} registered."
            self._mmo_account_log_entry(self.mmo_message, kind="register")
        elif action == "renew":
            self.execute_account_option("Renew Key")
            self.mmo_message = f"Account {account_id} key renewed."
            self._mmo_account_log_entry(self.mmo_message, kind="renew")
        elif action == "delete":
            self.accounts_manager.delete(account_id)
            self.mmo_message = f"Account {account_id} deleted."
            self._mmo_account_log_entry(self.mmo_message, kind="delete")
        elif action == "upgrade":
            self._mmo_upgrade_account_tier(account_id)
        self._mmo_log_event(self.mmo_message)

    def _mmo_cycle_account(self, step: int) -> None:
        accounts = list(self.accounts_manager.load().keys())
        if not accounts:
            self.mmo_message = "No accounts to cycle."
            return
        if self.account_id not in accounts:
            accounts.append(self.account_id)
        accounts = sorted(set(accounts))
        idx = accounts.index(self.account_id)
        next_idx = (idx + step) % len(accounts)
        new_id = accounts[next_idx]
        current_pos = self.world_player_manager.get_position(self.mmo_player_id)
        self.account_id = new_id
        self.mmo_player_id = new_id
        self.mining_manager.player_id = new_id
        self.world_player_manager.set_position(new_id, current_pos)
        self.mmo_message = f"Active account: {new_id}"

    def _mmo_account_log_entry(self, entry: str, *, kind: str = "event") -> None:
        if not entry:
            return
        payload = {
            "ts": datetime.now().isoformat(timespec="seconds"),
            "text": entry,
            "kind": kind,
        }
        self.mmo_account_log.append(payload)
        if len(self.mmo_account_log) > 24:
            self.mmo_account_log = self.mmo_account_log[-24:]

    def _mmo_next_account_tier(self, level: str) -> str:
        if level not in self.mmo_account_tiers:
            return self.mmo_account_tiers[0]
        idx = self.mmo_account_tiers.index(level)
        if idx >= len(self.mmo_account_tiers) - 1:
            return self.mmo_account_tiers[-1]
        return self.mmo_account_tiers[idx + 1]

    def _mmo_upgrade_account_tier(self, account_id: str) -> None:
        data = self.accounts_manager.get(account_id) or {}
        current = data.get("level", "guest")
        next_tier = self._mmo_next_account_tier(current)
        if next_tier == current:
            self.mmo_message = "Account already at top tier."
            return
        cost = int(self.mmo_account_tier_costs.get(next_tier, 0))
        if self.mmo_credits < cost:
            self.mmo_message = "Insufficient credits for upgrade."
            return
        self.mmo_credits -= cost
        data["level"] = next_tier
        data.setdefault("public_key", "PUBKEY")
        self.accounts_manager.register(account_id, next_tier, data["public_key"])
        self.mmo_message = f"Account upgraded to {next_tier}."
        self._mmo_account_log_entry(self.mmo_message, kind="upgrade")

    def _normalize_account_log(self, payload) -> list[dict[str, str]]:
        entries: list[dict[str, str]] = []
        if not payload:
            return entries
        for item in payload:
            if isinstance(item, dict) and item.get("text"):
                entries.append(
                    {
                        "ts": str(item.get("ts", "")),
                        "text": str(item.get("text", "")),
                        "kind": str(item.get("kind", "event")),
                    }
                )
            elif isinstance(item, str):
                entries.append({"ts": "", "text": item, "kind": "legacy"})
        return entries

    def _mmo_cycle_account_audit_filter(self) -> None:
        options = ["all", "week", "today"]
        if self.mmo_account_audit_filter not in options:
            self.mmo_account_audit_filter = "all"
            return
        idx = options.index(self.mmo_account_audit_filter)
        self.mmo_account_audit_filter = options[(idx + 1) % len(options)]

    def _mmo_filtered_account_log(self) -> list[dict[str, str]]:
        entries = list(self.mmo_account_log)
        if self.mmo_account_audit_upgrades_only:
            entries = [e for e in entries if e.get("kind") == "upgrade"]
        if self.mmo_account_audit_filter == "all":
            return entries
        now = datetime.now()
        if self.mmo_account_audit_filter == "today":
            cutoff = now.date()
            filtered = []
            for entry in entries:
                ts = entry.get("ts")
                if not ts:
                    continue
                try:
                    if datetime.fromisoformat(ts).date() == cutoff:
                        filtered.append(entry)
                except ValueError:
                    continue
            return filtered
        if self.mmo_account_audit_filter == "week":
            cutoff = now - timedelta(days=7)
            filtered = []
            for entry in entries:
                ts = entry.get("ts")
                if not ts:
                    continue
                try:
                    if datetime.fromisoformat(ts) >= cutoff:
                        filtered.append(entry)
                except ValueError:
                    continue
            return filtered
        return entries

    def _mmo_draw_account_audit(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Account Audit", x, y, palette=palette)
        y += 32
        filters = [
            f"Filter: {self.mmo_account_audit_filter.title()} (F)",
            f"Upgrades Only: {'On' if self.mmo_account_audit_upgrades_only else 'Off'} (U)",
        ]
        for line in filters:
            label = self.small_font.render(line, True, PALETTE["text_dim"])
            self.screen.blit(label, (x, y))
            y += 20
        y += 10
        entries = self._mmo_filtered_account_log()
        if not entries:
            label = self.menu_font.render(
                "No audit entries available.", True, PALETTE["text"]
            )
            self.screen.blit(label, (x, y))
            return
        for entry in entries[-10:]:
            ts = entry.get("ts") or "legacy"
            text = entry.get("text") or ""
            label = self.small_font.render(f"{ts} | {text}", True, PALETTE["text"])
            self.screen.blit(label, (x, y))
            y += 22

    def _mmo_draw_influence(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Influence Map", x, y, palette=palette)
        y += 32
        entries = self._mmo_influence_entries()
        if not entries:
            label = self.menu_font.render(
                "No regions available.", True, PALETTE["text"]
            )
            self.screen.blit(label, (x, y))
            return
        self.mmo_influence_index = min(
            self.mmo_influence_index,
            len(entries) - 1,
        )
        for idx, region in enumerate(entries[:12]):
            self._mmo_draw_row_highlight(panel, y, 22, active=idx == self.mmo_influence_index)
            name = region.get("name", "region")
            faction, _base = self._mmo_region_influence(region)
            influence = self._mmo_influence_value(region)
            color = (255, 220, 140) if idx == self.mmo_influence_index else PALETTE["text"]
            line = f"{name} | {faction} | Influence {influence}"
            label = self.menu_font.render(line, True, color)
            self.screen.blit(label, (x, y))
            y += 24
        y += 10
        hint = self.menu_font.render(
            "Enter: Invest 25g to boost influence (+5).",
            True,
            PALETTE["text_dim"],
        )
        self.screen.blit(hint, (x, y))

    def _mmo_draw_alerts(self) -> None:
        panel = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        palette = self._mmo_draw_panel(panel)
        x = panel.x + 20
        y = panel.y + 20
        self._mmo_draw_title("Alerts", x, y, palette=palette)
        y += 32
        if not self.mmo_alerts:
            label = self.menu_font.render("No active alerts.", True, PALETTE["text"])
            self.screen.blit(label, (x, y))
            return
        self.mmo_alert_index = min(
            self.mmo_alert_index,
            len(self.mmo_alerts) - 1,
        )
        level_colors = {
            "info": PALETTE["text"],
            "warn": (255, 210, 120),
            "error": (255, 160, 160),
        }
        for idx, alert in enumerate(self.mmo_alerts[:12]):
            self._mmo_draw_row_highlight(panel, y, 22, active=idx == self.mmo_alert_index)
            level = alert.get("level", "info")
            color = level_colors.get(level, PALETTE["text"])
            if idx == self.mmo_alert_index:
                color = (255, 220, 140)
            line = alert.get("text", "")
            label = self.menu_font.render(line, True, color)
            self.screen.blit(label, (x, y))
            self._mmo_draw_status_badge(panel, y, level)
            y += 24

    def _mmo_draw_overview_panel(self, regions: list[dict[str, object]]) -> None:
        panel_width = max(260, int(self.width * 0.32))
        panel_rect = pygame.Rect(
            self.width - panel_width - 10,
            10,
            panel_width,
            self.height - 20,
        )
        palette = self._mmo_draw_panel(panel_rect)
        x = panel_rect.x + 12
        y = panel_rect.y + 12
        self._mmo_draw_title("MMO Overview", x, y, palette=palette)
        y += 36
        stats = [
            f"Regions: {len(regions)}",
            f"Mining: {'On' if self.mining_enabled else 'Off'}",
            f"Mined: {self.mining_manager.mined}",
            f"AI Level: {self.mmo_ai_level}",
            f"Outposts: {len(self.mmo_outposts)}",
            f"Routes: {len(self.mmo_trade_routes)}",
            f"Ops: {len(self.mmo_operations)}",
            f"Events: {len(self.mmo_world_events)}",
            f"Contracts: {len(self.mmo_contracts)}",
            f"Stockpile: {sum(self.mmo_stockpile.values())}",
            f"Shipments: {len(self.mmo_shipments)}",
            f"Credits: {self.mmo_credits}",
            f"Expeditions: {len(self.mmo_expeditions)}",
            f"Alerts: {len(self.mmo_alerts)}",
            f"Directives: {len(self.mmo_directives)}",
            f"Bounties: {len(self.mmo_bounties)}",
            f"Influence: {len(self.mmo_influence)}",
            f"Fleet Escorts: {sum(1 for s in self.mmo_shipments if s.get('escorted'))}",
            f"Projects: {len(self.mmo_projects)}",
            f"Training: {len(self.mmo_training_queue)}",
            f"Sort: {self.mmo_sort_mode.title()}",
            f"Filter: {self.mmo_biome_filter.title()}",
            f"Remote: {len(self.mmo_remote_positions)}",
            f"Zoom: {self.mmo_zoom:.1f}x",
        ]
        if self.mmo_waypoint and self.mmo_waypoint.get("position"):
            wpos = self.mmo_waypoint["position"]
            player_pos = self.world_player_manager.get_position(self.mmo_player_id)
            distance = (
                (player_pos[0] - wpos[0]) ** 2 + (player_pos[1] - wpos[1]) ** 2
            ) ** 0.5
            waypoint_name = self.mmo_waypoint.get("name", "n/a")
            stats.append(f"Waypoint: {waypoint_name} ({distance:.2f})")
        for line in stats:
            label = self.menu_font.render(line, True, (200, 230, 255))
            self.screen.blit(label, (x, y))
            y += 26
        y += 8
        plan = self.mmo_backend.latest_plan() or {}
        summary = plan.get("summary", {}) if isinstance(plan, dict) else {}
        plan_title = self.menu_font.render("Auto-Dev Plan", True, PALETTE["text"])
        self.screen.blit(plan_title, (x, y))
        y += 30
        plan_lines = [
            f"Focus: {summary.get('focus', 'n/a')}",
            f"Boss: {summary.get('boss', 'n/a')}",
            f"Threat: {summary.get('threat', 'n/a')}",
            f"Security: {summary.get('network_security_score', 'n/a')}",
        ]
        for line in plan_lines:
            label = self.menu_font.render(line, True, (190, 215, 245))
            self.screen.blit(label, (x, y))
            y += 24
        y += 6
        legend_title = self.menu_font.render("Legend", True, PALETTE["text"])
        self.screen.blit(legend_title, (x, y))
        y += 26
        legend = [
            ("Plains", (70, 140, 220)),
            ("Forest", (80, 170, 120)),
            ("Desert", (210, 170, 90)),
            ("Tundra", (120, 180, 200)),
            ("Favorite", (255, 240, 180)),
            ("Waypoint", (255, 230, 150)),
            ("Outpost", (180, 220, 140)),
            ("Route", (120, 200, 230)),
            ("Event", (255, 200, 120)),
            ("Contract", (160, 210, 255)),
            ("Expedition", (140, 200, 255)),
            ("Bounty", (255, 170, 170)),
            ("Heatmap", (180, 90, 90)),
            ("Resource", (180, 200, 220)),
        ]
        for name, color in legend:
            pygame.draw.circle(self.screen, color, (x + 10, y + 10), 6)
            label = self.menu_font.render(name, True, PALETTE["text_dim"])
            self.screen.blit(label, (x + 24, y))
            y += 22
        y += 6
        list_title = self.menu_font.render("Regions", True, PALETTE["text"])
        self.screen.blit(list_title, (x, y))
        y += 28
        visible_count = max(4, int((panel_rect.height - y) / 24) - 2)
        if self.mmo_region_index < self.mmo_region_scroll:
            self.mmo_region_scroll = self.mmo_region_index
        if self.mmo_region_index >= self.mmo_region_scroll + visible_count:
            self.mmo_region_scroll = self.mmo_region_index - visible_count + 1
        end = min(len(regions), self.mmo_region_scroll + visible_count)
        for idx in range(self.mmo_region_scroll, end):
            region = regions[idx]
            name = str(region.get("name", "region"))
            color = (255, 235, 150) if idx == self.mmo_region_index else PALETTE["text_dim"]
            label = self.menu_font.render(name, True, color)
            self.screen.blit(label, (x, y))
            y += 22
        region = self._mmo_selected_region()
        if region:
            y += 10
            detail_title = self.menu_font.render("Details", True, PALETTE["text"])
            self.screen.blit(detail_title, (x, y))
            y += 26
            favorite = str(region.get("name", "")) in self.mmo_favorites
            detail_lines = [
                f"Biome: {region.get('biome', 'n/a')}",
                f"Level: {region.get('recommended_level', 'n/a')}",
                f"Seed: {str(region.get('seed', ''))[:8]}",
                f"Favorite: {'Yes' if favorite else 'No'}",
            ]
            feature = region.get("feature") or {}
            if isinstance(feature, dict) and feature:
                detail_lines.append(f"Feature: {feature.get('type', 'n/a')}")
            quest = region.get("quest") or {}
            if isinstance(quest, dict) and quest:
                detail_lines.append(f"Quest: {quest.get('name', 'n/a')}")
                objective = quest.get("objective")
                if objective:
                    detail_lines.append(f"Objective: {objective}")
            for line in detail_lines:
                label = self.menu_font.render(line, True, PALETTE["text_dim"])
                self.screen.blit(label, (x, y))
                y += 22

