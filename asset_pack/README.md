Asset Pack

This folder is reserved for runtime-loaded Hololive-themed sprites. Binary
assets are not committed to the repo; add your PNGs locally or let the game
generate placeholders at runtime.

Suggested layout:
- characters/<name>_right.png
- characters/<name>_left.png
- enemies/<name>_right.png
- enemies/<name>_left.png
- specials/<name>_<frame>.png
- effects/<name>_<frame>.png

Set `HOLO_ASSET_PACK=asset_pack` (or a custom path) to load assets from here.
