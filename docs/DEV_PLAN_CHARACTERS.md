# Character Abilities Plan

Each Hololive member will gain a unique special ability and stat profile. Planned concepts:

- **Gawr Gura**: Exploding trident throw with high attack but low defense and health. *(Stats implemented)*
- **Watson Amelia**: Time travel dash that slows opponents; high speed but low
  health. *(Stats implemented)*
- **Ninomae Ina'nis**: Tentacle grapple pulling enemies closer and a deep mana
  pool for frequent specials. *(Stats implemented)*
- **Takanashi Kiara**: Fiery winged leap dealing damage on landing and a balanced
  stat line. *(Stats implemented)*
- **Mori Calliope**: Soul scythe projectile that returns like a boomerang with
  high attack but lower health. *(Stats implemented)*
- **Ceres Fauna**: Healing area that restores ally health with a defensive stat
  line. *(Stats implemented)*
- **Ouro Kronii**: Time freeze parry with extended invulnerability and sturdy
  defenses. *(Stats implemented)*
- **IRyS**: Crystal shield absorbing projectiles with high defense but modest attack. *(Stats implemented)*
- **Nanashi Mumei**: Flock summon that disrupts enemy movement, hitting hard but with lower health. *(Stats implemented)*
- **Hakos Baelz**: Randomized chaos effect altering gravity or controls. *(Implemented)*
- **Shirakami Fubuki**: Freezing shard that slows enemies via a `FreezingProjectile`
  subclass with 9 attack, 5 defense and 95 health. *(Stats implemented)*
- **Natsuiro Matsuri**: Firework projectile that explodes overhead with 11 attack,
  5 defense and 100 health. *(Stats implemented)*
- **Sakura Miko**: Piercing beam that passes through enemies via a
  `PiercingProjectile` subclass with 12 attack, 3 defense and 85 health. *(Stats implemented)*
- **Minato Aqua**: Water blast that slows foes before exploding with 9 attack,
  7 defense and 100 health. *(Stats implemented)*
- **Usada Pekora**: Bouncing carrot bomb with attack 11, defense 5 and max
  health 95. *(Stats implemented)*
 - **Houshou Marine**: Anchor boomerang returning with attack 13, defense 5 and
   max health 90. *(Stats implemented)*
 - **Hoshimachi Suisei**: Piercing star projectile with attack 12, defense 6 and
   max health 95. *(Stats implemented)*
 - **Nakiri Ayame**: Swift dash attack with 11 attack, 4 defense and
   max health 90. *(Stats implemented)*
 - **Shirogane Noel**: Ground slam that sends a traveling shockwave with attack
   9, defense 8 and max health 110. *(Stats implemented)*
 - **Shiranui Flare**: Burning fireball that ignites enemies with attack 12,
   defense 4 and max health 95. *(Stats implemented)*

 - **Oozora Subaru**: Stunning blast that dazes foes with 10 attack, 6 defense
   and 105 health. *(Stats implemented)*
 - **Tokino Sora**: Uplifting melody that weaves through the air with 9 attack,
   5 defense and 110 health. *(Stats implemented)*

These abilities will be implemented as subclasses of the base `PlayerCharacter` class.
