"""
Results Management Module
Processes race outcomes and distributes prize money.
"""

class ResultsModule:
    def __init__(self, inventory_module, race_module, trophy_module=None):
        self.inventory = inventory_module
        self.race_mgmt = race_module
        self.trophy_room = trophy_module
        self.history = [] # List of results

    def finalize_race(self, race_id, position, prize_money, damaged=False):
        """
        Records the outcome of a race.
        INTEGRATION RULE: 
        1. Race results update the cash balance in the Inventory.
        2. 1st Place finishes unlock a Trophy in the Trophy Room.
        3. If 'damaged' is True, the Inventory marks the car as damaged.
        """
        race_data = self.race_mgmt.get_race(race_id)
        if not race_data:
            return False, f"Error: Race '{race_id}' was not found in schedule."
        
        car_name = race_data["car"]
        result = {
            "race_id": race_id,
            "driver": race_data["driver"],
            "car": car_name,
            "position": position,
            "prize": prize_money
        }
        
        # 1. Update system history
        self.history.append(result)
        
        # 2. Financial Integration: Add prize to inventory
        self.inventory.add_cash(prize_money)

        # 3. Damage Integration
        if damaged:
            self.inventory.set_damage(car_name, True)
        
        # 4. Trophy Integration: Award trophy for 1st place
        trophy_msg = ""
        if position == 1 and self.trophy_room:
            title = f"1st Place Trophy - {race_id}"
            _, trophy_msg = self.trophy_room.add_trophy(title)
        
        # 5. Mark race as completed
        race_data["status"] = "Completed"
        
        base_msg = f"Race '{race_id}' finalized. Result: P{position}, Prize: ${prize_money} added to inventory."
        if damaged: base_msg += f" WARNING: {car_name} was DAMAGED."
        
        return True, f"{base_msg} | {trophy_msg if trophy_msg else 'No Trophy'}"

    def get_history(self):
        """Return full competitive history."""
        return self.history
