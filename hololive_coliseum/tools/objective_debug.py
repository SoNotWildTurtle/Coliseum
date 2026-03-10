"""Debug CLI for objective rotation, progress, and rewards."""

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
        "--simulate-day-advance",
        type=int,
        default=0,
        help="Advance the injected clock by N days before refreshing objectives",
    )
    parser.add_argument(
        "--feed-event",
        default=None,
        help="Feed an objective event such as enemy_defeated or match_won",
    )
    parser.add_argument("--amount", type=int, default=1, help="Event amount")
    parser.add_argument("--claim", action="store_true", help="Claim pending rewards")
    return parser


def _apply_reward(profile, reward: dict[str, int], objective: Objective) -> None:
    balances = profile.economy.setdefault("balances", {})
    balances["coins"] = int(balances.get("coins", 0)) + int(reward.get("coins", 0))
    xp = int(reward.get("xp", 0))
    if xp <= 0:
        return
    progression = profile.progression
    manager = ExperienceManager(
        level=max(1, int(progression.get("level", 1))),
        xp=max(0, int(progression.get("xp", 0))),
        threshold=max(1, int(progression.get("threshold", 100))),
        growth=float(progression.get("growth", 1.0)),
        max_threshold=progression.get("max_threshold"),
    )
    manager.add_xp(xp)
    progression["level"] = int(manager.level)
    progression["xp"] = int(manager.xp)
    progression["threshold"] = int(manager.threshold)
    progression["growth"] = float(manager.growth)
    progression["max_threshold"] = manager.max_threshold
    profile.meta["last_objective_reward"] = objective.objective_id


def _print_state(profile, manager: ObjectiveManager) -> None:
    print(
        f"profile={profile.profile_id} level={profile.progression.get('level', 1)} "
        f"coins={profile.economy.get('balances', {}).get('coins', 0)} "
        f"streak={manager.daily_streak}"
    )
    for objective in manager.objectives.values():
        reward = objective.reward
        print(
            f"{objective.period:<6} {objective.objective_type:<16} "
            f"{objective.progress:>4}/{objective.target:<4} "
            f"completed={objective.completed!s:<5} rewarded={objective.rewarded!s:<5} "
            f"reward={reward} expires={objective.expires_utc}"
        )


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    store = ProfileStore(load_root=args.root)
    profile = store.load(args.profile)
    provider = FixedTimeProvider(TimeProvider().now_utc())
    manager = ObjectiveManager(
        time_provider=provider,
        reward_sink=lambda reward, objective: _apply_reward(profile, reward, objective),
        progression_level_provider=lambda: int(profile.progression.get("level", 1)),
    )
    manager.import_state(profile.objectives)
    fallback_region = profile.objectives.get("region_context", {}) if isinstance(profile.objectives, dict) else {}
    manager.ensure_region_objectives(fallback_region, fallback_name="Arena")
    if args.simulate_day_advance:
        provider.advance(days=args.simulate_day_advance)
        manager.refresh()
    if args.feed_event:
        updates = manager.record_event(args.feed_event, args.amount, meta={"source": "objective_debug"})
        print(f"updates={len(updates)}")
    if args.claim:
        rewards = manager.claim_completed_rewards(meta={"source": "objective_debug"})
        print(f"claimed={len(rewards)}")
    profile.objectives = manager.export_state()
    store.save(profile)
    if args.print_objectives or not (args.feed_event or args.claim or args.simulate_day_advance):
        _print_state(profile, manager)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
