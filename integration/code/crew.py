"""
Crew Management Module
Manages specifically assigned roles (Driver, Mechanic, Strategist)
and tracks skill levels for each crew member.
"""

class CrewModule:
    def __init__(self, registration_module):
        self.reg = registration_module
        self.crew_data = {} # {name: {"role": role, "skill": level}}

    def assign_role(self, name, role, skill_level=1):
        """
        Assigns a role and skill level to a registered member.
        INTEGRATION RULE: Must be registered in RegistrationModule first.
        """
        if not self.reg.is_registered(name):
            return False, f"Error: '{name}' is not in the system. Register first."
        
        # Valid roles as per assignment
        valid_roles = ["driver", "mechanic", "strategist"]
        if role.lower() not in valid_roles:
            return False, f"Invalid role. Must be one of: {valid_roles}"
        
        self.crew_data[name] = {
            "role": role.lower(),
            "skill": skill_level
        }
        return True, f"Assigned role '{role}' with skill level {skill_level} to {name}."

    def get_crew_member(self, name):
        """Retrieve core crew data."""
        return self.crew_data.get(name)

    def is_role(self, name, role):
        """Check if a specific member carries a specific role."""
        data = self.crew_data.get(name)
        if not data:
            return False
        return data["role"] == role.lower()

    def get_skill(self, name):
        """Get the skill level for a specific member."""
        data = self.crew_data.get(name)
        return data["skill"] if data else 0

    def list_crew(self):
        """List all active crew assignments."""
        return self.crew_data
