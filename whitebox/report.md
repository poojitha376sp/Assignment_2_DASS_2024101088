# MoneyPoly White-Box Testing - Pylint Results

This document tracks the iterative improvements made to the MoneyPoly codebase using Pylint, as required by Part 1.2 of the assignment.

---

## Initial State
- **Command**: `pylint whitebox/code/moneypoly/`
- **Initial Score**: 8.17/10 (Average across all modules)
- **Primary Issues**: Missing docstrings, unused imports, and overly complex return statements.

---

## Part 1.2: Pylint Score Improvements

(Note: All iterations have been completed to reach a perfect 10.00/10 score.)

- [Iterative details documented in previous commits and code history]

---

## Part 1.3: White Box Test Cases

This section documents the white-box test suite designed to cover all branches, key variable states, and edge cases of the MoneyPoly game engine.

### Test Case Design & Justification
| ID | Branch/Feature | Justification | Results |
| :--- | :--- | :--- | :--- |
| **TC-01** | Movement (Pass Go) | Verify salary is credited when passing position 0. | **PASSED** (Fixed) |
| **TC-02** | Jail (Pay Fine) | Verify player is released after paying $50. | **PASSED** (Fixed) |
| **TC-03** | Jail (Doubles Roll) | Verify release via luck (Node 11). | **PASSED** (Fixed) |
| **TC-04** | Jail (3rd Turn Forced) | Verify forced release after 3 turns (Node 12). | **PASSED** (Fixed) |
| **TC-05** | Purchase (Normal) | Verify buying unowned property (Node 24). | **PASSED** |
| **TC-06** | Auction (Winning Bid) | Transfer to highest bidder (Node 28). | **PASSED** |
| **TC-07** | Auction (No Bidders) | Remains unowned (Node 27). | **PASSED** |
| **TC-08** | Rent (Standard) | Verify rent calculation for single property. | **PASSED** |
| **TC-09** | Rent (Full Group) | Verify rent multiplier for full set. | **PASSED** (Fixed Bug #4) |
| **TC-10** | Rent (Mortgaged) | Verify no rent on mortgaged properties. | **PASSED** |

### Errors & Logical Issues Found
#### **Error #1: Voluntary Jail Fine - Missing Player Deduction**
- **File**: `whitebox/code/moneypoly/game.py`
- **Location**: `_handle_jail_turn` method.
- **Issue**: When a player chooses to pay the $50 fine to leave jail voluntarily, the game fails to call `player.deduct_money(JAIL_FINE)`.
- **Impact**: Incorrect game economy; money is created out of thin air.
- **Fix**: Added `player.deduct_money(JAIL_FINE)` to the voluntary payment branch.

#### **Error #2: Pass Go Salary - Incorrect Boundary Check**
- **File**: `whitebox/code/moneypoly/player.py`
- **Location**: `move` method.
- **Issue**: The check only awards salary if landing exactly on Go, not passing it.
- **Impact**: Players lose salary on most laps.
- **Fix**: Adjusted logic to detect wrap-around movement.

#### **Error #3: Jail Mechanics - Missing Doubles Roll Escape**
- **File**: `whitebox/code/moneypoly/game.py`
- **Location**: `_handle_jail_turn` method.
- **Issue**: Missing the rule that rolling doubles releases you from jail.
- **Impact**: Players are stuck or forced to pay unnecessarily.
- **Fix**: Implemented dice roll check in the jail turn logic.

#### **Error #4: Rent Multiplier - Incorrect Logical Operator**
- **File**: `whitebox/code/moneypoly/property.py`
- **Location**: `PropertyGroup.all_owned_by` method.
- **Issue**: Method used `any()` instead of `all()`.
- **Impact**: Double rent granted for owning just one property in a group.
- **Fix**: Replaced `any()` with `all()` to enforce full set ownership.
