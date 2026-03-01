# Development Notes

## 2026-02-06
- Extracted MMO hub logic and UI helpers into mixins to slim the main game module.
- Added MMO hub flow mixin for update/dispatch routines.
- Added MMO logic mixin tests for region sorting, resources, and threat scoring.
- Added MMO flow mixin tests for hazard mapping and escort logic.
- Added MMO automation mixin for autoplay and pipeline helpers.
- Added MMO hub checklist in testing docs for manual validation.
- Extended MMO hub actions and overlays (patrol assignment, intel trends, orders).
- Added threat history persistence and patrol dispatch targeting events/contracts.
- Added module docstrings to additional manager modules for analyzer coverage.

## 2025-07-06
- Switched prototype to use Pygame for quick iteration.
- Implemented basic `Player` class with gravity, movement, and jumping.
- Added ground platform to the `Game` loop and drawing logic.
- Updated README project title and description.
- Added simple test verifying player falls under gravity.

## 2025-07-07
- Generated placeholder character sprites and a sound effect.
- Updated `Player` to load an image if provided.
- Player in the game now uses the Gawr Gura sprite.
- Documented assets in the README and ignored `SavedGames` folder.

## 2025-07-08
- Implemented projectile system and firing with Z key.
- Player tracks facing direction and cooldown for shooting.
- Added tests for projectile movement.
- Restored full placeholder asset list in README.

## 2025-07-09
- Added `GravityZone` sprite and integrated a low-gravity area in the stage.
- Player now adjusts gravity based on zone collisions.
- Created unit test for gravity zones and updated existing tests to initialize pygame.

## 2025-07-10
- Implemented health and mana system for the `Player`.
- Drawing routine now displays health and mana bars on screen.
- Projectiles consume mana when fired and fail if insufficient.
- Added tests covering damage, mana usage, and status bar drawing.

## 2025-07-11
- Added melee attack sprite and blocking mechanic to `Player`.
- Game loop now handles melee attacks with the **X** key.
- Updated README to document controls.

## 2025-07-12
- Implemented parry ability activated with the **C** key.
- Replaced splash prompt with a menu system to start a new game.
- Added navigation for game type, player count, character, and map selection.
- Updated tests to cover parry logic.

## 2025-07-13
- Introduced map and chapter selection screens with placeholder images.
- Added a unique trident special attack for Gura, triggered by **V**.
- Created tests covering the new special attack.

## 2025-07-14
- Added `NetworkManager` with simple UDP sockets for upcoming multiplayer.
- Documented networking prototype in README and exported manager in package.
- Added unit test verifying send/receive between client and host.

## 2025-07-15
- Implemented broadcast-based server discovery mirroring Hive-style detection.
- Added menu step to choose online or offline multiplayer.
- Updated tests for discovery and menu options.

## 2025-07-16
- Completed settings menu with dynamic volume display and a new key-binding
  editor.
- Added states for editing controls and saving changes on exit.
- Updated README accordingly.

## 2025-07-17
- Added placeholder icons for characters, maps and chapters so menus look nicer.
- Character selection now displays AI count and a "Press J to join" prompt for
  local multiplayer.
- Added ability to add AI players from the character menu.
## 2025-07-18
- Added controller binding menu and saving of bindings
- Projectiles now aim toward the mouse and Gura's special attack explodes
- Added simple powerup spawns, level timer, and life system

## 2025-07-19
- Fixed crash when `settings.json` contains invalid JSON
- Volume adjustments no longer raise errors if the mixer fails to initialize

## 2025-07-20
- `save_settings` now recreates the save directory if it was deleted.
- Cleaned up a comment about the low-gravity zone.
- Network tests close sockets to avoid resource warnings.

## 2025-07-21
- Added `WatsonPlayer` with a time-dash special attack.
- Game now creates the player when a level starts so character selection matters.

## 2025-07-22
- Extended goals list with short- and long-term sections.
- AI players selected in the menu now spawn as enemies that pursue the player.

## 2025-07-23
- Added projectile and melee collision detection so enemies take damage when hit.
- Updated goals and development plan to mention combat collisions.

## 2025-07-24
- Enemies now deal contact damage to the player.
- Updated goals and development plan accordingly.

## 2025-07-25
- Added a "Growing Up" storyline for single-player with twenty chapter icons.
- Updated menus to list all chapters and load placeholder images.

## 2025-07-26
- Introduced `InaPlayer` with a tentacle grapple special attack.
- Character list now includes Ninomae Ina'nis and chapter menu supports her image.
- Collision logic pulls enemies toward the player when grapple projectile hits.

## 2025-07-27
- Refactored `Player` into `PlayerCharacter` and updated character subclasses.
- Added difficulty selector (Easy/Normal/Hard) to character menu.
- Researched Smash Bros AI which scales reaction time and randomness by level; plan to mimic this behavior.

## 2025-07-28
- Implemented three AI tiers that vary reaction delay and aggression.
- Enemies now shoot and use melee attacks, marking their projectiles so
  collisions damage the player.
- Updated collision handling for these enemy attacks and added tests.

## 2025-07-29
- Added SpikeTrap and IceZone hazards with player and enemy interactions.
- Extended Enemy AI to jump over hazards when possible.
- Created placeholder subclasses for each Hololive member with unique specials.
- Updated development plan and goals accordingly and added new tests.

## 2025-07-30
- Added `FubukiPlayer` with an ice shard that slows enemies.
- Updated menus and image lists to include Shirakami Fubuki.
- Documented the new ability in the development plan and goals.

## 2025-07-31
- Added volume cycling when selecting the option in the settings menu.
- Documented project structure and file paths in README and notes.

## 2025-08-01
- Introduced a `node_registry` module storing known server addresses.
- NetworkManager now registers hosts and handles `announce` messages to build a
  mesh of user-hosted nodes.
- Added a networking plan document and updated development plans and README.

## 2025-08-02
- Added **Node Settings** menu with options to start or stop hosting a
  blockchain node.
- Starting a node creates a `NetworkManager` in host mode and broadcasts an
  `announce` message so other nodes discover it.
- Stopping closes the socket to disable hosting and return to client mode.

## 2025-08-03
- Added ping response handling in `NetworkManager` and a helper to measure
  latency to other nodes.
- Clients now choose the best host by pinging all known nodes at startup.
 - Documented the new behavior in the networking plan and goals.

## 2025-08-04
- Nodes now act as DNS-style routers. Game hosts send a `register` packet so
  routers store their address. Clients send `find` to receive the list of
  available matches. Added helpers in `NetworkManager` and updated plans and
  goals accordingly.

## 2025-08-05
- Router nodes broadcast `games_update` packets when their host list changes.
  This keeps every node's list of joinable matches synchronized.

## 2025-08-06
- Router nodes now track active clients. When a player registers with a node
  it adds their address and broadcasts `clients_update` packets so other nodes
  learn about new peers.

## 2025-08-07
- Introduced `StateSync` helper and integrated it with `NetworkManager` so state
  packets only contain changed fields. Each update includes a sequence number to
  detect lost packets and reduce latency.

## File Overview

This section lists each source file and explains how the modules depend on one
another.  Paths are relative to the repository root.

| File | Description |
| ---- | ----------- |
| `main.py` | Small launcher that calls `hololive_coliseum.game.main`. |
| `hololive_coliseum/__init__.py` | Package initializer re-exporting all game classes for easy imports. |
| `hololive_coliseum/game.py` | Main loop, menu system and overall coordinator. Uses most other modules. |
| `hololive_coliseum/player.py` | Base character logic and subclasses for each VTuber plus the `Enemy` AI. |
| `hololive_coliseum/projectile.py` | Projectile sprites including exploding and grapple variants. |
| `hololive_coliseum/melee_attack.py` | Short-lived melee hitbox sprite. |
| `hololive_coliseum/gravity_zone.py` | Sprite representing low-gravity areas. |
| `hololive_coliseum/hazards.py` | Contains `SpikeTrap` and `IceZone` terrain hazards. |
| `hololive_coliseum/powerup.py` | Simple pickup items that heal or restore mana. |
| `hololive_coliseum/physics.py` | Utility functions for acceleration, friction and gravity. |
| `hololive_coliseum/network.py` | UDP networking helper used for online multiplayer. |
| `hololive_coliseum/node_registry.py` | Stores and updates known network node addresses. |
| `hololive_coliseum/save_manager.py` | Reads/writes `SavedGames/settings.json`. |
| `tests/` | Unit tests verifying gameplay mechanics and utilities. |
| `docs/` | Development plans and this notes file. |
| `Images/` | Placeholder art referenced by the menus. |
| `sounds/` | Placeholder directory kept empty with `.gitkeep`. |

- Added blockchain module to record multiplayer wins and wagers.

## 2025-08-08
- Removed stray merge conflict comments left from earlier revisions.
- Updated `.gitignore` to exclude temporary `test_nodes` directories created by
  the test suite.
## 2025-08-09
 - Clarified zero-vector projectile behavior and extended corresponding test.
## 2025-08-10
- Added HMAC signing to all network packets for basic security.
- Networking plan and goals updated with authentication details.
## 2025-08-11
- Implemented reliable packet mode in `NetworkManager` that resends important
  messages until an `ack` is received.
- Updated docs and goals with the new networking feature.

## 2025-08-12
- Reliable packets now have an integer importance level controlling resend rate
  and attempts.
- Added `refresh_nodes` and `prune_nodes` to drop unreachable peers.
- Blockchain module can verify and merge chains from other nodes.


## 2025-08-13
- Added holographic lithography compression for all network packets.
- NetworkManager now compresses outgoing messages and decompresses on receipt.

## 2025-08-14
- Added SHA256 verification and optional XOR encryption to the holographic
  compression module.
- NetworkManager passes an `encrypt_key` to transparently secure packets.

## 2025-08-15
- Introduced account registry storing public keys and access levels.
- Added encrypted messaging blocks to the blockchain. Messages use a mixed key
  so moderators can decrypt them if needed.

## 2025-08-16
- Split `blockchain.py` by moving account management into `accounts.py`.
- Extracted menu rendering helpers into `menus.py` so `game.py` is smaller.

## 2025-08-17
- Added `delete_account` helper to remove users from the account registry.
- Updated goals and development plan to mention account deletion.

## 2025-08-18
- Blockchain `add_game` now validates that all listed players exist in
  `accounts.json` before recording a block. Updated tests accordingly.

## 2025-08-19
- Added `get_balance` helper to query player currency totals.
- `wipe_saves` now removes directories for a clean slate.

## 2025-08-20
- Tweaked physics constants for smoother motion and introduced a dodge move bound to Left Ctrl.
- Enemy AI now checks nearby projectiles and may dodge them on harder difficulties.

## 2025-08-21
- Added Calliope's returning scythe and Kiara's explosive dive.
- Implemented boomerang and explosion projectiles to support these abilities.

## 2025-08-22
- Introduced `FreezingProjectile` and `FlockProjectile` subclasses for Fubuki and Mumei.
- Updated their special attacks to use these classes and added tests.

## 2025-08-23
- Added HealingZone sprite and updated Fauna's special to create a healing field.
- Updated docs and tests accordingly.

## 2025-08-24
- Implemented IRyS crystal shield that blocks enemy projectiles.
- Updated collision handling and documentation.
- Added unit test covering the shield ability.

## 2025-08-25
- Added PiercingProjectile and Sakura Miko's beam special that passes through enemies.
- Updated character plans, goals and documentation.

## 2025-08-26
- Introduced eight new placeholder characters to reach twenty total.
- Character select menu now displays a 5x4 grid of icons so each character has a dedicated box.
- Updated images list and character plans accordingly.

## 2025-08-27
- Added grid layout to the map selection screen and "Back" options on most menus.
- Implemented a simple lobby screen showing joined players before selecting a map.
- Updated tests and documentation.

## 2025-08-28
- Added Accounts submenu under Settings with Register/Delete options.
- `Game.execute_account_option` handles account actions and tests can invoke it.
- Documentation and goals updated to mark account management implemented.

## 2025-08-29
- Added a high-gravity zone to levels so jumps are shorter in that area.
- Updated development plan and goals to mention the new zone.
- Added tests ensuring both gravity zones load correctly.

## 2025-08-30
- Polished all menus with a teal border for better readability.
- Added a pause menu triggered with **Esc** containing Resume and Main Menu options.
- Documented the new feature and updated goals accordingly.

## 2025-08-31
- Added a Game Over screen that appears when the player loses all lives.
- The screen shows the time survived and returns to the main menu.

## 2025-09-01
- Game Over screen now also displays the best time across runs.
- Best time persists in settings and updates when a new record is reached.

## 2025-09-02
- Enemies are removed when their health reaches zero and the player gains a
  score point.
- The current score is shown during gameplay and on the Game Over screen.

## 2025-09-03
- Added victory condition when all enemies are defeated or the timer reaches the
  limit.
- A new Victory screen displays the final time, best time and score before
  returning to the main menu.

## 2025-09-04
- Game Over and Victory screens now wait three seconds before showing options.
- Added **Play Again** to return to character selection or **Main Menu** to quit
  the run.

## 2025-09-05
- Main menu offers **How to Play** and **Credits** entries with simple screens.

## 2025-09-06
- Tracked a high score across runs and displayed it on Game Over and Victory screens.
- Settings now save `best_score` alongside the best time.

## 2025-09-07
- Added a **Records** screen on the main menu showing the best time and high score.
- Planned to sync these records across nodes via the blockchain in future updates.

## 2025-09-08
- Simplified level setup with a character mapping table.
- Menu rendering now looks up draw functions from a dictionary so the game loop
  has fewer conditionals.
- The Settings menu includes **Show FPS** and **Reset Records** options.

## 2025-09-09
- Records now sync across nodes. When one player achieves a new best time or
  score, their node broadcasts the update and peers merge it into their own
  settings.

## 2025-09-10
- Added a **Latency Helper** toggle in the Node Settings menu.
- NetworkManager can now forward packets through relay nodes so players with
  better connections can help reduce latency for others.

## 2025-09-11
- Added a new **LavaZone** hazard dealing damage over time.
- Updated level setup to include a lava pit and adjusted collision handling.

## 2025-09-12
- Implemented a double jump mechanic so players can jump twice before landing.

## 2025-09-13
- Added Tokino Sora to the roster with an area-of-effect melody special.

## 2025-09-14
- Introduced `SkillManager` to centralize ability cooldowns. Gura and other characters register their specials with the manager.

## 2025-09-15
- Added basic `HealthManager`, `ManaManager` and `EquipmentManager` classes to begin modularizing player stats.
- PlayerCharacter now uses these managers internally.

## 2025-09-16
- Implemented `AIManager` to coordinate enemy actions.
- Added `NPCManager` to keep enemy and ally groups organized.
- Added `AllyManager` for future friendly NPC support.

## 2025-09-17
- Added MenuManager and GameStateManager modules for organizing menus and state transitions. Game now uses `_set_state` to update them.

## 2025-09-18
- Introduced `InventoryManager` to track collected items.
- Added `KeybindManager` so input bindings are stored separately from the `Game` class.
## 2025-09-19
- Added StatsManager for base attributes and ExperienceManager for level progression.

## 2025-09-20
- Created additional management modules including CombatManager, DamageManager,
  ThreatManager and LootManager.
- Added BuffManager plus appearance, animation and name managers.
- Implemented simple session, sync, instance and patch managers for future
  services.
## 2025-09-21
- Added security and UI-related management modules including AuthManager, CheatDetectionManager, BanManager, DataProtectionManager and LoggingManager.
- Implemented UIManager, NotificationManager, InputManager and AccessibilityManager for front-end features.
- Created ChatManager, VoiceChatManager and EmoteManager for communication.
- Added SoundManager and EffectManager placeholders for audio/visual effects.
## 2025-09-22
- Introduced ScriptManager, LocalizationManager and ResourceManager for scripting, translation and asset caching.
- Added server management modules: ClusterManager, MatchmakingManager, LoadBalancerManager and MigrationManager.
- Implemented BillingManager, AdManager, APIManager and SupportManager for external service integration.

## 2025-09-23
- Added color-coded anchor metadata to holographic compression so packets
  include cyan `(0,0,1)`, white `(0,0,0)`, black `(1,1,1)` and red `(1,1,0)`
  points describing the pointcloud bounds.
## 2025-09-24
- Created CraftingManager, ProfessionManager, TradeManager and EconomyManager
  to handle crafting, professions, trading and pricing.
## 2025-09-25
- Added CurrencyManager, TitleManager, ReputationManager, FriendManager,
  GuildManager and MailManager to flesh out social systems.
## 2025-09-26
- Introduced MapManager, EnvironmentManager, SpawnManager, EventManager and DungeonManager for world logic.
- Added HousingManager along with MountManager, PetManager and CompanionManager for player assets.
## 2025-09-27
- Expanded `ChatManager` with open/close state and capped history to display an
  in-game chat box. Updated tests and documentation.
## 2025-09-28
- Integrated the `ChatManager` with `Game` so players can toggle a chat box with
  Enter during matches. Text input is captured and sent through the manager.
  Added a new test verifying chat messages send correctly.
## 2025-09-29
- Moved volume handling into SoundManager so audio control is centralized.
## 2025-09-30
- Created additional manager modules for replays, screenshots, bots, telemetry,
  AI moderation, dynamic content, geo tracking, device handling, seasons,
  daily and weekly tasks, tutorials, onboarding, arenas, wars, tournaments,
  raids and parties. Exported them via `__init__` and updated documentation.
## 2025-10-01
- Integrated `MapManager` and `SpawnManager` with the game loop. Hazard and gravity
  zones now load from map data and power-ups spawn through the manager. Pickups
  are recorded by `EventManager`.
## 2025-10-02
- Migrated hazard collision logic into a dedicated `HazardManager` used by `Game`.
  Tests updated and documentation expanded.
## 2025-10-03
Delegated projectile and melee collision handling to `CombatManager`.
`Game` now calls the manager and no longer stores `last_enemy_damage`.
## 2025-10-04
Moved level setup logic into a `LevelManager` class. The game now delegates
map loading, sprite initialization and hazard placement to this manager.
## 2025-10-05
Extended holographic compression: anchor points now include virtual size,
luminosity and black/white metadata so packets can be reconstructed with
multiple detail levels.
## 2025-10-06
Added TransmissionManager to wrap holographic compression with adjustable zlib level and encryption key.

## 2025-10-07
Migrated packet signing and encryption into DataProtectionManager. NetworkManager now delegates encode/decode to this manager.

## 2025-10-08
Added initial story maps and boss logic. Each third chapter now loads a boss
from the roster and spawns extra minions using data stored in MapManager.

## 2025-10-09
Expanded story maps with hazard patterns and gravity zones that scale with each
chapter. Updated tests and documentation accordingly.

## 2025-10-10
Refined story map progression so chapters 1–5 use only spike traps, chapters
6–10 introduce ice hazards and chapters 11–20 add lava pits. Later stages now
include up to three gravity zones for increased challenge.

## 2025-10-11
Added AcidPool hazard and updated story maps so chapters 18–20 feature acid pools along with existing lava, ice and spike traps.
Updated docs and tests for the new hazard type.

## 2025-10-12
Expanded story maps with basic platform layouts. Each chapter now includes at
least one platform and later chapters add more for vertical movement. Updated
docs and tests accordingly.

## 2025-10-13
Added optional LZMA compression to holographic packets. `TransmissionManager`
selects the algorithm via a new ``algorithm`` argument.

## 2025-10-14
Implemented networked chat. The game now sends ``chat`` packets whenever a player
submits a message and received texts are added to the chat history.

## 2025-10-15
Added HUDManager for drawing the status display and removed inline HUD code from game.py.

## 2025-10-16
Introduced ScoreManager to track the current and best score. Game saves use this manager when levels end.
## 2025-10-17
InputManager now checks keyboard and controller bindings. Game uses it to detect actions after rebinding.

## 2025-10-18
Added optional bz2 compression to holographic packets for tighter encoding.

## 2025-10-19
Implemented time synchronization via `time_request` and `time_response` packets
so clients can compute offsets through `SyncManager`.

## 2025-10-20
Added run-length preprocessing and nonce-derived encryption keys to holographic
packets, improving compression ratios and security.

## 2025-10-21
Upgraded holographic packets to use keyed BLAKE2s digests and an ``auto``
compression mode that picks the smallest result between zlib and lzma, boosting
security while keeping processing requirements low.

## 2025-10-22
Holographic compression now streams decompression for all algorithms and embeds
a third base64 fragment carrying the sender's public key and signature so peers
can verify packet origin with minimal overhead.

## 2025-10-23
Added a **Renew Key** option in the Accounts menu. Regenerating the key pair
updates blockchain records and packet signing so new transmissions use the fresh
private key.

## 2025-10-24
Added per-field tolerances to StateSync so tiny movement changes are ignored, reducing network latency.

## 2025-10-25
Defeating enemies now grants coins through `CurrencyManager` whenever they are
eliminated.

## 2025-10-26
Added a `StaminaManager` so dodging consumes stamina which regenerates over time.

## 2025-10-27
Introduced a speed power-up that applies a brief haste effect using
`StatusEffectManager`.

## 2025-10-28
Added a shield power-up that temporarily makes the player invincible via
`ShieldEffect`.

## 2025-10-29
Introduced a poison projectile and `PoisonEffect` that deals periodic damage to
enemies.

## 2025-10-30
Blocking now drains stamina each frame and firing or melee attacks consume stamina.

## 2025-10-30
Added a bounce pad hazard that launches sprites upward when touched.

## 2025-10-31
Implemented teleport pads that relocate sprites and added player signatures to
blockchain game records for stronger verification.

## 2025-11-01
Refined menu visuals with a cyan-to-white gradient and highlighted selections.
Menus now expose Story, Arena and Custom modes more clearly.

## 2025-11-02
Story maps now split the ground into segments from chapter 10 onward, creating
pits that add variety and challenge to later levels.

## 2025-11-03
Introduced proof-of-work mining for blockchain blocks and broadcast them across
the network. The security layer now tags packets with nonces to prevent replay
attacks.

## 2025-11-04
Clients now bridge state packets: updates go to the host node for verification
and directly to other peers for faster synchronization.

## 2025-11-05
Upgraded the networking layer to encrypt packets with AES-GCM and random nonces
via `DataProtectionManager` for stronger confidentiality.

## 2025-11-06
Added an optional `MiningManager` that performs background proof-of-work using
spare CPU time to prepare future MMORPG content. `NetworkManager` now enforces a
per-peer rate limit, dropping traffic that exceeds the threshold to mitigate
flooding attacks.

## 2025-11-07
Mining results now feed a new `WorldSeedManager` which collects mined hashes as
seeds for deterministic MMO world generation.

## 2025-11-08
Added an `IterationManager` that saves each finished run to a timestamped
`.gguf` file so future builds can load or analyze previous game states.

## 2025-11-09
Added a `GoalAnalysisManager` that scans `.gguf` snapshot chains with a neural
network stub to mark goals completed.

## 2025-11-10
Extended `GuildManager` so the game can create multiple guilds and track
member ranks for upcoming MMORPG features.

## 2025-11-11
Story maps now spawn minions in every chapter with counts that scale with the
chapter number. Updated docs and tests to reflect the universal minion spawns.

## 2025-11-12
Router nodes reply to joining clients with the current client list and notify
peers when players join or depart. Clients can send a `client_leave` packet so
routers drop them from peer lists.

## 2025-11-13
Clients can now request the full blockchain from router nodes. A new
`chain_request` message triggers a response with the current chain so newcomers
merge the latest history before playing online.

## 2025-11-14
`DataProtectionManager` now embeds timestamps in packets and rejects stale ones
to strengthen replay protection.

## 2025-11-15
`DataProtectionManager` gained a sanitization step that removes sensitive fields
like passwords before encoding packets.

## 2025-11-16
Damage and health are now balanced by attack and defense stats. Combat uses
`DamageManager` and each character's `StatsManager` so tougher fighters shrug off
more damage.

## 2025-11-17
Added a `WorldGenerationManager` that converts stored world seeds and dynamic
content into new MMO regions, extending the self-creating world framework.

## 2025-11-18
Introduced moving platforms that slide horizontally and carry characters
standing on them to diversify arena layouts.

## 2025-11-19
Added crumbling platforms that vanish shortly after being stepped on to keep
players on the move.

## 2025-11-20
Introduced wind zones that push sprites sideways. Story maps from chapter eight
forward now include these hazards.

## 2025-11-21
Enemies retreat from the player when their health drops below thirty percent.

## 2025-11-22
Hard enemies now lead moving targets when firing so their projectiles track
the player's motion.

## 2025-11-23
Hard enemies dodge away when players get too close, making melee assaults more
challenging.

## 2025-11-24
Enemies can now block incoming projectiles when dodging fails, reducing damage
from shots they cannot evade.

## 2025-11-25
Boss enemies gained enhanced AI that triggers special attacks, keeping fights
unpredictable.

## 2025-11-26
Router nodes now broadcast their known peers and answer `get_nodes` requests,
allowing new clients to bootstrap their node list from any router.

## 2025-11-27
Basic anti-spoofing added: packets carry a client ID and routers drop messages
when the ID does not match the sender's address.

## 2025-11-28
Peers exchange a session token during the handshake and ignore packets without
the shared token, preventing unsolicited traffic.

## 2025-11-29
ScreenshotManager now saves PNG files under `SavedGames/screenshots` so players
can capture in-game moments.

## 2025-11-30
Pressing F12 during gameplay triggers ScreenshotManager to capture the current
screen to `SavedGames/screenshots`.

## 2025-12-02
Introduced a CameraManager to track viewport offsets so the camera can follow
the player. Updated plans and goals to include scrolling stages.

## 2025-12-03
Reworked the first two story maps to span two screens, placing extra hazards and
gravity zones near the far edge so the new camera scrolling gets exercised.

## 2025-12-04
Extended chapters 3 and 4 to two-screen arenas with distant hazards and extra
gravity zones so early maps all showcase scrolling.

## 2025-12-05
Chapters 5 and 6 now span two screens with far spike traps and an extra gravity
zone, keeping the opening stretch focused on horizontal scrolling.

## 2025-12-06
Chapters 7 and 8 now span two screens with distant hazards and extra gravity
zones so the first eight stages highlight camera scrolling.

## 2025-12-07
Chapters 9 and 10 now stretch to two-screen arenas with far spike traps,
wind zones, and extra gravity fields, extending the scrolling focus through the
first ten stages.

## 2025-12-08
Chapters 11 and 12 now expand to two-screen arenas with distant spike traps,
wind zones and extra gravity fields, keeping the scrolling introduction running
through the first twelve stages.

## 2025-12-09
Chapters 13 and 14 now expand to two-screen arenas with far spike traps, wind
zones and extra gravity fields, extending the scrolling introduction through
the first fourteen stages.

## 2025-12-10
Chapters 15 and 16 now expand to two-screen arenas with far spike traps, wind
zones and extra gravity fields, extending the scrolling introduction through
the first sixteen stages.

## 2025-12-11
Chapters 17 and 18 now span two screens with a pit splitting the ground.
Far-edge spike traps and gravity zones remain, so scrolling arenas continue
through the first eighteen stages.

## 2025-12-12
Chapters 19 and 20 keep the two-screen layout and break the floor into multiple
segments for a gauntlet of pits. Far spike traps and distant gravity zones let
the scrolling arena concept run through all twenty chapters.

## 2025-12-13
Gawr Gura now uses a custom stat profile with higher attack but lower defense
and health. Documentation and tests cover the new stats.

## 2025-12-14
Natsuiro Matsuri joins the roster with a firework special that launches an
exploding projectile upward. The roster now features twenty-two characters with
docs and tests updated.

## 2025-12-15
Watson Amelia and Ninomae Ina'nis gain unique stat profiles. Watson moves faster
but starts with lower health, while Ina sports higher defense and a larger mana
pool for frequent specials.

## 2025-12-16
Takanashi Kiara and Mori Calliope receive custom stat profiles. Kiara balances
attack and defense for steady survivability, while Calliope focuses on heavy
strikes but begins with lower health.

## 2025-12-17
Ceres Fauna and Ouro Kronii receive custom stat profiles. Fauna sacrifices
attack for higher defense and health, while Kronii leans into defense with a
modest health pool. Documentation and tests updated.

## 2025-12-18
IRyS and Nanashi Mumei gain tailored stat lines. IRyS reinforces her crystal
shield with higher defense and a larger health pool, while Mumei's flock attack
comes with greater power but reduced resilience. README, plans and tests now
reflect these profiles.

## 2025-12-19
Shirakami Fubuki and Natsuiro Matsuri receive their own stat profiles. Fubuki
trades raw power for speed and slightly less health, while Matsuri leans into
attack with standard defenses. Docs and tests updated.

## 2025-12-20
Sakura Miko and Minato Aqua gain custom stat profiles. Miko becomes a fragile
glass cannon with 12 attack, 3 defense and 85 health, while Aqua shores up
defense over damage at 9 attack, 7 defense and 100 health. README, plans and
tests now reflect these changes.

## 2025-12-21
Usada Pekora and Houshou Marine receive custom stat profiles. Pekora balances
solid attack with 11 attack, 5 defense and 95 health while Marine hits hard with
13 attack, 5 defense and 90 health but carries less health. Documentation and
tests updated.

## 2025-12-22
Hoshimachi Suisei and Nakiri Ayame gain stat profiles. Suisei blends precision
offense with sturdy defenses, and Ayame's dash favors attack over endurance.
README, plans and tests updated.

## 2025-12-23
Shirogane Noel and Shiranui Flare receive tailored stat lines. Noel leans into
defense at 9 attack, 8 defense and 110 health, while Flare's flame burst pushes
12 attack, 4 defense and 95 health. Documentation and tests now cover the
updates.

## 2025-12-24
Oozora Subaru and Tokino Sora gain unique stat profiles. Subaru stays balanced
with 10 attack, 6 defense and 105 health, while Sora favors endurance with 9
attack, 5 defense and 110 health. Documentation and tests updated.

## 2025-12-25
Shirakami Fubuki and Natsuiro Matsuri receive detailed stat profiles. Fubuki
keeps agile with 9 attack, 5 defense and 95 health, while Matsuri pushes offense
at 11 attack, 5 defense and 100 health. Documentation updated across the plan
and README.

## 2025-12-26
Enhanced several special attacks: Aqua's water blast now slows enemies before
bursting, Pekora's carrot bomb bounces once for extra flair, and Matsuri's
firework rises before exploding.

## 2025-12-27
Shirogane Noel's ground slam now emits a forward shockwave and Tokino Sora's
melody travels in a gentle wave, giving both characters distinctive projectiles.

## 2025-12-28
Shiranui Flare hurls a burning fireball that ignites targets while Oozora
Subaru's special now fires a stunning projectile that leaves enemies dazed.
## 2025-12-29
World seeds are now written to the blockchain and the seed manager can sync them
so all clients build MMO regions from the same hashes.

## 2025-12-30
Generated regions are added to the blockchain through a WorldRegionManager so
peers can share identical maps when the MMO world expands.

## 2025-12-31
WorldGenerationManager can now sync seeds and regions from the blockchain so
fresh clients rebuild existing MMO areas before generating new ones.

## 2026-01-01
World sync rebuilds any missing regions from seed blocks so clean installs
recreate the shared MMO world deterministically.
## 2026-01-02
Region blocks now carry a hash and the region manager verifies it during sync so
peers ignore tampered world data.

## 2026-01-03
Game result blocks now spawn a follow-up seed block derived from the game hash
so win/loss history directly feeds MMO world generation.

## 2026-01-04
Seed blocks now store the characters used in each match. A `VotingManager`
collects the most-played avatars and exposes a weekly blockchain vote from the
main menu so players can steer future MMO development.

## 2026-01-05
Character roster loads directly from `DEV_PLAN_CHARACTERS.md`, randomizing the
order each run. The weekly vote now lives entirely on the Vote menu, which
surfaces random candidates instead of auto-casting when a character is chosen.
## 2026-01-06
Character images and spawning now handle unknown names automatically, falling
back to the base `PlayerCharacter` when no dedicated subclass exists.

## 2026-01-07
Character selection now verifies that each name has a matching subclass and
filters out unimplemented fighters. Background mining targets roughly twenty
percent CPU and the node settings warn about the extra resource usage.
## 2026-01-08
Mining now feeds the world generator so every mined hash creates a new region,
letting the MMO world grow automatically from player contributions.
## 2026-01-09
Regions now include a radius and position so each mined block expands the live
world outward in concentric circles.

## 2026-01-10
Region placement now uses a golden-angle spiral so new areas spread evenly
around each expanding ring.

## 2026-01-11
Region blocks now store their spiral angle along with radius and position to
make world layouts easy to verify.

## 2026-01-12
World generation chooses the next region's radius based on the largest existing
value so new areas always land on the next outer ring even if gaps appear.
## 2026-01-13
Each generated region now includes a monument honoring the weekly vote winner,
letting community preferences fill the MMO world with landmarks.

## 2026-01-14
- Expanded autoplay to cycle MMO overlay tabs and toggle hub panels/layers.
- Added adaptive autoplay tuning that persists between runs.
- Enhanced enemy AI experience biasing for longer playthroughs.
- Added autoplay tracing to show inputs on-screen and in the console.
- Added a quick menu mode for autoplay that limits vote sampling per category.
- Added a quick MMO overlay cap for autoplay so menu runs can reach gameplay.
- Added a menu traversal budget to push autoplay into gameplay after a timeout.
- Added an autoplay MMO fast path to skip heavy world generation during runs.
- Disabled autoplay region generation when MMO fast mode is active.
- Added Elite and Adaptive difficulty tiers with smarter enemy positioning.
- Ensured the character selector surfaces at least 20 roster entries.
- Added main menu shortcuts for character and map selection.
- Defaulted the base window size to 1280x720 and reflowed menu spacing.
- Gave the main menu a split-panel layout with a status sidebar.
- Added paged character/map selectors with page indicators and Prev/Next controls.
- Expanded placeholder sprite motifs to better reflect individual character themes.
- Redesigned power-up drop sprites with animated glows and clearer iconography.
- Added unique special-attack animation styles, including dash auras and pulsing
  effects.
- Added textured platform/ground visuals plus stage barrier accents.
- Victory screens now include Auto-Dev reports and MMO briefings, seeded from
  post-match auto-dev plans.
- Added a cooldown tracker and arena minimap to the HUD.
- Refined Victory and Game Over screens with summary cards and next actions.
- Added filter cycling and preview panels to character and map selection.
- Expanded accessibility options with font scaling, high contrast, and prompts.
- Added a header ribbon styling to menu selection screens.
- Added patterned menu backdrops and framed option panels.
- Added animated header badges and selection chevrons to menu highlights.
- Added header state labels and a subtle sheen sweep on option panels.
- Added a subtle animated emblem ring in menu backgrounds.
- Added soft drop shadows to menu panels and summary cards.
- Added orbiting triangle glyphs to the menu emblem.
- Added a Holo Hype streak boost for arena momentum.
- Added combo cheer callouts and a spotlight aura for streaks.
- Added a crowd meter HUD panel that builds into Holo Hype.
- Added stage beams and idol sparkles to reinforce hype moments.
- Added stage ribbons and rotating cheer colors for idol flair.
- Added themed cheer callouts for power-up pickups.
- Added confetti and fan glow effects during Holo Hype.
- Added a short highlight flash when combo milestones trigger.
- Added a short Coliseum intro banner at match start.
- Added boss encore cheers and a small Holo Hype score bonus.
- Added a fan sign wave celebration after early kills.
- Added a crowd light-stick wave during early momentum moments.
- Added boss spotlight swaps during encore callouts.
- Added Special Stage cheers on special attacks.
- Added an MMO Launchpad menu plus post-arena MMO pipeline boosts and actions.
- Arena victories now unlock an MMO trial and offer an MMO supply grant.
- Grouped settings into Controls, Display, Audio, and System subpages.
- Added a `WorldPlayerManager` that tracks player positions in the MMO world.   

## 2026-01-15
The manager now blocks movement beyond generated regions, and a
`ThirdPersonCamera` provides an offset view for a 3rd-person perspective.

## 2026-01-16
`WorldPlayerManager` gained `move_player_relative` so forward and strafe input
can be rotated by a camera yaw for third-person movement.
## 2026-01-17
Added `ClassManager` and `ItemManager` to begin an MMO class and item system.
## 2026-01-18
Added inventory and equipment screens accessible from the pause menu so players
can equip items between battles.

## 2026-01-19
Introduced fantasy weapon and armor item classes and a grid-based equipment
menu that displays head, chest, leg, boot, weapon, offhand and ring slots.

## 2026-01-20
Added Sword, Bow, Wand, Axe and Spear weapon classes along with Tome, Orb and
Quiver offhand items to diversify equipment options.

## 2026-01-21
World generation now assigns a voted-on biome and rolls weapon and armor loot
for each region. The main menu's vote option splits into character and biome
categories.

## 2026-01-22
World regions now award experience to the account that spawned them. A new
`LevelingManager` tracks each player's XP and level so the MMO can scale
content automatically.

## 2026-01-23
Added a `GatheringManager` that turns gathering into a timing mini-game. Hitting
the sweet spot yields rare materials and bonus profession experience that feeds
the crafting system.

## 2026-01-24
Created a `MinigameManager` with a reaction challenge and an `AutoSkillManager`
that crafts new skills from player level and attack stats.

## 2026-01-25
Reaction mini-games now award crafting materials, and new crafting stations let
players combine materials into equipment.

## 2026-01-26
`NetworkManager` consults a `BanManager` to drop packets from banned user IDs,
blocking abusive peers.

## 2026-01-27
`AuthManager` now stores salted password hashes and locks accounts after three
failed logins, improving overall authentication security.

Session tokens now expire after an hour and a logout helper revokes them early,
so stolen tokens cannot be reused indefinitely.

## 2026-01-28
Introduced a `SharedStateManager` to broadcast synchronized gameplay data and
added combo-based scoring via `ScoreManager`.

## 2026-01-29
Added a Quick Start option on the main menu that launches the first story
chapter immediately.

## 2026-01-30
Floating damage numbers now appear when hits land, providing clearer combat
feedback.

## 2026-01-31
Added a `StateVerificationManager` that attaches CRC32 and SHA256 digests to
shared state packets so peers can verify game values with minimal memory.

## 2026-02-01
Introduced an Achievements menu listing unlocked milestones and saving them
between sessions.

## 2026-02-02
Pause menu now offers an Achievements option. Defeating the first enemy unlocks
the "First Blood" achievement.

## 2026-02-03
Settings menu gains an Accessibility submenu with a colorblind mode toggle.

## 2026-02-04
Added a Goals screen on the main menu that lists top project objectives.


## 2026-02-05
Added an `MMOBuilder` module that constructs seed, generation, region, player and voting managers for automatic MMO setup.

## 2026-02-06
Added generators for class skills, subclasses and trade skills along with an
auto balancer for class stats.

## 2026-02-07
Created a ClassGenerator to ensure unique class templates and updated
ClassManager to reject duplicate names.

## 2026-02-08
Added InteractionGenerator and InteractionManager to auto-create basic
interactive objects.

## 2026-02-09
Added a RecursiveGenerator that chains class, skill and trade generators and
let players pick an input method from the Settings menu.

## 2026-02-10
Added key rotation support so encryption and signing keys can update during a
session via `DataProtectionManager.rotate_keys` and `NetworkManager.rotate_keys`.

## 2026-02-11
Introduced an orange extra-life power-up that grants an additional life when
collected and is scheduled by the spawn manager.

## 2026-02-12
Added a mana power-up that fully restores the player's mana and is scheduled by
the spawn manager.

## 2026-02-13
Added a cyan stamina power-up that refills the player's stamina bar and is
scheduled alongside other pickups.

## 2026-02-14
Improved collision handling so invincible players ignore projectile, melee and
contact damage.

## 2026-02-15
Added critical hits so attacks sometimes deal double damage using a new
``crit_chance`` stat.

## 2026-02-16
Critical strikes now spawn yellow damage numbers, making powerful hits easy to
spot during battles. Enemy squad focus now uses a short hold window in
`AIManager` so groups avoid rapid retarget jitter when threat scores are close,
with tests covering both focus-hold and fallback target switching. Squad
special pacing now adapts to pressure as well, reducing the shared cooldown for
larger groups and high-focus openings.

## 2026-02-17
Added passive health regeneration so players regain one point per second after
three seconds without taking damage.

## 2026-02-18
Introduced a red attack power-up that temporarily increases the player's attack
stat.

## 2026-02-19
Added a violet defense power-up that temporarily boosts the player's defense
stat.

## 2026-02-20
Dodging now grants brief invulnerability frames so players can avoid damage with
well-timed rolls.

## 2026-02-21
Power-ups are collected even during dodges by sweeping the player's movement,
preventing missed pickups when rolling through them.

## 2026-02-22
Players cannot pick up power-ups while dodging, so items require a pause in
movement to collect.

## 2026-02-23
Goal analysis skips missing snapshot files to avoid crashes when paths are
absent.

## 2026-02-24
Added a ``crit_multiplier`` stat so critical hits can scale beyond double
damage. Updated damage calculations, stats manager, and tests.
 
## 2026-02-25
Enemies now roll for loot when defeated, with drops added to the player's
inventory to support future MMO itemization.

## 2026-02-26
Added a lightning zone hazard that periodically zaps and launches sprites,
expanding arena variety for future MMO regions.

## 2026-02-27
InventoryManager now accepts an optional capacity and the player inventory is
limited to thirty items, paving the way for MMO-style storage upgrades.

## 2026-02-28
Inventory now persists between sessions. LevelManager saves and loads items via
the save manager so progression carries into future MMO modes.

## 2026-03-01
Players can consume health potions from their inventory by pressing **H**,
restoring health and paving the way for more consumable items in the MMO.

## 2026-03-02
Player characters now earn experience for each defeated enemy, and the HUD
shows their current level to prepare for future MMO progression.

## 2026-03-03
Players can press **J** to drink a mana potion, restoring mana from inventory
and broadening consumable support for future MMO systems.

## 2026-03-04
Level ups now boost attack and max health, letting characters grow stronger as
they gain experience and progress toward MMO-scale power.

## 2026-03-05
Coin balances now persist between sessions. The game saves and reloads coins via
the settings file so the MMO economy can build over time.

## 2026-03-06
Enemies now patrol around their spawn points when the player is distant, keeping
arenas active and laying groundwork for roaming creatures in the MMO world.

## 2026-03-07
Added a day/night cycle via `EnvironmentManager` and hooked it into the game
loop so arenas shift lighting over time, paving the way for MMO time-of-day
events.

## 2026-03-08
Levels now roll random weather through `EnvironmentManager`. Rainy maps lower
friction, setting the stage for dynamic climates in future MMO regions.

## 2026-03-09
Introduced a quicksand hazard that drags fighters down and slows their
movement, preparing for desert regions in the MMO world.

## 2026-03-10
Added a fire zone hazard that ignites characters with burn damage over time,
laying groundwork for volcanic MMO regions.

## 2026-03-11
Introduced frost zones that freeze fighters briefly, establishing icy arenas
for future MMO regions.

## 2026-03-12
Added a TeamManager and wired it into CombatManager so allies no longer take
damage from each other, paving the way for team battles in the MMO.

## 2026-03-13
Added a fullscreen toggle in the settings menu so players can swap display modes,
supporting varied setups as the MMO expands.
## 2026-03-14
Introduced a sprint action that drains stamina for faster movement, preparing
for agile exploration in future MMO regions.

## 2026-03-15
Added a poison zone hazard that applies `PoisonEffect` for damage over time,
setting up toxic regions in the future MMO.

## 2026-03-16
Added a silence zone hazard that applies `SilenceEffect` to block special
attacks, foreshadowing anti-magic areas in the MMO.

## 2026-03-17
Added experience power-ups that grant extra XP when collected, accelerating
character progression for future MMO growth.

## 2026-03-18
Added a snowy weather type that increases friction via `EnvironmentManager`,
laying groundwork for wintry MMO regions.

## 2026-03-19
Added a screen-shake effect through `CameraManager` and hooked it to player
damage for punchier combat feedback.

## 2026-03-20
Added a red screen flash whenever the player takes damage for clearer hit
feedback and future MMO combat effects.

## 2026-03-21
Displayed the active score combo on the HUD so players can track streaks and
earnings, enhancing feedback for future MMO combat.

## 2026-03-22
Added a pulsing red low-health warning on the HUD to alert players during tough
 battles.
## 2026-03-23
Rendered small health bars above enemies to clarify remaining threats for future MMO encounters.
## 2026-03-24
Introduced regen zones that slowly heal sprites standing inside, adding safe
areas for longer battles and future MMO arenas.

## 2026-03-25
Connected the `ReputationManager` to combat so enemy defeats grant faction
standing, persisting between runs and surfacing on the Records menu to set up
future MMO diplomacy systems.

## 2026-03-26
Linked arena matches to the shared MMO world by adding an
`EventModifierManager`. It reads the latest generated region and applies
biome-themed modifiers during level setup, slowing stamina regen in deserts,
boosting experience in forests and amplifying hazard damage in tundra regions.
The change introduced fractional stamina regeneration and hazard damage
scaling so these seasonal events feel meaningful in the Coliseum.

## 2026-03-27
Extended `EnvironmentManager` with weather-tinted ambient lighting overlays.
The game now dims or brightens the arena based on the MMO day/night cycle so
Coliseum battles visibly share the same evolving world.

## 2026-03-28
Hooked a deterministic `WeatherForecastManager` into `EnvironmentManager`. Both
the MMO world and Coliseum matches can now preview upcoming storms and share the
same weather schedule, keeping climate changes synchronized across modes.

## 2026-03-29
Introduced an `ObjectiveManager` that builds daily and weekly goals from the
current region. Enemy defeats, coin gains, power-up pickups, and match victories
feed the manager, and completed objectives pay out coins or experience. Progress
is rendered on the HUD and objectives persist through the save system so arenas
and MMO regions stay aligned.

## 2026-03-30
Character voting is now entirely menu-driven and the resulting tallies apply
balancing modifiers during level setup. Low-vote fighters earn small buffs while
popular picks are gently nerfed so the roster stays competitive without manual
tuning.

## 2026-03-31
Voting timestamps are stored per category so accounts can cast character, biome,
and future ballots in the same week. The vote manager migrates existing data and
keeps parallel polls synchronized on disk.

## 2026-04-01
Coliseum matches now report their score, duration, character choice and hazard
interactions to an `AutoDevFeedbackManager`. The world generator reads this
telemetry when creating new MMO regions, updating recommended levels and
recording the trending hazard in an ``auto_dev`` field so the arena drives
future content automatically.

## 2026-04-02
Auto-development insights now seed a hazard mastery objective. The objective
manager reads the ``auto_dev`` field from generated regions and adds a weekly
goal targeting the trending hazard so arenas train players for upcoming MMO
zones. Hazard collisions now notify the manager so progress advances as soon as
players survive those traps.

## 2026-04-03
Added an `AutoDevTuningManager` that translates hazard telemetry into arena
support plans. The manager shortens spawn timers for counter power-ups whenever
hazard challenges spike and stores the resulting `support_plan` alongside the
world generator's `auto_dev` insight so MMO regions highlight the same defensive
tools that arenas are practicing with.

## 2026-04-04
Introduced an `AutoDevProjectionManager` to forecast the hazards most likely to
pressure upcoming runs. The projection feeds both the region metadata and the
arena HUD so designers can line up counter-power-ups before the MMO rotates in
those threats.

## 2026-04-05
Linked the projection and objective data through a new `AutoDevScenarioManager`.
World generation now stores scenario briefs that list the hazard, recommended
counter plan and objective reminders so MMO designers can stage focused drills
for upcoming threats.

## 2026-04-06
Introduced an `AutoDevRoadmapManager` that compiles feedback summaries, tuning
plans, projection focus entries and scenario briefs into a single roadmap entry
on each generated region. Designers can now review priority actions and
counter-power-up recommendations without stitching together data from multiple
managers.

## 2026-04-07
Added an `AutoDevFocusManager` that weights roadmap focus, feedback trends,
projection danger scores, scenario briefs and tuning plans to produce a concise
``auto_dev.focus`` report. The world generator stores this sprint summary on
each region so designers, narrative leads and encounter builders share the same
priority list when expanding the MMO.

## 2026-04-08
Extended the auto-dev pipeline with encounter tooling. Monster, spawn, mob-AI
and boss managers now turn the focus report into themed mobs, group scheduling
and set-piece fights, while the quest manager links regional trade skills to
those bosses. The research manager records the raw CPU percentage used to study
other games so the managerial intelligence guiding the MMO knows when to scale
or throttle background experimentation.

## 2026-04-09
Upgraded the research manager to sample live CPU load so regions capture the
latest raw utilisation percentage alongside historical averages. Introduced an
`AutoDevGuidanceManager` that stitches monsters, spawn danger, AI directives,
boss picks, quests and research data into a managerial guidance brief the world
generator stores on each region.

## 2026-04-10
Introduced an `AutoDevEvolutionManager` that merges guidance, roadmap, focus,
research and encounter data into a horizon-based evolution brief. World
generation stores the plan alongside monsters, spawn groups and quests so MMO
planners receive concrete next actions with the latest processing utilisation
figures.

## 2026-04-11
Recorded raw utilisation percentages in the research manager summary and added
an `AutoDevIntelligenceManager` that audits monsters, spawn plans, quests,
guidance and evolution data. World generation now stores the resulting
general-intelligence brief so planners see overall compute load, encounter
alignment and strategic directives for each region.

## 2026-04-12
Expanded the intelligence brief with encounter blueprints, quest synergy data
and backend guidance. Regions now expose group sizing, AI behaviours, boss
synergy, quest coverage and the raw research percentage inside the oversight
summary so planners can rebalance compute when utilisation spikes.

## 2026-04-13
Broadened the general-intelligence brief with monster catalogues, spawn tempo
summaries, mob-AI development cues, boss outlooks and trade-skill matrices so
each region records deeper encounter context alongside processing utilisation.

## 2026-04-14
Layered additional analytics into the auto-dev intelligence brief. Regions now
capture group mechanics (lanes, burstiness and spawn tempo), mob AI training
gaps, boss pressure relative to supporting monsters, and detailed quest
dependencies. The brief also records a processing utilisation breakdown and the
overlap between guidance directives and upcoming evolution objectives so
back-end planners can steer the MMO's self-evolution with richer data.

## 2026-04-15
Extended the general-intelligence report with monster creation queues, lane
reinforcement tactics, AI iteration plans, boss spawn strategies and quest
cadence summaries. The report now exposes the raw processing percentage
alongside averages everywhere it appears, and world regions store the raw value
next to the existing utilisation metric so planners can balance compute, trade
skills and boss encounters from a single view.

## 2026-04-16
Augmented the auto-dev intelligence layer with processing-channel analytics,
an orchestration pipeline that flags which stages still need attention, and a
management playbook that recommends backend actions. Regions now surface the
per-channel utilisation split plus the next unblock step so operations teams
can react quickly when research or evolution work overheats.

## 2026-04-17
Tracked competitive-research samples so the auto-dev research manager records
how much raw compute goes into analysing other games. The intelligence brief
now reports the rival focus alongside spawn-lane coordination, mob-AI
innovation, boss-readiness signals and trade-skill alignment, rolling those
metrics into a new managerial snapshot so backend teams can steer the MMO's
self-evolution with concrete coordination and utilisation data.

## 2026-04-18
Extended the auto-dev research brief with explicit competitive raw percentages
and the share of the latest utilisation sample allocated to rival studies. World
generation now stores monster creation, group spawn, mob-AI, boss spawn and
quest-generation summaries alongside those research ratios. The general
intelligence layer gained monster-forge status tracking, detailed group-spawn
mechanics, mob-AI innovation cadence, boss spawn matrices, quest tradecraft
reports, research pressure gauges and managerial alignment snapshots so backend
guidance can see how creation, spawns, AI, bosses and trade skills evolve
against competitive research budgets.

## 2026-04-19
Added an AutoDevNetworkManager that summarises relay latency, reliability,
bandwidth trends and security incidents. World generation now records the
network brief on each region, and the intelligence layer reports network health,
security posture, upgrade recommendations, processing overhead and the latest
security focus alongside the existing encounter analytics so planners can
balance compute and relay budgets from a single report.

## 2026-04-20
Extended the networking analytics with automated security scoring, holographic
transmission metrics and verification layers. Network briefs now include the
automation score, recommended control playbooks, layered anchor quality and a
spectral throughput index, and these values flow into world generation and the
general-intelligence report. The holographic compression pipeline records layer
metadata and spectral hints so auto-dev can reason about anchor integrity while
maintaining lightweight packets.

## 2026-04-21
Refined the auto-dev pipeline so monster rosters now expose AI foci and spawn
synergies, group plans report reinforcement curves, mob AI directives surface
training modules and boss plans list battle strategies. Quest generation tracks
difficulty tiers and tags tied to trade skills, letting the intelligence brief
summarise tradecraft at a glance. Network analytics add automation tiers and a
channel map while holographic packets record phase signatures, layer energy and
channel vectors to strengthen the lithographic transport telemetry.

## 2026-04-22
Captured a dedicated competitive research pressure gauge so the intelligence
brief highlights how much raw processing is spent studying other games, and fed
the value into world generation for region dashboards. Network analytics now
produce an upgrade backlog, security auto-dev directives and holographic
diagnostics that summarise triangulation and anchor health. Holographic
compression emits triangulation metadata, vector maps and vparam listings so
network security tooling can reason about packet geometry while keeping the
pointcloud payload compact.

## 2026-04-23
Auto-dev intelligence gained mutation-path tracking, group-support matrices,    
AI modularity maps and boss latency alerts so planners can cross-check monster  
creation, spawn tactics and trade-linked quests from one brief. Research        
benchmarking now records primary rival titles and utilisation trends while a    
managerial guidance map calls out whether to realign, defend or boost support.  
Network analytics layer on a resilience matrix, zero-trust blueprint and        
anomaly tally, and holographic compression ships bandwidth profiles,
telemetry signatures and stability indices to strengthen lithographic packet    
verification.

## 2026-04-24
Character and map grids now show P1/P2 selection badges in local multiplayer,  
map selection resolves randomly between the players' chosen stages, and the map
menu includes a Random Map option for quick picks.

## 2026-04-25
Selection screens now include guidance panels and active-picker callouts, while 
arena enemies can dash to close distance and fire a special volley attack.      

## 2026-04-26
Settings submenus now return to their parent sections so autoplay can traverse 
controls and system tooling in one visit.
Autoplay skips destructive system actions unless explicitly enabled.
Map thumbnails now resolve for every map name with placeholders when artwork is
missing, so story maps show up cleanly in the grid.
Menu thumbnails now scale to grid size to keep character/map/chapter layouts
consistent.
Chapter selection now mirrors the framed grid styling and includes a guide
panel plus selected chapter feedback.
Character select now shows an input prompt to match the map and chapter menus.
Map selection now echoes the current single-player pick alongside the grid.
Chapter selection now shows a chapter preview panel and a character portrait
panel so story picks stay connected to the roster.
Lobby menus now include match summary, roster cards, and stage/portrait preview
panels for consistent pre-match context.
Autoplay now sweeps character, map, and chapter previews before selections to
keep the UI visible during automated tours.
Map and chapter previews now surface a simple threat rating to guide stage
selection.
Lobby readiness cards now include Ready/Waiting indicators plus a stage preview
carousel.
Autoplay preview sweeps now pause briefly before cycling; timing is controlled
by `HOLO_AUTOPLAY_PREVIEW_DELAY`.
Placeholder sprites now support expanded Hololive and map motifs with extra
panel striping to look more professional at runtime.
HUD now shows a stage threat chip during matches.
Threat-aware AI now boosts aggression on higher-threat stages.
Added a standard sprite generator script for deterministic local assets.
Added a deterministic special-attack VFX sprite generator that now outputs
multi-frame sequences, and wired specials to animate them when present.
Autoplay now adapts aggression, caution, and defensive timing to stage threat.
Arena maps now extend wider with camera panning, floor gaps that trigger fall
deaths, and a brief revive invulnerability window on respawn.
Autoplay agent now kites, sprints, avoids fall gaps, and reports periodic
telemetry via the new monitoring interval.
Matches now allow toggling the autoplay agent on/off with the F10 key.
Autoplay can now run an explorer profile that intentionally samples features
and writes detailed logs into `SavedGames/autoplay.log`.
