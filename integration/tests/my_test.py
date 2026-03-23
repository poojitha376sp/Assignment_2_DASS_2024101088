from integration.code.main import StreetRaceManager
manager = StreetRaceManager()

manager.registration.register_member("Alice", "driver")
manager.crew.assign_role("Alice", "driver")
manager.registration.register_member("Bob", "mechanic")
manager.crew.assign_role("Bob", "mechanic")
manager.inventory.add_car("GTR")

# 1. Run a race that causes damage
manager.races.create_race("R_CRASH", "Alice", "GTR")
print("--- TEST: Racing and Crashing ---")
_, msg = manager.results.finalize_race("R_CRASH", position=5, prize_money=0, damaged=True)
print(msg)

# 2. Check if Inventory knows it is damaged
print(f"\nIs GTR damaged in Inventory? {manager.inventory.is_damaged('GTR')}")

# 3. Run Repair mission
print("\n--- TEST: Repair Mission ---")
_, msg = manager.missions.assign_mission("Repair", "Bob", "GTR")
print(msg)
print(f"Is GTR damaged now? {manager.inventory.is_damaged('GTR')}")
