"""
Trophy Room Module
Stores achievements and awards earned by the team through race victories.
Integration with Results.
"""

class TrophyModule:
    def __init__(self):
        self.trophies = [] # List of strings: ["Winner of RACE_001", ...]

    def add_trophy(self, title):
        """Unlocks a new trophy."""
        self.trophies.append(title)
        return True, f"Trophy Unlocked: {title}!"

    def has_trophy(self, title):
        """Check if a specific trophy exists."""
        return title in self.trophies

    def list_trophies(self):
        """Return all earned trophies."""
        return self.trophies
