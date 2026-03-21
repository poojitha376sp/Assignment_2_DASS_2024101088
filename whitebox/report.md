# MoneyPoly White-Box Testing - Pylint Results

This document tracks the iterative improvements made to the MoneyPoly codebase using Pylint, as required by Part 1.2 of the assignment.

---

## Initial State
- **Command**: `pylint whitebox/code/moneypoly/`
- **Initial Score**: 8.17/10 (Average across all modules)
- **Primary Issues**: Missing docstrings, unused imports, and overly complex return statements.

---

## Iteration 1: Module Docstring in `player.py`
- **Target File**: `whitebox/code/moneypoly/player.py`
- **Pylint Warning**: `C0114: Missing module docstring`
- **Description**: Added a high-level description to the `player.py` module. Docstrings at the module level are essential for explaining the file's purpose to other developers and maintaining structural clarity.
- **Score Before**: 7.92/10
- **Score After**: 8.12/10 (+0.20)
- **Action**: Added a concise, IIITH student-style summary of the module's role in managing player state.

---

## Iteration 2: Module Docstring in `property.py`
- **Target File**: `whitebox/code/moneypoly/property.py`
- **Pylint Warning**: `C0114: Missing module docstring`
- **Description**: Added a high-level description to the `property.py` module. This details the data models for both individual properties and color groups.
- **Score Before**: 8.98/10
- **Score After**: 9.15/10 (+0.17)
- **Action**: Documented the module's responsibility for board tile entities and group arithmetic.

---

## Iteration 3: Module Docstring in `board.py`
- **Target File**: `whitebox/code/moneypoly/board.py`
- **Pylint Warning**: `C0114: Missing module docstring`
- **Justification**: Added a high-level description to `board.py`. This module acts as the central registry for both special squares and purchasable properties, so a docstring helps explain how indexing works.
- **Score Before**: 6.92/10
- **Score After**: 7.18/10 (+0.26)
- **Action**: Added an overview explaining the SPECIAL_TILES map and the Board initialization sequence.

---

## Iteration 4: Module Docstring in `dice.py`
- **Target File**: `whitebox/code/moneypoly/dice.py`
- **Pylint Warning**: `C0114: Missing module docstring`
- **Justification**: Added a high-level description to `dice.py`. This module acts as the engine of player movement, so it's important to document how it handles both RNG and the specific "doubles streak" rule.
- **Score Before**: 7.04/10
- **Score After**: 7.41/10 (+0.37)
- **Action**: Added a summary of the Dice class and its role in the game loop.

---

## Iteration 5: Module Docstring in `bank.py`
- **Target File**: `whitebox/code/moneypoly/bank.py`
- **Pylint Warning**: `C0114: Missing module docstring`
- **Justification**: Added a high-level description to `bank.py`. Since this module handles all the financial transactions and emergency loans, a module docstring is needed to explain its internal accounting.
- **Score Before**: 7.71/10
- **Score After**: 8.24/10 (+0.53)
- **Action**: Added a summary of the Bank class and its role in the MoneyPoly economy. I also took the opportunity to remove an unused math import.

---

## Iteration 6: Module Docstring in `cards.py`
- **Target File**: `whitebox/code/moneypoly/cards.py`
- **Pylint Warning**: `C0114: Missing module docstring`
- **Justification**: Added a high-level description to `cards.py`. This module handles the logic for drawing Chance and Community Chest cards, so a docstring is useful for explaining how deck cycling works.
- **Score Before**: 0.38/10
- **Score After**: 0.77/10 (+0.39)
- **Action**: Added a summary of the CardDeck class and the contents of the card lists.

---

## Iteration 7: Module Docstring in `config.py`
- **Target File**: `whitebox/code/moneypoly/config.py`
- **Pylint Warning**: `C0114: Missing module docstring`
- **Justification**: Added a high-level description to `config.py`. This module is the "brain" of the game's constants, so a docstring here identifies it as the central location for prices, indices, and rule limits.
- **Score Before**: 9.29/10
- **Score After**: 10.0/10 (+0.71)
- **Action**: Added an overview of the global constants used throughout the MoneyPoly game.

---

## Iteration 8: Module Docstring in `game.py`
- **Target File**: `whitebox/code/moneypoly/game.py`
- **Pylint Warning**: `C0114: Missing module docstring`
- **Justification**: Added a high-level description to `game.py`. This is the core controller of the entire MoneyPoly engine. A docstring here explains how it initializes the board and handles the main game loop and turn rotations.
- **Score Before**: 8.70/10
- **Score After**: 8.73/10 (+0.03)
- **Action**: Summarized the Game class and its coordination of players, bank, and dice.

---

## Iteration 9: Module Docstring in `ui.py`
- **Target File**: `whitebox/code/moneypoly/ui.py`
- **Pylint Warning**: `C0114: Missing module docstring`
- **Justification**: Added a high-level description to `ui.py`. This module handles all player-to-game communications, including display formatting and input loops. Documentation here explains the interaction layer of the MoneyPoly engine.
- **Score Before**: 9.55/10
- **Score After**: 9.77/10 (+0.22)
- **Action**: Summarized the UI class and its role in presenting the board state and collecting player decisions.

---

## Iteration 10: Class Docstring in `property.py` (PropertyGroup)
- **Target File**: `whitebox/code/moneypoly/property.py`
- **Pylint Warning**: `C0115: Missing class docstring`
- **Justification**: Added a class-level docstring to `PropertyGroup`. This class is responsible for logical groupings of properties (like color sets), so documenting its purpose is important for understanding the rent-calculation hierarchy.
- **Score Before**: 9.15/10
- **Score After**: 9.32/10 (+0.17)
- **Action**: Added a technical summary of how PropertyGroup tracks membership and color consistency.

---

## Iteration 11: Class Docstring in `bank.py` (Bank)
- **Target File**: `whitebox/code/moneypoly/bank.py`
- **Pylint Warning**: `C0115: Missing class docstring`
- **Justification**: Added a class-level docstring to `Bank`. This class serves as the central ledger for the game's economy. Documenting its purpose clarifies the relationship between global funds and individual player loans.
- **Score Before**: 8.24/10
- **Score After**: 8.53/10 (+0.29)
- **Action**: Added an architectural overview of the Bank class and its financial management role.

---

## Iteration 12: Final Class Docstrings Group (Board, CardDeck, Game)
- **Target Files**: 
  - `whitebox/code/moneypoly/board.py`
  - `whitebox/code/moneypoly/cards.py`
  - `whitebox/code/moneypoly/game.py`
- **Pylint Warning**: `C0115: Missing class docstring`
- **Justification**: As per the user's suggestion to group minor docstring fixes, I am adding class-level documentation to the remaining core classes. This ensures all primary objects in the MoneyPoly engine have defined responsibilities.
- **Score Before**: 8.08/10 (Group average)
- **Score After**: 8.08/10 (+0.00 net, but C0115 warnings resolved)
- **Action**: Added concise class summaries explaining the roles of the Board, CardDeck, and Game controllers.

---

## Iteration 13: Unused Imports and Final Newlines Cleanup (Grouped)
- **Target Files**: 
  - `whitebox/code/moneypoly/player.py`
  - `whitebox/code/moneypoly/dice.py`
  - `whitebox/code/moneypoly/game.py`
- **Pylint Warnings**: 
  - `W0611: Unused import` (sys, os, BOARD_SIZE, GO_TO_JAIL_POSITION)
  - `C0304: Final newline missing`
- **Justification**: Following your suggestion to group small, score-polishing fixes, I am clearing these basic style violations across multiple files. This reduces visual noise and ensures the imports are strictly necessary.
- **Score Before**: 8.57/10 (Group average)
- **Score After**: 8.78/10 (+0.21)
- **Action**: Removed unused imports from header sections and ensured all files end with the standard blank line.

---

## Iteration 15: Grouped Refactoring (property.py and player.py)
- **Target Files**: 
  - `whitebox/code/moneypoly/property.py`
  - `whitebox/code/moneypoly/player.py`
- **Pylint Warnings**: 
  - `R1705: Unnecessary "else" after "return"` (property.py)
  - `W0612: Unused variable 'old_position'` (player.py)
- **Justification**: These refactors improve code clarity and remove dead code. De-indenting logic after a return statement and removing unused assignments makes the codebase leaner and easier to maintain.
- **Score Before**: 8.87/10 (Group average)
- **Score After**: 9.14/10 (+0.27)
- **Action**: Removed the `else` block in `property.py:get_rent()` and deleted the unused `old_position` assignment in `player.py:move()`. Also ensured both files have correct final newlines.

---

## Iteration 16: Logic and Exception Handling Cleanup (game.py and ui.py)
- **Target Files**: 
  - `whitebox/code/moneypoly/game.py`
  - `whitebox/code/moneypoly/ui.py`
- **Pylint Warnings**: 
  - `R1723: Unnecessary "elif" after "break"` (game.py)
  - `W1309: Using an f-string that does not have any interpolated variables` (game.py)
  - `W0702: No exception type(s) specified` (ui.py)
- **Justification**: These fixes address logical branch clarity and defensive programming. De-indenting after a break reduces nesting complexity, removing redundant f-string markers saves overhead, and specifying exception types (Exception) prevents accidental catching of system signals like Ctrl+C.
- **Score Before**: 8.89/10 (Group average)
- **Score After**: 8.97/10 (+0.08)
- **Action**: Corrected the branch logic in `game.py`, removed the empty f-marker, and updated the bare `except` in `ui.py` to `except ValueError`.

---

## Iteration 17: Line Length Cleanup in `cards.py`
- **Target File**: `whitebox/code/moneypoly/cards.py`
- **Pylint Warning**: `C0301: Line too long`
- **Justification**: `cards.py` contains many hardcoded data strings that exceed the 100-character limit, resulting in a significantly low Pylint score. Wrapping these strings across multiple lines makes the data easier to read and brings the module into full compliance with PEP8 standards.
- **Score Before**: 0.77/10
- **Score After**: 10.00/10 (+9.23)
- **Action**: Reformatted `CHANCE_CARDS` and `COMMUNITY_CHEST_CARDS` to ensure no line exceeds 100 characters.

---

## Iteration 18: Refactoring Complex Logic in `game.py`
- **Target File**: `whitebox/code/moneypoly/game.py`
- **Pylint Warning**: `R0912: Too many branches (15/12)`
- **Justification**: The `_apply_card` method contains a large `if-elif` chain to handle different card actions. While functional, this high branch count makes the method harder to test and maintain. Extracting the logic into a more modular structure (like a dispatch table or smaller helpers) reduces complexity and satisfies Pylint's refactoring rules.
- **Score Before**: 9.84/10 (Project Average)
- **Score After**: 9.90/10 (Project Average) / 9.97/10 (Module)
- **Action**: Extracted complex card actions into dedicated private methods. Also resolved unnecessary parentheses and ensured both files have correct final newlines.

---

## Part 1.3: White Box Test Cases
This section documents the white-box test suite designed to cover all branches, key variable states, and edge cases of the MoneyPoly game engine.

### Test Case Design & Justification
| ID | Branch/Feature | Justification | Results |
| :--- | :--- | :--- | :--- |
| **TC-01** | Movement (Pass Go) | Verify salary is credited when passing position 0. | **FAILED** (Found Bug #2) |
| **TC-02** | Jail (Pay Fine) | Verify player is released after paying $50. | **FAILED** (Found Bug #1) |
| **TC-03** | Jail (Doubles Roll) | Verify release via luck (Node 11). | **FAILED** (Found Bug #3) |
| **TC-04** | Jail (3rd Turn Forced) | Verify forced release after 3 turns (Node 12). | **PASSED** (Logic present) |

### Errors & Logical Issues Found
#### **Error #1: Voluntary Jail Fine - Missing Player Deduction**
- **File**: `whitebox/code/moneypoly/game.py`
- **Location**: `_handle_jail_turn` method (approx. lines 281-282).
- **Issue**: When a player chooses to pay the $50 fine to leave jail voluntarily, the game calls `self.resources["bank"].collect(JAIL_FINE)` but fails to call `player.deduct_money(JAIL_FINE)`.
- **Impact**: Incorrect game economy; money is created out of thin air.
- **Fix**: Add `player.deduct_money(JAIL_FINE)` to the voluntary payment branch.

#### **Error #2: Pass Go Salary - Incorrect Boundary Check**
- **File**: `whitebox/code/moneypoly/player.py`
- **Location**: `move` method (line 55).
- **Issue**: The check `if self.position == 0` only awards the $200 salary if the player lands **exactly** on the Go square. It fails to award salary if the player **passes** Go (e.g., moving from 38 to 1).
- **Impact**: Players lose their salary most turns they circle the board, significantly breaking game progression.
- **Fix**: Change the logic to check if the new position is less than the old position (indicating a wrap-around) and ensure the landing case is still covered.

#### **Error #3: Jail Mechanics - Missing Doubles Roll Escape**
- **File**: `whitebox/code/moneypoly/game.py`
- **Location**: `_handle_jail_turn` method.
- **Issue**: The classic Monopoly rule where a player can escape jail by rolling doubles is completely unimplemented. The code currently only allows escape via cards or payment.
- **Impact**: Game rules violation; players are forced to wait or pay even if they roll doubles.
- **Fix**: Implement a dice roll check in the jail turn logic if the player declines to pay the fine.

## Iteration 14: Attribute Initialization in `dice.py`
- **Target File**: `whitebox/code/moneypoly/dice.py`
- **Pylint Warning**: `W0201: Attribute 'doubles_streak' defined outside __init__`
- **Justification**: In Python, all instance attributes should be declared in the constructor. Initializing `doubles_streak` in `__init__` makes the object state explicit and avoids runtime errors if the attribute is accessed before the first roll.
- **Score Before**: 9.62/10
- **Score After**: 10.00/10 (+0.38)
- **Action**: Added `self.doubles_streak = 0` to the `Dice` constructor.
