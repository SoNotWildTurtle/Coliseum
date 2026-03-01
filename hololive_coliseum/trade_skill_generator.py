"""Generate trade skills for professions."""

from __future__ import annotations

from typing import Iterable, Sequence


class TradeSkillGenerator:
    """Create trade skill entries with recipe hooks, levels, and experience."""

    _SPECIALISATIONS = {
        "Alchemy": ("Potion Brewing", "Catalyst Refining", "Essence Infusion"),
        "Armouring": ("Plate Sculpting", "Mail Linking", "Ward Embedding"),
        "Brewing": ("Herbal Fermentation", "Spiced Infusions", "Mythic Ales"),
        "Foraging": ("Wild Harvesting", "Herbal Surveying", "Fungal Lore"),
        "Enchanting": ("Focus Attunement", "Sigil Binding", "Mythic Channeling"),
        "Engineering": (
            "Mechanism Drafting",
            "Reactor Stabilising",
            "Modular Assembly",
        ),
        "Fishing": ("Tidal Reading", "Net Weaving", "Deepwater Mastery"),
        "Fletching": ("Feather Selection", "Bow Carving", "Tension Harmonies"),
        "Herbalism": ("Seed Mapping", "Essence Pruning", "Bloom Alignment"),
        "Inn-Keeping": ("Hearth Stewardship", "Guest Harmony", "Festival Planning"),
        "Jewelcrafting": (
            "Facet Mapping",
            "Aura Binding",
            "Focus Setting",
        ),
        "Leatherworking": (
            "Hide Preservation",
            "Flex Weaving",
            "Runic Stitching",
        ),
        "Logging": ("Tree Whispering", "Sap Analysis", "Heartwood Reading"),
        "Mining": ("Ore Prospecting", "Gem Extraction", "Deep Delving"),
        "Prospecting": ("Vein Charting", "Purity Sampling", "Geode Resonance"),
        "Runecrafting": (
            "Sigil Design",
            "Glyph Etching",
            "Channel Harmonising",
        ),
        "Seductress": ("Charm Studies", "Stagecraft", "Velvet Negotiations"),
        "Smithing": ("Weapon Forging", "Armor Tempering", "Rune Inlay"),
        "Spellcrafting": ("Arcane Geometry", "Mana Threading", "Resonance Focus"),
        "Trapping": ("Snare Setting", "Lure Craft", "Beast Reading"),
    }

    _LEVEL_BANDS = {
        "Alchemy": (18, 40),
        "Armouring": (22, 38),
        "Brewing": (10, 26),
        "Foraging": (6, 18),
        "Enchanting": (30, 52),
        "Engineering": (24, 44),
        "Fishing": (6, 24),
        "Fletching": (12, 28),
        "Herbalism": (4, 20),
        "Inn-Keeping": (4, 18),
        "Jewelcrafting": (26, 46),
        "Leatherworking": (14, 30),
        "Logging": (8, 22),
        "Mining": (1, 22),
        "Prospecting": (12, 30),
        "Runecrafting": (28, 50),
        "Seductress": (32, 54),
        "Smithing": (16, 34),
        "Spellcrafting": (34, 58),
        "Trapping": (8, 24),
    }

    _RECIPE_HINTS = {
        "Mining": (
            {
                "name": "Starforged Greatsword",
                "product": "weapon",
                "materials": ("Starmetal Ore", "Celestial Flux"),
            },
        ),
        "Smithing": (
            {
                "name": "Bulwark Vanguard",
                "product": "armor",
                "materials": ("Refined Steel", "Tempered Plates"),
            },
            {
                "name": "Stormedge Saber",
                "product": "weapon",
                "materials": ("Folded Steel", "Charged Crystal"),
            },
        ),
        "Leatherworking": (
            {
                "name": "Skystride Harness",
                "product": "armor",
                "materials": ("Cloudscale Hide", "Resonant Thread"),
            },
        ),
        "Logging": (
            {
                "name": "Heartwood Longbow",
                "product": "bow",
                "materials": ("Ancient Timber", "Silk Bowstring"),
            },
        ),
        "Runecrafting": (
            {
                "name": "Wardbinder Aegis",
                "product": "armor",
                "materials": ("Runic Stone", "Mythic Lattice"),
            },
        ),
        "Engineering": (
            {
                "name": "Pulsefire Lance",
                "product": "weapon",
                "materials": ("Machined Alloy", "Arc Core"),
            },
        ),
        "Jewelcrafting": (
            {
                "name": "Radiant Diadem",
                "product": "armor",
                "materials": ("Sunstone Gem", "Auric Filament"),
            },
        ),
        "Armouring": (
            {
                "name": "Aegisheart Plate",
                "product": "armor",
                "materials": ("Hardened Mail", "Guardian Sigil"),
            },
        ),
        "Alchemy": (
            {
                "name": "Aurora Channeler",
                "product": "wand",
                "materials": ("Prismatic Essence", "Glass Core"),
            },
        ),
        "Brewing": (
            {
                "name": "Brewmaster's Ward",
                "product": "armor",
                "materials": ("Hearth Malt", "Spirit Foam"),
            },
        ),
        "Foraging": (
            {
                "name": "Verdant Lattice",
                "product": "material",
                "materials": ("Blooming Fronds", "Sunlit Dew"),
            },
        ),
        "Enchanting": (
            {
                "name": "Starseer Wand",
                "product": "wand",
                "materials": ("Astral Resin", "Silver Filigree"),
            },
        ),
        "Fishing": (
            {
                "name": "Tidecaller's Bow",
                "product": "bow",
                "materials": ("Sea Glass", "Coral String"),
            },
        ),
        "Fletching": (
            {
                "name": "Galecrest Longbow",
                "product": "bow",
                "materials": ("Yew Plank", "Stormfeather"),
            },
        ),
        "Herbalism": (
            {
                "name": "Lifespring Infusion",
                "product": "material",
                "materials": ("Verdant Herbs", "Crystalline Sap"),
            },
        ),
        "Inn-Keeping": (
            {
                "name": "Hearthguard Apron",
                "product": "armor",
                "materials": ("Warm Linen", "Copper Buttons"),
            },
        ),
        "Seductress": (
            {
                "name": "Velvet Whisper Veil",
                "product": "armor",
                "materials": ("Silken Lace", "Moonlight Thread"),
            },
        ),
        "Prospecting": (
            {
                "name": "Auric Prospect Kit",
                "product": "material",
                "materials": ("Survey Lens", "Refined Gravel"),
            },
        ),
        "Spellcrafting": (
            {
                "name": "Resonant Arcanum",
                "product": "wand",
                "materials": ("Void Crystal", "Echo Wire"),
            },
        ),
        "Trapping": (
            {
                "name": "Beastweave Harness",
                "product": "armor",
                "materials": ("Sinew Cord", "Totem Stitch"),
            },
        ),
    }

    _GATHERING_SYNERGIES = {
        "Foraging": {
            "armor": {"health": 6},
            "wand": {"attack": 2},
        },
        "Herbalism": {
            "wand": {"attack": 3, "defense": 1},
            "armor": {"health": 4},
        },
        "Logging": {
            "bow": {"attack": 4, "defense": 1},
        },
        "Prospecting": {
            "weapon": {"attack": 3},
            "armor": {"defense": 2},
        },
        "Trapping": {
            "bow": {"attack": 2},
            "armor": {"defense": 1},
        },
    }

    def generate(self, profession: str) -> dict[str, object]:
        """Return a trade skill record with zero starting experience and recipes."""

        name = profession.title()
        specialisations = self._SPECIALISATIONS.get(
            name, (f"{name} Basics", "Artisan Fundamentals")
        )
        recipes = self._RECIPE_HINTS.get(name, ())
        min_level, max_level = self.level_band(name)
        synergy = self.gathering_synergy(name)
        return {
            "name": name,
            "experience": 0,
            "specialisations": tuple(specialisations),
            "recipes": tuple(
                {
                    "name": hint["name"],
                    "product": hint["product"],
                    "materials": tuple(hint["materials"]),
                }
                for hint in recipes
            ),
            "level_band": {"min": min_level, "max": max_level},
            "difficulty_tier": self._tier_for_band((min_level, max_level)),
            "gathering_synergy": synergy,
        }

    def list_core_skills(self) -> tuple[str, ...]:
        """Return the baseline set of trade skills recognised by the generator."""

        return tuple(sorted(self._SPECIALISATIONS))

    def level_band(self, profession: str) -> tuple[int, int]:
        """Return the recommended level band for ``profession``."""

        name = profession.title()
        return self._LEVEL_BANDS.get(name, (6, 24))

    def is_gathering(self, profession: str) -> bool:
        """Return ``True`` when ``profession`` is a gathering discipline."""

        return profession.title() in self._GATHERING_SYNERGIES

    def gathering_synergy(self, profession: str) -> dict[str, dict[str, int]]:
        """Return crafting bonuses supplied by a gathering ``profession``."""

        name = profession.title()
        bonuses = self._GATHERING_SYNERGIES.get(name, {})
        return {product: dict(stats) for product, stats in bonuses.items()}

    def collect_gathering_bonuses(
        self, skills: Sequence[str]
    ) -> dict[str, dict[str, int]]:
        """Aggregate crafting bonuses from gathering ``skills``."""

        aggregated: dict[str, dict[str, int]] = {}
        for skill in skills:
            name = skill.title()
            if name not in self._GATHERING_SYNERGIES:
                continue
            band = self.level_band(name)
            scale = max(1, int(((band[0] + band[1]) / 2) // 10))
            for product_type, stats in self._GATHERING_SYNERGIES[name].items():
                bucket = aggregated.setdefault(product_type, {})
                for stat, value in stats.items():
                    bucket[stat] = bucket.get(stat, 0) + value + scale
        return aggregated

    def iter_recipe_sources(self, skills: Sequence[str]) -> Iterable[tuple[str, dict[str, object]]]:
        """Yield ``(skill, recipe)`` pairs for the supplied trade ``skills``."""

        for skill in skills:
            record = self.generate(skill)
            for recipe in record["recipes"]:
                yield record["name"], recipe

    @staticmethod
    def _tier_for_band(band: tuple[int, int]) -> str:
        """Return a tier label for the provided level ``band``."""

        minimum, maximum = band
        midpoint = (minimum + maximum) / 2
        if midpoint < 20:
            return "novice"
        if midpoint < 40:
            return "adept"
        return "master"
