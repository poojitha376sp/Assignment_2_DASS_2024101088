"""
Inventory Management Module
Manages Cars, Spare Parts, Tools, and the system's global Cash Balance.
"""

class InventoryModule:
    def __init__(self, initial_cash=10000):
        self.cash = initial_cash
        self.cars = [] # List of Car IDs or names
        self.parts = {} # {part_name: count}
        self.tools = [] # List of tools

    def add_cash(self, amount):
        """Adds money to the balance."""
        self.cash += amount
        return self.cash

    def deduct_cash(self, amount):
        """Deducts money if sufficient balance exists."""
        if self.cash < amount:
            return False, f"Insufficient funds: ${self.cash} available."
        self.cash -= amount
        return True, self.cash

    def add_car(self, car_name):
        """Add a car to the inventory."""
        self.cars.append(car_name)
        return True, f"'{car_name}' added to garage."

    def has_car(self, car_name):
        """Check for vehicle availability."""
        return car_name in self.cars

    def add_parts(self, part_name, count=1):
        """Add spare parts to stock."""
        self.parts[part_name] = self.parts.get(part_name, 0) + count
        return True

    def use_parts(self, part_name, count=1):
        """Consume spare parts."""
        if self.parts.get(part_name, 0) < count:
            return False, f"Not enough {part_name} in stock."
        self.parts[part_name] -= count
        return True, f"Used {count} {part_name}."

    def get_status(self):
        """Diagnostic of all current assets."""
        return {
            "cash": self.cash,
            "cars": self.cars,
            "parts": self.parts,
            "tools": self.tools
        }
