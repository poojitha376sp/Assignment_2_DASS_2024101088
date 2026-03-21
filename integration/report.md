# StreetRace Manager - Integration Testing Report

This report documents the design, implementation, and integration testing of the StreetRace Manager system.

---

## 2.1 Call Graph (Logic Design)
The system is designed with a **Controller-Service** architecture. The `StreetRaceManager` acts as the central hub (Controller), invoking methods across **9 specialized modules** (Services). The complete node-by-node atlas is in `diagrams/call_graph_atlas.md`.

### **Core Function Call Map (20 Inter-Module Arrows):**
*   **Race Flow**: `M1: run_race_sequence()` → `R1: create_race()` (calls `C2: is_role()` + `I4: has_car()`) → `RE1: finalize_race()` (calls `R2: get_race()`, `I1: add_cash()`, `I7: set_damage()`, `TR1: add_trophy()`) → `S2: trigger_win_bonus()` (calls `I1: add_cash()`).
*   **Tuning Flow**: `M2: perform_tuning()` → `T1: upgrade_car()` (calls `C2: is_role()`, `I6: use_parts()`, `I2: deduct_cash()`, and on failure: `I5: add_parts()` rollback).
*   **Mission Flow**: `M3: start_mission()` → `MS1: assign_mission()` (calls `C2: is_role()`, `I8: is_damaged()`, `I7: set_damage()`).
*   **Registration Guard**: `C1: assign_role()` → `RG2: is_registered()`.

*(Note: The physical Call Graph diagram is hand-drawn and submitted as an image in `diagrams/`.)*

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
| **INT-08** | Trophy Unlock Flow | Results, TrophyRoom | 1st Place finishes automatically unlock a trophy. |
| **INT-09** | Damage & Repair Rule | Results, Inv, Mission | Damaged cars from races must be fixed by a Mechanic mission. |

---

## 2.3 Additional Modules (Bonus)
1.  **Vehicle Tuning Module**: Integrates with Crew (Mechanic check) and Inventory (Resources) to improve car stats permanently.
2.  **Sponsorships Module**: Integrates with Results (Win event) and Inventory (Payouts) to provide revenue bonuses.
3.  **Trophy Room Module**: Integrates with Results (Win event) to store team achievements and medals.

---

## 2.4 Testing Results Summary
All **9 Integration Scenarios** passed 100% using `pytest`. No logical issues were found in the final integrated flow.

---

## 2.5 Exhaustive Integration Audit (Final Proof)
A comprehensive end-to-end simulation was performed in `exhaustive_workflow.py` to verify the stability of the 9-module cluster.

### **Audit Lifecycle Phases:**
1.  **Recruitment**: Successfully registered Alice (Driver), Bob (Mechanic), and Charlie (Strategist).
2.  **Asset Management**: Populated garage and warehouse; verified resource availability for tuning.
3.  **Competition Flow**: Alice won a high-stakes race; verified automatic **Trophy Unlock** and **Sponsorship Bonus** ($35,000 total gain).
4.  **Resilience**: Simulated a vehicle crash; verified that only a **Mechanic** could perform the **Repair Mission**.
5.  **Tuning**: Bob successfully upgraded the Skyline GTR using inventory engine modules.
6.  **Logistics**: Charlie executed a rescue mission requiring strategical clearance.

**Final System State**: 100% stability. Final financial balance: **$44,500**.
