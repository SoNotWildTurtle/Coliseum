# Hololive Coliseum Development Plan

## Project Overview
Hololive Coliseum is a platform fighting game inspired by Super Smash Brothers, featuring popular Hololive VTubers as playable characters. The game will support single-player and multiplayer modes with both keyboard/mouse and console controller input.

Additional networking concepts are described in `DEV_PLAN_NETWORK.md`.

## Goals
- Create a playable prototype with advanced features.
- Implement unique skills for each VTuber character.
- Develop multiple maps with special gravity zones and moving platforms affecting physics and projectiles.
- Support local and online multiplayer modes.
- Provide basic AI opponents for single-player mode.
- Add experience gains from enemy defeats and show player levels on the HUD.

## Key Features
1. **Playable Characters**
   - Unique movesets and special attacks for each Hololive member.
   - Distinct base stats per character; Gura emphasizes attack over defense,
     Watson favors speed with lower health, Ina gains extra mana for more
     specials, Kiara balances offense and defense, Calliope trades health for
     heavier hits, Fauna invests in defense and vitality at the cost of attack,
    Kronii relies on a sturdy parry with moderate power, IRyS boosts her shield
    with high defense, Mumei hits hard but sacrifices health, Fubuki stays agile
    with 9 attack, 5 defense and 95 health, Matsuri pushes attack above average
    at 11 attack, 5 defense and 100 health, Miko hits hard but is frail with 12
    attack, 3 defense and 85 health, Aqua prefers sturdy defenses over damage at
    9 attack, 7 defense and 100 health, Pekora balances solid attack with 11
    attack, 5 defense and 95 health, Marine swings hard with 13 attack, 5
    defense and 90 health, Suisei mixes precision offense with sturdy defenses, Ayame's dash
    favors attack over endurance, Noel's ground slam emphasizes defense with 9
    attack, 8 defense and 110 health, Flare's burning fireball pushes offense with 12
    attack, 4 defense and 95 health, Subaru's stunning blast stays balanced at
    10 attack, 6 defense and 105 health, while Sora's melody favors endurance
    with 9 attack, 5 defense and 110 health.
   - Animations for walking, jumping, attacking, and using special skills.
   - Double jump mechanic for increased mobility.

2. **Maps**
   - Different stages with interactive elements.
   - Gravity modifiers (+/- gravity zones) altering character jump height and projectile paths, wind zones that push fighters sideways, plus bounce pads and moving platforms that keep fighters on their toes.
   - Late chapters feature crumbling platforms that vanish shortly after use.
   - Chapters 1–18 span two screen widths so the camera scrolls horizontally,
     with Chapters 17 and 18 introducing a central pit before later stages
     become more segmented.

3. **Input Support**
   - Keyboard + mouse control scheme.
   - Console controller support (e.g., Xbox, PlayStation, generic USB controllers).

4. **Multiplayer**
   - Local multiplayer with up to four players.
   - Networked multiplayer using rollback netcode if feasible.

5. **Menus**
   - Gradient-styled interfaces with highlighted selections.
   - Covers Story, Arena and Custom modes plus settings and records.

## Development Steps
1. **Engine Selection**
   - For the initial prototype, we use Pygame to quickly iterate on mechanics.

2. **Project Setup**
   - Initialize repository with engine project files.
   - Generate placeholder assets at runtime based on the `README.md` asset list.

3. **Core Gameplay**
   - Character controller for movement and jumping.
   - Basic attacks and hit detection.
   - Gravity zone logic.
   - Health and mana resource system with UI bars.

4. **Character Abilities**
   - Implement unique abilities for each VTuber.
   - Balance and test.

5. **Multiplayer Implementation**
   - Add local multiplayer.
   - Integrate networked multiplayer.
   - Allow players to join on the character screen and add AI opponents.

6. **Polish and Content**
   - Improved animations and sound effects.
   - Additional stages and items.

## Milestones
1. Prototype with one character and one stage.
2. Demo with multiple characters and local multiplayer.
3. Online multiplayer beta.
4. Version 1.0 release with polished visuals and gameplay.

## Next Steps
- Continue refining player abilities and additional characters.
  - Aqua's water blast slows enemies before exploding.
  - Pekora's carrot bomb now bounces once before detonation.
  - Matsuri's firework rises before bursting overhead.
  - Noel's ground slam emits a traveling shockwave.
  - Sora's melodic note weaves through the air.
- Add Ouro Kronii with a time-freeze parry. *(Implemented)*
- Add IRyS with a crystal shield. *(Implemented)*
- Add Hakos Baelz with a chaos effect. *(Implemented)*
- Add Sakura Miko with a piercing beam special. *(Implemented)*
- Polish melee attack, blocking, and parry mechanics.
- Add a double jump so players can reach higher platforms. *(Implemented)*
- Expand maps and experiment with more gravity zones. *(High-gravity zone implemented)*
- Introduce spike traps, ice zones, lava pits and late-game acid pools, and teach AI to avoid them.
- Add a stamina-based sprint for bursts of speed. *(Implemented)*
- Refine existing local multiplayer features.
- Flesh out menu flow for starting a game, adding chapter selection for story mode and graphical previews for characters and maps.
- Add a Quick Start button on the main menu for instantly launching the first
  story chapter. *(Implemented)*
- Add grid-based map selection menu with a Back option and lobby screen listing joined players.
- Populate story mode with twenty chapter icons representing Gura's growth.
- Each chapter should spawn minion enemies that ramp up with the chapter
  number. Every third chapter also features a boss fight with a roster
  character. Boss encounters use improved AI that unleashes periodic special attacks.
- From chapter 10 onward split the ground into segments so late maps include
  pits in addition to elevated platforms.
- Prototype networking with a lightweight UDP manager. Extend it with broadcast
  discovery so clients can find local hosts automatically and add an online vs
  offline selection to the menus. Introduce a `node_registry` storing known
  server addresses so user-hosted nodes can discover each other similar to a
  Hive network. Add a latency check that pings all known nodes and selects the
  closest one automatically. Extend nodes so they track active hosts and answer
  `find` requests from clients, effectively acting as DNS routers for the game.
  Nodes should also gossip their registries by broadcasting `nodes_update`
  packets and handle `get_nodes` requests so newcomers can bootstrap from any
  router.
  Share connected clients across router nodes using `clients_update` packets so
  the mesh can discover active players in real time. When a client registers,
  the router should reply with the current client list and send `client_add` or
  `client_remove` messages as peers join or leave. Clients will send
  `client_leave` when disconnecting. Introduce tolerances in the
  state sync system so insignificant movement isn't transmitted, keeping packet
  sizes tiny.
  Add anti-spoofing by having packets carry a client ID; routers verify the ID
  against the source address before accepting data. Exchange a session token
  after the handshake and drop packets missing the token to block unsolicited
  traffic.
  Add a reliable packet mode that resends important messages until an
  acknowledgement is received. Reliable packets should include an
  ``importance`` value to adjust retry rate. Provide ``refresh_nodes`` to remove
  unreachable peers and merge longer valid blockchains from other nodes. Allow
  clients to send ``chain_request`` so router nodes reply with the current chain.
  Introduce holographic lithography compression so packets are encoded as
  compact pointclouds split into two base64 strings. Include colored anchor
  points at `(0,0,1)`, `(0,0,0)`, `(1,1,1)` and `(1,1,0)` so the decoder knows
  the pointcloud bounds. Before compression, run-length encode repeated byte
  sequences for smaller payloads. Verify pointcloud data with a keyed BLAKE2s
  digest and optionally XOR encrypt it using a nonce-derived key when an
  `encrypt_key` is supplied. Allow an ``auto`` compression mode to pick the
  smallest output between zlib and lzma.
- Harden save loading against corrupt files and ensure volume controls work even when the audio mixer is unavailable.
- Automatically recreate the `SavedGames` folder if it is deleted so settings save reliably.
- Spawn AI players during matches with simple pursuit logic.
- Add a difficulty selector in the character menu to scale AI behavior.
- Expand AI into Easy, Normal and Hard levels that vary reaction time and
  attack frequency.
- Introduce a dodge move for players and teach higher level AI to dodge incoming projectiles.
- Teach hard AI to lead moving targets when firing to improve accuracy.
- Teach enemies to retreat when their health drops low to prolong fights.
- Implement patrol behavior so distant enemies pace around their spawn until the player returns.
- Detect collisions between attacks and enemies to apply damage during combat,
  and make enemies hurt the player on contact.
- Implement encrypted messaging on the blockchain. Register account keys and
  use a mixed admin key to audit messages if abuse occurs.
- Add helper to remove accounts from `accounts.json` via the settings menu. *(Implemented)*
- Validate players against the account registry before saving a block to the
  chain.
- Offer a **Renew Key** option so accounts can generate a fresh key pair used for
  blockchain records and packet signing.
- Add `get_balance` helper returning the stored currency for a player.
- Add a pause menu accessible with Esc during gameplay. *(Implemented)*
- Show a Game Over screen with time survived when the player loses all lives.
- Record the best survival time and show it on the Game Over screen.
- Record the best score using a `ScoreManager` and show it on the Game Over and Victory screens.
- Track a score for defeated enemies and display it during play and on the Game
  Over screen.
- Show a Victory screen when every enemy is defeated or the timer expires.
- Delay the end screen buttons for a few seconds and include a **Play Again**
  option that returns to character selection.
- Add **How to Play** and **Credits** screens accessible from the main menu.
- Provide a **Records** screen showing the best survival time and high score.
- Sync these records across nodes so every client sees the latest leaderboard. *(Implemented)*
- Surface top project goals through a Goals screen on the main menu. *(Implemented)*
- Simplify menu drawing with a lookup table for splash and option screens.
- Add **Show FPS** toggle and **Reset Records** to the settings menu.
- Add a fullscreen toggle so players can switch display modes.
- Provide a **Latency Helper** option so nodes can relay packets for others and
  reduce their ping.

- Introduce a `SkillManager` so abilities register once and share cooldown logic.
- Add `HealthManager` and `ManaManager` classes so health and mana logic is modular.
- Implement a `StaminaManager` to govern dodge stamina costs.
- Drain stamina when blocking or performing attacks.
- Create an `EquipmentManager` framework for future item slots.
- Refactor enemy updates into an `AIManager`.
- Track NPCs with a dedicated `NPCManager` and update friendly helpers through an `AllyManager`.
- Use a `MenuManager` to manage option navigation.
- Use a `GameStateManager` so state transitions are consistent.
- Add an `InventoryManager` so items collected during play can be tracked.
- Cap inventory capacity to encourage future storage upgrades.
- Persist inventory between sessions for long-term progression.
- Provide inventory and equipment screens accessible from the pause menu.
- Add explicit weapon and offhand classes (sword, bow, wand, axe, spear,
  shield, tome, orb, quiver).
- Add a `QuestManager` to record tasks and progress.
- Add an `AchievementManager` so milestones persist between sessions.
- Expose an Achievements screen from the main menu to list unlocked milestones.
- Unlock a "First Blood" achievement on the player's first kill and allow viewing
  achievements from the pause menu.
- Centralize input bindings with a `KeybindManager` for easier customization.
- Introduce a `StatsManager` for STR/DEX/INT and temporary buffs.
- Add an `ExperienceManager` to handle XP gain and leveling.
- Increase attack and max health on level up to reward progression.
- Implement a `CombatManager` to handle collisions, turn order and targeting.
- Add a `DamageManager` for calculations and reductions.
- Assign fighters to teams with a `TeamManager` so friendly fire can be
  disabled.
- Track aggro with a `ThreatManager` so AI focuses the biggest threat.
- Provide a `LootManager` for randomized drops.
- Wrap status effects with a `BuffManager` for stacking rules.
- Store skins and models in an `AppearanceManager`.
- Control animation state with an `AnimationManager`.
- Manage display names via a `NameManager`.
- Maintain login sessions using a `SessionManager`.
- Exchange time offsets through a `SyncManager`.
- Implement `time_request`/`time_response` handshake so clients store offsets.
- Create and destroy gameplay instances with an `InstanceManager`.
- Record client versions in a simple `PatchManager`.
- Add `AuthManager` and `BanManager` for login and blacklist handling.
- Detect cheats via `CheatDetectionManager` and log them with `LoggingManager`.
 - Encrypt packets with AES-GCM and sign them with `DataProtectionManager`.
 - Include timestamps in packets and reject ones that are older than a few seconds.
 - Strip sensitive fields like passwords before encoding packets to limit data leaks.
 - Expire session tokens and allow logout so stolen credentials lose value quickly.
 - Provide `UIManager`, `NotificationManager` and `InputManager` for front-end organization. InputManager should report pressed actions using keyboard or controller bindings.
- Support chats and voice via `ChatManager` and `VoiceChatManager`.
- Integrate the `ChatManager` into the game loop with an Enter key toggle and message history so players can chat during matches.
- Allow chat messages to be sent across the network using lightweight packets.
- Play sounds and trigger effects through `SoundManager` and `EffectManager`.
- Draw the HUD via a dedicated `HUDManager` instead of inline game logic.
- Extend the HUD with a resource panel, status-effect tracker and match insight
  banner so arena runs surface coins, inventory load, auto-dev focus and network
  activity at a glance. Layer an auto-dev telemetry panel beneath the resource
  summary and a world ticker near the bottom to stream trending hazards,
  recommended levels, quest hooks and pending network upgrades from the MMO
  simulation.
- Add a `ScriptManager`/`ScriptingEngine` for map events and modding support.
- Introduce a `LocalizationManager` for multi-language text.
- Cache assets with a `ResourceManager` for quicker loading.
- Coordinate servers via a `ClusterManager` and match players with a `MatchmakingManager`.
- Use a `LoadBalancerManager` to pick the best server and a `MigrationManager` for world transfers.
- Implement a `BillingManager` for purchases, an `AdManager` for promotions and an `APIManager` for integrations.
- Provide a `SupportManager` so players can submit tickets.
- Introduce a `CraftingManager` and `ProfessionManager` for crafting and profession progression.
- Add a `TradeManager` so players can swap items and an `EconomyManager` for shared prices.
- Track currency through a `CurrencyManager`.
- Reward players with coins for each enemy defeated.
- Persist currency balances between sessions to support the MMO economy.
- Unlock titles via a `TitleManager` and track faction standing with a `ReputationManager`.
  - Enemy defeats now award faction reputation that persists between sessions and
    is surfaced on the Records screen.
- Rotate daily and weekly goals with an `ObjectiveManager` that tailors
  objectives to the active region, tracks progress for enemy kills, coin gains,
  power-up pickups and victories, and dispenses coin or experience rewards.
- Maintain friends lists through a `FriendManager` and guilds via a `GuildManager`.
- Provide per-user mailboxes with a `MailManager`.
- Maps are organized through a `MapManager` that includes hazard definitions while an `EnvironmentManager` stores weather settings.
 - Power-ups now spawn via a `SpawnManager` and pickups are recorded in the `EventManager`.
 - Hazard collisions are handled through a `HazardManager` applying damage and friction effects.
 - Level setup is coordinated by a new `LevelManager` that prepares sprites and hazards for each stage.
 - Handle dungeons through a `DungeonManager` and player housing via a `HousingManager`.
- Sync arena climates with MMO regions by attaching a `WeatherForecastManager`
  to `EnvironmentManager`, letting both preview the same deterministic weather schedule.
- Manage mounts, pets and companions with dedicated managers.
- Manage volume settings through SoundManager instead of the Game class.
- Store replays with `ReplayManager` and PNG screenshots in `SavedGames/screenshots`
  via `ScreenshotManager`. Bind F12 to capture a screenshot during play.
- Spawn bots using a `BotManager` and log telemetry with a `TelemetryManager`.
- Moderate chat via `AIModerationManager` and generate dynamic quests with `DynamicContentManager`.
- Track AR locations using a `GeoManager` and connected devices through a `DeviceManager`.
- Advance seasons with `SeasonManager` and reset daily or weekly tasks through `DailyTaskManager` and `WeeklyManager`.
- Guide new players with `TutorialManager` and `OnboardingManager`.
- Organize PvP and PvE competition using `ArenaManager`, `WarManager`, `TournamentManager`, `RaidManager` and `PartyManager`.
  - Extend the arena loop with background `ArenaAIPlayer` agents that score each
    match, updating a running fun level so the `AutoBalancer` can apply balance
    tweaks that reflect simulated player sentiment even when the queue is quiet.
  - Track a slowly adapting baseline fun level and expose it via an
    `ArenaFunSnapshot` helper so downstream tooling can read current fun,
    baseline and momentum values while planning adjustments.
  - Feed that baseline into the `AutoBalancer` so global stat nudges keep the
    arena trending toward long-term fun goals before agent-specific tweaks are
    applied.
  - Simulate iterative playtests through `ArenaAIPlayer.playtest_arena` so each
    agent surfaces projected fun ratings, volatility penalties and the
    archetypes influencing its recommendations.
  - Aggregate those playtests with `ArenaManager.run_ai_playtests` to produce an
    `ArenaFunReport` that augments the snapshot with volatility and AI consensus
    metrics, allowing `AutoBalancer` to react to fun momentum swings and unstable
    streaks in near real-time.
  - Publish an `ArenaFunForecast` via `ArenaManager.generate_fun_forecast` so
    planning tools can read expected fun levels, risk bands, recommended focus
    and archetype trends captured during background playtests.
  - Extend `AutoBalancer` to ingest the fun forecast, layering stabilisation or
    experimentation pushes on top of AI feedback while scaling responses when
    consensus is low.
  - Distil those reports into an `ArenaFunTuningPlan` with per-class
    `ArenaFunDirective` entries so downstream automation can apply deterministic
    boosts, trims or stabilisation nudges before processing the latest AI
    feedback.
  - Let the AI roster scrimmage with `ArenaManager.simulate_ai_matches`,
    publishing an `ArenaFunSeasonSummary` that reports participation, momentum
    and archetype focus. Feed that summary into `AutoBalancer.balance` through
    the `fun_season` argument so arena adjustments reflect what the simulated
    pilots enjoyed across the full season.
* Integrate TransmissionManager with NetworkManager for improved compression and selectable algorithms.
* Introduce speed power-ups that grant brief movement boosts via `StatusEffectManager`.
* Add shield power-ups that confer short invincibility using `ShieldEffect`.
* Include extra-life power-ups so players can earn additional lives mid-stage.
* Add mana power-ups that fully restore a player's mana bar.
* Add stamina power-ups that refill a player's stamina bar.
* Introduce attack power-ups that briefly boost a player's attack stat.
* Allow poison projectiles that apply a `PoisonEffect` for damage over time.
* Introduce teleport pads that instantly relocate sprites on contact.
* Record per-player signatures in blockchain blocks so peers can verify match
  results.
* Mine each block with a proof-of-work nonce and broadcast new blocks. Packets
  include random nonces to guard against replay attacks.
* Balance combat using attack and defense stats via `StatsManager` and
  `DamageManager`.
* Introduce critical hits that deal double damage based on a character's
  ``crit_chance`` stat with a configurable ``crit_multiplier`` and show yellow
  damage numbers when they occur.
* Bridge game state packets through both host nodes and direct peers, letting
  the node verify updates while peers receive them with minimal latency.
* Drop packets that exceed a per-peer rate limit to protect against flooding.
* Allow players to opt into background proof-of-work mining for future MMO
  generation. The miner targets about 20% CPU usage and the node settings note
  the higher resource consumption.
* Store mined block hashes as world seeds via a `WorldSeedManager` for
  deterministic world generation. Record each game block's hash as an additional
  seed so match results influence future regions.
* Synchronize world seeds through the blockchain so all clients share region data.
* Generate new world regions from collected seeds using a
  `WorldGenerationManager` so the MMO grows with player activity. Place each
  region on a golden-angle spiral, giving it a radius one greater than any
  existing region and recording its angle and position so new areas occupy
  expanding rings.
* Publish generated regions back to the blockchain with a `WorldRegionManager`
  so peers can rebuild identical maps.
* Derive arena modifiers from the newest region via an
  `EventModifierManager`, letting desert biomes slow stamina regeneration,
  forest biomes grant bonus experience and tundra biomes raise hazard damage so
  Coliseum matches mirror the evolving MMO world.
* Track player positions with a `WorldPlayerManager` and block movement when
  they reach the largest existing radius.
* Provide a helper that converts forward and strafe input into world
  coordinates for third-person movement.
* Add a `sync_world` helper that pulls seeds and regions from the blockchain so
  new clients can rebuild existing areas.
* Rebuild any regions missing locally by expanding seed blocks during sync so
  fresh installations generate the same MMO world.
* Store a hash alongside each region block and validate it during sync to keep
  shared world data trustworthy.
* Record each finished game as a `.gguf` snapshot using an `IterationManager`
  so future versions can analyze prior runs.
* Run a neural network over snapshot chains to tick completed goals
  automatically.
* Support multiple guilds with ranked members via `GuildManager`.
* Teach hard enemies to dodge away when the player closes in to keep combat
  unpredictable.
* Let enemies raise a block when dodging fails so nearby projectiles deal less
  damage.
* Introduce a `CameraManager` so stages can scroll while keeping the player
  centered.
* Add a `ThirdPersonCamera` so the MMO can display a 3rd-person perspective.
* Record the character roster in seed blocks and expose a weekly vote contract
  through a `VotingManager` accessed from the main menu.
* Votes are submitted exclusively from the menu, the ballot presents a random
  subset of the roster each week, and accounts can participate in every
  category once per week so parallel polls run simultaneously.
* Vote totals inform small balancing modifiers that buff underrepresented
  characters and gently nerf the most popular picks.
* New names listed in `DEV_PLAN_CHARACTERS.md` appear automatically on the select
  screen when a matching subclass exists, ensuring every entry has a custom
  class.
* Background mining feeds the world generator so each mined hash creates a new
  region for the future MMO.
* Newly generated regions land on expanding rings so the live world grows
  outward with every block.
* Each generated region places a monument for the weekly vote winner so the map
  fills with player-chosen landmarks.
* Introduce `ClassManager` and `ItemManager` modules so MMO modes can define
  class archetypes and registered items.
* Define weapon, armor and accessory item classes and display them in a
  slot-based equipment screen similar to Diablo.
* Generate a biome and randomized weapon/armor loot for each blockchain region
  and let players vote on upcoming biomes from a dedicated menu option.
* Award experience for generated regions and track player levels with a
  `LevelingManager` so future MMO content can scale automatically.
* Introduce a `GatheringManager` with a timing-based mini-game that feeds the
  crafting and profession systems with common and rare materials.
* Add a `MinigameManager` whose reaction challenges award crafting materials
  and an `AutoSkillManager` that generates skills using player level and stats.
* Introduce a `ClassGenerator` that produces unique class templates and ensure
  `ClassManager` rejects duplicate names so balancing keeps classes distinct.
* Place crafting stations in maps so players can combine gathered materials
  into equipment.
* Integrate a `BanManager` with networking so hosts can drop packets from
  abusive user IDs.
* Hash account passwords, lock logins after repeated failures and expire
session tokens via `AuthManager` to harden authentication.
* Allow encryption and signing keys to rotate at runtime via
  `DataProtectionManager`.
* Extend `ScoreManager` with combo multipliers for rapid kills.
* Display the current combo count on the HUD.
* Add a `SharedStateManager` to broadcast synchronized gameplay data.
* Layer a `DistributedStateManager` over the shared-state helpers so multi-server clusters share
  deltas, track acknowledgements, replay delta history, deliver snapshot handshakes for new
  nodes, publish sync plans without losing sequence guarantees, stream targeted catch-up
  batches for lagging peers and surface per-node lag telemetry for operators.
* Spawn floating damage numbers whenever attacks connect.
* Allow health to regenerate if players avoid damage for a few seconds.
* Provide a `StateVerificationManager` that attaches CRC32 and SHA256 digests
  to shared state packets so clients can verify game state with minimal
  memory overhead.
* Provide an `MMOBuilder` that instantiates world and voting managers for automatic MMO setup.
* Introduce skill, subclass and trade skill generators alongside an
  auto-balancer to streamline future class and profession additions.
* Expand trade skills with specialisations, balanced level bands and recipe
  hooks, and wire a `TradeSkillCraftingManager` into world generation so
  professions like Brewing, Enchanting, Fishing, Fletching, Inn-Keeping and
  Seductress produce deterministic armor, weapon, bow and wand blueprints for
  the MMO economy while new gathering tracks (Foraging, Herbalism, Logging,
  Prospecting, Trapping) funnel resource bonuses into those crafts.
* Provide an `InteractionGenerator` and `InteractionManager` so new interactions
  can be scripted rapidly.
* Add a `RecursiveGenerator` that chains existing generators to build class,
  skill and trade records in one call and expose an input method toggle in the
  settings menu.
* Introduce a defense power-up that briefly increases the player's defense
  stat.
* Add experience power-ups that grant bonus XP toward level-ups.
* Grant dodge moves temporary invulnerability so skilled players can avoid
  incoming damage.
* Prevent power-up collection during dodges so evasion requires trade-offs.
* Drop loot items via `LootManager` when enemies are defeated, adding them to
  the player's inventory for later crafting.
* Introduce a lightning zone hazard that zaps and knocks back sprites for more
  varied arenas and future MMO regions.
* Add quicksand pits that pull fighters downward and slow movement to support
  desert biomes in the future MMO.
* Add fire zones that ignite characters with burn damage, paving the way for
  volcanic regions in the future MMO.
* Introduce poison zones that inflict damage over time, setting up toxic swamp
  regions in the MMO.
* Add silence zones that disable special abilities, preparing anti-magic
  regions for the MMO.
* Introduce frost zones that freeze fighters briefly, laying groundwork for
  icy MMO regions.
* Add regen zones that restore health over time so arenas can include support
  areas for prolonged MMO battles.
* Allow players to drink health or mana potions from their inventory to regain
  resources, establishing consumable item support.
* Cycle day and night using `EnvironmentManager` to prepare for persistent world
  time.
* Tint arenas with weather-aware ambient lighting so the shared MMO clock is
  visible during Coliseum matches.
* Randomize weather like rain that reduces friction and snow that increases it,
  laying groundwork for dynamic climates in future MMO regions.
* Shake the camera briefly when the player is hit to make combat feel more
  impactful and lay groundwork for future visual effects.
* Flash the screen red when the player is damaged to reinforce hits and set up
  future MMO combat effects.
* Pulse the screen red when health is low to warn players during intense battles.
* Draw health bars above enemies to help players track remaining foes and prepare for group MMO encounters.
* Feed arena telemetry into an `AutoDevFeedbackManager` so world generation can
  adjust recommended levels and record trending hazards for future MMO regions.
* Translate auto-dev hazard insights into rotating "hazard mastery" objectives
  so players train against the traps most likely to appear in upcoming regions.
* Build an `AutoDevTuningManager` that shortens key power-up timers when certain
  hazards spike and publishes the resulting support plan with each generated
  MMO region.
* Add an `AutoDevProjectionManager` that forecasts the next wave of hazardous
  encounters, embedding a projection summary in world data and sharing it with
  arenas so designers can stage countermeasures in advance.
* Layer in an `AutoDevScenarioManager` that merges those projections with
  objective data to produce actionable scenario briefs stored on each region.
* Combine all auto-dev signals through an `AutoDevRoadmapManager` so every
  region records a prioritised checklist of hazard counters and training beats
  for designers.
* Distil those signals into sprint priorities with an `AutoDevFocusManager` so
  roadmap entries, projections, scenarios and support plans feed a shared
  ``auto_dev.focus`` summary.
* Extend auto-dev further with monster, spawn, mob-AI, boss and quest managers
* Introduce an `AutoDevEvolutionManager` that converts aggregated guidance into follow-up evolution plans for MMO planners.
  so regions ship with encounter plans tied to local trade skills, while a
  research manager logs raw CPU utilisation percentages used to study peer games
  and guide the MMO's self-evolving roadmap.
* Blend functionality, design, systems and innovation telemetry through an
  `AutoDevCreationManager` so the pipeline ships creation blueprints with concept
  portfolios, prototype windows and creation gap analytics for downstream
  automation.
  Augment the brief with mechanics synergy and functionality extension indices,
  plus shared expansion tracks, so creation planning stays aligned with the
  latest modernization targets and holographic/network guardrails.
* Install an `AutoDevBlueprintManager` that synthesises functionality, mechanics,
  creation, design and systems telemetry into blueprint cohesion and alignment
  scores, publishing the threads, tracks and backend actions required to close
  blueprint gaps while surfacing the merged network and holographic requirements
  that keep mechanics innovation tied to mitigation and modernization plans.
* Introduce an `AutoDevIterationManager` that weaves functionality, mechanics,
  creation and blueprint telemetry together with network auto-dev, security and
  holographic diagnostics. Publish deterministic iteration cycles, actions,
  gap summaries and guardrail-aware network/lithographic requirements so the
  managerial intelligence matrix can schedule functionality/mechanics prototypes
  with awareness of processing utilisation and research pressure.
* Introduce an `AutoDevSynthesisManager` that merges creation, functionality,
  mechanics, design and systems briefs (and their networking, security,
  modernization and holographic telemetry) into a synthesis report with expansion
  tracks, directives, network requirements and alignment summaries for planners.
* Extend the blueprint stack with an `AutoDevConvergenceManager` that fuses
  functionality, mechanics, creation, dynamics and synthesis signals (plus
  gameplay, interaction, research, network, modernization and security data)
  into a convergence brief. Surface convergence scores, cohesion metrics,
  merged tracks/threads/directives, and unified network/holographic requirements
  so the auto-dev pipeline can schedule upgrades while keeping guardrails and
  codebase alignment in view.
* Follow convergence with an `AutoDevImplementationManager` that transforms the
  functionality, mechanics, gameplay, creation, synthesis and convergence
  telemetry (plus mitigation, remediation, modernization, research and guidance
  data) into a deterministic implementation brief. Surface readiness scores,
  implementation gap and risk indices, shared delivery windows, merged network
  and holographic requirements, and backlog directives so execution planning has
  full awareness of codebase constraints and guardrail posture.
* Layer on an `AutoDevExecutionManager` that merges the implementation,
  convergence, creation and continuity briefs with network, security,
  resilience and modernization telemetry. Surface execution scores, gap and risk
  indices, combined action threads, guardrail-sensitive delivery windows, and
  aggregated network/holographic requirements so the functionality gap report,
  managerial intelligence matrix and modernization workflows can track execution
  stability alongside implementation, mitigation and governance priorities.
* Feed those encounter outputs into an `AutoDevGuidanceManager` so designers
  receive a managerial general-intelligence brief tying monsters, AI directives,
  quests, bosses and research utilisation together.
* Add an `AutoDevIntelligenceManager` that audits monsters, spawns, quests,
  guidance, evolution briefs and research data to deliver general-intelligence
  oversight with the latest processing utilisation readings.
* Introduce an `AutoDevNetworkManager` so networking telemetry highlights relay
  health, bandwidth trends, security incidents and processing load alongside
  other managerial insights.
* Enhance the networking brief with automated security scoring, holographic
  layer analytics and verification summaries so operations teams know when to
  rotate keys, audit relays or reinforce anchor quality across the holographic
  transport.
* Extend that intelligence layer with encounter blueprints, quest synergy
  summaries and backend guidance so planners can route compute when research
  pressure climbs.
* Broaden the intelligence brief with monster catalogues, spawn overviews, mob
  AI development cues, boss outlooks and trade-skill matrices so oversight
  captures encounter depth at a glance.
* Capture group spawn mechanics, AI training gaps, boss pressure, quest
  dependencies, processing utilisation breakdowns and evolution alignment inside
  the intelligence brief so backend guidance can steer the MMO's self-evolution
  with richer data.
* Layer on monster creation queues, lane-based reinforcement tactics, AI
  iteration plans, boss spawn strategies, quest cadence metrics and explicit raw
  processing fields so the general-intelligence brief can balance trade skills,
  bosses and compute budgets in one place.
* Extend the intelligence brief with processing-channel analytics, an
  orchestration pipeline that flags which stages still need attention, and a
  management playbook that recommends backend actions and compute posture based
  on the latest utilisation readings.
* Layer competitive-research tracking plus spawn coordination, AI innovation,
  boss readiness and trade-skill alignment analytics into the intelligence
  brief, then roll them into a managerial snapshot so backend teams can steer
  self-evolution with clear utilisation data.
* Add monster-forge status reports, detailed group-spawn mechanics, mob-AI
  innovation cadence, boss spawn matrices, quest tradecraft summaries, research
  pressure shares and managerial alignment flags to the intelligence brief so
  backend planners see how creation, spawns, AI, bosses and trade skills evolve
  alongside competitive research budgets.
* Expand the intelligence brief with monster AI foci, spawn synergies,
  reinforcement curves, boss strategy callouts and quest difficulty breakdowns
  while the network manager now returns security tiers, channel maps and phase
  signatures so backend guidance and holographic transport share the same
  actionable telemetry.
* Extend the plan with a competitive-research pressure gauge, a security
  auto-dev overview that merges automation focus with upgrade backlogs, and
  holographic diagnostics that log triangulation vectors and vparam maps so the
  intelligence layer can track packet geometry alongside relay stability.
* Build on those analytics with mutation-path tracking, group-support matrices,
  AI modularity maps, boss latency alerts and quest trade dependencies so the
  intelligence brief ties monsters, spawns, AI and trade skills directly to
  network posture. Add a resilience matrix, zero-trust blueprint and anomaly
  ledger to the networking brief while holographic compression emits bandwidth
  profiles, telemetry signatures and stability indices for downstream packet
  verification.
