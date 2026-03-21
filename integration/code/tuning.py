"""
Vehicle Tuning Module
Upgrades Car performance (Speed, Handling) using Cash and Spare Parts.
Requires a Mechanic from CrewManagement.
"""

class TuningModule:
    def __init__(self, crew, inventory):
        self.crew = crew
        self.inventory = inventory
        self.modifications = {} # {car_name: {"speed": x, "handling": y}}

    def upgrade_car(self, car_name, mechanic_name, upgrade_type):
        """
        Enhances car performance.
        INTEGRATION RULES:
        1. Must have a "Mechanic" registered in Crew.
        2. Consumes 500 Cash and 1 Spare Part from Inventory.
        """
        # 1. Mechanic Check
        if not self.crew.is_role(mechanic_name, "mechanic"):
            return False, f"Error: '{mechanic_name}' is not a Mechanic. Cannot tune car."
        
        # 2. Part Check
        success, msg = self.inventory.use_parts("Engine Module", 1)
        if not success:
            return False, msg
            
        # 3. Cash Check
        success, msg = self.inventory.deduct_cash(500)
        if not success:
            # Rollback part usage (simple logic for now)
            self.inventory.add_parts("Engine Module", 1)
            return False, msg
            
        # 4. Perform Upgrade
        if car_name not in self.modifications:
            self.modifications[car_name] = {"speed": 0, "handling": 0}
            
        if upgrade_type == "speed":
            self.modifications[car_name]["speed"] += 10
        elif upgrade_type == "handling":
            self.modifications[car_name]["handling"] += 10
            
        return True, f"'{car_name}' tuned by {mechanic_name}! {upgrade_type.capitalize()} improved."

    def get_car_stats(self, car_name):
        """Get the tuning improvements for a car."""
        return self.modifications.get(car_name, {"speed": 0, "handling": 0})
