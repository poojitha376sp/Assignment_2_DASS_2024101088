# StreetRace Manager - Integration Testing Report

This report documents the design, implementation, and integration testing of the StreetRace Manager system.

---

## 2.1 Call Graph (Logic Design)
The system is designed with a **Controller-Service** architecture. The `StreetRaceManager` acts as the central hub (Controller), invoking methods across 8 specialized modules (Services).

### **Core Function Call Map:**
*   **Race Flow**: `StreetRaceManager.run_race_sequence()` -> `RaceModule.create_race()` (calls `CrewModule.is_role()` and `InventoryModule.has_car()`) -> `ResultsModule.finalize_race()` (calls `InventoryModule.add_cash()`).
*   **Tuning Flow**: `StreetRaceManager.perform_tuning()` -> `TuningModule.upgrade_car()` (calls `CrewModule.is_role()`, `InventoryModule.use_parts()`, and `InventoryModule.deduct_cash()`).
*   **Mission Flow**: `StreetRaceManager.start_mission()` -> `MissionModule.assign_mission()` (calls `CrewModule.is_role()`).
*   **Bonus Flow**: `SponsorModule.trigger_win_bonus()` -> `InventoryModule.add_cash()`.

*(Note: The physical Call Graph diagram must be drawn by hand based on this logic.)*

---

## 2.2 Integration Test Design
The following test cases validate the interaction boundary between modules.

| ID | Scenario | Modules Involved | Expected Result |
| :--- | :--- | :--- | :--- |
| **INT-01** | Register-to-Crew Guard | Registration, Crew | Role assignment fails if member is not registered. |
| **INT-02** | Valid Race Lifecycle | Reg, Crew, Inv, Race | Successful race scheduling with verified Driver & Car. |
| **INT-03** | Role Violation Guard | Crew, Race | Race creation fails if the designated member is not a "Driver". |
| **INT-04** | Financial Sync | Race, Results, Inventory | Win prize is automatically added to the global cash balance. |
| **INT-05** | Mission Skill Lock | Crew, Mission | Mission fails if the assigned member does not have the required role. |
| **INT-06** | Resource Consumption| Crew, Inv, Tuning | Car upgrade successfully deducts cash, parts, and verifies mechanic. |
| **INT-07** | Sponsor Integration | Sponsor, Results, Inv | Win bonus from a signed sponsor is credited to inventory. |

---

## 2.3 Additional Modules (Bonus)
1.  **Vehicle Tuning Module**: Integrates with Crew (Mechanic check) and Inventory (Resources) to improve car stats permanently.
2.  **Sponsorships Module**: Integrates with Results (Win event) and Inventory (Payouts) to provide revenue bonuses.

---

## 2.4 Testing Results Summary
All **7 Integration Scenarios** passed 100% using `pytest`. No logical issues were found in the final integrated flow, as the boundary guards effectively prevented illegal state transitions (e.g., non-drivers racing).
