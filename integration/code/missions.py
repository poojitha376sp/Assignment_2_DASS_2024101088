"""
Mission Planning Module
Assigns special mission tasks based on team skills and role availability.
"""

class MissionModule:
    def __init__(self, crew_module):
        self.crew = crew_module
        self.missions = {
            "Delivery": "driver",
            "Rescue": "strategist",
            "Sabotage": "mechanic"
        }
        self.active_assignments = []

    def assign_mission(self, mission_type, member_name):
        """
        Assigns a mission to a crew member.
        INTEGRATION RULE: Missions cannot start if required roles are unavailable.
        """
        if mission_type not in self.missions:
            return False, f"Unknown mission type: '{mission_type}'."
        
        required_role = self.missions[mission_type]
        
        # Role check against CrewModule
        if not self.crew.is_role(member_name, required_role):
            return False, f"Access Denied: Mission '{mission_type}' requires a '{required_role}'. {member_name} is not qualified."
        
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
