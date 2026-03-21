# Call Graph Node Atlas (Part 2.1)

This document maps **every function** in the StreetRace Manager system to a node for the hand-drawn Call Graph. Each node shows who calls it (**Predecessor**) and who it calls (**Successor**).

---

## **1. Central Controller (main.py — StreetRaceManager)**

| Node | Function | Purpose | Predecessor (Called By) | Successor (Calls) |
| :--- | :--- | :--- | :--- | :--- |
| **M1** | `run_race_sequence()` | Orchestrates a full race lifecycle: schedule → finalize → bonus. | USER | `R1`, `RE1`, `S2` |
| **M2** | `perform_tuning()` | Orchestrates a vehicle upgrade session. | USER | `T1` |
| **M3** | `start_mission()` | Orchestrates a team mission assignment. | USER | `MS1` |

---

## **2. Registration Module (registration.py)**

| Node | Function | Purpose | Predecessor (Called By) | Successor (Calls) |
| :--- | :--- | :--- | :--- | :--- |
| **RG1** | `register_member()` | Adds name + role to the registry dictionary. | USER | — (leaf) |
| **RG2** | `is_registered()` | Returns True/False for membership check. | `C1` | — (leaf) |
| **RG3** | `get_role()` | Retrieves the role string for a member. | USER | — (leaf) |

---

## **3. Crew Management Module (crew.py)**

| Node | Function | Purpose | Predecessor (Called By) | Successor (Calls) |
| :--- | :--- | :--- | :--- | :--- |
| **C1** | `assign_role()` | Sets role + skill level. **Requires registration first.** | USER | `RG2` |
| **C2** | `is_role()` | Checks if member holds a specific role (e.g., "driver"). | `R1`, `MS1`, `T1` | — (leaf) |
| **C3** | `get_skill()` | Returns the numeric skill level of a member. | USER | — (leaf) |

---

## **4. Inventory Module (inventory.py)**

| Node | Function | Purpose | Predecessor (Called By) | Successor (Calls) |
| :--- | :--- | :--- | :--- | :--- |
| **I1** | `add_cash()` | Deposits money (prize/bonus) into the balance. | `RE1`, `S2` | — (leaf) |
| **I2** | `deduct_cash()` | Withdraws money for tuning. Fails if insufficient. | `T1` | — (leaf) |
| **I3** | `add_car()` | Adds a vehicle to the garage list. | USER | — (leaf) |
| **I4** | `has_car()` | Checks if a car exists in garage. | `R1` | — (leaf) |
| **I5** | `add_parts()` | Stocks spare parts (also used in rollback). | USER, `T1` (rollback) | — (leaf) |
| **I6** | `use_parts()` | Consumes spare parts for tuning. | `T1` | — (leaf) |
| **I7** | `set_damage()` | Marks a car as damaged or fixed. | `RE1`, `MS1` | — (leaf) |
| **I8** | `is_damaged()` | Checks if a car is currently in damaged state. | `MS1` | — (leaf) |

---

## **5. Race Management Module (race.py)**

| Node | Function | Purpose | Predecessor (Called By) | Successor (Calls) |
| :--- | :--- | :--- | :--- | :--- |
| **R1** | `create_race()` | Validates driver role + car existence, then schedules. | `M1` | `C2`, `I4` |
| **R2** | `get_race()` | Returns race data dict for a given race_id. | `RE1` | — (leaf) |

---

## **6. Results Module (results.py)**

| Node | Function | Purpose | Predecessor (Called By) | Successor (Calls) |
| :--- | :--- | :--- | :--- | :--- |
| **RE1** | `finalize_race()` | Records outcome, updates cash, handles damage, awards trophy. | `M1` | `R2`, `I1`, `I7`, `TR1` |

---

## **7. Mission Planning Module (missions.py)**

| Node | Function | Purpose | Predecessor (Called By) | Successor (Calls) |
| :--- | :--- | :--- | :--- | :--- |
| **MS1** | `assign_mission()` | Validates role, checks damage state for Repair missions. | `M3`, USER | `C2`, `I8`, `I7` |

---

## **8. Vehicle Tuning Module (tuning.py)**

| Node | Function | Purpose | Predecessor (Called By) | Successor (Calls) |
| :--- | :--- | :--- | :--- | :--- |
| **T1** | `upgrade_car()` | Improves car stats. Consumes parts + cash, requires mechanic. | `M2` | `C2`, `I6`, `I2`, `I5` (rollback) |

---

## **9. Sponsorships Module (sponsors.py)**

| Node | Function | Purpose | Predecessor (Called By) | Successor (Calls) |
| :--- | :--- | :--- | :--- | :--- |
| **S1** | `sign_sponsor()` | Registers a sponsor deal for a specific race. | USER | — (leaf) |
| **S2** | `trigger_win_bonus()` | Awards bonus cash to inventory if deal exists. | `M1` | `I1` |

---

## **10. Trophy Room Module (trophy.py)**

| Node | Function | Purpose | Predecessor (Called By) | Successor (Calls) |
| :--- | :--- | :--- | :--- | :--- |
| **TR1** | `add_trophy()` | Stores an achievement string in the trophy list. | `RE1` | — (leaf) |

---

## **Summary of Inter-Module Calls (22 Total)**

| # | From (Caller) | To (Callee) | Module Boundary |
| :--- | :--- | :--- | :--- |
| 1 | `M1` (Main) | `R1` (Race) | Main → Race |
| 2 | `M1` (Main) | `RE1` (Results) | Main → Results |
| 3 | `M1` (Main) | `S2` (Sponsors) | Main → Sponsors |
| 4 | `M2` (Main) | `T1` (Tuning) | Main → Tuning |
| 5 | `M3` (Main) | `MS1` (Missions) | Main → Missions |
| 6 | `R1` (Race) | `C2` (Crew) | Race → Crew |
| 7 | `R1` (Race) | `I4` (Inventory) | Race → Inventory |
| 8 | `RE1` (Results) | `R2` (Race) | Results → Race |
| 9 | `RE1` (Results) | `I1` (Inventory) | Results → Inventory |
| 10 | `RE1` (Results) | `I7` (Inventory) | Results → Inventory |
| 11 | `RE1` (Results) | `TR1` (Trophy) | Results → Trophy |
| 12 | `MS1` (Missions) | `C2` (Crew) | Missions → Crew |
| 13 | `MS1` (Missions) | `I8` (Inventory) | Missions → Inventory |
| 14 | `MS1` (Missions) | `I7` (Inventory) | Missions → Inventory |
| 15 | `T1` (Tuning) | `C2` (Crew) | Tuning → Crew |
| 16 | `T1` (Tuning) | `I6` (Inventory) | Tuning → Inventory |
| 17 | `T1` (Tuning) | `I2` (Inventory) | Tuning → Inventory |
| 18 | `T1` (Tuning) | `I5` (Inventory) | Tuning → Inventory (rollback) |
| 19 | `S2` (Sponsors) | `I1` (Inventory) | Sponsors → Inventory |
| 20 | `C1` (Crew) | `RG2` (Registration) | Crew → Registration |
