"""
Results Management Module
Processes race outcomes and distributes prize money.
"""

class ResultsModule:
    def __init__(self, inventory_module, race_module):
        self.inventory = inventory_module
        self.race_mgmt = race_module
        self.history = [] # List of results

    def finalize_race(self, race_id, position, prize_money):
        """
        Records the outcome of a race.
        INTEGRATION RULE: Race results update the cash balance in the Inventory.
        """
        race_data = self.race_mgmt.get_race(race_id)
        if not race_data:
            return False, f"Error: Race '{race_id}' was not found in schedule."
        
        result = {
            "race_id": race_id,
            "driver": race_data["driver"],
            "car": race_data["car"],
            "position": position,
            "prize": prize_money
        }
        
        # 1. Update system history
        self.history.append(result)
        
        # 2. Financial Integration: Add prize to inventory
        self.inventory.add_cash(prize_money)
        
        # 3. Mark race as completed
        race_data["status"] = "Completed"
        
        return True, f"Race '{race_id}' finalized. Result: P{position}, Prize: ${prize_money} added to inventory."

    def get_history(self):
        """Return full competitive history."""
        return self.history
