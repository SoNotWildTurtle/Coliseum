# Project Goals and Architecture Overview

This document collects the current goals and explains how each part of the
prototype works.  It complements `DEV_PLAN.md` and the other development notes.

## High Level Goals

- Build a platform fighter inspired by Super Smash Brothers with Hololive
  VTubers.
- Support both single player and multiplayer, locally and online.
- Provide controller and keyboard/mouse input with configurable bindings.
- Include special abilities, projectiles, melee attacks, blocking and parry
  mechanics.
- Provide visual hit feedback with camera shake and red damage flashes.
- Prototype powerups, gravity zones and varied hazards including spikes, ice,
  lava, acid, quicksand, lightning, wind, teleport and regen zones alongside AI
  opponents.
- Randomize weather each level; rain reduces friction while snow increases it,
  foreshadowing varied MMO regional climates.
- Mirror MMO region conditions in arena matches via an
  `EventModifierManager` that applies biome-themed stamina, experience and
  hazard adjustments.
- Feed match telemetry into an auto-development pipeline so arena performance
  can guide future MMO content and difficulty.
- Use auto-development insights to add hazard mastery objectives that train
  players against whichever traps are trending in shared MMO regions.
- Deploy an AutoDevTuningManager that accelerates counter power-ups and shares
  support plans with newly generated MMO regions.
- Forecast upcoming hazard pressure with an AutoDevProjectionManager so each
  region records a projection summary and arenas surface the same guidance on
  their HUDs.
- Build an AutoDevScenarioManager that pairs projections with objectives so new
  regions store designer-facing scenario briefs for MMO planning.
- Aggregate these insights through an AutoDevRoadmapManager so regions expose a
  prioritised checklist of countermeasures for designers.
- Surface the combined signals through an AutoDevFocusManager so every region
  records a sprint-ready ``auto_dev.focus`` summary for designers and writers.
- Extend auto-development to script monster rosters, spawn plans, mob AI,
  bosses and quests while recording the raw research CPU usage that powers the
  managerial intelligence guiding MMO evolution.
- Capture competitive research pressure, network security auto-dev directives
  and holographic diagnostics so general-intelligence reports can balance
  monster creation, evolution planning and relay hardening from the same data.
- Blend those encounter outputs into an AutoDevGuidanceManager so every region
  surfaces a managerial brief anchored by current processing utilisation.
- Promote horizon planning with an AutoDevEvolutionManager that merges
  guidance, roadmap, focus, research and encounter data into actionable
  evolution briefs.
- Layer on an AutoDevIntelligenceManager that audits monsters, spawn plans,
  quests, guidance and evolution briefs to provide general-intelligence
  oversight using the live processing percentages captured by the research
  manager.
- Feed networking telemetry through an AutoDevNetworkManager so latency,
  relay reliability, bandwidth trends, security incidents and processing load
  appear alongside other MMO planning signals.
- Layer automated security scoring, holographic layer analytics and verification
  summaries into the networking brief so planners can rotate keys, audit relays
  and monitor anchor quality without leaving the auto-dev reports.
- Expand the intelligence output with encounter blueprints, quest synergy
  coverage and backend guidance so planners can react to spikes in research
  utilisation.
- Capture richer oversight data by cataloguing monster hazards, summarising
  spawn tempos, highlighting mob-AI development focus, scoring boss outlooks
  and mapping trade-skill coverage for each region.
- Extend the intelligence brief with group mechanics analytics, mob-AI training
  gaps, boss pressure gauges, quest dependency maps, processing utilisation
  breakdowns and evolution alignment signals so backend planners can steer the
  MMO's self-evolution.
- Continue broadening the intelligence brief with monster creation queues,
  lane reinforcement tactics, AI iteration plans, boss spawn strategies, quest
  cadence metrics and explicit raw processing outputs so compute, trade skills
  and boss fights stay aligned.
- Surface monster-forge status, detailed group-spawn mechanics, mob-AI
  innovation cadence, boss spawn matrices, quest tradecraft summaries, research
  pressure share and managerial alignment indicators so the general-intelligence
  brief keeps backend guidance actionable.
- Extend the same brief with monster AI foci, spawn synergies, reinforcement
  curves, quest difficulty tags and network automation tiers so managerial
  guidance and holographic telemetry stay aligned on actionable signals.
- Publish processing-channel analytics plus an orchestration pipeline and
  management playbook so backend teams know which stage to unblock next and how
  to adjust compute posture when research utilisation shifts.
- Add extra-life powerups that allow players to gain additional lives mid-match.
- Introduce mana powerups that refill the player's mana bar.
- Introduce stamina powerups that refill the player's stamina bar.
- Allow players to sprint at the cost of stamina for short speed boosts.
- Include attack powerups that temporarily boost player attack.
- Level layouts evolve with segmented floors, moving and crumbling platforms in
  later chapters, forcing players to navigate pits and vertical arenas.
- Provide polished menus with gradient backgrounds and access to all gameplay
  modes.
- Save each finished run as a `.gguf` snapshot so later builds can review
  previous game states.
- Analyze snapshot chains with a neural network to automatically check off
  completed goals.

## Development Plan

The detailed plan lives in `docs/DEV_PLAN.md`.  In short, we are iterating on a
Pygame prototype first.  Features are added in small steps:

1. Core player movement with acceleration and friction.
2. Combat options: shooting, melee, blocking, parry and unique specials.
3. Menus for splash screen, game type selection, character selection and maps.
4. Settings menu with key/controller bindings, volume and save management.
5. Local multiplayer and a lightweight UDP networking layer for online play,
   using a `node_registry` so hosts can discover each other across the internet
   and including anti-spoofing checks that verify packet sender IDs.
6. Additional characters and maps with unique mechanics.

## Module Overview

### `hololive_coliseum.game.Game`
Handles the main Pygame loop. It coordinates player input, spawns
projectiles and melee attacks, updates gravity zones and powerups and saves
settings on exit. Menu drawing helpers now live in `menus.py` which is mixed
into the `Game` class.

Key methods:
- `run()` — main loop switching between menu states and gameplay.
- Menu navigation updates internal state to choose characters, maps and
  multiplayer options.

### `hololive_coliseum.player.PlayerCharacter`
Base sprite for all characters and enemies.  Features include:
- Acceleration and friction based movement using `physics` helpers.
- Jumping, blocking, parry and gravity adjustment.
- Ability to double jump before landing.
- Health, mana and life tracking with a `draw_status` helper.
- `shoot`, `melee_attack` and `special_attack` create offensive sprites.

`StatsManager` supplies base attributes. Gura overrides them for higher attack
but lower defense and health.

`GuraPlayer` extends this class to add the trident special attack.  `Enemy`
subclasses `PlayerCharacter` and contains a tiny AI routine.

### `hololive_coliseum.projectile`
Defines `Projectile` and `ExplodingProjectile`.  Projectiles move each frame and
are removed when leaving the screen or when their timer expires.

### `hololive_coliseum.melee_attack`
Small hitbox sprite used for close range attacks.  It self-destructs after a few
frames.

### `hololive_coliseum.gravity_zone`
Provides the `GravityZone` sprite that modifies gravity for any `Player` inside
its rectangle.  The `Game` loop checks for collisions with these zones and sets
the player's gravity multiplier accordingly.

### `hololive_coliseum.platform`
Provides `Platform`, `MovingPlatform` and `CrumblingPlatform` sprites used as
static, sliding or temporary footholds that maps can place anywhere in the arena.

### `hololive_coliseum.powerup`
Simple powerups that restore health, mana or stamina, grant speed, shields or
attack boosts, or add extra lives when the player collides with them. They are
spawned periodically by the `Game` loop.

### `hololive_coliseum.hazards`
Defines `SpikeTrap`, `IceZone`, `LavaZone`, `AcidPool`, `PoisonZone`, `SilenceZone`, `QuicksandZone`, `BouncePad`, `TeleportPad`, `WindZone` and `RegenZone` terrain hazards.
`Game` adds these to maps and enemy AI will attempt to avoid them.

### `hololive_coliseum.physics`
Contains helper functions for gravity, acceleration and friction.  These are used
by the `Player` class to keep movement consistent.

### `hololive_coliseum.network`
A lightweight UDP manager with discovery so clients can locate local hosts.
Hosts call `poll()` to process incoming data.  Clients call `discover()` to find
servers.  Both sides use `send_state()` for game data. Router nodes reply with
the current client list to new registrations and broadcast `client_add` and
`client_remove` notices so peers maintain direct connections.

### `hololive_coliseum.node_registry`
Reads and writes `nodes.json` in the save directory, keeping a list of known
servers. Hosts add themselves to the registry and share their address via
`announce` packets so a mesh of nodes can be built.

### `hololive_coliseum.menus`
Provides ``MenuMixin`` with helpers to draw splash and option menus. ``Game``
inherits from this mixin so the rendering code is kept separate from gameplay.

### `hololive_coliseum.save_manager`
Loads and saves configuration files in the `SavedGames` directory.  `Game` uses
it to store window size, volume and input bindings.  The settings menu can also
invoke `wipe_saves()` to clear this folder.

### `hololive_coliseum.accounts`
Manages user accounts stored in ``accounts.json``. Functions allow registering
public keys and access levels so messages on the blockchain can be encrypted for
each user. Accounts can also be deleted.

## File Dependencies

- `game.py` imports almost all other modules and drives the simulation.
- `player.py` relies on `physics.py` for movement logic and spawns projectiles,
  melee attacks and special projectiles from other modules.
- `network.py` is optional but used when online multiplayer is selected.
- `save_manager.py` is required by `game.py` to persist settings.
- Tests under `tests/` import these modules to verify key features.

## Interplay

During gameplay, `Game` calls `player.handle_input()` which uses
`physics.accelerate` and `physics.apply_friction` to update velocity.  Each frame
`player.update()` applies gravity via `physics.apply_gravity` and checks for
parry timing.  When attacks occur, new `Projectile` or `MeleeAttack` sprites are
added to the `all_sprites` group.  `GravityZone` sprites alter the player's
gravity multiplier, and `PowerUp` sprites restore health or mana when collected.

Settings are loaded at startup and saved on exit through `save_manager`.  If
online mode is chosen, `NetworkManager` handles packet exchange for state
synchronization or discovery of other hosts.

## Short-Term Goals

- Flesh out each VTuber's unique abilities (see `DEV_PLAN_CHARACTERS.md`).
- Generate class templates via a ClassGenerator and prevent duplicates in the
  ClassManager.
- Add combo-based scoring to reward consecutive kills.
- Display the current combo on the HUD.
- Rotate regional objectives via an `ObjectiveManager`, persist their progress
  in saves, and display daily/weekly summaries on the HUD.
  *Daily and weekly objectives now sync across arenas and MMO regions and render
  on the HUD with completion rewards.*
- Provide a `SharedStateManager` for synchronized values across clients.
- Track teams through a `TeamManager` and ignore damage between allies.
- Offer a Quick Start menu option to jump directly into the first story
  chapter.
- Surface project goals through a main menu Goals screen so players can view
  current objectives.
- Permit network encryption and signing keys to rotate during runtime.
- Allow toggling fullscreen mode from the settings menu.
*Gawr Gura stats tuned.*
*Watson Amelia stats tuned.*
*Ninomae Ina'nis stats tuned.*
*Takanashi Kiara stats tuned.*
*Mori Calliope stats tuned.*
*Ceres Fauna stats tuned.*
*Ouro Kronii stats tuned.*
*Shirakami Fubuki stats tuned.*
*Natsuiro Matsuri stats tuned.*
*Sakura Miko stats tuned.*
*Minato Aqua stats tuned.*
*Usada Pekora stats tuned.*
*Houshou Marine stats tuned.*
*Shirakami Fubuki stat profile documented (9 atk, 5 def, 95 hp).*
*Natsuiro Matsuri stat profile documented (11 atk, 5 def, 100 hp).*
*Sakura Miko stat profile documented (12 atk, 3 def, 85 hp).*
*Minato Aqua stat profile documented (9 atk, 7 def, 100 hp).*
*Usada Pekora stat profile documented (11 atk, 5 def, 95 hp).* 
*Houshou Marine stat profile documented (13 atk, 5 def, 90 hp).*
*Aqua's splash now slows foes and Pekora's carrot bounces before exploding.*
*Noel's slam launches a ground shockwave and Sora's melody sways through the air.*
*Watson Amelia implemented.*
 *Ninomae Ina'nis implemented.*
 *Shirakami Fubuki implemented.*
 *Sakura Miko implemented.*
*Ceres Fauna implemented.*
*Nanashi Mumei implemented with aggressive stat profile.*
*Ouro Kronii implemented.*
*IRyS implemented with defensive stat profile.*
   *Hakos Baelz implemented.*
- Bridge state updates through host nodes and direct peers so latency stays low
  while game state is verified by the node.
   *Tokino Sora implemented.*
   *Minato Aqua implemented.*
   *Usada Pekora implemented with balanced offense and defense.*
   *Houshou Marine implemented with heavy attack and lighter health.*
   *Hoshimachi Suisei implemented with 12 attack, 6 defense and 95 health.*
   *Nakiri Ayame implemented with 11 attack, 4 defense and 90 health.*
   *Shirogane Noel implemented with 9 attack, 8 defense and 110 health.*
   *Shiranui Flare implemented with 12 attack, 4 defense and 95 health and a burning fireball special.*
   *Oozora Subaru implemented with 10 attack, 6 defense and 105 health and a stunning blast special.*
   *Tokino Sora implemented with 9 attack, 5 defense and 110 health.*
  - Roster expanded to **22** playable characters with unique specials.
- Expand map mechanics with gravity zones, spike traps, ice patches, lava pits and late-game acid pools. *(High-gravity zone added)*
- Every third story chapter includes a boss battle using one of the playable
  characters plus additional minion enemies.
- Boss enemies wield enhanced AI that triggers their special attacks.
- Improve enemy AI to navigate around hazards intelligently.
- Add AI-controlled opponents that use the shared `PlayerCharacter` base class.
- Provide a difficulty selector so AI behavior can scale from Easy to Hard.
- Add a `CameraManager` so stages can scroll as the player moves.
- Provide a `ThirdPersonCamera` for a 3rd-person MMO view.
- Implement three AI levels with different reaction times and aggression.
- Add a dodge action for players and let advanced AI attempt dodges when threatened.
- Hard enemies lead moving targets when firing.
- Teach enemies to retreat when their health is low.
- Enemies patrol near their spawn when players are out of range.
- Support double jumps for greater mobility. *(Implemented)*
- Implement combat collisions so projectiles and melee attacks damage
  enemies, and enemies now harm the player on contact.
- Polish menus with clearer prompts and optional controller hints. *(Improved with teal borders)*
- Draw menus via a lookup table instead of long chains of conditionals.
- Add an in-game pause menu triggered with Esc.
- Display a Game Over screen when the player runs out of lives.
- Track the best survival time and show it on the Game Over screen.
- Track the highest score and show it on Game Over and Victory screens.
- Keep a running score of defeated enemies and display it during gameplay and on
  the Game Over screen.
- Show a Victory screen when the timer expires or all enemies are defeated.
- End screens should pause for a moment before showing **Play Again** and
  **Main Menu** buttons; Play Again returns to character selection.
- Provide **How to Play** instructions and a **Credits** screen in the main menu.
- Include a **Records** menu showing your best time and high score.
- Sync records across nodes so everyone sees the latest leaderboard.
- Add **Show FPS** and **Reset Records** options to the settings menu.
- Include an **Accessibility** submenu to toggle colorblind mode.
- Add grid-based map selection and a lobby screen listing joined players.
- Continue adding tests for new mechanics as they appear.
- Cover edge cases like zero-length projectile shots to prevent crashes.
- Unlock a "First Blood" achievement when the player defeats their first enemy and
  expose Achievements from the pause menu.
- Design the "Growing Up" story mode with 20 chapter icons that load each level.
- Story chapters include hazard layouts and gravity zones that grow in
  complexity. Early chapters use only spike traps, mid chapters add ice
  patches, later chapters introduce lava pits with up to three gravity
  modifiers, the final chapters feature acid pools for an extra challenge, and
  bounce pads appear throughout to launch fighters skyward.
  Maps also define basic platform layouts that become more intricate in later
  chapters to encourage vertical gameplay.
  The opening twenty chapters stretch across two screens so players experience
  horizontal scrolling immediately. Chapters 17 and 18 add a central pit, and
  Chapters 19 and 20 split the ground into multiple segments while keeping the
  wide format.
- Record multiplayer results in a lightweight blockchain so wins submit a block
  shared with other players. Include search tools and a simple currency for
  betting on matches.
- Allow clients to request the full blockchain from router nodes and merge the
  latest history so all peers stay synchronized.
- Allow players to start or stop acting as a blockchain node from the settings
  menu to help grow a decentralized network.
- Offer a **Latency Helper** toggle so willing players can act as relay nodes and
  route traffic for others when they have a faster connection.
- Provide account management features including deleting accounts when needed. *(Implemented)*
- Add a **Renew Key** action so accounts can rotate key pairs used for packet
  signatures and blockchain entries.
- Validate that all players recorded on the blockchain have registered accounts.
- Record world-generation seeds on the blockchain so MMO regions can be shared
  across nodes. Derive extra seeds from each game result so victories help grow
  the world.
- Provide `get_balance` to read each player's currency amount from `balances.json`.
- Ping known nodes at startup and connect to the one with the lowest latency.
- Nodes act as game routers: hosts register with them and clients query for
  available matches so players can find each other across the mesh.
- Router nodes exchange game lists via `games_update` packets and also
  synchronize active clients with `clients_update` so the mesh knows who is
  online.
- Nodes share their known peers via `nodes_update` packets and respond to
  `get_nodes` requests so registries remain synchronized.
- State updates use the `StateSync` delta system with sequence numbers for
  efficient packet sizes and minimal latency.
- Skip tiny state changes via per-field tolerances so jitter doesn't flood the
  network with unnecessary packets.
- Packets include an HMAC signature when a shared secret is set so nodes can
  discard tampered data.
- Compress network traffic using a holographic lithography approach that
  converts each packet into a compact pointcloud represented by two base64
  strings. Anchor points at `(0,0,1)` (cyan), `(0,0,0)` (white), `(1,1,1)` (black)
  and `(1,1,0)` (red) describe the bounds so peers can reconstruct packets.
  Anchors include virtual size, luminosity and black/white metadata so the cloud
  can be rebuilt with different levels of detail.
- Verify the pointcloud bytes with a keyed BLAKE2s digest and optionally XOR
  encrypt them while in transit.
 - Embed a timestamp in each packet and drop messages that arrive too late to
   further reduce replay risks.
- Important control packets support a **reliable** mode that resends them until
  acknowledged so critical data like game registration is not lost.
- Reliable packets accept an integer importance so crucial updates retry faster
  and more often.
- Nodes periodically drop unreachable peers from the registry to keep the mesh
  healthy.
- Blockchain data can be verified and longer valid chains replace stale copies.

## Long-Term Goals

- Improve network latency handling and implement rollback if possible.
- Add proper sprites and sound effects once the gameplay loop is solid.
- Introduce a full story mode with chapters and cutscenes.
- Package the game for multiple platforms with configurable installers.
- Handle corrupt save files gracefully and keep UI responsive even without audio support.
- Ensure the save directory is recreated automatically if missing.
- Support encrypted player messaging with public and admin keys so abusive
  chats can be audited while regular messages remain private.

- Centralize special ability cooldowns through a `SkillManager`.
- Add dedicated `HealthManager` and `ManaManager` classes for resource tracking.
- Add a `StaminaManager` so dodging and similar actions consume stamina.
- Drain stamina when blocking or attacking to balance combat.
- Introduce an `EquipmentManager` so players can equip items in various slots.
- Provide a `ClassManager` so MMO modes can define archetypes with base stats.
- Add an `ItemManager` that registers equippable items and their bonuses.
- Manage all enemies through an `AIManager` so decision logic stays organized.
- Provide an `NPCManager` for grouping enemies and potential allies.
- Add an `AllyManager` to update friendly NPC behavior.
- Track menu navigation with a `MenuManager` so option handling is reusable.
- Track the current game state in a `GameStateManager` for cleaner transitions.
- Manage player inventory with an `InventoryManager` and enforce capacity limits for future expansion.
- Expose inventory and equipment screens from the pause menu.
- Persist inventory to disk so items carry across sessions.
- Track quests with a `QuestManager` so objectives can be completed.
- Record achievements with an `AchievementManager`.
- Display unlocked achievements through a main menu screen.
- Store key mappings in a `KeybindManager` so rebinding works consistently.
- Provide a `StatsManager` for core attributes with modifiers.
- Implement an `ExperienceManager` for XP and leveling logic.
- Level ups should raise attack and max health.
- Track scores via a `ScoreManager` so high scores persist between runs.
- Introduce a `CombatManager` for collisions and turn order.
- Add a `DamageManager` to handle reductions.
- Keep aggro tables in a `ThreatManager`.
- Generate item drops with a `LootManager`.
- Coordinate buffs through a `BuffManager`.
- Store character skins in an `AppearanceManager`.
- Track animations via an `AnimationManager`.
- Support renames with a `NameManager`.
- Manage login tokens using a `SessionManager`.
- Keep clocks synchronized through a `SyncManager`.
- Allow clients to send a `time_request` packet so routers reply with
  `time_response` containing their current time.
- Spin up separate sessions using an `InstanceManager`.
- Track game versions with a `PatchManager`.
- Enforce logins and bans with `AuthManager` and `BanManager`.
 - Session tokens expire and can be revoked with logout to protect accounts.
 - Detect cheating through `CheatDetectionManager` and record events via `LoggingManager`.
 - Secure data using `DataProtectionManager` for AES-GCM encrypted and signed packets.
 - Desensitize packets by removing sensitive fields before encoding to avoid leaking
   secrets over the network.
- Organize UI with `UIManager` and show alerts via `NotificationManager`.
 - Centralize controls with `InputManager` and accessibility settings with `AccessibilityManager`. InputManager must detect pressed actions from both keyboards and controllers.
- Provide text and voice communication using `ChatManager` and `VoiceChatManager`.
- The chat manager is integrated with gameplay: pressing Enter toggles the chat box and messages are stored in a limited history.
- Chat messages should travel over the network so players can text each other during online games.
- Manage audio and visual effects through `SoundManager` and `EffectManager`.
- Render the status display using a `HUDManager` so timer and score drawing is centralized.
- Load and execute scripts with a `ScriptManager`.
- Provide translations through a `LocalizationManager`.
- Cache assets using a `ResourceManager`.
- Manage cross-server groups via a `ClusterManager` and `MatchmakingManager`.
- Balance server load with a `LoadBalancerManager` and support migrations through a `MigrationManager`.
- Track purchases using a `BillingManager` and display ads with an `AdManager`.
- Integrate third-party services through an `APIManager` and handle support tickets via `SupportManager`.
- Handle crafting via a `CraftingManager` and track professions through a `ProfessionManager`.
- Manage player trades with a `TradeManager` and global prices via an `EconomyManager`.
- Track gold and other money with a `CurrencyManager`.
- Award coins for each enemy defeat.
- Persist each player's coin balance between sessions.
- Unlock titles using a `TitleManager` and adjust faction standing via a `ReputationManager`.
  - Enemy defeats now increase faction reputation and the Records menu lists the
    leading factions for future MMO diplomacy systems.
- Maintain friends and guilds through `FriendManager` and `GuildManager`.
- Provide mailboxes through a `MailManager`.
- World data is organized through a `MapManager` with hazard info and an `EnvironmentManager` for weather.
- Power-up timing uses a `SpawnManager` with events recorded by an `EventManager`.
- Hazards are applied through a `HazardManager` that processes collisions.
- Level initialization is performed by a `LevelManager` so maps, enemies and hazards are created consistently.
- Handle dungeon lockouts using a `DungeonManager` and store housing via a `HousingManager`.
- Track mounts with a `MountManager`, pets with a `PetManager` and companions via a `CompanionManager`.
- Store match replays in a `ReplayManager` and save screenshots under
  `SavedGames/screenshots` with a `ScreenshotManager`. Press F12 to capture
  the current screen during play.
- Spawn automated bots through a `BotManager` and gather analytics via a `TelemetryManager`.
- Flag abusive chat with an `AIModerationManager` and generate quests using a `DynamicContentManager`.
- Track GPS coordinates with a `GeoManager` and haptic devices with a `DeviceManager`.
- Advance seasons using a `SeasonManager` and reset daily/weekly tasks with `DailyTaskManager` and `WeeklyManager`.
- Record tutorial progress via `TutorialManager` and initial guidance with `OnboardingManager`.
- Rank players using an `ArenaManager`, tally faction wars with a `WarManager`, schedule tournaments via a `TournamentManager`, manage raid groups through a `RaidManager` and handle parties in a `PartyManager`.
- Centralize volume adjustments in the SoundManager.
- Balance combat so attack stats deal damage and defense reduces it.
* Use TransmissionManager for packet compression with tunable zlib, bz2 or lzma algorithms.
* Preprocess packets with run-length encoding and encrypt them with per-packet nonce keys.
* Encode a public-key signature as a third base64 fragment and stream decompression so packets remain lightweight.
* Power-ups can grant temporary speed or invincibility boosts handled by the `StatusEffectManager`.
* Projectiles can inflict poison damage over time via `PoisonEffect`.
* Levels may include teleport pads that move sprites to predefined positions.
* Blockchain blocks include player signatures to ensure match history is
  tamper-evident.
* Blocks are mined with a small proof-of-work nonce and broadcast to peers via
  the networking layer.
* Packets carry unique nonces so replayed messages are rejected by
  `DataProtectionManager`.
* Enforce per-peer rate limits in `NetworkManager` to drop flooding attempts.
* Exchange session tokens after the handshake so packets without the shared token
  are discarded immediately.
* Provide a toggleable `MiningManager` so clients can contribute proof-of-work
  to future MMORPG world generation. The miner should use roughly 20% CPU and
  the settings menu must warn about the extra resource cost.
* Gather mined block hashes with a `WorldSeedManager` to seed future worlds.
* Build regions from stored seeds using a `WorldGenerationManager` so the MMO
  world expands automatically.
* Place each generated region on a golden-angle spiral, giving it a radius one
  greater than any existing region and recording its angle and position so the
  shared map grows in evenly spaced concentric circles.
* Publish generated regions back to the chain with a `WorldRegionManager` so all
  peers explore the same maps.
* Track player positions with a `WorldPlayerManager` and block movement at the
  current region's radius.
* Support third-person movement inputs by converting forward and strafe values
  into world offsets.
* Allow the world generator to sync seeds and regions from the blockchain so
  newcomers can reconstruct prior worlds.
* When syncing, rebuild regions for any new seeds so clients regenerate missing
  areas deterministically.
* Compute and store a hash for each region block so tampered world data is
  rejected during sync.
* Allow players to create guilds and manage member ranks through `GuildManager`.
* Hard enemies dodge away when players close in, making melee takedowns harder.
* Enemies block projectiles they cannot dodge, adding defensive variety.
* Store characters in seed blocks and let accounts cast weekly blockchain votes
  per category through a menu-driven `VotingManager`.
* Selecting a character no longer casts a ballot automatically; players vote
  from the menu, the ballot presents a random subset of the roster, and accounts
  can participate in every category once per week while the resulting totals
  drive balancing modifiers.
* Adding a name to `DEV_PLAN_CHARACTERS.md` places it on the selection grid when
  a matching subclass exists, keeping the roster limited to implemented
  fighters.
* Background mining should trigger region generation so the MMO world grows from
  player-contributed hashes.
* World generation should decorate new regions with monuments honoring weekly
  vote winners.
* Expand equipment with fantasy gear classes and a Diablo-style slot
  visualization so players see swords, bows, wands, axes and spears plus
  offhand items like shields, tomes and orbs on a paper doll.
* Regions generated from mined seeds should include a voted-on biome and
  random weapon and armor loot, with the main menu offering character and biome
  voting options.
* Generated regions should award experience so a `LevelingManager` can track
  player levels for the expanding MMO world.
* Gathering should use a timing mini-game that can drop rare materials and feed
  crafting and profession experience.
* Reaction challenges should award crafting materials, and maps should include
  crafting stations where players convert materials into gear.
* Introduce extra mini-games and auto-generated skills so characters gain new
  abilities based on their level and attack stat.
* Networking should ignore packets from banned user IDs via a `BanManager` to
  block abusive peers.
* Authentication should hash passwords and lock accounts after too many failed
  login attempts using `AuthManager`.
* Session tokens should expire automatically and be invalidated on logout.
* Display floating damage numbers for clearer hit feedback.
* Allow critical hits that deal double damage based on a character's
  ``crit_chance`` stat and scale damage by ``crit_multiplier``, showing yellow
  damage numbers.
* Health should regenerate slowly when a player avoids damage for a few seconds.
* Attach CRC32 and SHA256 digests to shared state so peers can verify game
  values without storing large histories.
* Track competitive-research utilisation and surface spawn coordination, AI
  innovation, boss readiness and trade-skill alignment in the auto-dev
  intelligence brief.
* Offer an `MMOBuilder` to wire seed, generation, region, player and voting managers together.
* Provide generators for class skills, subclasses and trade skills, plus an auto
  balancer to keep class stats in line.
* Add an interaction generator and manager so interactive objects can be added quickly.
* Chain class, skill and trade generation through a recursive helper and let
  players choose an input method from the settings menu.
* Implement a defense power-up that grants a short-lived defense boost.
* Add an experience power-up that awards bonus experience toward level-ups.
* Let dodge rolls provide brief invulnerability frames so precise timing avoids
  damage.
* Prevent power-ups from being collected during dodge rolls to balance risk
  and reward.
* Defeated enemies should roll loot drops that populate the player's inventory
  using `LootManager`.
* Include lightning zones that periodically zap players, setting the stage for
  dynamic weather in future MMO regions.
* Fire zones should ignite characters for damage over time, preparing volcanic
  MMO areas.
* Frost zones should freeze fighters briefly, enabling slippery arenas for
  upcoming MMO winter regions.
* Allow players to use consumable items like health and mana potions from their
  inventory to restore resources.
* Enemy defeats should grant experience and display the player's level on the
  HUD so progression carries into future MMO modes.
* Levels should cycle between day and night through `EnvironmentManager` to
  mirror MMO time.
* Arena lighting should apply weather-tinted ambient overlays so matches share
  the MMO world's day/night ambience.
* Attach a `WeatherForecastManager` so arenas and MMO regions preview the same
  upcoming weather before it arrives.
* Camera should shake when the player is damaged to convey impact and prepare
  for richer visual feedback systems.
* Warn players with a pulsing red screen when health falls too low.
* Display health bars above enemies for clearer combat awareness during arenas and future MMO battles.
* Extend auto-dev goals with mutation-path analytics, group-support matrices,
  AI modularity maps, boss latency alerts and quest trade dependencies so MMO
  planners can coordinate monsters, spawns and trade skills with live network
  posture. Add resilience, zero-trust and anomaly metrics to networking goals
  while holographic telemetry exposes bandwidth profiles and stability indices
  for packet verification.
