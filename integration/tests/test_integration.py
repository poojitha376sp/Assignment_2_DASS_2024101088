"""
Integration Test Suite - StreetRace Manager
Validates the interaction and data flow between 8 interdependent modules.
"""

import pytest
from integration.code.main import StreetRaceManager

@pytest.fixture
def manager():
    """Initializes a clean StreetRaceManager for every test."""
    return StreetRaceManager()

def test_integration_01_reg_to_crew_guard(manager):
    """Scenario: Cannot assign a role to an unregistered member."""
    # Try to assign role to 'Alice' without registering her
    success, msg = manager.crew.assign_role("Alice", "driver", skill_level=5)
    assert success is False
    assert "not in the system" in msg

def test_integration_02_valid_race_flow(manager):
    """Scenario: Register -> Assign Driver -> Add Car -> Create Race (Success)"""
    # 1. Register Member
    manager.registration.register_member("Alice", "driver")
    # 2. Assign Role (Integration: Registration -> Crew)
    manager.crew.assign_role("Alice", "driver", skill_level=10)
    # 3. Add Vehicle
    manager.inventory.add_car("Supra")
    
    # 4. Create Race (Integration: Crew + Inventory -> Race)
    success, msg = manager.races.create_race("RACE_001", "Alice", "Supra")
    assert success is True
    assert "scheduled" in msg

def test_integration_03_invalid_race_role(manager):
    """Scenario: Cannot race with a non-driver (e.g. a Mechanic)."""
    manager.registration.register_member("Bob", "mechanic")
    manager.crew.assign_role("Bob", "mechanic", skill_level=10)
    manager.inventory.add_car("Supra")
    
    # Attempt to race with Bob (Mechanic)
    success, msg = manager.races.create_race("RACE_002", "Bob", "Supra")
    assert success is False
    assert "not a qualified Driver" in msg

def test_integration_04_financial_flow_win(manager):
    """Scenario: Winning a race updates the Inventory cash balance."""
    initial_cash = manager.inventory.cash # Default 10000
    
    # Setup: Alice in Supra
    manager.registration.register_member("Alice", "driver")
    manager.crew.assign_role("Alice", "driver")
    manager.inventory.add_car("Supra")
    manager.races.create_race("RACE_003", "Alice", "Supra")
    
    # 1. Finalize Race (Integration: Race -> Results -> Inventory)
    manager.results.finalize_race("RACE_003", position=1, prize_money=5000)
    
    # 2. Verify Cash Update
    assert manager.inventory.cash == initial_cash + 5000

def test_integration_05_mission_role_lock(manager):
    """Scenario: Mission requiring a Strategist fails if only a Driver is available."""
    manager.registration.register_member("Alice", "driver")
    manager.crew.assign_role("Alice", "driver")
    
    # Try to start a 'Rescue' mission (Requires Strategist)
    success, msg = manager.missions.assign_mission("Rescue", "Alice")
    assert success is False
    assert "requires a 'strategist'" in msg

def test_integration_06_tuning_3way_integration(manager):
    """Scenario: Tuning requires Mechanic, Parts, and Cash."""
    # Setup
    manager.registration.register_member("Mike", "mechanic")
    manager.crew.assign_role("Mike", "mechanic")
    manager.inventory.add_car("GTR")
    manager.inventory.add_parts("Engine Module", 5)
    initial_cash = manager.inventory.cash
    
    # 1. Perform Tuning (Integration: Crew + Inventory + Tuning)
    success, msg = manager.tuning.upgrade_car("GTR", "Mike", "speed")
    
    assert success is True
    assert manager.inventory.cash == initial_cash - 500
    assert manager.inventory.parts["Engine Module"] == 4
    assert manager.tuning.get_car_stats("GTR")["speed"] == 10

def test_integration_07_sponsorship_bonus_flow(manager):
    """Scenario: Winner receives both prize AND sponsor bonus."""
    initial_cash = manager.inventory.cash
    
    # Setup
    manager.registration.register_member("Sam", "driver")
    manager.crew.assign_role("Sam", "driver")
    manager.inventory.add_car("RX7")
    manager.races.create_race("RACE_ULTRA", "Sam", "RX7")
    
    # Sign Sponsor (Integration: Inventory + Sponsor)
    manager.sponsors.sign_sponsor("RACE_ULTRA", bonus=2000)
    
    # Finalize Win (Integration: 5-Module Flow)
    manager.results.finalize_race("RACE_ULTRA", position=1, prize_money=3000)
    manager.sponsors.trigger_win_bonus("RACE_ULTRA")
    
    # Total Cash: 10000 + 3000 + 2000 = 15000
    assert manager.inventory.cash == initial_cash + 3000 + 2000
