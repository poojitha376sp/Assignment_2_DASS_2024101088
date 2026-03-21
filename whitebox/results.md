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
