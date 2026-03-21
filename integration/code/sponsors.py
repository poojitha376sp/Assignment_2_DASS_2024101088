"""
Sponsorships Module
Tracks active sponsor deals and distributes bonuses for wins.
Integration with Results and Inventory.
"""

class SponsorModule:
    def __init__(self, inventory):
        self.inventory = inventory
        self.active_deals = {} # {race_id: bonus_amount}

    def sign_sponsor(self, race_id, bonus):
        """Signs a sponsor for a specific race."""
        self.active_deals[race_id] = bonus
        return True, f"Sponsor signed for Race '{race_id}'. Win bonus: ${bonus}."

    def trigger_win_bonus(self, race_id):
        """
        Awards bonus if a deal exists for the race.
        INTEGRATION RULE: Bonus is credited to Inventory.
        """
        bonus = self.active_deals.get(race_id, 0)
        if bonus > 0:
            self.inventory.add_cash(bonus)
            return True, f"Sponsorship Bonus of ${bonus} credited to inventory."
        return False, "No sponsor bonus for this race."

    def list_deals(self):
        """Show current sponsorship contracts."""
        return self.active_deals
