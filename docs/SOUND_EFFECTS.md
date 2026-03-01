# Sound Effects

The game can load optional sound effect files from `sounds/`. If the files are
missing, it generates short synth tones at runtime so combat still feels
responsive without committing binary assets.

## Supported Filenames
- `hit_light.wav` or `hit_light.ogg`
- `hit_heavy.wav` or `hit_heavy.ogg`
- `hit_crit.wav` or `hit_crit.ogg`
- `melee_swing.wav` or `melee_swing.ogg`
- `special_cast.wav` or `special_cast.ogg`

## Behavior
- When a sound file is present it is loaded and played through `SoundManager`.
- When a sound file is missing a short synthesized tone is generated instead.
- The game never commits binary sound assets in the repository.
