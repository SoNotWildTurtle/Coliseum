"""Headless CLI for inspecting and simulating objective progression."""

from __future__ import annotations

import argparse

from hololive_coliseum.experience_manager import ExperienceManager
from hololive_coliseum.objective_manager import ObjectiveManager, Objective
from hololive_coliseum.profile_store import ProfileStore
from hololive_coliseum.time_provider import FixedTimeProvider, TimeProvider


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect and simulate objectives.")
    parser.add_argument("--profile", default="default", help="Profile ID to load")
    parser.add_argument("--root", default=None, help="Optional profile root override")
    parser.add_argument("--print", action="store_true", dest="print_objectives")
    parser.add_argument(
        "--advance-days",
        type=int,
        default=0,
        help="Advance the injected clock by N days before refreshing objectives",
    )
    parser.add_argument(
        "--advance-weeks",
        type=int,
        default=0,
        help="Advance the injected clock by N weeks before refreshing objectives",
    )
    parser.add_argument(
        "--event",
        default=None,
        help="Feed an objective event such as enemy_defeated or match_won",
    )
    parser.add_argument("--amount", type=int, default=1, help="Event amount")
    parser.add_argument("--claim", action="store_true", help="Claim pending rewards")
    parser.add_argument(
        "--simulate-day-advance",
        type=int,
        default=None,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--feed-event",
        default=None,
        help=argparse.SUPPRESS,
    )
    return parser


def _profile_data(profile: dict[str, object]) -> dict[str, object]:
    data = profile.get("data", {}) if isinstance(profile, dict) else {}
    return data if isinstance(data, dict) else {}


def _apply_reward(profile: dict[str, object], reward: dict[str, int], objective: Objective) -> None:
    data = _profile_data(profile)
    economy = data.get("economy", {})
    if not isinstance(economy, dict):
        economy = {}
    balances = economy.get("balances", {})
    if not isinstance(balances, dict):
        balances = {}
    balances["coins"] = int(balances.get("coins", 0)) + int(reward.get("coins", 0))
    economy["balances"] = balances
    data["economy"] = economy
    xp = int(reward.get("xp", 0))
    if xp > 0:
        progression = data.get("progression", {})
        if not isinstance(progression, dict):
            progression = {}
        manager = ExperienceManager(
            level=max(1, int(progression.get("level", 1))),
            xp=max(0, int(progression.get("xp", 0))),
            threshold=max(1, int(progression.get("threshold", 100))),
            growth=float(progression.get("growth", 1.12)),
            max_threshold=progression.get("max_threshold"),
        )
        manager.add_xp(xp)
        progression["level"] = int(manager.level)
        progression["xp"] = int(manager.xp)
        progression["threshold"] = int(manager.threshold)
        progression["growth"] = float(manager.growth)
        progression["max_threshold"] = manager.max_threshold
        data["progression"] = progression
    meta = data.get("meta", {})
    if not isinstance(meta, dict):
        meta = {}
    meta["last_objective_reward"] = objective.objective_id
    data["meta"] = meta
    profile["data"] = data


def _print_state(profile: dict[str, object], manager: ObjectiveManager) -> None:
    data = _profile_data(profile)
    progression = data.get("progression", {}) if isinstance(data.get("progression"), dict) else {}
    economy = data.get("economy", {}) if isinstance(data.get("economy"), dict) else {}
    balances = economy.get("balances", {}) if isinstance(economy.get("balances"), dict) else {}
    print(
        f"profile={profile.get('profile_id', 'default')} "
        f"level={progression.get('level', 1)} "
        f"coins={balances.get('coins', 0)} "
        f"streak={manager.daily_streak}"
    )
    for objective in manager.objectives.values():
        print(
            f"{objective.period:<6} {objective.objective_type:<16} "
            f"{objective.progress:>4}/{objective.target:<4} "
            f"completed={objective.completed!s:<5} rewarded={objective.rewarded!s:<5} "
            f"reward={objective.reward} expires={objective.expires_utc}"
        )


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    advance_days = (
        args.advance_days
        if args.simulate_day_advance is None
        else int(args.simulate_day_advance)
    )
    event_name = args.event or args.feed_event
    store = ProfileStore(load_root=args.root)
    profile, _warnings = store.load(args.profile)
    provider = FixedTimeProvider(TimeProvider().now_utc())
    data = _profile_data(profile)
    progression = data.get("progression", {}) if isinstance(data.get("progression"), dict) else {}
    manager = ObjectiveManager(
        profile_id=args.profile,
        time_provider=provider,
        reward_sink=lambda reward, objective: _apply_reward(profile, reward, objective),
        progression_level_provider=lambda: int(progression.get("level", 1)),
    )
    manager.import_state(data.get("objectives", {}))
    fallback_region = (
        data.get("objectives", {}).get("region_context", {})
        if isinstance(data.get("objectives", {}), dict)
        else {}
    )
    manager.ensure_region_objectives(fallback_region, fallback_name="Arena")
    if advance_days:
        provider.advance(days=int(advance_days))
        manager.refresh()
    if args.advance_weeks:
        provider.advance(weeks=int(args.advance_weeks))
        manager.refresh()
    if event_name:
        updates = manager.record_event(
            event_name,
            args.amount,
            meta={"source": "objective_debug"},
        )
        print(f"updates={len(updates)}")
    if args.claim:
        rewards = manager.claim_completed_rewards(meta={"source": "objective_debug"})
        print(f"claimed={len(rewards)}")
    data["objectives"] = manager.export_state()
    profile["data"] = data
    store.save(args.profile, profile)
    if args.print_objectives or not (event_name or args.claim or advance_days or args.advance_weeks):
        _print_state(profile, manager)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
