# Hololive Coliseum
Prototype platform fighter featuring Hololive VTubers.
All playable characters extend a common `PlayerCharacter` class providing movement,
combat actions and resource tracking. The roster is generated from
`docs/DEV_PLAN_CHARACTERS.md`. The game verifies that each listed name has a
matching subclass before adding it to the selection grid, ensuring every fighter
has a unique implementation. Weekly blockchain votes are cast directly from the
Vote menu and present a random set of candidates each run. Players can cast one
ballot per category each week, letting character, biome, and future votes run in
parallel without waiting for other polls. Recent vote totals feed into
matchmaking balance: underrepresented characters receive small stat buffs while
the most popular picks are trimmed slightly so the roster stays competitive week
to week.
A **Quick Start** option on the main menu jumps straight into the first story
chapter. The pause menu offers Inventory, Equipment, and Achievements screens so
items can be managed between fights and milestones reviewed. Defeating your
first enemy unlocks the "First Blood" achievement. When foes fall a loot table
roll awards random items to the player's inventory, which holds up to thirty
items by default. Inventory contents persist between sessions, laying
groundwork for MMO-style itemization and future storage upgrades. Press **H**
to drink a health potion when one is available or **J** to sip a mana potion,
consuming the item from the inventory and restoring the corresponding
resource.
Hold **Right Shift** to sprint, draining stamina for a brief burst of speed.
Each defeated foe also grants experience, raising the player's level shown on
the HUD. Level ups boost attack and max health, supporting long-term MMO
progression.
The main menu now uses a responsive layout and resolution-aware font scaling so
text remains legible from low to high display sizes.
Every enemy is tagged with a faction, and defeating members of that faction
earns reputation tracked by the `ReputationManager`. Reputation totals persist
between sessions and appear on the Records screen, laying groundwork for
faction-based progression in the eventual MMO.
MMO hub networking tracks remote player presence and prunes stale peers to keep
the shared roster accurate.
Join/leave signals and snapshot requests let reconnecting peers resynchronize
their MMO hub state quickly.
The MMO world layer now syncs region summaries, influence, events, outposts,
operations, and trade routes using distributed deltas and snapshots.
Shard identifiers keep MMO management sessions isolated while conflict
resolution merges newer updates across peers. World state sync resets when the
active shard changes to prevent cross-shard bleed-through.
World removals propagate through tombstones so expired events and retired
entries converge without a central server.
Distributed matchmaking queues pair players through host nodes without a
central service.
Match readiness now uses accept/decline handshakes and auto shard selection
balances load across management shards.
Match status is displayed in the MMO status panel, with a ready countdown in the
MMO header, and shard migration can be triggered to move to a healthier shard.
Directives and bounties now sync through the MMO world layer with tombstone
removals for consistent cleanup.
Shard health is visible in the Network panel, with manual cycle/confirm controls
and auto-migration thresholds for balanced routing.
Shard switches cache the last known world state per shard and restore it on
return while still requesting fresh snapshots for validation. Cache entries
expire after a short TTL to avoid reusing stale shard data.
The MMO HUD now includes a shard status widget and refreshed neon styling for a
futuristic Hololive-themed presentation.
Allied fighters now trigger support actions, dropping emergency healing zones
or shield bursts when the player is in danger.
Arena AI callouts provide lightweight taunts and support chatter during intense
moments; toggle with `HOLO_AI_CALLOUTS=0` to silence them.
Callouts now include coordinated focus-fire cues plus stamina/mana warnings
when the player is running low.
Enemy squads now hold their focus target briefly when threat scores are close,
reducing rapid retarget jitter while still swapping quickly to high-priority
openings.
Squad special cooldown now adapts to pressure: larger enemy groups and strong
focus opportunities trigger earlier follow-up specials to keep encounters
aggressive without fully removing shared cooldown pacing.
Self-evolution blueprints now surface adaptive tuning guidance, linking
continuity risk, resilience grade, and governance state into a cadence and
risk-budget recommendation for the live pipeline.
Adaptive tuning now feeds into mob spawn pacing, adjusting wave sizes and
intervals alongside power-up spawn timers.
An `ObjectiveManager` now rotates daily and weekly goals based on the active
region. It watches enemy defeats, coin gains, power-up pickups, and match wins,
awarding coins or experience when objectives finish. Progress appears directly
on the HUD so arenas and the evolving MMO share the same set of strategic
targets. Auto-development telemetry now adds hazard mastery objectives,
challenging players to endure whichever trap is currently trending so Coliseum
runs prepare explorers for the MMO's next regions. Rotation is deterministic
through an injected UTC time provider, so daily and weekly resets, streak
bonuses, persistence, telemetry hooks, and debug simulations all behave
consistently in tests and tooling.
An `AutoDevScenarioManager` converts those hazard projections and objectives
into scenario briefs. Each region stores the recommended counter plan and
objective reminders so MMO designers see ready-made drills for the latest
hazards.
New auto-development managers push the pipeline further: an
`AutoDevMonsterManager` assembles themed enemy rosters, the spawn and mob-AI
managers choreograph group deployments and behaviours, and an
`AutoDevBossManager` ties the most dangerous threats into headline encounters.
The quest manager then links local trade skills with those bosses so regions
ship with handcrafted tasks. The research manager samples live CPU load,
records the raw percentage invested in studying rival games, and stores both
averaged and on-the-spot utilisation values so planners can redirect budgets in
seconds. The `AutoDevGuidanceManager` rolls every insight into a managerial
brief, the `AutoDevEvolutionManager` turns those signals into horizon-based
action plans, and the new `AutoDevIntelligenceManager` audits the entire
pipeline to provide general-intelligence oversight that keeps the MMO's
self-evolution on track.
A complementary `AutoDevNetworkManager` now evaluates the relay mesh, tracking
latency averages, node reliability, bandwidth trends, and security incidents.
Its brief feeds both world generation and the intelligence layer so planners
know when to promote fresh relay hubs, harden routes after suspicious traffic,
or pre-provision bandwidth before weekend surges. The brief now publishes the
network processing load and the current security focus, giving backend teams a
single view of relay health, compute draw, and mitigation priorities. Security
automation scores, recommended control playbooks, and holographic transmission
metrics (layer counts, anchor quality, encrypted channels) are surfaced for the
auto-dev intelligence manager so MMO guidance can react immediately to network
pressure.
The latest iteration adds a competitive research pressure gauge that surfaces
the raw percentage spent studying rival games, a security auto-dev overview that
merges automation focus with upgrade backlogs, and holographic diagnostics that
report triangulation quality, anchor health, and verification integrity. The
general-intelligence brief now publishes a self-evolution dashboard tying
backend directives, pipeline stages, and relay processing data together so
planners see where compute is invested at a glance.
Fresh enhancements extend that general-intelligence layer with mutation-path
tracking for monster rosters, group-support matrices that reflect which quests
reinforce spawn lanes, and modular AI maps that highlight reusable behaviour
packages. Boss spawn alerts now factor in live relay latency while quest trade
dependencies summarise every craft that feeds a headline encounter. Research
benchmarking lists the primary rival game alongside utilisation trends and the
managerial guidance map recommends whether planners should realign, defend, or
boost support. A dedicated action feed captures the next self-evolution steps
so regions carry explicit follow-up tasks for the auto-dev crew.

The auto-dev stack now fabricates monster creation blueprints that bundle
mutation tracks, spawn threads, and staged AI development paths so encounter
designers can forecast how mobs evolve alongside their cohorts. Group spawn
planning surfaces cohort matrices, escalation plans, and support threads which
feed directly into expanded mob-AI coordination matrices and evolution threads.
Boss selection folds in spawn-lane support, phase transitions, and trade-skill
hooks while quests annotate their spawn dependencies and trade synergies. The
research brief highlights raw utilisation percentages dedicated to rival-game
studies, the guidance layer grades managerial intelligence with self-evolution
vectors, and the network overview now delivers holographic phase-shift maps,
channel vectors, and upgrade paths that marry security auto-dev directives with
lithographic transmission health.

The newly introduced `AutoDevBlueprintManager` layers a dedicated functionality blueprint pass over those creation and mechanics feeds. It rolls functionality scores, mechanics novelty, creation risk, and the latest codebase debt snapshot into cohesion, alignment, and gap indices while fusing network and holographic requirements from the supporting managers. Blueprint briefs now enumerate the tracks, threads, and backend actions that tie mechanics concepts back to the codebase modules slated for hardening so the MMO's self-evolving guidance can stage functionality upgrades with the same care applied to encounter and network planning.

Building on that, the `AutoDevIterationManager` blends functionality, mechanics, creation, and blueprint telemetry with network-upgrade, security, and holographic diagnostics so planners receive deterministic iteration cycles. Its brief aggregates iteration scorecards, gap summaries from the codebase analyzer, network auto-dev upgrade hooks, and lithographic guardrail requirements into a single actionable snapshot. The manager also folds research utilisation pressure, innovation novelty, and execution windows into explicit actions so managerial intelligence can schedule functionality/mechanics prototypes with awareness of processing utilisation and security guardrails.

An `AutoDevPipeline` module now wraps those managers into a single orchestrated
entry point. It builds monster rosters, spawn groups, mob-AI directives, boss
focus, quest chains, and research reports before fusing them into guidance and a
network brief. The pipeline also exposes a holographic transmission snapshot,
surfacing channel, diagnostic, phase-shift and enhancement matrices so
networking upgrades and security auto-dev tooling can react to real processing
utilisation in one call. The orchestrator now tracks a managerial general-
intelligence score alongside the narrative rating, publishes a backend guidance
vector, and records a governance outlook so live-ops planners can see whether
automation is operating in monitoring, directed, or autonomous modes.
A weakness-analysis pass highlights fragile areas by combining network health,
security scoring, research pressure, and managerial posture into one mitigation
brief. A new `AutoDevCodebaseAnalyzer` feeds that pass with repository metrics,
flagging high-complexity modules, missing docstrings, and under-tested systems
while tracking a risk-weighted debt profile so the pipeline can surface concrete
remediation tasks alongside encounter and network guidance. The freshly added
`AutoDevMitigationManager` then turns those
signals into prioritised action lists, scheduling security hardening, codebase
refactors, research throttles, and holographic transmission upgrades into
immediate, sprint, and continuous execution windows so the auto-dev loop begins
implementing fixes instead of only reporting on them. A companion
`AutoDevRemediationManager` now consumes those task lists, applies a simulated
set of high-priority fixes, projects the resulting security, coverage, and
research improvements, and records which holographic layers were activated so
engineers can tell which mitigations are already handled by automation versus
those that remain queued for the next sprint.

An `AutoDevEvolutionManager` folds the monster, spawn, quest, research, and
guidance streams into a forward-looking evolution brief so leadership can see
how much processing the self-guided loop is consuming, which objectives lock the
next horizon, and where trade skills should be promoted to support those goals.
The transmission layer now receives attention from an `AutoDevTransmissionManager`
that calibrates holographic compression algorithms, phase-alignment actions, and
security-layer depth based on network telemetry, mitigation priority, and the
latest remediation results. Its calibration output accompanies the traditional
holographic snapshot so network automation knows whether to favour aggressive
compression, hardened encryption, or bandwidth preservation for lithographic
links. A dedicated stability report summarises the baseline and projected
security/coverage deltas, annotates the debt outlook produced by the analyzer,
and highlights monitoring notes when research utilisation spikes, giving the
auto-dev planners a single confirmation that the requested fixes are actually
closing the weaknesses they identified.
A newly added `AutoDevResilienceManager` now tracks how those fixes translate
into live resilience. It blends code coverage, network security automation,
research pressure, and holographic guardrail data to produce a deterministic
resilience grade, highlight the most urgent stabilisation actions, and note
where lithographic transmissions need tuning. The pipeline publishes that brief
alongside a managerial intelligence matrix that fuses guidance posture, network
guardrail status, resilience actions, and projected stability deltas so the
managerial general intelligence driving the MMO can steer backend automation
without leaving the orchestrated plan.
The resilience stream now feeds an `AutoDevContinuityManager` that creates a
repeatable outlook for the next two weeks. Its continuity plan captures short-
term stabilisation windows, mid-term security automation pushes, and longer-
range technical-debt retirements while blending the network security backlog,
codebase weak spots, mitigation directives, and holographic guardrail data. The
resulting continuity report exposes a risk digest, refreshed network security
playbooks, and holographic transmission actions so planners can see which
improvements are already queued by auto-dev versus which ones still need manual
shepherding. Those continuity signals are threaded back into the managerial
intelligence matrix, giving leadership an explicit continuity index, focus, and
timeline next to the resilience and governance summaries.
An `AutoDevGovernanceManager` now sits on top of those feeds, calculating an
oversight score and state that reflect network security, projected remediation
gains, continuity health, and holographic readiness. It distils the backlog
from mitigation, continuity and guardrail directives into a manageable set of
oversight actions, highlights which areas (network, codebase, continuity or
security) demand attention, and publishes a backend support map with alignment
and holographic scores so leadership knows where to reinforce the auto-dev
loop. Governance outputs are threaded directly into the managerial intelligence
matrix, keeping the guidance layer aware of the current oversight posture and
recommended actions.
A newly introduced `AutoDevSelfEvolutionManager` blends those governance
signals with guidance, network security, remediation progress, transmission
calibration, and raw research utilisation into a blueprint for the MMO's
self-evolution cadence. The blueprint emits a readiness index, state, and next
actions that fold in network upgrade directives, security hardening steps,
codebase modernisation focus, and holographic guardrail tuning. It also
summarises remediation throughput across codebase, network, and research
domains so managerial intelligence can see which weaknesses are already being
addressed. The auto-dev pipeline publishes that blueprint alongside the plan
output and mirrors the readiness state inside the managerial intelligence
matrix, keeping backend guidance tightly coupled to the expanded holographic
and security automation feeds.
To keep that loop anchored in live network telemetry, an
`AutoDevNetworkUpgradeManager` now fuses the network assessment, security brief,
transmission calibration, and modernization targets into a network auto-dev
plan. The manager reports upgrade tracks, security automation follow-ups,
holographic actions, and processing health while linking back to the codebase
modules that impact networking or lithographic relays. Its readiness score and
priority feed the managerial intelligence matrix, while the auto-dev plan
exports a reusable `network_auto_dev_plan` and pre-digested action list so
operations teams can accelerate upgrades, hardening, and holographic tuning
without guessing which weak spots matter most.
To translate those modernization targets into specific fix sequences, the
`AutoDevModernizationManager` correlates codebase scorecards, remediation
throughput, network security posture, and holographic calibration directives.
It prioritises high-risk modules, highlights which holographic adjustments and
network guardrails unblock them, and maps mitigation and remediation actions
onto sprint-sized timelines. The resulting modernization brief publishes
cross-domain actions, weakness resolutions, and research allocation guidance
that are mirrored in the managerial intelligence matrix so backend planners can
track modernization urgency alongside governance, security, and continuity
signals.
A complementary `AutoDevOptimizationManager` then layers modernization
priorities with the network auto-dev plan, remediation throughput, and
holographic calibration to identify the highest-impact optimisation windows. It
reports the backend focus required to reinforce managerial intelligence,
packages network hardening directives, and keeps holographic guardrail actions
paired with the remediation forecast so teams can align fixes with lithographic
adjustments. The optimisation brief also condenses codebase weaknesses,
modernization dependencies, and fix windows into a reusable action list that is
mirrored inside the managerial intelligence matrix and pipeline exports,
ensuring backend planners have a direct line from weakness analysis to applied
upgrades.

To keep those optimisation and modernization pushes grounded in tangible
improvements, an `AutoDevIntegrityManager` now fuses coverage telemetry,
security scores, holographic diagnostics, modernization targets, optimisation
actions, and resilience insights into a unified integrity report. The manager
highlights coverage, security, and holographic gaps, tracks phase-alignment
delta, and distils restoration, holographic, and network hardening actions so
backend planners know which fixes reinforce lithographic transmissions versus
codebase stability. The auto-dev pipeline exports this report as
`integrity_report` while mirroring top-level values such as
`integrity_score`, `integrity_priority`, `integrity_restoration_actions`,
`holographic_integrity_actions`, and `network_hardening_actions`, and the
managerial intelligence matrix now surfaces the same priority and action set for
oversight teams.
To extend encounter creativity, an `AutoDevMechanicsManager` now blends monster
archetypes, quest synergies, mob AI evolution threads, modernization targets,
and holographic diagnostics into a mechanics blueprint. The manager scores
novelty, cohesion, and risk, packages functionality tracks that connect
modernization, optimisation, and remediation work, and surfaces gameplay
threads alongside network and transmission considerations so backend planners
understand how new mechanics impact infrastructure. The pipeline exports the
blueprint as `mechanics_blueprint` and mirrors its priority, novelty and risk
scores, functionality tracks, gameplay threads, and holographic/network hooks
within the managerial intelligence matrix for quick planning reference.
Building on that blueprint, an `AutoDevInnovationManager` synthesises mechanic
novelty, modernization targets, optimisation support, network posture, and
holographic calibration into a functionality innovation brief. The manager
grades innovation momentum, maps functionality tracks to concrete feature
concepts, and details the network, security, and holographic requirements that
each concept will demand. Research pressure, backend guidance threads, and
recent remediation progress are folded into the brief so the managerial
intelligence matrix and exported plan surface the priority, innovation score,
backend action bundles, and gameplay inspirations required to evolve MMO
functionality alongside the auto-dev security, modernization, and resilience
cycles.
An `AutoDevExperienceManager` now interprets the mechanics blueprint, the
innovation brief, modernization priorities, resilience posture, and continuity
timelines into experience arcs that capture how new functionality will land in
play. The manager blends gameplay threads with innovation feature concepts,
evaluates experience momentum, and packages functionality enhancements with the
network, security, and holographic choreography required to deliver them. The
pipeline exports the resulting `experience_brief` alongside the orchestrated
plan, surfacing experience priorities, arcs, backend directives, research
implications, and network blueprints. The managerial intelligence matrix mirrors
those priorities, enhancement bundles, and experience threads so planners can
see how functionality creation interacts with modernization, security, and
holographic workloads when guiding the MMO's self-evolution.
To push functionality planning even further, an `AutoDevFunctionalityManager`
now synthesises the mechanics, innovation, and experience telemetry with the
codebase analyzer, modernization playbooks, mitigation priorities, and
network-security automation. The manager assembles functionality tracks that tie
feature concepts to modernization steps, remediation progress, and
self-evolution directives, grades the opportunity versus risk using resilience
and integrity posture, and outlines the holographic and network requirements
needed to launch each concept safely. It also captures continuity windows,
managerial directives, and research implications so the backend guidance layer
can coordinate functionality experiments with trade-skill quests, holographic
upgrades, and security guardrails. The auto-dev pipeline exposes this briefing as
`functionality_brief`, mirroring its priority, tracks, directives, and risk
indices in both the plan payload and the managerial intelligence matrix to keep
functionality creation tightly coupled with mitigation and modernization work.
To stretch the gameplay design thinking even further, an `AutoDevDynamicsManager`
now fuses the functionality briefing with mechanics novelty, innovation
concepts, experience choreography, modernization targets, and live network and
security telemetry. The manager scores cross-domain synergy, highlights shared
system tracks and gameplay threads, and distils the combined network and
holographic requirements into actionable backend directives. It also folds in
continuity windows, codebase progress, and self-evolution follow-ups so the
managerial intelligence matrix and exported plan surface a `dynamics_brief`
alongside existing mechanics, innovation, experience, and functionality data.
This keeps functionality creation grounded in the MMO's broader resilience,
security, and modernization posture while continuously upgrading holographic
transmission guardrails and network auto-dev playbooks.
To translate those systems signals into actionable player experiences, an
`AutoDevPlaystyleManager` now fuses functionality tracks, experience arcs,
mechanic archetypes, and the new dynamics telemetry with research, network, and
holographic diagnostics. The manager scores playstyle cohesion versus risk,
assembles archetypes with clear tuning actions, and mirrors the combined network
and holographic requirements needed to safely expose the experiences to players.
Its briefing is published alongside the other orchestration outputs so the
managerial intelligence matrix can track playstyle priorities, directives, and
archetype readiness while the holographic transmission stack receives explicit
phase and guardrail updates.
To carry those playstyle directions into concrete gameplay loops, an
`AutoDevGameplayManager` synthesises functionality priorities, dynamics synergy,
playstyle cohesion, mechanics threads, experience arcs, and the surrounding
network, security, and holographic telemetry. The manager assembles loop
blueprints that call out the systems dynamic at play, the required holographic
phase adjustments, the network upgrade backlog, and the mitigation actions that
keep modernization, optimisation, and governance directives aligned. Its
blueprint surfaces named loops, managerial actions, codebase alignment targets,
and research implications; all of these flow into both the orchestration payload
and the managerial intelligence matrix so planners can see how gameplay
experiments mesh with modernization work, network security automation, and
ongoing holographic lithographic upgrades.
To help the auto-dev stack reason about how those loops blend into broader
feature work, an `AutoDevInteractionManager` now fuses functionality briefs,
mechanics blueprints, gameplay loops, and the supporting network and holographic
telemetry. The manager scores interaction readiness against functionality gaps,
highlights cross-domain tracks and threads that need reinforcement, and mirrors
the network and holographic requirements that must stay in lockstep with the
security, mitigation, and modernization plans. It also folds in research
pressure, codebase alignment, and self-evolution readiness so the orchestration
outputs expose an `interaction_brief` alongside the existing mechanics,
innovation, experience, and gameplay telemetry. The managerial intelligence
matrix mirrors the interaction priority, tracks, gap index, and backend actions
so planners can quickly see how functionality creation, gameplay loops, and
network upgrades reinforce each other.
Building on that layer, the auto-dev pipeline now introduces an
`AutoDevDesignManager` to push functionality and mechanics creation into an
explicit design blueprint. The manager blends functionality tracks, mechanics
novelty, innovation concepts, dynamics synergy, gameplay loops, and the latest
interaction telemetry with network auto-dev readiness, transmission diagnostics,
and governance directives. It returns a deterministic design score, priority,
creation tracks, prototype threads, and consolidated network and holographic
requirements while mirroring research pressure and security gaps. Codebase
alignment is fed from the analyzer’s new design fragility metrics so the
blueprint highlights which modules and modernization steps underpin each track.
The design brief flows into the orchestration payload and managerial intelligence
matrix, giving planners an at-a-glance view of design priorities, directives,
and risk posture next to the functionality, dynamics, playstyle, and gameplay
telemetry.
To keep those design tracks stitched to the broader functionality and mechanics
strategy, an `AutoDevSystemsManager` now synthesises the design blueprint with
functionality briefs, dynamics, playstyle, gameplay loops, and interaction
signals. The manager folds in research pressure, modernization roadmaps, network
auto-dev readiness, and holographic calibration to score systems cohesion,
prioritise directives, and publish consolidated network and lithographic
requirements. Its brief exposes systems alignment indices, recommended upgrade
actions, architecture overviews, and codebase focus modules so downstream
automation can reason about how gameplay concepts map onto hardened backend and
security guardrails.
To deepen how the stack reasons about creating new mechanics and functionality,
an `AutoDevCreationManager` now fuses the functionality, design, systems,
innovation, and gameplay telemetry with codebase creation metrics, modernization
timelines, and holographic diagnostics. The creation blueprint surfaces weighted
creation scores, aggregated tracks and threads, concept portfolios, prototype
windows, and consolidated network and lithographic requirements. It mirrors the
codebase analyzer’s new creation gap index, focus modules, and recommendations
while publishing risk posture and governance alignment so planners can steer
feature evolution alongside modernization, optimization, and integrity pushes.
Both the orchestration payload and the managerial intelligence matrix expose the
creation brief, ensuring downstream automation sees how functionality concepts,
mechanics novelty, and network guardrails align before shipping new systems.
The blueprint now also quantifies a mechanics synergy index and a functionality
extension index so planners can see how well new functionality candidates pair
with emerging mechanics threads and modernization targets. Mechanics and
functionality expansion tracks are exported alongside the existing creation
threads so orchestration can schedule cross-team work on the same set of tracks
without losing the holographic or network context that keeps those loops secure.
To keep functionality creation honest about weak spots, the pipeline now ships a
`functionality_gap_report` that cross-references functionality tracks and
mechanics threads against the codebase scorecards and modernization targets. The
report calls out uncovered tracks, highlights high-risk modules, and forwards the
top modernization actions so remediation and modernization managers can close
the loop between design ambition and codebase hardening. A synergy gap metric
helps planners see how much uplift is still required before the next wave of
playstyle briefs can safely ship.
The new `AutoDevSynthesisManager` extends this loop further by blending the
creation, functionality, mechanics, design, and systems briefs (alongside
network, security, modernization, optimization, and holographic telemetry) into
a synthesis brief. The manager scores overall creation/mechanics cohesion,
publishes consolidated expansion tracks, directives, and concept threads, and
mirrors the merged network and lithographic requirements needed to ship those
expansions safely. Its alignment summary feeds both the functionality gap report
and the managerial intelligence matrix so planners can see the synthesis gap
index, supporting signals, and codebase coverage before committing to the next
wave of mechanics and functionality upgrades.
To deepen the way creation work aligns with mechanics and functionality, the
`AutoDevConvergenceManager` fuses the functionality, mechanics, creation,
dynamics, and synthesis layers with gameplay, interaction, network, security,
research, and modernization telemetry. The convergence brief scores overall
integration and cohesion, lists converged tracks, threads, and directives, and
merges the relevant network and holographic requirements so orchestration can
sequence upgrades without losing guardrail coverage. It also forwards
codebase-focused alignment signals—rooted in the analyzer's new convergence
metrics—so mitigation, modernization, and gameplay planners can see which
modules need reinforcement before new mechanics/functionality bundles ship.
To translate these convergence signals into execution packages, the
`AutoDevImplementationManager` blends functionality, mechanics, gameplay,
creation, synthesis, convergence, and managerial telemetry into a deterministic
implementation brief. The manager scores delivery readiness, highlights tracks
and threads that must land together, merges network and holographic
requirements, and distils backlog, directives, and delivery windows from the
mitigation, remediation, and modernization layers. Its output surfaces the raw
implementation gap, risk index, readiness window, and backlog so planners can
sequence upgrades with full awareness of codebase constraints, research
pressure, and guardrail coverage.
To keep the automation focused on shipping those implementation bundles, the
`AutoDevExecutionManager` fuses the implementation, convergence, creation, and
continuity layers with network, security, resilience, and modernization
telemetry. The execution brief reports a blended execution score, gap index,
and risk profile; merges cross-domain tracks, windows, and directives; and
summarises the network and holographic guardrails that must remain intact while
delivery proceeds. It also feeds the codebase analyzer's new execution signals
back into the plan so the functionality gap report and managerial intelligence
matrix surface execution stability, backlog focus modules, and guardrail-ready
actions alongside the existing modernization and implementation snapshots.
A revamped codebase analyzer now ships modernisation targets alongside the
existing risk scorecards. High-risk modules list concrete refactor and test
steps, while the auto-dev plan exposes those directives as
`codebase_modernization_targets` and the governance brief mirrors them within
its codebase directive list. The analyzer now also calculates a
`functionality_gap_index`, surfaces the modules lacking coverage, and estimates a
`mechanics_alignment_score` so the interaction and functionality managers can
anchor new mechanics in the reality of the codebase. Even when few hotspots
remain, the analyzer keeps a baseline directive so auto-dev automation can
continue scheduling background improvements without losing momentum. With the
new design manager, the analyzer additionally reports a deterministic
`design_fragility_index`, the focus modules most at risk, and targeted design
recommendations so modernization and mitigation workflows can prioritise the
foundation beneath each design track. It now also surfaces a
`systems_fragility_index`, focus modules, and actionable recommendations,
coupled with a `systems_alignment_index`, so the new systems manager and
functionality gap report can highlight where mechanics creation and backend
coverage diverge before new functionality ships.
A new reporting layer adds encounter blueprints that distil monster rosters,
spawn schedules and mob AI directives into a single view, flags how quests tie
back to headline bosses, and surfaces the raw research percentage captured by
the analysis pipeline. Fresh analytics now capture the monster-creation queue,
show the raw processing percentage alongside average samples, and summarise the
spawn tactics per lane so planners know which reinforcements anchor each wave.
Network diagnostics now surface holographic efficiency and phase-coherence
indices so security and relay teams can see how lithographic transmissions are
responding to applied mitigations in real time.
Additional summaries catalog monster hazards and threat tiers, outline spawn
tempos, highlight mob-AI development focus, and grade boss
outlooks alongside trade-skill matrices so planners can assess roster depth at
a glance. The latest general-intelligence pass also records group mechanics such
as lane pressure, burstiness and spawn tempo, maps out AI training gaps, and
scores boss pressure relative to supporting monsters. Quest dependencies now
list the objectives each trade skill supports so designers can trace how crafted
gear feeds headline encounters. The new creation, spawn and boss strategy
sections outline archetype counts, reinforcement styles, recommended raid sizes
and quest cadence so MMO planners can coordinate monsters, bosses and trade
skills in the same view. A processing overview keeps the raw utilisation
percentage front and centre with sample history, while an evolution alignment
summary shows where guidance directives overlap with upcoming objectives.

The guidance layer now quantifies its managerial intelligence with a weighted
breakdown of risk, network, research and quest contributions, publishes a
backend-alignment score, and exposes a guidance backbone so operators know
which levers the general-intelligence system is emphasising in real time. A new
auto-dev backend dashboard surfaces those alignment metrics alongside network
guardrail severity, mitigation priority, and remediation progress so leadership
can confirm that applied fixes are tracking toward the projected stability
targets. The codebase analyzer feeds this dashboard through module scorecards
that call out high-risk files, recommended refactors, and remediation progress,
letting the pipeline report exactly which weaknesses have been addressed and
which remain outstanding.

Networking automation now calculates lithographic transmission guardrails and
integrity scores, pairing holographic diagnostics with zero-trust directives so
the system can recommend when to reinforce anchors, throttle non-essential
channels, or mirror packets across redundant relays. The transmission manager
ingests those guardrails during calibration, returning a detailed holographic
snapshot that combines phase alignment actions, guardrail follow-ups, and
lithographic integrity metrics with the usual compression and security layer
guidance. Together these upgrades extend the auto-dev loop's managerial
intelligence, network security automation, and holographic lithographic control
so the MMO can continue evolving under a transparent, self-correcting plan.
Calibration also publishes a spectral waveform profile that scores holographic
stability, bandwidth density, and phase indices while recommending actions such
as lattice smoothing or layer-density increases when the guardrails spot drift.
This richer telemetry helps the continuity manager and network automation agree
on when to reinforce the lithographic lattice versus when to maintain existing
throughput balances.

A dedicated `AutoDevSecurityManager` now interprets network, mitigation,
remediation, research, and guidance telemetry into a unified security brief. It
reports the current threat level, projected security score, the hardening work
already underway inside the codebase, and a holographic lattice summary so
network and holographic operators align on which directives should run next.

`AutoDevPipeline` surfaces that brief alongside the orchestrated plan,
publishing `security_threat_level`, `network_security_actions`, and a
standalone `holographic_lattice` snapshot. The transmission calibration consumes
the lattice and emits a `lattice_overlay` that combines waveform guidance with
guardrail follow-ups, while the managerial intelligence matrix now embeds a
security projection so leadership can audit hardening progress without leaving
the auto-dev report.
Backend guidance entries blend guidance priorities, evolution objectives and
research pressure so planners can quickly redirect compute or adjust quests when
utilisation spikes. New processing-channel analytics call out how much raw
compute each of research, guidance, evolution and networking consumes so
operations teams understand where background studies and relay upkeep are
running hot. The intelligence brief
also publishes an orchestration pipeline that tracks readiness for monster
design, group spawning, mob AI, boss selection, quest generation and research
intelligence, alongside a management playbook that lists the next unblock step
and the recommended compute posture for the backend crew.
Monster-forge dashboards now expose roster status and elite ratios, while a
group-spawn mechanics view highlights lane patterns, burst windows and enemy
totals. The mob-AI innovation plan reports coordination cadence, and a boss
spawn matrix links trade-skill support counts with recommended raid sizes. Quest
tradecraft summaries map boss objectives to trade skills and spawn lanes so
crafting, encounters and reinforcements stay aligned. Research pressure gauges
pair the raw processing percentage spent on rival-game studies with its share of
the latest utilisation sample, and a managerial alignment snapshot flags when
backend priorities diverge from the live pipeline focus so auto-dev planners can
course correct before MMO evolution drifts.

Competitive-research analytics now surface which rival titles consume live
processing time and how that study load compares against encounter prep. The
research brief adds volatility, trend direction, pressure indices, and raw
competitive utilisation percentages so compute stewards can rebalance
background studies quickly. The general-intelligence brief grades spawn-lane
coordination, mob-AI innovation, boss spawn readiness and trade-skill alignment
so monster creation, group spawning and quest design evolve together. A
managerial overview pulls those signals into a single snapshot, tracking
coordination scores, raw processing pressure, competitive focus and upcoming
evolution objectives to anchor the MMO's self-directed growth to actionable
metrics while the weakness-analysis layer flags when governance posture needs
oversight.
Networking analytics now layer on a resilience matrix with uptime scores and
hardening guidance, a zero-trust blueprint that suggests concrete packet-level
controls, anomaly summaries that tally untrusted relays versus suspicious
events, and a network-security score that blends automation performance with
incident pressure. Holographic telemetry exposes a richer signal matrix with
stability indices, bandwidth profiles, condensed signatures, and enhancement
actions so peers can validate pointcloud integrity with minimal overhead while
directing lithographic upgrades.
A `TeamManager` assigns players and enemies to teams and the combat system
skips damage between allies, preparing the arena for future team-based modes
and cooperative MMO battles.
The arena's lighting cycles between day and night, laying groundwork for
persistent world time in later MMO modes.
Each level also randomizes weather through the `EnvironmentManager`; rainy maps
reduce friction so characters slide more, while snowy maps increase friction to
slow movement, preparing dynamic climates for the future MMO. Taking damage
briefly shakes the camera and flashes the screen red for added impact feedback.
The main menu also exposes a **Goals** screen that lists top development
objectives drawn from the project documentation.
Gathering professions feed a timing-based mini-game: hitting the sweet spot
grants rare materials and extra experience which the crafting system turns into
equipment. Reaction challenges now drop crafting materials as well, and maps
contain crafting stations where these materials can be combined into gear.
An AutoSkillManager creates new abilities based on a character's level and
attack stats.
A SkillGenerator, SubclassGenerator, TradeSkillGenerator and ClassGenerator
craft skills, subclasses, profession abilities and unique class templates,
while an AutoBalancer nudges class stats toward parity. An InteractionGenerator
and InteractionManager quickly create simple interactive objects for levels.
A new RecursiveGenerator chains these helpers together so entire class,
skill and profession sets can be produced in one call.

Trade skills now expose specialisations, recipe hints and balanced level bands,
covering professions such as Brewing, Enchanting, Fishing, Fletching,
Inn-Keeping, Seductress and a full suite of gathering tracks including
Foraging, Herbalism, Logging, Prospecting and Trapping. Each trade skill
records the recommended level range and a difficulty tier (novice, adept or
master) so regional planners can align gathering routes with world progression
while tracking the bonuses those gatherers feed into downstream crafting.
The ``TradeSkillCraftingManager`` turns those recipes into deterministic armor,
weapon, bow and wand blueprints and now aggregates gathering synergies so
herbalists, prospectors and woodcutters inject extra stats into related gear.
Gathering professions also surface ``material`` outputs that record yield and
purity for planning resource loops. Crafted gear is registered with the
``ItemManager`` so world generation can drop profession-driven loot while
documenting the recipe materials alongside the crafted items and the bonuses
applied by supporting gatherers.
The repository goals are detailed in [docs/GOALS.md](docs/GOALS.md).
Codebase maps live in [docs/CODEBASE_ANALYSIS.md](docs/CODEBASE_ANALYSIS.md).
Interaction graphs live in [docs/CODEBASE_GRAPHS.md](docs/CODEBASE_GRAPHS.md).
Story mode chapters are outlined in [docs/DEV_PLAN_STORY.md](docs/DEV_PLAN_STORY.md).
Networking details live in [docs/DEV_PLAN_NETWORK.md](docs/DEV_PLAN_NETWORK.md).
Contributor expectations are summarized in [CODE_REQUIREMENTS.md](CODE_REQUIREMENTS.md).


## Asset Placeholders
The repository references placeholder images and a sound effect so the game runs
without additional downloads. PNGs are generated at runtime into Images/ if
they are missing, and no binary assets are committed to the repo.
Directories
- `SavedGames/`
- `Images/`
- `sounds/`
The `SavedGames` folder stores settings in `settings.json`. Selecting "Wipe Saves" from the settings menu clears this directory.
If the folder is missing, it will be recreated automatically the next time settings are saved.
The file also tracks your best survival time and high score so far.
Each finished run additionally writes a `.gguf` snapshot under
`SavedGames/iterations` so later versions can review past states. A neural
network can analyze these snapshots to tick off completed goals.
To review or prune old snapshots, run:
```bash
python tools/cleanup_savedgames.py --keep 20 --dry-run
```
Use `--archive <dir>` or `--delete` to apply changes.
Press F12 during play to capture a screenshot; images are saved under
`SavedGames/screenshots`.

Images (PNGs)
```
./Images/Watson_Amelia_right.png
./Images/Watson_Amelia_left.png
./Images/Gawr_Gura_right.png
./Images/Gawr_Gura_left.png
./Images/Ninomae_Inanis_right.png
./Images/Ninomae_Inanis_left.png
./Images/Takanashi_Kiara_right.png
./Images/Takanashi_Kiara_left.png
./Images/Mori_Calliope_right.png
./Images/Mori_Calliope_left.png
./Images/Ceres_Fauna_right.png
./Images/Ceres_Fauna_left.png
./Images/Ouro_Kronii_right.png
./Images/Ouro_Kronii_left.png
./Images/IRyS_right.png
./Images/IRyS_left.png
./Images/Nanashi_Mumei_right.png
./Images/Nanashi_Mumei_left.png
./Images/Natsuiro_Matsuri_right.png
./Images/Natsuiro_Matsuri_left.png
./Images/Hakos_Baelz_right.png
./Images/Hakos_Baelz_left.png
./Images/Shirakami_Fubuki_right.png
./Images/Shirakami_Fubuki_left.png
./Images/Sakura_Miko_right.png
./Images/Sakura_Miko_left.png
./Images/Minato_Aqua_right.png
./Images/Minato_Aqua_left.png
./Images/Usada_Pekora_right.png
./Images/Usada_Pekora_left.png
./Images/Houshou_Marine_right.png
./Images/Houshou_Marine_left.png
./Images/Hoshimachi_Suisei_right.png
./Images/Hoshimachi_Suisei_left.png
./Images/Nakiri_Ayame_right.png
./Images/Nakiri_Ayame_left.png
./Images/Shirogane_Noel_right.png
./Images/Shirogane_Noel_left.png
./Images/Shiranui_Flare_right.png
./Images/Shiranui_Flare_left.png
./Images/Oozora_Subaru_right.png
./Images/Oozora_Subaru_left.png
./Images/Tokino_Sora_right.png
./Images/Tokino_Sora_left.png
./Images/character_right.png
./Images/character_left.png
./Images/enemy_right.png
./Images/enemy_left.png
./Images/boss_right.png
./Images/boss_left.png
./Images/map_default.png
./Images/chapter1.png
./Images/chapter2.png
./Images/chapter3.png
./Images/chapter4.png
./Images/chapter5.png
./Images/chapter6.png
./Images/chapter7.png
./Images/chapter8.png
./Images/chapter9.png
./Images/chapter10.png
./Images/chapter11.png
./Images/chapter12.png
./Images/chapter13.png
./Images/chapter14.png
./Images/chapter15.png
./Images/chapter16.png
./Images/chapter17.png
./Images/chapter18.png
./Images/chapter19.png
./Images/chapter20.png
```

Audio Tracks
(no audio files included)

Sound Effects (optional)
Place any of the following files in `sounds/` to enable impact audio cues.
Supported extensions are `.wav` or `.ogg` (the loader uses the first match).
```
sounds/hit_light.wav
sounds/hit_heavy.wav
sounds/hit_crit.wav
sounds/melee_swing.wav
sounds/special_cast.wav
```
If the files are missing the game generates short synth tones at runtime and
still records the last-played cue name for tests and UI telemetry.

## Running the Prototype

Requires Python 3.10 or newer.

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   (Python 3.13+ installs pygame-ce automatically via requirements.txt.)
2. Launch the game:
   ```bash
   python -m hololive_coliseum
   ```
   To force headless mode (for CI/tests), set PYGAME_HEADLESS=1 before
   launching.
   To run a short automated playtest, set HOLO_AUTOPLAY=1 and optionally
   HOLO_AUTOPLAY_DURATION (milliseconds). Add HOLO_AUTOPLAY_FLOW=1 to walk
   through menus, and HOLO_AUTOPLAY_MENU_DELAY to slow menu pacing. For example:
   ```bash
   set HOLO_AUTOPLAY=1
   set HOLO_AUTOPLAY_FLOW=1
   set HOLO_AUTOPLAY_DURATION=15000
   set HOLO_AUTOPLAY_LEVELS=3
   set HOLO_AUTOPLAY_VISIBLE=1
   python -m hololive_coliseum
   ```
   For a single-command visible autoplay demo, you can also run:
   ```bash
   python tools/run_autoplay_demo.py --mode flow
   python tools/run_autoplay_demo.py --mode agent
   python tools/run_autoplay_demo.py --mode flow --mmo
   python tools/run_autoplay_demo.py --mode agent --full
   ```
   The main menu includes **Match Options** for lives, allies, AI opponents,
   and mob waves before starting a run, plus an **Accounts** shortcut for
   account management.
   Autoplay menu flow now cycles through every menu option (including settings, 
   info screens, vote categories, and pause submenus) and returns to gameplay   
   or the main menu between selections. Settings submenus now return to their   
   parents so autoplay can traverse controls and system tooling in one pass.    
   Autoplay skips destructive system actions unless you set                     
   `HOLO_AUTOPLAY_SYSTEM_ACTIONS=1`. Autoplay also pauses on character, map,    
   and chapter menus to sweep previews before selecting; the pause duration    
   is controlled with `HOLO_AUTOPLAY_PREVIEW_DELAY` (milliseconds).
Autoplay uses an advanced agent that kites, sprints, and avoids fall gaps
on wider maps. Set `HOLO_AUTOPLAY_EXPLORER=1` to enable the feature-testing
explorer profile. Set `HOLO_AUTOPLAY_MONITOR=1` to emit periodic telemetry
(interval via `HOLO_AUTOPLAY_MONITOR_INTERVAL` in milliseconds) and
`HOLO_AUTOPLAY_LOG=1` to persist logs in `SavedGames/autoplay.log`.
Autoplay can audit per-character action usage with
`HOLO_AUTOPLAY_SKILL_AUDIT=1` and the interval in milliseconds via
`HOLO_AUTOPLAY_SKILL_AUDIT_INTERVAL`. Set `HOLO_AUTOPLAY_SKILL_AUDIT_FORCE=1`
to bias the autoplay agent toward missing actions and
`HOLO_AUTOPLAY_SKILL_AUDIT_REPORT=1` to append results to
`SavedGames/skill_audit.json`.
   During matches, press **F10** to toggle the autoplay agent on/off.
   To generate standardized placeholder sprites locally, run:
   ```bash
   python tools/generate_standard_sprites.py
   ```
   The repository does not commit binary sprite assets, so this script is the
   supported way to materialize consistent placeholders.
   To generate standardized special-attack VFX sprites, run:
   ```bash
   python tools/generate_special_vfx_sprites.py
   ```
   This writes multi-frame VFX sequences (`name_0.png` ... `name_5.png`) plus
   a fallback `name.png` for each special.


The current prototype includes a basic player with gravity plus health, mana and
stamina bars. A cyan splash screen leads to a gradient-styled menu system that
covers Story, Arena and Custom modes. Combat offers
melee with **X**, projectiles with **Z**, blocking on **Shift**, a parry on
**C**, and dodges using **Left Ctrl**, granting brief invulnerability but
ignoring any power-ups along the path. Attacks, blocking and dodges spend
stamina which regenerates over time. Health slowly regenerates if you avoid
 damage for a short while. Low-gravity zones allow higher jumps while high gravity limits
movement. Spike traps, ice patches, lava pits and later acid pools all cause
damage, and enemies try to leap over them. Arena stages now extend beyond the
screen width with a horizontal camera pan. Falling through floor gaps costs a
life and revives the player with a short invulnerability window.
If the player strays too far, enemies patrol near their spawn points until reengaging.

Movement uses acceleration and friction for smoother control. Players can also
double jump. Menus include character, map and chapter grids with **Back** buttons.
Offline multiplayer shows a **Press J to join** prompt and an **Add AI Player**
option. A **Difficulty** choice cycles from Easy to Hard so AI adjusts its
aggression. When badly hurt, enemies try to retreat before re-engaging. Hard
opponents lead their shots to track moving targets and dodge away if the player
rushes them. When dodging fails they raise their shields to block incoming
projectiles.

Arena lighting now follows the shared day/night cycle from the MMO world. The
environment manager computes a weather-tinted ambient overlay so nights appear
cooler and darker while daytime battles stay bright, reinforcing that Coliseum
matches occur inside the same evolving universe. A weather forecast manager now
generates deterministic climate schedules so arenas and MMO regions can plan
ahead, with the game previewing upcoming storms before they arrive.

Projectiles and melee attacks harm enemies. Damage comes from each fighter's
attack stat and is reduced by the target's defense, keeping battles balanced.
Attacks can also critically hit, multiplying damage by a character's
``crit_multiplier`` (default ``2``) whenever their ``crit_chance`` stat
triggers. Critical strikes show yellow damage numbers so players can see when
they land a powerful hit. Floating damage numbers pop
above characters whenever hits land.
Some fighters tweak these values; Gura starts with stronger attacks but lower
defense and health, Watson moves faster at the cost of durability, Ina wields a
deeper mana pool for sustained specials, Kiara balances offense and defense,
Calliope hits hard but has lower health, Fauna sacrifices attack for extra
defense and vitality, Kronii's extended parry leans into defense, IRyS bolsters
her crystal shield with higher defense but modest attack, Mumei's flock packs
extra power at the expense of health, Fubuki trades some power for agility with
9 attack, 5 defense and 95 health, Matsuri leans into offense at 11 attack, 5
defense and 100 health, Miko channels high attack with fragile defenses at 12
attack, 3 defense and 85 health, Aqua favors sturdy defense over raw damage at 9
attack, 7 defense and 100 health, Pekora balances solid attack with 11 attack,
5 defense and 95 health, Marine swings hard with 13 attack, 5 defense and 90
health, Suisei mixes precision offense
with sturdy defenses at 12 attack, 6 defense and 95 health, Ayame's swift dash
leans on 11 attack, 4 defense and 90 health, Noel's ground slam now launches a
traveling shockwave with 9 attack, 8 defense and 110 health, Flare's searing
fireball pushes offense at 12 attack, 4 defense and 95 health, Subaru's stunning
blast dazes foes with 10 attack, 6 defense and 105 health, while Sora's melody
weaves through the air with 9 attack, 5 defense and 110 health.
Press **V** for a special move like Gura's trident, Aqua's slowing splash,
Pekora's bouncing carrot, Noel's rolling shockwave, Flare's burning fireball,
Subaru's stunning blast or Sora's weaving melody.
Press **H** to drink a health potion or **J** to consume a mana potion if one is
in your inventory.
Specials aim with the mouse and often explode on impact. A status effect
manager handles freezes or slows. A `ClassManager` stores MMO class templates
while an `ItemManager` catalogs gear such as swords, bows, wands, axes and spears
alongside offhand items like shields, tomes and orbs.
An equipment screen lays out head, chest, leg and weapon slots so players can see
items on a Diablo-style paper doll. Items and quests are tracked, the HUD displays
lives, a timer and score, and each defeated enemy awards a coin via the
`CurrencyManager`. Coin totals persist between sessions to support long-term
progression. Match telemetry now feeds a richer HUD. A compact resource panel in the top-right
keeps coins, inventory capacity, level, XP and core stats visible at a glance
while a status-effect tracker highlights remaining buff or debuff durations. A
banner near the timer summarises difficulty, active match modifiers, auto-dev
support focus and networking state so players always understand the arena
context without diving into menus. A stacked auto-dev panel beneath the resource
summary surfaces trending hazards, recommended levels, challenges and focus
tracks from the MMO's self-evolving planners, and a world ticker along the
bottom broadcasts the latest generated region, quest hook and network upgrade
pressure so arena runs stay aligned with the broader MMO simulation in real     
time. HUD panels now use layered gradients and glow accents for a richer        
presentation. A cooldown tracker and compact arena minimap sit in the          
lower-left. Health, mana, stamina, speed, shield, attack, defense, experience 
        extra-life power-ups spawn periodically; green items restore health, blue
        refill mana, cyan refill stamina, yellow items briefly increase movement
        speed, purple ones grant temporary invincibility, red items boost attack,
        violet items raise defense, white items award experience and orange items
        add a life.
Poisoned attacks deal damage over time.
Rapid enemy defeats build a score combo shown on the HUD that awards extra points.
Hot streaks now trigger a Holo Hype boost that buffs attack and speed briefly.
Combo streaks also fire idol cheer callouts and a spotlight aura.
The HUD now includes a crowd meter that swells into Holo Hype during streaks.
Arena lighting now adds stage beams and idol sparkles during hype moments.
Stage ribbons and colorful cheer callouts add more idol flavor to runs.
Power-up pickups now pop themed idol cheer text for extra feedback.
Holo Hype now showers confetti and glowing fan sticks around the arena.
Combo milestones now flash a quick idol highlight overlay.
Arena starts now include a short Hololive Coliseum intro banner.
Boss spawns now trigger a “Boss Encore!” cheer and a brief highlight flash.
Holo Hype grants a small bonus score per defeat.
Early kills now trigger a fan sign wave celebration.
The crowd now bobs with light sticks during early momentum surges.
Boss spotlights briefly focus the biggest threat during encore callouts.
Special attacks now trigger a “Special Stage!” cheer and a quick highlight flash.
When health falls below a quarter, the screen pulses red to warn of imminent defeat.
Enemies display small health bars above their heads so players can gauge remaining foes during fights.
The difficulty selector now includes Elite and Adaptive AI tiers.

**InputManager** centralizes keyboard and controller checks so new bindings take
effect immediately. The **Settings** menu edits key bindings, chooses the input
method (auto, keyboard or controller), cycles window size and display mode
(windowed, borderless, fullscreen),
adjusts HUD size (now including smaller presets), volume, and the FPS counter.
Extra window size presets add more aspect-ratio options for different displays.
It
can wipe saves or start and stop blockchain node hosting through **Node
Settings**. An **Accessibility** submenu toggles colorblind mode, and the       
**Accounts** submenu registers, deletes or renews the current account's key     
pair. Press **Esc** to pause or **Enter** to chat. Menus display a cyan-to-white
gradient with a teal
border plus optional high-contrast styling, font scaling, and input prompts for
clarity.
border plus subtle animated glows for an arcade feel, and include **How to
Play**, **Credits**, and **Achievements** screens. Menu titles also shimmer     
with a light sweep and a soft vignette adds depth. Multiplayer opens a lobby    
showing all joined players before map selection.
The main menu now includes direct **Character Select** and **Map Select** shortcuts for quick setup.
Character and map selectors page through longer lists with **Prev Page** and **Next Page** controls.
Selectors now include filter cycling and preview panels with stats and map data,
plus a Random Map option for quick stage picks.
Local multiplayer tags character/map tiles with P1/P2 badges and resolves the
stage randomly among the players' selected maps.
Selection screens include guidance panels and highlight the active picker in
local multiplayer.
Menus default to a 1600x900 window for more breathing room.
The main menu uses a split-panel layout with a status sidebar for arena/MMO
information.
Menus now feature a top header ribbon to frame each selection screen.
Menu screens add a subtle patterned backdrop and framed option panels for
clearer hierarchy.
Selection highlights now include animated chevrons and header badges for
sharper menu focus.
Menu headers display the current state label, and option panels use a soft
sheen sweep to add motion.
Menu backgrounds now include a subtle emblem ring to deepen the Coliseum vibe.
Menu panels and summary cards now cast soft drop shadows for depth.
Menu emblems now feature orbiting triangle glyphs for extra iconography.

Losing all lives shows a **Game Over** screen summarizing time and score, then  
presents **Play Again** or **Main Menu** buttons. Beating all enemies or the timer
shows a **Victory** screen with the same summary plus Auto-Dev/MMO links and an
MMO Launchpad for post-arena setup.
Game Over and Victory now use summary cards with a clear Next Actions panel.

The **Records** menu lists your best time and high score. When online, nodes
broadcast these numbers so everyone sees the latest results. A weekly **Vote**
menu lets each account cast a blockchain-backed ballot to steer future MMO
development. Players can vote on new characters or on which biome the next
region should use.
### Story Mode
The single-player campaign follows Gura's growth from rookie idol to
battle-tested hero.
Selecting an icon loads its corresponding map using the placeholder images listed above.
Additional characters, maps, and features will be introduced over time.
At least 20 roster characters are available in the character selector.
Clearing Chapter 20 unlocks the MMO hub on the main menu, which previews        
generated regions, quests, and biomes derived from arena telemetry.
Three arena victories unlock an MMO trial via the post-match Launchpad.
In the MMO hub, use WASD or the arrow keys to move. Press E to sync the nearest
region, R to discover new frontier regions, and P to refresh the auto-dev plan.
Use Left/Right to select a region, F to focus the camera on it, G to cycle biome
filters, B to favorite, W to set a waypoint, and C to clear it. Use +/- to zoom,
Tab to toggle the overview panel, M for minimap, and X to toggle the event log.
Press I for details, H for help, V for favorites, L for quest log, Y for growth
report, U for party status, N for network status, and O for notifications. The
MMO hub also exposes K for the market board, Q for faction standings, J for the
operations board, and T for hub settings. Press F1-F9 to switch overlay tabs,
F10 for guilds, F11 for events, F12 for contracts, and Esc to return to the main
menu. Use S to cycle sorting, Z to open intel, 0-9 to toggle map layers, and    
PageUp/PageDown plus Enter to manage lists. Use Shift+D for infrastructure and
Shift+P/Shift+T for patrols and the timeline. Shift+L opens logistics, Shift+S
opens the resource survey, Shift+F opens diplomacy, and Shift+R opens research.
Shift+C opens crafting, Shift+M opens market orders, Shift+G opens strategy, and
Shift+Y opens the campaign board. Shift+E opens expeditions, Shift+O opens the
roster, Shift+A opens alerts, Shift+X opens the command deck,
Shift+B opens the bounty board, Shift+N opens the influence map,
Shift+U opens the fleet control, Shift+H opens the project board,
and Shift+K opens the academy board. The help overlay is now paged with
PageUp/PageDown, and first-time MMO visits show a short guided tour.
The hub persists player
positions, region
metadata, verified state snapshots, and auto-dev plans to `SavedGames/mmo_state.db`
for faster warm starts.
When a network session is active, the MMO hub also broadcasts compact state
updates so nearby clients can see each other on the world map.
Use `HOLO_MMO_AI` to spawn roaming MMO agents in the hub and
`HOLO_AUTOPLAY_AI_PLAYERS` to add AI fighters during autoplay runs.
Autoplay supports MMO auto-generation with `HOLO_AUTOPLAY_GENERATION_INTERVAL`
(ms between region seeds), `HOLO_AUTOPLAY_LEVEL_EXTENSION` (seconds added to the
current level per generation), and `HOLO_AUTOPLAY_LEVEL_LIMIT` (base level timer
for autoplay runs).
AI agents scale up over multiple playthroughs; each completed run increments a
stored progression level that increases MMO agent speed and exploration odds.
Enemy AI now tracks combat experiences and adjusts action bias over time,
allowing smarter reaction timing and tactical choices in longer playthroughs.
AI experience snapshots are saved to `SavedGames/ai_experiences.json` to support
deeper analysis; set `HOLO_AI_EXPERIENCE_INTERVAL` to control logging cadence.  
Autoplay now rotates through every menu screen, including the MMO overlay tabs,
and can optionally force the MMO entry into the main menu with
`HOLO_AUTOPLAY_FORCE_MMO=1` to explore locked hubs. The autoplay agent adapts its
aggression and defensive bias over time, persisting tuning in
`SavedGames/settings.json`; use `HOLO_AUTOPLAY_LEARN_INTERVAL` to control how
often feedback updates apply. Set `HOLO_AUTOPLAY_TRACE=1` to show on-screen and
console input traces; use `HOLO_AUTOPLAY_TRACE_INTERVAL` to control logging
cadence and `HOLO_AUTOPLAY_TRACE_LIMIT` to cap overlay lines. Use
`HOLO_AUTOPLAY_EXTENDED=1` to run longer visible passes and `HOLO_AUTOPLAY_EXTENDED_DURATION`
to tune the default duration. Set `HOLO_AUTOPLAY_FULL=1` to play through every
story chapter without a time limit.
Set `HOLO_AUTOPLAY_ALLIES=1` to spawn AI allies during autoplay; tune ally lives
with `HOLO_AUTOPLAY_ALLY_LIVES`. Use `HOLO_AUTOPLAY_LIVES` to grant extra player
lives for longer demos. Autoplay can also enable neutral mob waves with
`HOLO_AUTOPLAY_MOBS=1` and configure them via `HOLO_MOB_SPAWN_INTERVAL`,
`HOLO_MOB_WAVE`, and `HOLO_MOB_MAX`.
Extended autoplay defaults to a 120s level limit unless HOLO_AUTOPLAY_LEVEL_LIMIT is set.
The MMO hub unlocks only after clearing the final story chapter. In the MMO hub,
press Ctrl+A to open the Account Center overlay, then use R to register, K to
renew keys, U to upgrade tiers, Delete to remove the active account, and
PageUp/PageDown to cycle accounts. Ctrl+L opens Account Audit; use F to cycle
time filters and U to toggle upgrades-only.
Use `HOLO_AUTOPLAY_MENU_QUICK=1` with `HOLO_AUTOPLAY_VOTE_LIMIT` to cap how many
vote options get sampled per category before moving on to gameplay.
Use `HOLO_AUTOPLAY_MMO_OVERLAY_LIMIT` to cap MMO overlay cycling when quick
menu mode is enabled.
Use `HOLO_AUTOPLAY_MENU_BUDGET` (ms) to force a jump into gameplay after a
menu traversal timeout.
Use `HOLO_AUTOPLAY_MMO_FAST=1` to skip heavy MMO world generation during
autoplay runs.
Set `HOLO_AUTOPLAY_MINING=1` to enable background mining during autoplay runs so
the MMO world continues growing while AI playtests run.
Use `HOLO_AUTOPLAY_MINING_INTENSITY` to tune the mining CPU share (default 0.2).
 The opening twenty chapters stretch across two screen widths so the camera
 scrolls as you advance. Chapters 17 and 18 introduce a central pit, while 19
 and 20 break the ground into multiple segments yet still span both screens.
Each chapter spawns AI minions and later chapters add more of them. Every third
chapter pits the player against a boss drawn from the roster of playable
characters, adding an extra minion for a tougher fight. Bosses use enhanced AI
that periodically unleashes their special attacks. Chapters also include hazard
layouts and gravity zones
that grow in difficulty: the first few stages use simple spike traps with one
gravity modifier, mid chapters add icy patches and a second zone, chapters from
eight onward blow fighters sideways with wind zones, later levels feature lava
    pits with up to three gravity modifiers, chapters after eleven add regen
    zones that heal those who stand still, chapters after thirteen scatter
    quicksand pits that drag fighters downward, chapters after fifteen freeze
    fighters with frost zones, chapters after sixteen ignite fighters with fire
    zones that inflict burn damage, the final chapters add acid pools and
    lightning zones for even greater danger, poison zones inflict damage over
    time, silence zones block special attacks, bounce pads launch fighters
    skyward, teleport pads instantly relocate combatants, and green regen zones
    slowly heal those who linger within.
Each chapter also defines a set of platforms that grow more numerous in later
levels, and some of them slide back and forth to create moving footing. In later
chapters the ground itself splits into segments, forming pits that require
precise jumps. Platforms are loaded during level setup so characters and
enemies can land on them just like the ground. A few late-game platforms
crumble shortly after being stepped on, forcing players to keep moving.

### Networking Prototype
The package now contains a `NetworkManager` module that uses UDP sockets for
lightweight communication. Hosts answer broadcast discovery packets so clients
can automatically locate games on the local network. A separate
`node_registry` module stores known server addresses in `SavedGames/nodes.json`
alongside a small set of built-in nodes. When a host starts it registers its
address in this file and can broadcast an `announce` packet to share its
location with other nodes. Clients maintain their own registry and add entries
whenever they receive an `announce` message. Router nodes periodically share
their full node lists with `nodes_update` packets, and clients may issue
`get_nodes` requests to fetch the latest registry. When connecting online the
game pings all known nodes and chooses the one with the lowest latency. Nodes also
 act as lightweight routers: hosts register their match with nearby nodes and
 clients query those routers to receive a list of available games. Router nodes
 exchange `games_update` packets so each peer keeps the same set of available
matches and additionally share `clients_update` packets so each node knows
which users are currently online. When a client registers with a router, the
router replies with the current client list and notifies existing peers when
players join or depart. Clients may send a `client_leave` message when
disconnecting so routers drop them from these lists. State updates include a
sequence number and only transmit fields that changed using the lightweight
`StateSync` delta system. Small movements below configurable thresholds are
ignored so packets
remain tiny and latency stays low. Packets now carry the sender's client ID, and
nodes verify that this ID matches the source address to deter spoofing. When a
shared secret is configured, packets also include an HMAC signature so nodes can
discard tampered data. Encryption and signing keys can rotate during long
sessions to limit exposure. The menus include an online versus offline
multiplayer option to choose whether to connect to discovered nodes or play
locally.
A `SharedStateManager` builds on `StateSync` to maintain a synchronized
dictionary of gameplay values that modules can update and broadcast. A
`StateVerificationManager` supplies CRC32 and SHA256 digests for each state
packet so peers can confirm they share the same values without storing
additional history.
After a handshake, peers attach a session token to every packet. Tokens expire
after an hour and can be revoked with a logout request, so stolen credentials
quickly become useless. Messages missing a valid token are ignored, stopping
strangers from injecting data. Hosts also maintain a ban list so packets from
barred user IDs are dropped before processing.
Packets are compressed using a holographic lithography method. Each message is
converted to a pointcloud and split into two base64 strings for transmission,
then reconstructed on receipt to keep bandwidth low. Repeated byte sequences are
run-length encoded before compression for extra savings. Compression streams
data in small buffers and can select the smallest result between zlib, bz2 and
lzma so decompression stays lightweight. The encoded pointcloud contains four
color-coded anchor points: cyan at `(0,0,1)` marks the start, white at
`(0,0,0)` the bottom front, black at `(1,1,1)` the far back-right and red at
`(1,1,0)` the bottom-right. These anchors let the receiver determine the
pointcloud bounds before decoding. Each anchor includes a virtual size,
luminosity value and black/white level so the cloud can be reconstructed with
multiple layers of detail. The encoder now records lightweight layer metadata
(`L1`-`L3`) with density, size, and energy hints plus spectral and phase
signatures so auto-dev networking can score anchor quality and tune holographic
throughput on the fly. A `channel_vectors` payload exposes entropy, diversity,
and coherence while the accompanying `channel_map` records both compression
strategy and measured coherence so relays can judge stability before accepting
state. A third base64 fragment carries the sender's public key and a
signature so recipients can verify the packet's origin. The encoded pointcloud
also includes a BLAKE2s digest so corrupted data is ignored. Each packet stores
a timestamp and is dropped if it arrives too late, providing extra protection
against replay attempts. When a key is supplied, `DataProtectionManager`
encrypts packets with AES-GCM using a random nonce before transmission to add
confidentiality alongside the digest. It also strips sensitive fields like
passwords before encoding so intercepted packets reveal no private details.
Critical packets can be marked **reliable** so the sender will resend them
until an acknowledgement is received, ensuring important updates are not lost
even over an unreliable connection. Reliable packets now include an
``importance`` value that increases the resend rate and retry count for
critical messages.
Chat messages are exchanged using small ``chat`` packets so players can text
each other during online matches.
Nodes periodically prune unreachable peers from the registry so discovery
remains accurate even as servers appear and disappear.
To help defend against flooding attacks the manager tracks messages per peer
and drops traffic that exceeds a configurable rate.
Starting a node from the **Node Settings** menu turns the game into a host that
shares blockchain updates and discovers peers to form an IP mesh. The same menu
offers a **Stop Node** option to revert to client-only mode.
Advanced users can also enable a **Latency Helper** option in Node Settings.
When active, the client announces itself as a relay so other players can route
traffic through the lowest‑latency path. Router nodes share their available
relays and clients may send packets via these helpers if it shortens the route.
The node menu also exposes a **Background Mining** toggle that performs
proof-of-work in a background thread using spare CPU time to generate data for
the planned MMORPG world. Each mined hash feeds the world generator to spawn
new regions so the MMO can expand automatically.
During matches, clients now *bridge* their state packets: each update travels to
the host node for verification and directly to other peers for rapid
synchronization. This dual path, inspired by Tor's Snowflake bridges, keeps
gameplay responsive while making man-in-the-middle attacks harder because both
copies must agree before a client accepts the data.
Clients can synchronize their clocks with a router by sending a ``time_request``
packet and reading the ``time_response``. The resulting offset is stored via
``SyncManager`` so future state packets include accurate timestamps.
Whenever a new best time or high score is achieved, the node broadcasts a
``records_update`` packet so peers can merge the latest numbers into their own
settings.
Every packet carries a random nonce so replayed messages are rejected before
they influence the game.

### Game History Blockchain
Every completed online match is recorded in a lightweight blockchain stored in
`SavedGames/chain.json`. Each block contains the game ID, participating
usernames, winner and an optional wager amount. Winners "mine" a block when a
match ends, searching for a nonce so the hash begins with two zeros before the
result is shared with other nodes. Balances are tracked in
`balances.json` so players can bet currency on matches. Utility functions allow
searching the chain by game ID or user ID for features like leaderboards and
friends lists. A helper `get_balance(user_id)` returns the currency total for
any account. Hashes mined in the background and each recorded match are written
as `seed` blocks so clients can sync world-generation seeds for the future MMO.
Seed blocks record the characters used so the weekly vote menu can present the
randomized candidate list. Ballots are now submitted directly through the Vote
menu rather than automatically during character selection, and accounts can cast
one vote per category each week so parallel polls run side by side. Those vote
totals also drive the balancing adjustments applied at match start.
The blockchain can
be verified for tampering and merged with
longer chains received from peers so all nodes share the same history. Game
records now store signatures from all participating players. Entries are only
accepted if every player has a registered account so invalid user IDs cannot be
added. Keys can be regenerated from the **Accounts** menu and are used when
signing packets and blockchain blocks. Nodes broadcast new blocks immediately so
peers can extend their local chains. New clients may request the current chain
from a router node using ``chain_request`` so everyone starts with the same
history.

Messages between players can also be stored in the chain. Each account
registers a public key and an access level (user, mod or admin). Accounts can
be removed later if needed. When a
message is sent, it is encrypted with a random key that is wrapped twice:
once with the recipient's public key and once with the admin key. This keeps
chats private while still allowing moderators to decrypt abusive messages using
the mixed key.

Players may opt into background mining from the node menu. When enabled, a
``MiningManager`` performs proof-of-work on dummy blocks using roughly twenty
percent of available CPU time, laying groundwork for a future MMORPG world that
grows as players contribute processing power. A note in the node settings
explains the extra resource usage. Mined hashes are stored by a
``WorldSeedManager`` so future iterations can use them as deterministic seeds
when generating the online world.
These seeds feed a ``WorldGenerationManager`` which combines them with
procedurally generated content to grow the MMO world automatically. Regions are
positioned on a golden-angle spiral, choosing a radius one greater than any
existing region. Each block records its radius, angle and position so the live
map expands in ever-larger circles. The manager can
sync seeds and regions from the blockchain before generating new ones and
rebuild missing regions from seed blocks so fresh clients recreate the same
maps.
Generated regions are written back to the chain via a ``WorldRegionManager`` so
peers can reconstruct the same areas.
An ``MMOBuilder`` helper assembles these world and voting managers automatically so future modes can
initialize the MMO stack with minimal code.
Region blocks include a ``region_hash`` field which lets clients verify the
data and ignore tampered regions during sync.
Regions also place a monument honoring the current weekly vote winner so the
community fills the MMO world with player-chosen landmarks. Biome votes decide
each region's environment, and every area rolls weapon and armor loot so the
blockchain tracks its rewards.
Generating a region also grants experience to the account that triggered it.
The LevelingManager records each player's experience and level, letting the
MMO scale difficulty and rewards as explorers advance.

Arena matches feed an ``AutoDevFeedbackManager`` which records scores, match
lengths, the characters used and which hazards were most frequently triggered.
When the world generator builds the next region it consults this feedback to
raise recommended levels based on recent performance and adds an ``auto_dev``
summary describing the trending hazard and favorite combatants. The data keeps
the MMO's outward expansion aligned with how players are actually performing in
the Coliseum.

To keep the arena itself trending toward a more playful tone, a refreshed
``ArenaManager`` now tracks a running fun level backed by background AI
combatants. These ``ArenaAIPlayer`` agents evaluate the pace, variety, fairness
and support on offer in recent matches. Their aggregated ratings update the fun
score and generate feedback that the ``AutoBalancer`` can consume when nudging
class statistics, so the Coliseum quietly simulates player sentiment even when
human competitors are offline.

The same manager now maintains a slowly adapting baseline fun level that
captures how entertaining the Coliseum feels over longer stretches. Its
``ArenaFunSnapshot`` helper exposes the current fun level, baseline, AI
projection and momentum so downstream planners can tell whether the arena is
improving or stagnating at a glance. ``AutoBalancer`` reads that baseline and
applies global stat adjustments before per-class tweaks, ensuring the entire
roster trends toward the sustained fun level players—and their AI stand-ins—are
aiming for.

Each ``ArenaAIPlayer`` now supports a ``playtest_arena`` routine which simulates
several background matches to surface projected fun ratings, volatility
penalties and the archetypes that shaped the feedback. ``ArenaManager`` consumes
those deeper playtests through ``run_ai_playtests`` to generate an
``ArenaFunReport`` that extends the snapshot with volatility and AI consensus
tracking. The report feeds the ``AutoBalancer`` so momentum swings and unstable
fun streaks translate directly into class stat nudges even when human players
are offline.

To look further ahead the arena loop now publishes an ``ArenaFunForecast``
derived from the snapshot, fun report, and recent archetype preferences.
``ArenaManager.generate_fun_forecast`` blends baseline, momentum, volatility,
and AI consensus into an expected fun value, recommended focus, and archetype
summary that downstream tools can digest. Designers can also call
``get_ai_archetype_focus`` to retrieve the leading playstyle requests captured
during background playtests.

The ``AutoBalancer`` consumes that forecast alongside moment-to-moment reports
so balancing nudges respect the recommended focus. Stabilisation pushes now add
extra defense and health, experimental windows reward bolder attack values, and
alignment directives amplify AI feedback when consensus is low. The risk band
also provides a lightweight guardrail, padding stats whenever the arena tips too
far away from the long-term fun baseline.

Background playtests now distil all of that telemetry into an
``ArenaFunTuningPlan``. The plan captures the tuned target fun level, baseline
shift, volatility hints, and a bundle of ``ArenaFunDirective`` entries for each
class that the AI agents highlighted. Each directive records an action (boost,
trim or stabilise), a weighting, and stat biases so downstream tooling can react
deterministically. ``AutoBalancer`` can consume the plan directly; it honours the
global shift before applying every directive, ensuring boosted classes gain
attack bias during experimental windows while fragile archetypes receive the
defensive padding the plan prescribes.

The AI roster now scrimmages on its own via ``ArenaManager.simulate_ai_matches``.
Those sessions surface an ``ArenaFunSeasonSummary`` detailing the season fun,
baseline, momentum, participation rate, highlighted archetypes, and the win
leaderboard for the background pilots. Feeding that summary into
``AutoBalancer.balance`` with the ``fun_season`` argument tilts class adjustments
toward the archetypes and pacing that the AI cohort found most entertaining.

An accompanying ``AutoDevTuningManager`` interprets those hazard trends to tune
arena support. When lava, fire or other threats spike it reduces the spawn
timers for protective power-ups so practice matches surface the tools players
need most. The manager also adds a ``support_plan`` entry to each region's
``auto_dev`` data, flagging which boosts designers should highlight as the MMO
evolves.

To keep designers ahead of the curve an ``AutoDevProjectionManager`` now
studies the latest telemetry window and forecasts the hazards most likely to
pressure upcoming runs. The manager records a ``projection`` summary alongside
each generated region and shares the same snapshot with the arena HUD so
matches can showcase the countermeasures the MMO will soon require. Combined
with the support plan, the projection provides a rolling roadmap of which
power-ups, hazards and modifiers deserve immediate attention.

An ``AutoDevRoadmapManager`` now aggregates those insights into a single
checklist for each region. It merges the telemetry summary, support plan,
projection focus and scenario briefs into an ``auto_dev.roadmap`` entry so
designers can review priority actions, projected danger scores and recommended
counter-power-ups before staging the MMO's next beat.

An ``AutoDevFocusManager`` builds on that roadmap by weighing every available
signal and highlighting the hazards that deserve immediate attention. It
combines roadmap focus, telemetry challenges, projection danger scores,
scenario briefs and tuning plans into a concise ``auto_dev.focus`` report so
designers, writers and encounter planners can rally around the same sprint
priorities.

Arena matches now consume this world data through an
``EventModifierManager``. The newest generated region provides biome-themed
match modifiers: desert areas halve stamina regeneration but grant extra
experience, forest regions reward additional experience outright, and tundra
zones increase hazard damage to reflect their harsh climate. Monument features
add a small inspiration bonus while high recommended levels further toughen
hazards. When a stage loads the modifiers are applied automatically so the
Coliseum and MMO share the same seasonal conditions.

Player locations in this online world are tracked by a
``WorldPlayerManager``. It records global coordinates for each account and
blocks movement at the edge of the known map so explorers stay within
generated regions. For third-person controls it also exposes
``move_player_relative`` which turns forward and strafe inputs into world
offsets based on a camera yaw.

## Project Structure

This repository contains several directories and Python modules that make up the
prototype. The key paths are listed below with a short description of how they
interact:

Directories
| Path | Purpose |
| ---- | ------- |
| `hololive_coliseum/` | Core game modules including the main loop, player classes and helpers. |
| `docs/` | Development notes, goals and design plans. |
| `tests/` | Pytest suite covering gameplay and systems. |
| `Images/` | Placeholder sprites loaded by the game menus. |
| `sounds/` | Placeholder location for sound effects (empty in repo). |
| `SavedGames/` | Created at runtime to store `settings.json`. |

Important files
| Path | Called From | Calls |
| ---- | ---------- | ----- |
| `main.py` | Entry point script executed directly. | `hololive_coliseum.game.main` |
| `hololive_coliseum/__init__.py` | Imported when using `hololive_coliseum` as a package. | Re-exports main classes from submodules. |
| `hololive_coliseum/game.py` | Invoked by `main.py` or `python -m hololive_coliseum`. | Coordinates gameplay, settings and networking. |
| `hololive_coliseum/menus.py` | Imported by `game.py`. | Renders splash, option, inventory and equipment menus. |
| `hololive_coliseum/player.py` | Used by `game.py` to create players and enemies. | Imports `physics`, `projectile`, `melee_attack`. |
| `hololive_coliseum/projectile.py` | Instantiated from `player.py` or `game.py`. | None (pure sprite logic). |
| `hololive_coliseum/melee_attack.py` | Spawned from `player.py`. | None. |
| `hololive_coliseum/hazards.py` | Loaded by `game.py` to place spike traps, ice zones, lava pits, acid pools, fire zones, frost zones, quicksand pits, lightning zones, poison zones, silence zones, bounce pads, teleport pads, wind zones and regen zones. | None. |
| `hololive_coliseum/gravity_zone.py` | Used in `game.py` to create low‑gravity areas. | None. |
| `hololive_coliseum/platform.py` | Static and moving platforms players can stand on. | None. |
| `hololive_coliseum/powerup.py` | Spawned by `game.py` during matches for healing, mana, stamina, speed, shield, attack, defense, experience or extra-life boosts. | None. |
| `hololive_coliseum/skill_manager.py` | Used by `player.py` to manage ability cooldowns. | None. |
| `hololive_coliseum/auto_skill_manager.py` | Generates skills from level and stats. | None. |
| `hololive_coliseum/health_manager.py` | Provides health tracking and passive regeneration used by `player.py`. | None. |
| `hololive_coliseum/mana_manager.py` | Provides mana tracking helpers used by `player.py`. | None. |
| `hololive_coliseum/stamina_manager.py` | Tracks stamina for dodging, blocking and attacks. | None. |
| `hololive_coliseum/stats_manager.py` | Returns STR, DEX and other stats with temporary modifiers. | None. |
| `hololive_coliseum/experience_manager.py` | Tracks XP and levels up when thresholds are reached. | None. |
| `hololive_coliseum/leveling_manager.py` | Stores per-player experience managers for the MMO. | Used by `WorldGenerationManager`. |
| `hololive_coliseum/score_manager.py` | Tracks the current and best score with combo bonuses. | None. |
| `hololive_coliseum/shared_state_manager.py` | Maintains shared state snapshots for networking. | `state_sync` |
| `hololive_coliseum/distributed_state_manager.py` | Streams state deltas across distributed servers with snapshot handshakes, history resends, catch-up batches and peer lag sync-plan helpers. | `shared_state_manager`, `transmission_manager`, `node_manager`, `cluster_manager` |
| `hololive_coliseum/class_manager.py` | Stores MMO class templates. | None. |
| `hololive_coliseum/class_generator.py` | Creates unique class templates. | None. |
| `hololive_coliseum/item_manager.py` | Defines fantasy item classes and registers them. | None. |
| `hololive_coliseum/equipment_manager.py` | Stores equipped items for each player. | None. |
| `hololive_coliseum/inventory_manager.py` | Tracks collected items with optional capacity limits. | None. |
| `hololive_coliseum/quest_manager.py` | Manages active quests and progress. | None. |
| `hololive_coliseum/achievement_manager.py` | Records unlocked achievements. | None. |
| `hololive_coliseum/keybind_manager.py` | Holds configurable key mappings. | None. |
| `hololive_coliseum/ai_manager.py` | Coordinates enemy decision making. | Used by `game.py` during play. |
| `hololive_coliseum/npc_manager.py` | Holds enemy and ally sprite groups. | Used by `game.py` to organize NPCs. |
| `hololive_coliseum/ally_manager.py` | Updates friendly NPCs that assist the player. | Called from `game.py` each frame. |
| `hololive_coliseum/menu_manager.py` | Tracks menu selection and navigation. | Used by `game.py` when handling menus. |
| `hololive_coliseum/game_state_manager.py` | Stores the current and previous game state. | Updated by `game.py` whenever the state changes. |
| `hololive_coliseum/team_manager.py` | Assigns entities to teams and checks ally relationships. | Used by `CombatManager`. |
| `hololive_coliseum/network.py` | Created by `game.py` when online play is chosen. | Uses UDP sockets for discovery, state and record sharing. |
| `hololive_coliseum/transmission_manager.py` | Wraps holographic compression with selectable algorithms and level control. | Used by `NetworkManager`. |
| `hololive_coliseum/data_protection_manager.py` | Encrypts packets with AES-GCM and adds HMAC signatures. | Used by `NetworkManager`. |
| `hololive_coliseum/state_sync.py` | Helper for delta-compressed state updates with sequence numbers. | None. |
| `hololive_coliseum/state_verification_manager.py` | Computes CRC32 and SHA256 digests so peers can verify shared state cheaply. | `shared_state_manager` |
| `hololive_coliseum/holographic_compression.py` | Encodes packets into pointcloud base64 pairs plus a public-key signature fragment with optional XOR encryption, digest verification and zlib, bz2 or lzma compression. | None. |
| `hololive_coliseum/node_registry.py` | Shared helper for tracking known server nodes. | Read/writes `SavedGames/nodes.json`. |
| `hololive_coliseum/mining_manager.py` | Runs optional background proof-of-work mining. | None. |
| `hololive_coliseum/world_seed_manager.py` | Stores mined block hashes as world seeds and can sync them from the blockchain. | Used by `MiningManager`. |
| `hololive_coliseum/world_region_manager.py` | Stores generated regions and syncs them from the blockchain. | Used by `WorldGenerationManager`. |
| `hololive_coliseum/world_generation_manager.py` | Builds MMO regions from seeds and content and syncs blockchain seeds and regions. | Used by future MMO modes. |
| `hololive_coliseum/auto_dev_feedback_manager.py` | Captures arena telemetry for MMO auto-development. | Used by `game.py`, `HazardManager` and `WorldGenerationManager`. |
| `hololive_coliseum/auto_dev_scenario_manager.py` | Builds scenario briefs that connect projections to objectives. | Used by `WorldGenerationManager`. |
| `hololive_coliseum/auto_dev_monster_manager.py` | Generates monster templates from hazards and trade skills. | Used by `WorldGenerationManager`. |
| `hololive_coliseum/auto_dev_spawn_manager.py` | Plans monster group spawn timing based on scenario danger. | Used by `WorldGenerationManager`. |
| `hololive_coliseum/auto_dev_mob_ai_manager.py` | Produces AI directives for the generated monster roster. | Used by `WorldGenerationManager`. |
| `hololive_coliseum/auto_dev_boss_manager.py` | Chooses bosses tied to the current roadmap and projections. | Used by `WorldGenerationManager`. |
| `hololive_coliseum/auto_dev_quest_manager.py` | Builds quests that respond to trade skills and boss plans. | Used by `WorldGenerationManager`. |
| `hololive_coliseum/auto_dev_research_manager.py` | Samples runtime CPU load and stores raw processing percentages for auto-dev research. | Used by `WorldGenerationManager`. |
| `hololive_coliseum/auto_dev_guidance_manager.py` | Blends encounter, quest and research data into general-intelligence guidance. | Used by `WorldGenerationManager`. |
| `hololive_coliseum/auto_dev_evolution_manager.py` | Synthesises guidance, roadmap and research into evolution plans. | Used by `WorldGenerationManager`. |
| `hololive_coliseum/auto_dev_intelligence_manager.py` | Provides general-intelligence oversight using live processing data, raw utilisation percentages, monster creation analytics, spawn tactics, and AI/boss/quest guidance. | Used by `WorldGenerationManager`. |
| `hololive_coliseum/auto_dev_network_manager.py` | Evaluates relay latency, security posture and bandwidth demand for MMO networking. | Used by `WorldGenerationManager`. |
| `hololive_coliseum/world_player_manager.py` | Tracks player positions and spawns new regions when explorers wander past the current map. | Used by future MMO modes. |
| `hololive_coliseum/mmo_builder.py` | Builds seed, generation, region, player and voting managers for MMO setup. | None. |
| `hololive_coliseum/save_manager.py` | Called by `game.py` and tests to persist settings and inventory. | Reads/writes JSON in `SavedGames` and merges record updates from peers. |
| `hololive_coliseum/iteration_manager.py` | Saves each run's state as `.gguf` snapshots. | Used by `game.py` when matches end. |
| `hololive_coliseum/goal_analysis_manager.py` | Checks `.gguf` snapshots to tick goals. | None. |
| `hololive_coliseum/accounts.py` | Used by the blockchain and tests. | Provides an `AccountsManager` class for storing public keys and access levels. |
| `hololive_coliseum/voting_manager.py` | Tracks weekly votes per category and records them on the blockchain. | Used by the main menu. |
| `hololive_coliseum/combat_manager.py` | Handles collisions and turn order. | Used by `game.py`. |
| `hololive_coliseum/damage_manager.py` | Computes final damage after reductions. | None. |
| `hololive_coliseum/damage_number.py` | Shows floating damage indicators. | `game.py` |
| `hololive_coliseum/threat_manager.py` | Tracks threat values for AI targeting. | None. |
| `hololive_coliseum/loot_manager.py` | Generates loot from drop tables. | Used by `game.py`. |
| `hololive_coliseum/buff_manager.py` | Applies buffs and debuffs using the status effect system. | None. |
| `hololive_coliseum/appearance_manager.py` | Stores selected skins per entity. | None. |
| `hololive_coliseum/animation_manager.py` | Tracks animation states and frames. | None. |
| `hololive_coliseum/name_manager.py` | Handles naming and renames for characters. | None. |
| `hololive_coliseum/session_manager.py` | Maintains login sessions to prevent duplicates. | None. |
| `hololive_coliseum/sync_manager.py` | Computes time offsets between clients. | None. |
| `hololive_coliseum/instance_manager.py` | Creates and destroys gameplay instances. | None. |
| `hololive_coliseum/patch_manager.py` | Records the current patch version. | None. |
| `hololive_coliseum/auth_manager.py` | Stores salted password hashes, issues expiring tokens, and locks accounts after repeated failures. | None. |
| `hololive_coliseum/cheat_detection_manager.py` | Flags suspicious behavior. | None. |
| `hololive_coliseum/ban_manager.py` | Maintains banned account list. | None. |
| `hololive_coliseum/logging_manager.py` | Collects log events. | None. |
| `hololive_coliseum/ui_manager.py` | Tracks active UI elements. | None. |
| `hololive_coliseum/notification_manager.py` | Queues in-game notifications. | None. |
| `hololive_coliseum/input_manager.py` | Stores key and controller mappings. | None. |
| `hololive_coliseum/accessibility_manager.py` | Toggles colorblind modes and fonts. | None. |
| `hololive_coliseum/chat_manager.py` | Manages text chat messages and chat box state. | Used by `game.py` during matches. |
| `hololive_coliseum/voice_chat_manager.py` | Tracks users in voice channels. | None. |
| `hololive_coliseum/emote_manager.py` | Provides available emotes. | None. |
| `hololive_coliseum/sound_manager.py` | Plays sound effects and music. | None. |
| `hololive_coliseum/hud_manager.py` | Draws health, mana, timer, score, combo, and damage flashes. | Used by `game.py` during play. |
| `hololive_coliseum/camera_manager.py` | Follows the player, offers a third-person offset, and supports screen shake. | None. |
| `hololive_coliseum/effect_manager.py` | Triggers particle effects. | None. |
| `hololive_coliseum/script_manager.py` | Loads and stores small scripts. | None. |
| `hololive_coliseum/localization_manager.py` | Provides basic text translation. | None. |
| `hololive_coliseum/resource_manager.py` | Caches loaded assets. | None. |
| `hololive_coliseum/cluster_manager.py` | Tracks nodes in a cluster. | None. |
| `hololive_coliseum/matchmaking_manager.py` | Groups players for matches. | None. |
| `hololive_coliseum/load_balancer_manager.py` | Chooses the least busy server. | None. |
| `hololive_coliseum/migration_manager.py` | Handles player transfers between servers. | None. |
| `hololive_coliseum/billing_manager.py` | Records purchases and subscriptions. | None. |
| `hololive_coliseum/ad_manager.py` | Manages in-game ads. | None. |
| `hololive_coliseum/api_manager.py` | Stores third-party API endpoints. | None. |
| `hololive_coliseum/support_manager.py` | Tracks support tickets. | None. |
| `hololive_coliseum/crafting_manager.py` | Handles crafting recipes. | None. |
| `hololive_coliseum/crafting_station.py` | Interactable station that crafts items from recipes. | None. |
| `hololive_coliseum/profession_manager.py` | Tracks profession XP and levels. | None. |
| `hololive_coliseum/gathering_manager.py` | Runs a timing-based gathering mini-game. | None. |
| `hololive_coliseum/minigame_manager.py` | Hosts quick reaction mini-games. | None. |
| `hololive_coliseum/trade_manager.py` | Manages item trades between players. | None. |
| `hololive_coliseum/economy_manager.py` | Stores global item prices. | None. |
| `hololive_coliseum/skill_generator.py` | Crafts skill templates for classes. | None. |
| `hololive_coliseum/subclass_generator.py` | Derives subclasses from base class stats. | None. |
| `hololive_coliseum/trade_skill_generator.py` | Creates trade skills for professions. | None. |
| `hololive_coliseum/recursive_generator.py` | Chains class, skill and trade generators. | None. |
| `hololive_coliseum/interaction_generator.py` | Creates simple interactable templates. | None. |
| `hololive_coliseum/interaction_manager.py` | Registers interactables and triggers responses. | None. |
| `hololive_coliseum/auto_balancer.py` | Adjusts class stats toward the average. | None. |
| `hololive_coliseum/currency_manager.py` | Tracks player currency balances. | None. |
| `hololive_coliseum/title_manager.py` | Unlocks and sets active titles. | None. |
| `hololive_coliseum/reputation_manager.py` | Stores faction reputation. | None. |
| `hololive_coliseum/friend_manager.py` | Maintains the friends list. | None. |
| `hololive_coliseum/guild_manager.py` | Manages multiple guilds and member ranks. | None. |
| `hololive_coliseum/mail_manager.py` | Sends and retrieves player mail. | None. |
| `hololive_coliseum/map_manager.py` | Stores maps with hazard data and tracks the active map. | Used by `game.py` during level setup. |
| `hololive_coliseum/environment_manager.py` | Tracks weather and day/night cycle. | None. |
| `hololive_coliseum/spawn_manager.py` | Schedules power-ups and other spawns. | Used by `game.py` to time drops. |
| `hololive_coliseum/level_manager.py` | Initializes sprites and hazards for each level. | Called by `game.py` when starting a stage. |
| `hololive_coliseum/hazard_manager.py` | Applies hazard effects to players and enemies. | Used by `game.py` during play. |
| `hololive_coliseum/event_manager.py` | Records triggered world events. | None. |
| `hololive_coliseum/dungeon_manager.py` | Manages dungeon lockouts for players. | None. |
| `hololive_coliseum/housing_manager.py` | Stores player housing data. | None. |
| `hololive_coliseum/mount_manager.py` | Tracks mounts per player. | None. |
| `hololive_coliseum/pet_manager.py` | Maintains collectible pets. | None. |
| `hololive_coliseum/companion_manager.py` | Assigns companions to players. | None. |
| `hololive_coliseum/replay_manager.py` | Stores match replays. | None. |
| `hololive_coliseum/screenshot_manager.py` | Saves screenshots under `SavedGames/screenshots`. | None. |
| `hololive_coliseum/bot_manager.py` | Spawns automated bot players. | None. |
| `hololive_coliseum/telemetry_manager.py` | Collects gameplay analytics. | None. |
| `hololive_coliseum/ai_moderation_manager.py` | Flags abusive chat. | None. |
| `hololive_coliseum/dynamic_content_manager.py` | Generates quests and items. | None. |
| `hololive_coliseum/geo_manager.py` | Tracks GPS locations for AR modes. | None. |
| `hololive_coliseum/device_manager.py` | Registers haptic and motion devices. | None. |
| `hololive_coliseum/season_manager.py` | Advances the current season. | None. |
| `hololive_coliseum/daily_task_manager.py` | Resets daily quests. | None. |
| `hololive_coliseum/weekly_manager.py` | Resets weekly challenges. | None. |
| `hololive_coliseum/tutorial_manager.py` | Tracks tutorial progress. | None. |
| `hololive_coliseum/onboarding_manager.py` | Guides new players. | None. |
| `hololive_coliseum/arena_manager.py` | Records PvP rankings. | None. |
| `hololive_coliseum/war_manager.py` | Stores faction war points. | None. |
| `hololive_coliseum/tournament_manager.py` | Organizes brackets. | None. |
| `hololive_coliseum/raid_manager.py` | Handles raid groups. | None. |
| `hololive_coliseum/party_manager.py` | Manages party membership. | None. |

The tests import the modules above to verify behavior. Development documents in 
`docs/` describe goals and planning for future work.

## Testing

Run the full suite with `pytest -q`. See `docs/TESTING.md` for headless and
targeted test runs, plus manual smoke checks.

To snapshot project health and repository drift, run
`python tools/analyze_project_state.py`. The command writes
`PROJECT_STATE_ANALYSIS.md` in the repository root.
