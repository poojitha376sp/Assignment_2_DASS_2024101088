"""
Registration Module
Responsible for registering new crew members into the system.
"""

class RegistrationModule:
    def __init__(self):
        self.members = {} # {name: role}

    def register_member(self, name, role):
        """Registers a new crew member with a basic role."""
        if not name or not role:
            return False, "Name and role are required."
        if name in self.members:
            return False, f"Member '{name}' is already registered."
        
        self.members[name] = role
        return True, f"Member '{name}' registered as '{role}'."

    def is_registered(self, name):
        """Check if a member exists in the registry."""
        return name in self.members

    def get_role(self, name):
        """Retrieve the role of a registered member."""
        return self.members.get(name)

    def list_members(self):
        """Return all registered members."""
        return self.members
