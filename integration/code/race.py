"""
Race Management Module
Responsible for organizing races by pairing drivers with vehicles.
"""

class RaceModule:
    def __init__(self, crew_module, inventory_module):
        self.crew = crew_module
        self.inventory = inventory_module
        self.active_races = {} # {race_id: {"driver": name, "car": car}}

    def create_race(self, race_id, driver_name, car_name):
        """
        Creates a new race event if resources are available.
        INTEGRATION RULES:
        1. Only "Driver" role members can participate.
        2. Car must exist in Inventory.
        """
        # 1. Role Integrity Check
        if not self.crew.is_role(driver_name, "driver"):
            return False, f"Access Denied: '{driver_name}' is not a qualified Driver."
        
        # 2. Resource Integrity Check
        if not self.inventory.has_car(car_name):
            return False, f"Resource Missing: '{car_name}' NOT in inventory."

        self.active_races[race_id] = {
            "driver": driver_name,
            "car": car_name,
            "status": "Scheduled"
        }
        return True, f"Race '{race_id}' scheduled with {driver_name} in the {car_name}."

    def get_race(self, race_id):
        """Retrieve race details."""
        return self.active_races.get(race_id)

    def list_races(self):
        """Show all scheduled and completed races."""
        return self.active_races
