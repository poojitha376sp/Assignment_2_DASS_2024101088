"""
White Box Test Suite for MoneyPoly (Part 1.3)
Focus: Movement and Jail Branches (TC-01 to TC-04)
Revised with correct Dice methods and input mocks.
"""
import pytest
from unittest.mock import patch
from moneypoly.game import Game
from moneypoly.config import STARTING_BALANCE, GO_SALARY, JAIL_FINE

@pytest.fixture
def clean_game():
    """Fixture to provide a clean game instance with two players."""
    return Game(["Alice", "Bob"])

def test_tc01_movement_pass_go(clean_game):
    """
    TC-01: Movement (Pass Go) - Node 16 in CFG.
    Verify player receives $200 when passing or landing on Go.
    """
    player = clean_game.players[0]
    initial_balance = player.balance
    
    # Move player from 39 (Boardwalk) to 1 (Mediterranean Ave)
    player.position = 39
    
    # Mock input for landing on Mediterranean Ave (Skip buying)
    with patch('builtins.input', return_value='s'):
        clean_game._move_and_resolve(player, 2)
    
    assert player.position == 1
    assert player.balance == initial_balance + GO_SALARY

def test_tc02_jail_pay_fine(clean_game):
    """
    TC-02: Jail (Pay Fine) - Node 6 in CFG.
    Verify player is released after paying $50.
    EXPECTED TO FAIL until Error #1 is fixed.
    """
    player = clean_game.players[0]
    player.go_to_jail()
    assert player.jail_info["in_jail"] is True
    
    # Mock input to choose 'y' for paying fine
    # Note: _handle_jail_turn also rolls dice after release
    with patch('moneypoly.ui.confirm', return_value=True), \
         patch('builtins.input', return_value='s'), \
         patch('moneypoly.dice.Dice.roll', return_value=5):
        clean_game._handle_jail_turn(player)
        
    assert player.jail_info["in_jail"] is False
    assert player.jail_info["turns"] == 0
    # Balance check (reveals Bug #1)
    assert player.balance == STARTING_BALANCE - JAIL_FINE

def test_tc03_jail_roll_doubles(clean_game):
    """
    TC-03: Jail (Doubles Roll) - Node 11 in CFG.
    Verify player is released if they roll doubles.
    """
    player = clean_game.players[0]
    player.go_to_jail()
    
    # Mock input to choose 'n' for paying fine, then mock doubles roll
    with patch('moneypoly.ui.confirm', return_value=False), \
         patch('builtins.input', return_value='s'), \
         patch('moneypoly.dice.Dice.roll', return_value=8), \
         patch('moneypoly.dice.Dice.is_doubles', return_value=True):
        clean_game._handle_jail_turn(player)
        
    assert player.jail_info["in_jail"] is False
    assert player.balance == STARTING_BALANCE # No fine paid

def test_tc04_jail_three_turn_limit(clean_game):
    """
    TC-04: Jail (3rd Turn Forced Fine) - Node 12 in CFG.
    Verify player is forced to pay fine and move after 3 turns.
    """
    player = clean_game.players[0]
    player.go_to_jail()
    player.jail_info["turns"] = 2 # Already spent 2 turns
    
    # Mock input to choose 'n' for paying fine, then failing doubles
    with patch('moneypoly.ui.confirm', return_value=False), \
         patch('builtins.input', return_value='s'), \
         patch('moneypoly.dice.Dice.roll', return_value=7), \
         patch('moneypoly.dice.Dice.is_doubles', return_value=False):
        clean_game._handle_jail_turn(player)
        
    assert player.jail_info["in_jail"] is False
    assert player.balance == STARTING_BALANCE - JAIL_FINE
    assert player.jail_info["turns"] == 0
