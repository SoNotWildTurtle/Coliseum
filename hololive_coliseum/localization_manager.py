"""Localization lookups and language settings."""

class LocalizationManager:
    """Provide basic string localization using language dictionaries."""

    def __init__(self, default_lang: str = "en") -> None:
        self.default = default_lang
        self.translations: dict[str, dict[str, str]] = {}

    def set(self, lang: str, key: str, text: str) -> None:
        self.translations.setdefault(lang, {})[key] = text

    def translate(self, key: str, lang: str | None = None) -> str:
        lang = lang or self.default
        return self.translations.get(lang, {}).get(key, key)
