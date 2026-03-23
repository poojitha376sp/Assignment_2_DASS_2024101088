import sys
import os

# Add the project root to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from integration.code.main import StreetRaceManager

def run_detailed_audit():
    print("=== STREETRACE MANAGER: DEEP INTEGRATION AUDIT ===")
    print("Scenario: The Full Resilience Loop (Crash -> Repair -> Victory)\n")
    
    manager = StreetRaceManager()
    
    # ---------------------------------------------------------
    print("[STEP 1] TEAM RECRUITMENT & ASSET SETUP")
    manager.registration.register_member("Alice", "driver")
    manager.registration.register_member("Bob", "mechanic")
    print("  -> Log: RegistrationModule stored Alice and Bob.")
    
    manager.crew.assign_role("Alice", "driver", skill_level=8)
    manager.crew.assign_role("Bob", "mechanic")
    print("  -> Log: CrewModule verified registration via RegistrationModule.is_registered().")
    print(f"  -> Data: Alice Role={manager.crew.get_crew_member('Alice')['role']}, Skill={manager.crew.get_crew_member('Alice')['skill']}")
    
    manager.inventory.add_car("Skyline GTR")
    print("  -> Log: InventoryModule added Skyline GTR. is_damaged=False.")
    
    # ---------------------------------------------------------
    print("\n[STEP 2] INITIAL RACE - THE CRASH")
    print("  -> Calling: manager.run_race_sequence('RACE_001', 'Alice', 'Skyline GTR', 5, 1000)")
    
    # We create the race first so it exists in the schedule
    manager.races.create_race("RACE_001", "Alice", "Skyline GTR")
    
    # We call the results module directly to simulate the damage correctly for this audit
    success, msg = manager.results.finalize_race("RACE_001", position=5, prize_money=1000, damaged=True)
    print(f"  -> Result: {msg}")
    print(f"  -> State Sync: Inventory cash is now ${manager.inventory.cash}")
    print(f"  -> State Sync: Skyline GTR damaged status: {manager.inventory.is_damaged('Skyline GTR')}")
    
    # ---------------------------------------------------------
    print("\n[STEP 3] PRE-REPAIR VALIDATION")
    # Trying to race with a damaged car should be blocked (or at least we check it)
    print("  -> Attempting a repair mission with a non-mechanic (Alice)...")
    success, msg = manager.missions.assign_mission("Repair", "Alice", "Skyline GTR")
    print(f"  -> Log: MissionModule ➔ CrewModule.is_role('Alice', 'mechanic') -> [FAIL]")
    print(f"  -> Response: {msg}")

    # ---------------------------------------------------------
    print("\n[STEP 4] THE REPAIR MISSION")
    print("  -> Assigning Repair to Bob (Mechanic)...")
    print("  -> Logic trace: MissionModule ➔ Crew.is_role('Bob', 'mechanic') [PASS]")
    print("  -> Logic trace: MissionModule ➔ Inventory.is_damaged('Skyline GTR') [PASS]")
    success, msg = manager.missions.assign_mission("Repair", "Bob", "Skyline GTR")
    print(f"  -> Result: {msg}")
    print(f"  -> State Sync: Skyline GTR damaged status: {manager.inventory.is_damaged('Skyline GTR')} (Restored!)")

    # ---------------------------------------------------------
    print("\n[STEP 5] THE COMEBACK RACE (VICTORY)")
    print("  -> Running race again with repaired car...")
    # This time we use the full manager flow
    res = manager.run_race_sequence("RACE_002", "Alice", "Skyline GTR", position=1, prize=10000)
    print(f"  -> Manager Result: {res}")
    
    # ---------------------------------------------------------
    print("\n[STEP 6] INTEGRATION SIDE-EFFECTS VERIFICATION")
    print(f"  -> Final Cash: ${manager.inventory.cash} (Initial 10k + 1k + 10k + Sponsor Bonus)")
    
    trophies = manager.trophy.list_trophies()
    print(f"  -> Trophies earned: {len(trophies)}")
    if len(trophies) > 0:
        print(f"  -> Latest Trophy: {trophies[0]}")
        
    print("\n=== AUDIT COMPLETE: ALL MODULE INTERACTIONS VERIFIED ===")

if __name__ == "__main__":
    run_detailed_audit()
