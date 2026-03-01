# Networking Plan

The prototype uses a simple UDP based system for minimal latency. Discovery works
through broadcast packets so clients can locate hosts on the local network. To
expand beyond a single LAN, the `node_registry` module keeps a list of known
servers in `SavedGames/nodes.json`. Each host registers itself and sends an
`announce` packet to other nodes. When a node receives an announcement it adds
the sender to its registry. This creates a lightweight mesh of user-hosted nodes
without central coordination.
Router nodes also gossip their known peers: after processing announcements they
broadcast `nodes_update` packets so everyone shares the same registry. Clients or
new nodes can ask any router for the latest list via a `get_nodes` request.
Clients ping all known nodes at startup and pick the one with the lowest
round-trip latency to use for online sessions. In addition to discovery,
nodes maintain a list of registered game hosts. When a player starts a match
they send a `register` packet to nearby nodes. Other clients can issue `find`
requests to any node and receive the list of currently available games. This
DNS-like approach lets user-hosted nodes route players to each other without a
central server. It also helps clients choose the closest peer when multiple
hosts are available.
Router nodes also share their game lists with each other using `games_update`
packets so the mesh stays synchronized even as matches come and go. They
likewise synchronize active clients by broadcasting `clients_update` packets
whenever a player joins or leaves a node. When a client registers, the router
replies with the current client list and sends `client_add` messages to existing
peers so they can connect directly. Clients send a `client_leave` packet when
disconnecting and routers forward a `client_remove` notice to remaining peers.
This will make it easier to scale the prototype toward a larger MMO-style
environment where servers need to know which players are online.
State updates exchanged during gameplay carry a sequence number and only include
fields that changed since the previous update. The `StateSync` helper computes
these diffs and can ignore tiny float changes using configurable tolerances so
messages remain tiny and reduce network overhead.

Each packet now includes an HMAC signature when a shared secret is configured.
Nodes verify the signature before processing data so malicious or malformed
packets are discarded. When a key is provided, AES-GCM encryption keeps messages
private while remaining lightweight. Keys can rotate during long sessions to
limit exposure.
To prevent spoofing, packets carry the sender's ID and routers reject messages
when the claimed ID does not match the source address.
The **Accounts** menu offers a *Renew Key* button so players can rotate the
Ed25519 key pair used for packet signing and blockchain entries.
To further reduce bandwidth usage, packets are compressed using a holographic
lithography technique. Messages are converted to a pointcloud with four anchor
points marking `(0,0,1)`, `(0,0,0)`, `(1,1,1)` and `(1,1,0)` in cyan, white,
black and red. Anchors now store a virtual size, luminosity and black/white
level so the pointcloud can be reconstructed at multiple detail layers. Before
compression, repeated byte sequences are run-length encoded. The data is split
into two base64 strings and recombined on receipt. Compression can pick the
smallest result between zlib, bz2 and lzma via an ``auto`` setting in the
``TransmissionManager`` and uses streaming decompressors so uncompression stays
lightweight. The encoded bytes include a third base64 fragment carrying the
sender's public key and a signature so peers can verify the packet's origin.
Each packet also embeds a BLAKE2s digest so the receiver can check integrity
before decoding. When a key is supplied, `DataProtectionManager` encrypts the
compressed bytes with AES-GCM using a random nonce so data in transit remains
private even over unsecured networks. Before this step the manager removes
designated sensitive fields, preventing secrets like passwords from leaving
the client.
Important control packets can also be sent in **reliable** mode. When enabled
the sender stores a copy and will resend it until an `ack` message confirms the
receiver got it. Each reliable packet includes an integer *importance* value so
critical packets are retried more aggressively. Higher importance reduces the
wait between resends and increases the total number of attempts. This ensures
registration and blockchain updates are delivered even if a packet is dropped.
Simple ``chat`` packets carry short text messages between players so the in-game
chat box works online.
Clients may synchronize their clocks by sending a ``time_request`` to a router
node. The router responds with a ``time_response`` containing its current time
so the client can compute an offset via ``SyncManager``.
Nodes periodically prune entries from `nodes.json` if they no longer respond to
a ping so discovery remains accurate over time.
Players can toggle hosting from the **Node Settings** menu. Starting a node
spawns a `NetworkManager` in host mode, registers the address, broadcasts an
`announce` packet and begins sharing new blockchain blocks. Choosing "Stop Node"
closes the socket and the game falls back to client-only behavior.

Game results are stored in a lightweight blockchain. When an online match
finishes the winner "mines" a block containing the participant IDs and optional
bet amount. The block is written to `chain.json` and shared with other nodes via
the announce system. Player balances in `balances.json` track wagers and can be
synchronized in the same way.
Remote chains can be verified and merged so all nodes eventually share the
longest valid history.

New peers may issue a ``chain_request`` to a router node. The router replies
with the current chain so newcomers can merge the latest history before
participating in online matches.

Blocks now carry digital signatures from all listed players. When chains are
exchanged nodes verify these signatures against the account registry before
accepting new blocks.

Each block is also mined with a small proof-of-work requirement so its hash
begins with ``00``. Hosts broadcast newly mined blocks to clients and peer nodes
immediately so the mesh stays in sync.

Nodes also broadcast ``records_update`` packets containing their best survival
time and high score. Peers merge these records so leaderboards stay consistent
across the mesh.
Clients can volunteer to act as relay nodes by enabling the *Latency Helper*
setting. Router nodes maintain a list of these relays and share them with peers.
Packets may be forwarded through a relay when it offers a faster path between
two players, keeping latency low even across distant networks.
During gameplay, each client also bridges its state packets: updates are sent to
the host node for verification and directly to other peers for immediate
synchronization. This Snowflake-style dual path helps deter man-in-the-middle
attacks because both copies must match, while the direct peer link minimizes
latency.

All packets include a random nonce, timestamp and HMAC signature. Replay
attempts or stale messages older than a few seconds are discarded before they
affect game state.
After the initial handshake, peers attach a session token to every packet and
drop messages with missing or incorrect tokens, preventing unauthorized
injections. Hosts also consult a `BanManager` to ignore packets from user IDs
on a ban list.

Shared state packets additionally carry CRC32 and SHA256 digests from a
`StateVerificationManager`, allowing peers to confirm matching game values
without retaining historical snapshots.

`NetworkManager` enforces a configurable per-peer rate limit so excessive
traffic is dropped before it can flood the connection. Nodes may also enable a
background mining mode that performs proof-of-work on dummy blocks. This
hashing lays groundwork for a future MMORPG world that grows as players
contribute spare processing power.

Future work will experiment with rollback netcode and more efficient state
synchronization once the gameplay loop stabilizes.
