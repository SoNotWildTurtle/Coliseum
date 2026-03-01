"""Dynamic content rotation and curation."""

class DynamicContentManager:
    """Generate basic random quests or items."""

    def __init__(self):
        self.counter = 0
        self.content = {}

    def create(self, kind: str) -> str:
        self.counter += 1
        cid = f"{kind}_{self.counter}"
        self.content[cid] = kind
        return cid

    def list_content(self):
        return dict(self.content)
