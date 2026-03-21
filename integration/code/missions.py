"""
Mission Planning Module
Assigns special mission tasks based on team skills and role availability.
"""

class MissionModule:
    def __init__(self, crew_module, inventory_module=None):
        self.crew = crew_module
        self.inventory = inventory_module
        self.missions = {
            "Delivery": "driver",
            "Rescue": "strategist",
            "Sabotage": "mechanic",
            "Repair": "mechanic"
        }
        self.active_assignments = []

    def assign_mission(self, mission_type, member_name, car_name=None):
        """
        Assigns a mission to a crew member.
        INTEGRATION RULE: 
        1. Missions cannot start if required roles are unavailable.
        2. 'Repair' mission requires a Mechanic AND the car must be damaged.
        """
        if mission_type not in self.missions:
            return False, f"Unknown mission type: '{mission_type}'."
        
        required_role = self.missions[mission_type]
        
        # 1. Role Check
        if not self.crew.is_role(member_name, required_role):
            return False, f"Access Denied: Mission '{mission_type}' requires a '{required_role}'. {member_name} is not qualified."
        
        # 2. Damage Integrity Check (Specific for Repair)
        if mission_type == "Repair":
            if not car_name:
                return False, "Error: Must specify a car name for Repair missions."
            if not self.inventory.is_damaged(car_name):
                return False, f"Optimization Error: '{car_name}' is not damaged. No repair needed."
            
            # If successful, repair the car in inventory
            self.inventory.set_damage(car_name, False)

        assignment = {
            "mission": mission_type,
            "assigned_to": member_name,
            "status": "In Progress"
        }
        self.active_assignments.append(assignment)
        return True, f"Mission '{mission_type}' successfully assigned to {member_name}."

    def list_missions(self):
        """Show active missions."""
        return self.active_assignments
