"""
Integration Test Suite - StreetRace Manager (Section 2.2)
~75 unique integration tests covering every Call Graph edge.
Each test validates cross-module data flow, not individual module logic.
"""

import pytest
from integration.code.main import StreetRaceManager


@pytest.fixture
def mgr():
    """Fresh StreetRaceManager for every test."""
    return StreetRaceManager()


# ═══════════════════════════════════════════════════════════
# GROUP A: Registration ↔ Crew Integration (C1 → RG2)
# ═══════════════════════════════════════════════════════════

def test_A01_unregistered_cannot_get_role(mgr):
    """Role assignment must check registration status first."""
    ok, msg = mgr.crew.assign_role("Ghost", "driver")
    assert ok is False and "not in the system" in msg

def test_A02_registered_driver_gets_role(mgr):
    """Registration → Crew: Driver role assignment succeeds after registration."""
    mgr.registration.register_member("Alice", "driver")
    ok, _ = mgr.crew.assign_role("Alice", "driver", skill_level=8)
    assert ok is True
    assert mgr.crew.get_crew_member("Alice")["skill"] == 8

def test_A03_registered_mechanic_gets_role(mgr):
    """Registration → Crew: Mechanic role works the same integration path."""
    mgr.registration.register_member("Bob", "mechanic")
    ok, _ = mgr.crew.assign_role("Bob", "mechanic", skill_level=5)
    assert ok is True

def test_A04_registered_strategist_gets_role(mgr):
    """Registration → Crew: Strategist role completes the trio."""
    mgr.registration.register_member("Charlie", "strategist")
    ok, _ = mgr.crew.assign_role("Charlie", "strategist")
    assert ok is True

def test_A05_invalid_role_rejected_even_if_registered(mgr):
    """Crew rejects invalid roles even after passing the registration gate."""
    mgr.registration.register_member("Dan", "hacker")
    ok, msg = mgr.crew.assign_role("Dan", "hacker")
    assert ok is False and "Invalid role" in msg

def test_A06_duplicate_registration_blocked(mgr):
    """Registration module prevents double-entry before Crew can even see it."""
    mgr.registration.register_member("Alice", "driver")
    ok, msg = mgr.registration.register_member("Alice", "mechanic")
    assert ok is False and "already registered" in msg


# ═══════════════════════════════════════════════════════════
# GROUP B: Crew ↔ Race Integration (R1 → C2, R1 → I4)
# ═══════════════════════════════════════════════════════════

def test_B01_driver_can_race(mgr):
    """Race checks Crew: Valid driver + valid car = race scheduled."""
    mgr.registration.register_member("Alice", "driver")
    mgr.crew.assign_role("Alice", "driver")
    mgr.inventory.add_car("Supra")
    ok, _ = mgr.races.create_race("R1", "Alice", "Supra")
    assert ok is True

def test_B02_mechanic_cannot_race(mgr):
    """Race checks Crew: Mechanic role is blocked from racing."""
    mgr.registration.register_member("Bob", "mechanic")
    mgr.crew.assign_role("Bob", "mechanic")
    mgr.inventory.add_car("Supra")
    ok, msg = mgr.races.create_race("R2", "Bob", "Supra")
    assert ok is False and "not a qualified Driver" in msg

def test_B03_strategist_cannot_race(mgr):
    """Race checks Crew: Strategist role is also blocked from racing."""
    mgr.registration.register_member("Charlie", "strategist")
    mgr.crew.assign_role("Charlie", "strategist")
    mgr.inventory.add_car("Supra")
    ok, _ = mgr.races.create_race("R3", "Charlie", "Supra")
    assert ok is False

def test_B04_unregistered_cannot_race(mgr):
    """Race checks Crew: Nobody in crew = instant rejection."""
    mgr.inventory.add_car("GTR")
    ok, _ = mgr.races.create_race("R4", "Nobody", "GTR")
    assert ok is False

def test_B05_missing_car_blocks_race(mgr):
    """Race checks Inventory: No car in garage = rejected."""
    mgr.registration.register_member("Alice", "driver")
    mgr.crew.assign_role("Alice", "driver")
    ok, msg = mgr.races.create_race("R5", "Alice", "Phantom")
    assert ok is False and "NOT in inventory" in msg

def test_B06_both_driver_and_car_missing(mgr):
    """Race checks both Crew AND Inventory: First failure wins."""
    ok, _ = mgr.races.create_race("R6", "Nobody", "Phantom")
    assert ok is False

def test_B07_same_driver_two_races(mgr):
    """Same driver can be entered in multiple races."""
    mgr.registration.register_member("Alice", "driver")
    mgr.crew.assign_role("Alice", "driver")
    mgr.inventory.add_car("Supra")
    mgr.inventory.add_car("GTR")
    ok1, _ = mgr.races.create_race("R7a", "Alice", "Supra")
    ok2, _ = mgr.races.create_race("R7b", "Alice", "GTR")
    assert ok1 and ok2

def test_B08_same_car_two_races(mgr):
    """Same car can be reused across races (no lock-out)."""
    mgr.registration.register_member("Alice", "driver")
    mgr.crew.assign_role("Alice", "driver")
    mgr.inventory.add_car("Supra")
    mgr.races.create_race("R8a", "Alice", "Supra")
    ok, _ = mgr.races.create_race("R8b", "Alice", "Supra")
    assert ok is True


# ═══════════════════════════════════════════════════════════
# GROUP C: Race ↔ Results ↔ Inventory (RE1 → R2, RE1 → I1)
# ═══════════════════════════════════════════════════════════

def test_C01_finalize_existing_race(mgr):
    """Results looks up Race via get_race: existing race succeeds."""
    mgr.registration.register_member("Alice", "driver")
    mgr.crew.assign_role("Alice", "driver")
    mgr.inventory.add_car("Supra")
    mgr.races.create_race("R10", "Alice", "Supra")
    ok, _ = mgr.results.finalize_race("R10", position=1, prize_money=1000)
    assert ok is True

def test_C02_finalize_nonexistent_race(mgr):
    """Results looks up Race: non-existent race = error."""
    ok, msg = mgr.results.finalize_race("FAKE", position=1, prize_money=1000)
    assert ok is False and "not found" in msg

def test_C03_prize_adds_to_cash(mgr):
    """Results → Inventory: Prize money flows into cash balance."""
    initial = mgr.inventory.cash
    mgr.registration.register_member("A", "driver")
    mgr.crew.assign_role("A", "driver")
    mgr.inventory.add_car("X")
    mgr.races.create_race("R11", "A", "X")
    mgr.results.finalize_race("R11", position=1, prize_money=7500)
    assert mgr.inventory.cash == initial + 7500

def test_C04_zero_prize_no_change(mgr):
    """Results → Inventory: Zero prize doesn't alter balance."""
    initial = mgr.inventory.cash
    mgr.registration.register_member("A", "driver")
    mgr.crew.assign_role("A", "driver")
    mgr.inventory.add_car("X")
    mgr.races.create_race("R12", "A", "X")
    mgr.results.finalize_race("R12", position=10, prize_money=0)
    assert mgr.inventory.cash == initial

def test_C05_multiple_races_accumulate_cash(mgr):
    """Results → Inventory: Cash accumulates across multiple finalized races."""
    initial = mgr.inventory.cash
    mgr.registration.register_member("A", "driver")
    mgr.crew.assign_role("A", "driver")
    mgr.inventory.add_car("X")
    for i in range(5):
        rid = f"BATCH_{i}"
        mgr.races.create_race(rid, "A", "X")
        mgr.results.finalize_race(rid, position=1, prize_money=1000)
    assert mgr.inventory.cash == initial + 5000

def test_C06_race_status_changes_to_completed(mgr):
    """Results updates Race data: status flips to 'Completed'."""
    mgr.registration.register_member("A", "driver")
    mgr.crew.assign_role("A", "driver")
    mgr.inventory.add_car("X")
    mgr.races.create_race("R13", "A", "X")
    mgr.results.finalize_race("R13", position=3, prize_money=500)
    assert mgr.races.get_race("R13")["status"] == "Completed"

def test_C07_result_history_stores_driver_and_car(mgr):
    """Results records the correct driver and car from Race data."""
    mgr.registration.register_member("Alice", "driver")
    mgr.crew.assign_role("Alice", "driver")
    mgr.inventory.add_car("Supra")
    mgr.races.create_race("R14", "Alice", "Supra")
    mgr.results.finalize_race("R14", position=2, prize_money=200)
    entry = mgr.results.get_history()[0]
    assert entry["driver"] == "Alice"
    assert entry["car"] == "Supra"


# ═══════════════════════════════════════════════════════════
# GROUP D: Results ↔ Damage State (RE1 → I7)
# ═══════════════════════════════════════════════════════════

def test_D01_race_with_damage_marks_car(mgr):
    """Results → Inventory: damaged=True sets car as damaged."""
    mgr.registration.register_member("A", "driver")
    mgr.crew.assign_role("A", "driver")
    mgr.inventory.add_car("Z")
    mgr.races.create_race("CRASH1", "A", "Z")
    mgr.results.finalize_race("CRASH1", position=20, prize_money=0, damaged=True)
    assert mgr.inventory.is_damaged("Z") is True

def test_D02_race_without_damage_leaves_car_ok(mgr):
    """Results → Inventory: damaged=False (default) keeps car clean."""
    mgr.registration.register_member("A", "driver")
    mgr.crew.assign_role("A", "driver")
    mgr.inventory.add_car("Z")
    mgr.races.create_race("SAFE1", "A", "Z")
    mgr.results.finalize_race("SAFE1", position=5, prize_money=100)
    assert mgr.inventory.is_damaged("Z") is False

def test_D03_only_raced_car_gets_damaged(mgr):
    """Results → Inventory: Damage targets only the raced car, not others."""
    mgr.registration.register_member("A", "driver")
    mgr.crew.assign_role("A", "driver")
    mgr.inventory.add_car("Car1")
    mgr.inventory.add_car("Car2")
    mgr.races.create_race("DC1", "A", "Car1")
    mgr.results.finalize_race("DC1", position=10, prize_money=0, damaged=True)
    assert mgr.inventory.is_damaged("Car1") is True
    assert mgr.inventory.is_damaged("Car2") is False

def test_D04_damage_persists_across_operations(mgr):
    """Inventory damage state persists until explicitly repaired."""
    mgr.registration.register_member("A", "driver")
    mgr.crew.assign_role("A", "driver")
    mgr.inventory.add_car("Z")
    mgr.races.create_race("P1", "A", "Z")
    mgr.results.finalize_race("P1", position=20, prize_money=0, damaged=True)
    # Do other stuff
    mgr.inventory.add_cash(5000)
    mgr.inventory.add_car("NewCar")
    # Damage still there
    assert mgr.inventory.is_damaged("Z") is True


# ═══════════════════════════════════════════════════════════
# GROUP E: Results ↔ Trophy Room (RE1 → TR1)
# ═══════════════════════════════════════════════════════════

def test_E01_first_place_gets_trophy(mgr):
    """Results → Trophy: Position 1 triggers add_trophy."""
    mgr.registration.register_member("A", "driver")
    mgr.crew.assign_role("A", "driver")
    mgr.inventory.add_car("X")
    mgr.races.create_race("T1", "A", "X")
    mgr.results.finalize_race("T1", position=1, prize_money=100)
    assert mgr.trophy.has_trophy("1st Place Trophy - T1")

def test_E02_second_place_no_trophy(mgr):
    """Results → Trophy: Position 2 does NOT trigger add_trophy."""
    mgr.registration.register_member("A", "driver")
    mgr.crew.assign_role("A", "driver")
    mgr.inventory.add_car("X")
    mgr.races.create_race("T2", "A", "X")
    mgr.results.finalize_race("T2", position=2, prize_money=100)
    assert len(mgr.trophy.list_trophies()) == 0

def test_E03_last_place_no_trophy(mgr):
    """Results → Trophy: Dead last finisher earns nothing."""
    mgr.registration.register_member("A", "driver")
    mgr.crew.assign_role("A", "driver")
    mgr.inventory.add_car("X")
    mgr.races.create_race("T3", "A", "X")
    mgr.results.finalize_race("T3", position=50, prize_money=0)
    assert len(mgr.trophy.list_trophies()) == 0

def test_E04_multiple_wins_multiple_trophies(mgr):
    """Results → Trophy: Each 1st place win earns a distinct trophy."""
    mgr.registration.register_member("A", "driver")
    mgr.crew.assign_role("A", "driver")
    mgr.inventory.add_car("X")
    for i in range(3):
        rid = f"WIN_{i}"
        mgr.races.create_race(rid, "A", "X")
        mgr.results.finalize_race(rid, position=1, prize_money=100)
    assert len(mgr.trophy.list_trophies()) == 3

def test_E05_trophy_title_contains_race_id(mgr):
    """Trophy title must reference the specific race for traceability."""
    mgr.registration.register_member("A", "driver")
    mgr.crew.assign_role("A", "driver")
    mgr.inventory.add_car("X")
    mgr.races.create_race("GRAND_PRIX", "A", "X")
    mgr.results.finalize_race("GRAND_PRIX", position=1, prize_money=100)
    assert "GRAND_PRIX" in mgr.trophy.list_trophies()[0]


# ═══════════════════════════════════════════════════════════
# GROUP F: Missions ↔ Crew Role Check (MS1 → C2)
# ═══════════════════════════════════════════════════════════

def test_F01_delivery_needs_driver(mgr):
    """Mission → Crew: 'Delivery' requires driver role."""
    mgr.registration.register_member("A", "driver")
    mgr.crew.assign_role("A", "driver")
    ok, _ = mgr.missions.assign_mission("Delivery", "A")
    assert ok is True

def test_F02_delivery_rejects_mechanic(mgr):
    """Mission → Crew: Mechanic can't do Delivery (needs driver)."""
    mgr.registration.register_member("B", "mechanic")
    mgr.crew.assign_role("B", "mechanic")
    ok, _ = mgr.missions.assign_mission("Delivery", "B")
    assert ok is False

def test_F03_rescue_needs_strategist(mgr):
    """Mission → Crew: 'Rescue' requires strategist role."""
    mgr.registration.register_member("C", "strategist")
    mgr.crew.assign_role("C", "strategist")
    ok, _ = mgr.missions.assign_mission("Rescue", "C")
    assert ok is True

def test_F04_rescue_rejects_driver(mgr):
    """Mission → Crew: Driver can't do Rescue (needs strategist)."""
    mgr.registration.register_member("A", "driver")
    mgr.crew.assign_role("A", "driver")
    ok, msg = mgr.missions.assign_mission("Rescue", "A")
    assert ok is False and "strategist" in msg

def test_F05_sabotage_needs_mechanic(mgr):
    """Mission → Crew: 'Sabotage' requires mechanic role."""
    mgr.registration.register_member("B", "mechanic")
    mgr.crew.assign_role("B", "mechanic")
    ok, _ = mgr.missions.assign_mission("Sabotage", "B")
    assert ok is True

def test_F06_sabotage_rejects_strategist(mgr):
    """Mission → Crew: Strategist can't do Sabotage (needs mechanic)."""
    mgr.registration.register_member("C", "strategist")
    mgr.crew.assign_role("C", "strategist")
    ok, _ = mgr.missions.assign_mission("Sabotage", "C")
    assert ok is False

def test_F07_unknown_mission_type(mgr):
    """Mission rejects unknown mission types before even checking Crew."""
    mgr.registration.register_member("A", "driver")
    mgr.crew.assign_role("A", "driver")
    ok, msg = mgr.missions.assign_mission("Heist", "A")
    assert ok is False and "Unknown" in msg

def test_F08_mission_with_unregistered_member(mgr):
    """Mission → Crew: Unregistered member has no role, so mission fails."""
    ok, _ = mgr.missions.assign_mission("Delivery", "Ghost")
    assert ok is False


# ═══════════════════════════════════════════════════════════
# GROUP G: Missions ↔ Inventory Damage (MS1 → I8, I7)
# ═══════════════════════════════════════════════════════════

def test_G01_repair_damaged_car_succeeds(mgr):
    """Mission → Inventory: Repair mission fixes a damaged car."""
    mgr.registration.register_member("B", "mechanic")
    mgr.crew.assign_role("B", "mechanic")
    mgr.inventory.add_car("Z")
    mgr.inventory.set_damage("Z", True)
    ok, _ = mgr.missions.assign_mission("Repair", "B", car_name="Z")
    assert ok is True
    assert mgr.inventory.is_damaged("Z") is False

def test_G02_repair_undamaged_car_fails(mgr):
    """Mission → Inventory: Can't repair a car that isn't damaged."""
    mgr.registration.register_member("B", "mechanic")
    mgr.crew.assign_role("B", "mechanic")
    mgr.inventory.add_car("Z")
    ok, msg = mgr.missions.assign_mission("Repair", "B", car_name="Z")
    assert ok is False and "not damaged" in msg

def test_G03_repair_without_car_name_fails(mgr):
    """Mission → Inventory: Repair requires specifying which car."""
    mgr.registration.register_member("B", "mechanic")
    mgr.crew.assign_role("B", "mechanic")
    ok, msg = mgr.missions.assign_mission("Repair", "B")
    assert ok is False and "Must specify" in msg

def test_G04_driver_cannot_repair(mgr):
    """Mission → Crew + Inventory: Drivers lack mechanic clearance."""
    mgr.registration.register_member("A", "driver")
    mgr.crew.assign_role("A", "driver")
    mgr.inventory.add_car("Z")
    mgr.inventory.set_damage("Z", True)
    ok, msg = mgr.missions.assign_mission("Repair", "A", car_name="Z")
    assert ok is False and "mechanic" in msg

def test_G05_repair_one_of_two_damaged_cars(mgr):
    """Mission → Inventory: Only the specified car gets repaired."""
    mgr.registration.register_member("B", "mechanic")
    mgr.crew.assign_role("B", "mechanic")
    mgr.inventory.add_car("Car1")
    mgr.inventory.add_car("Car2")
    mgr.inventory.set_damage("Car1", True)
    mgr.inventory.set_damage("Car2", True)
    mgr.missions.assign_mission("Repair", "B", car_name="Car1")
    assert mgr.inventory.is_damaged("Car1") is False
    assert mgr.inventory.is_damaged("Car2") is True


# ═══════════════════════════════════════════════════════════
# GROUP H: Tuning ↔ Crew + Inventory (T1 → C2, I6, I2, I5)
# ═══════════════════════════════════════════════════════════

def test_H01_tuning_happy_path(mgr):
    """Tuning → Crew + Inventory: Mechanic + parts + cash = success."""
    mgr.registration.register_member("B", "mechanic")
    mgr.crew.assign_role("B", "mechanic")
    mgr.inventory.add_car("GTR")
    mgr.inventory.add_parts("Engine Module", 2)
    initial_cash = mgr.inventory.cash
    ok, _ = mgr.tuning.upgrade_car("GTR", "B", "speed")
    assert ok is True
    assert mgr.inventory.cash == initial_cash - 500
    assert mgr.inventory.parts["Engine Module"] == 1

def test_H02_driver_cannot_tune(mgr):
    """Tuning → Crew: Driver role is rejected."""
    mgr.registration.register_member("A", "driver")
    mgr.crew.assign_role("A", "driver")
    mgr.inventory.add_car("GTR")
    mgr.inventory.add_parts("Engine Module", 1)
    ok, msg = mgr.tuning.upgrade_car("GTR", "A", "speed")
    assert ok is False and "not a Mechanic" in msg

def test_H03_tuning_no_parts(mgr):
    """Tuning → Inventory: No parts = blocked before cash deduction."""
    mgr.registration.register_member("B", "mechanic")
    mgr.crew.assign_role("B", "mechanic")
    initial_cash = mgr.inventory.cash
    ok, msg = mgr.tuning.upgrade_car("GTR", "B", "speed")
    assert ok is False and "Not enough" in msg
    assert mgr.inventory.cash == initial_cash  # Cash untouched

def test_H04_tuning_no_cash_rollback(mgr):
    """Tuning → Inventory: Insufficient cash rolls back consumed parts."""
    mgr.registration.register_member("B", "mechanic")
    mgr.crew.assign_role("B", "mechanic")
    mgr.inventory.add_parts("Engine Module", 1)
    mgr.inventory.cash = 100  # Not enough for $500
    ok, _ = mgr.tuning.upgrade_car("GTR", "B", "speed")
    assert ok is False
    assert mgr.inventory.parts["Engine Module"] == 1  # Rolled back

def test_H05_speed_upgrade_adds_10(mgr):
    """Tuning records: Speed stat increases by exactly 10."""
    mgr.registration.register_member("B", "mechanic")
    mgr.crew.assign_role("B", "mechanic")
    mgr.inventory.add_parts("Engine Module", 1)
    mgr.tuning.upgrade_car("GTR", "B", "speed")
    assert mgr.tuning.get_car_stats("GTR")["speed"] == 10

def test_H06_handling_upgrade_adds_10(mgr):
    """Tuning records: Handling stat increases by exactly 10."""
    mgr.registration.register_member("B", "mechanic")
    mgr.crew.assign_role("B", "mechanic")
    mgr.inventory.add_parts("Engine Module", 1)
    mgr.tuning.upgrade_car("GTR", "B", "handling")
    assert mgr.tuning.get_car_stats("GTR")["handling"] == 10

def test_H07_multiple_upgrades_accumulate(mgr):
    """Tuning records: Multiple upgrades stack correctly."""
    mgr.registration.register_member("B", "mechanic")
    mgr.crew.assign_role("B", "mechanic")
    mgr.inventory.add_parts("Engine Module", 3)
    mgr.tuning.upgrade_car("GTR", "B", "speed")
    mgr.tuning.upgrade_car("GTR", "B", "speed")
    mgr.tuning.upgrade_car("GTR", "B", "handling")
    stats = mgr.tuning.get_car_stats("GTR")
    assert stats["speed"] == 20
    assert stats["handling"] == 10

def test_H08_untuned_car_has_zero_stats(mgr):
    """Tuning records: Cars with no upgrades return default zero stats."""
    assert mgr.tuning.get_car_stats("NeverTuned") == {"speed": 0, "handling": 0}


# ═══════════════════════════════════════════════════════════
# GROUP I: Sponsors ↔ Inventory (S2 → I1)
# ═══════════════════════════════════════════════════════════

def test_I01_sponsor_bonus_credits_cash(mgr):
    """Sponsor → Inventory: Triggered bonus adds cash."""
    initial = mgr.inventory.cash
    mgr.sponsors.sign_sponsor("SP1", 5000)
    ok, _ = mgr.sponsors.trigger_win_bonus("SP1")
    assert ok is True
    assert mgr.inventory.cash == initial + 5000

def test_I02_no_sponsor_no_bonus(mgr):
    """Sponsor → Inventory: No deal = no bonus triggered."""
    initial = mgr.inventory.cash
    ok, _ = mgr.sponsors.trigger_win_bonus("NOSPONSOR")
    assert ok is False
    assert mgr.inventory.cash == initial

def test_I03_different_sponsors_different_races(mgr):
    """Sponsor → Inventory: Each race has its own sponsor deal."""
    mgr.sponsors.sign_sponsor("RACE_A", 1000)
    mgr.sponsors.sign_sponsor("RACE_B", 3000)
    initial = mgr.inventory.cash
    mgr.sponsors.trigger_win_bonus("RACE_A")
    mgr.sponsors.trigger_win_bonus("RACE_B")
    assert mgr.inventory.cash == initial + 4000

def test_I04_sponsor_overwrites_previous_deal(mgr):
    """Sponsor: Signing a new deal for same race replaces the old one."""
    mgr.sponsors.sign_sponsor("RACE_X", 1000)
    mgr.sponsors.sign_sponsor("RACE_X", 9999)
    initial = mgr.inventory.cash
    mgr.sponsors.trigger_win_bonus("RACE_X")
    assert mgr.inventory.cash == initial + 9999


# ═══════════════════════════════════════════════════════════
# GROUP J: Full Workflow Integration (Multi-module chains)
# ═══════════════════════════════════════════════════════════

def test_J01_full_race_win_workflow(mgr):
    """Register → Role → Car → Race → Win → Cash + Trophy."""
    initial = mgr.inventory.cash
    mgr.registration.register_member("Ace", "driver")
    mgr.crew.assign_role("Ace", "driver")
    mgr.inventory.add_car("Charger")
    mgr.races.create_race("FINAL", "Ace", "Charger")
    mgr.results.finalize_race("FINAL", position=1, prize_money=10000)
    assert mgr.inventory.cash == initial + 10000
    assert mgr.trophy.has_trophy("1st Place Trophy - FINAL")

def test_J02_full_crash_repair_workflow(mgr):
    """Register → Race → Crash → Hire Mechanic → Repair mission."""
    mgr.registration.register_member("A", "driver")
    mgr.crew.assign_role("A", "driver")
    mgr.inventory.add_car("Supra")
    mgr.races.create_race("CRASH", "A", "Supra")
    mgr.results.finalize_race("CRASH", position=20, prize_money=0, damaged=True)
    assert mgr.inventory.is_damaged("Supra") is True
    # Recruit mechanic and repair
    mgr.registration.register_member("B", "mechanic")
    mgr.crew.assign_role("B", "mechanic")
    mgr.missions.assign_mission("Repair", "B", car_name="Supra")
    assert mgr.inventory.is_damaged("Supra") is False

def test_J03_win_with_sponsor_bonus(mgr):
    """Register → Race → Win → Prize + Sponsor Bonus both land in Inventory."""
    initial = mgr.inventory.cash
    mgr.registration.register_member("A", "driver")
    mgr.crew.assign_role("A", "driver")
    mgr.inventory.add_car("X")
    mgr.sponsors.sign_sponsor("MEGA", 5000)
    mgr.races.create_race("MEGA", "A", "X")
    mgr.results.finalize_race("MEGA", position=1, prize_money=3000)
    mgr.sponsors.trigger_win_bonus("MEGA")
    assert mgr.inventory.cash == initial + 8000

def test_J04_tune_then_race(mgr):
    """Mechanic tunes car, then driver races it. Cross-role integration."""
    mgr.registration.register_member("A", "driver")
    mgr.crew.assign_role("A", "driver")
    mgr.registration.register_member("B", "mechanic")
    mgr.crew.assign_role("B", "mechanic")
    mgr.inventory.add_car("GTR")
    mgr.inventory.add_parts("Engine Module", 1)
    mgr.tuning.upgrade_car("GTR", "B", "speed")
    assert mgr.tuning.get_car_stats("GTR")["speed"] == 10
    ok, _ = mgr.races.create_race("TUNED", "A", "GTR")
    assert ok is True

def test_J05_cash_depletion_and_replenishment(mgr):
    """Tuning depletes cash, winning replenishes it."""
    mgr.registration.register_member("A", "driver")
    mgr.crew.assign_role("A", "driver")
    mgr.registration.register_member("B", "mechanic")
    mgr.crew.assign_role("B", "mechanic")
    mgr.inventory.add_car("GTR")
    mgr.inventory.add_parts("Engine Module", 1)
    
    before_tune = mgr.inventory.cash
    mgr.tuning.upgrade_car("GTR", "B", "speed")
    assert mgr.inventory.cash == before_tune - 500
    
    mgr.races.create_race("EARN", "A", "GTR")
    mgr.results.finalize_race("EARN", position=1, prize_money=2000)
    assert mgr.inventory.cash == before_tune - 500 + 2000

def test_J06_full_team_parallel_missions(mgr):
    """Three crew members each do their specialty mission simultaneously."""
    mgr.registration.register_member("A", "driver")
    mgr.registration.register_member("B", "mechanic")
    mgr.registration.register_member("C", "strategist")
    mgr.crew.assign_role("A", "driver")
    mgr.crew.assign_role("B", "mechanic")
    mgr.crew.assign_role("C", "strategist")
    ok1, _ = mgr.missions.assign_mission("Delivery", "A")
    ok2, _ = mgr.missions.assign_mission("Sabotage", "B")
    ok3, _ = mgr.missions.assign_mission("Rescue", "C")
    assert ok1 and ok2 and ok3
    assert len(mgr.missions.list_missions()) == 3

def test_J07_crash_repair_then_race_again(mgr):
    """Full lifecycle: Race → Crash → Repair → Race again with same car."""
    mgr.registration.register_member("A", "driver")
    mgr.crew.assign_role("A", "driver")
    mgr.registration.register_member("B", "mechanic")
    mgr.crew.assign_role("B", "mechanic")
    mgr.inventory.add_car("Supra")
    
    # Race 1: crash
    mgr.races.create_race("R1", "A", "Supra")
    mgr.results.finalize_race("R1", position=20, prize_money=0, damaged=True)
    assert mgr.inventory.is_damaged("Supra") is True
    
    # Repair
    mgr.missions.assign_mission("Repair", "B", car_name="Supra")
    assert mgr.inventory.is_damaged("Supra") is False
    
    # Race 2: success
    mgr.races.create_race("R2", "A", "Supra")
    ok, _ = mgr.results.finalize_race("R2", position=1, prize_money=5000)
    assert ok is True

def test_J08_run_race_sequence_full_flow(mgr):
    """Main controller orchestrates Race → Results → Sponsors in one call."""
    initial = mgr.inventory.cash
    mgr.registration.register_member("A", "driver")
    mgr.crew.assign_role("A", "driver")
    mgr.inventory.add_car("X")
    mgr.sponsors.sign_sponsor("AUTO", 1000)
    result = mgr.run_race_sequence("AUTO", "A", "X", position=1, prize=2000)
    assert mgr.inventory.cash == initial + 3000
    assert "Trophy" in result

def test_J09_controller_tuning(mgr):
    """Main controller's perform_tuning delegates to TuningModule correctly."""
    mgr.registration.register_member("B", "mechanic")
    mgr.crew.assign_role("B", "mechanic")
    mgr.inventory.add_parts("Engine Module", 1)
    ok, _ = mgr.perform_tuning("GTR", "B", "speed")
    assert ok is True

def test_J10_controller_mission(mgr):
    """Main controller's start_mission delegates to MissionModule correctly."""
    mgr.registration.register_member("C", "strategist")
    mgr.crew.assign_role("C", "strategist")
    ok, _ = mgr.start_mission("Rescue", "C")
    assert ok is True
