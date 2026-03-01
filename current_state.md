# Current State

## Goals
- Align README claims with implemented behavior and surface gaps that need
  explicit follow-up work.
- Harden MMO hub networking: relay discovery, shard switching, world snapshot
  sync, and matchmaking workflows should be observable and testable.
- Expand coverage for live-ops tooling (auto-dev pipeline, world state sync,
  and network verification) so regressions are caught early.
- Elevate Coliseum combat AI to coordinated squad behavior with role-driven
  ally support and crowd-control prioritization.

## Active Tasks
1. Wire vote-based balancing into character initialization or match setup so
   vote totals actually affect stats as described.
2. Extend networking test coverage to include relay discovery and relay offers,
   and add integration coverage for MMO world snapshot deltas over the network.
3. Audit shard stats announcements and ensure shard auto-migration inputs are
   validated before use in the UI and logic layers.
4. Review README networking claims against the concrete code paths in
   `hololive_coliseum/network.py`, `hololive_coliseum/game_mmo_logic.py`, and
   `hololive_coliseum/game_mmo_automation.py` to confirm behavior or adjust docs.
5. Expand Coliseum gameplay coverage beyond networking: combat feel, AI
   behaviors, progression loops, and arena modifiers need deeper tests.
6. Ensure every unique character skill has an explicit animation or VFX
   sequence and track gaps by character.

## Functionality Gaps To Close
- Vote balancing exists (`Game.apply_vote_balancing`) but is not invoked from
  character setup or matchmaking.
- Roster selection is not strictly driven by `docs/DEV_PLAN_CHARACTERS.md` when
  that list is shorter than the desired roster size; it is backfilled from the
  hard-coded class registry.
- Skill animation coverage is inconsistent across characters; some unique
  specials rely on default projectile visuals without distinct VFX sequences.

## Networking Checks (Initial)
- Presence tracking and stale-peer pruning are implemented via
  `MMOPresenceManager` and used in the MMO hub loop.
- MMO snapshot requests and world-state deltas are sent/received through
  `NetworkManager` and `MMOWorldStateManager`.
- Relay forwarding exists, and relay discovery/offer coverage is being expanded
  in tests.
- Matchmaking supports queueing, accept/decline handshakes, and ready timeouts,
  with UI overlays in `GameMMOUI`.
- Coverage now includes relay discovery, world delta delivery, and world
  snapshot delivery integration tests.

## Next Up
1. Add a small integration test that simulates an MMO world snapshot delta being
   broadcast and applied to a peer.
2. Decide how vote balancing should apply (pre-match stat modifiers or live
   scaling) and document it in README once implemented.
3. Expand Coliseum feature coverage: combat outcomes, hazard stacking, ally
   support triggers, and event modifiers across regions.
4. Audit character skills for missing VFX and implement an animation entry for
   each unique special.

## Coliseum Expansion Focus
- Combat and damage tuning: critical hits, defense reductions, damage flash,
  and hazard damage stacking should have scenario tests.
- Ally support behaviors: heal/shield triggers, cooldowns, and notification
  cues should be verified in isolation.
- Arena modifiers: event-based stamina/XP/hazard effects should be applied and
  reset cleanly across matches.
- Progression loops: inventory capacity upgrades, reputation gains, and level
  scaling should assert persistence and balance outcomes.
- Squad AI coordination: target focus scoring should incorporate crowd control
  states and avoid simultaneous specials across enemies.
- Ally formation roles: tank/intercept/support stance switching should influence
  hold distance and protect-player behaviors.
- Combat feel polish: hitstop and critical-impact camera shake should be tuned
  alongside per-skill VFX passes.
- Progression pacing: XP now scales by enemy stats/difficulty and level-ups
  boost defense, mana, and stamina alongside health/attack.
- Combat feedback now includes hit SFX hooks and per-skill knockback tuning.
- Optional runtime synth SFX now cover missing audio files without committing
  binary assets.
- SFX debug overlay can display the last played cue in the HUD.
- Audio settings now include an SFX profile toggle (Default/Arcade/Muted).
- Knockback caps and stagger duration scaling are in place for combat tuning.
- HUD debug now shows SFX profile alongside last played cue.
- Knockback strength scales with enemy difficulty tiers.
- Per-character special SFX events are now emitted for future custom audio.
- Per-character melee SFX events now emit character-tagged cues.
- Hitstop and camera shake now scale with attacker difficulty.
- Weapon-tagged melee SFX events are emitted when a weapon is equipped.
- Weapon-tagged SFX now map per profile (e.g., Arcade axes hit harder cues).
- Hit flash intensity scales with attacker difficulty.
- Projectile VFX intensity scales with attacker difficulty.
- Per-character melee SFX tags now support weapon-specific cues.
- Per-weapon melee VFX styles now vary by weapon type.
- Special VFX intensity now scales with attacker difficulty.
- Per-character melee VFX palettes now differentiate each roster member.
- Special VFX styles now swap variants at higher difficulty tiers.
- Weapon-specific impact scaling now feeds hitstop and camera shake intensity.
- HUD SFX debug overlay now includes the last impact scale for hitstop/camera shake.
- Snapshot-style VFX hashes are now available for regression tracking.
- AI targeting now treats active stagger windows as a crowd-control cue.
