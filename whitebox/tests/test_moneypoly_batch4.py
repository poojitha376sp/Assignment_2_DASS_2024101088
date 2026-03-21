"""
White Box Test Suite for MoneyPoly (Part 1.3)
Focus: Special Movement & Bankruptcy (TC-11 to TC-14)
Corrected for new Game.py bankruptcy rescue loop.
"""
import pytest
from unittest.mock import patch
from moneypoly.game import Game
from moneypoly.config import JAIL_POSITION

@pytest.fixture
def clean_game():
    """Fixture to provide a clean game instance with two players."""
    return Game(["Alice", "Bob"])

def test_tc12_movement_go_to_jail(clean_game):
    """TC-12: Movement (Go To Jail Tile)."""
    player = clean_game.players[0]
    clean_game.turn_info["index"] = 0
    with patch('moneypoly.dice.Dice.roll', return_value=30), \
         patch('moneypoly.dice.Dice.is_doubles', return_value=False):
        clean_game.play_turn()
    assert player.position == JAIL_POSITION
    assert player.jail_info["in_jail"] is True

def test_tc13_movement_third_double(clean_game):
    """TC-13: Movement (3rd Double Rule)."""
    player = clean_game.players[0]
    clean_game.turn_info["index"] = 0
    with patch('random.randint', side_effect=[1, 1, 2, 2, 3, 3]), \
         patch.object(clean_game, '_handle_property_tile'):
        clean_game.play_turn()
        clean_game.play_turn()
        clean_game.play_turn()
    assert player.position == JAIL_POSITION
    assert player.jail_info["in_jail"] is True

def test_tc11_bankruptcy_mortgage_recovery(clean_game):
    """TC-11: Bankruptcy (Mortgage Recovery)."""
    alice = clean_game.players[0]
    bob = clean_game.players[1]
    med = clean_game.resources["board"].get_property_at(1)
    
    med.owner = bob
    alice.balance = 20
    oriental = clean_game.resources["board"].get_property_at(6)
    oriental.owner = alice
    alice.properties.append(oriental)
    
    # Alice needs to pay $50 rent. Balance becomes -30.
    # Logic: _check_bankruptcy calls ui.confirm -> True, then _menu_mortgage -> 1, then ui.confirm -> False.
    with patch.object(med, 'get_rent', return_value=50), \
         patch('moneypoly.ui.confirm', side_effect=[True, False]), \
         patch('moneypoly.ui.safe_int_input', return_value=1):
        clean_game.pay_rent(alice, med)
        clean_game._check_bankruptcy(alice)
        
    assert oriental.is_mortgaged is True
    assert alice.balance == 20 # -30 + 50
    assert not alice.is_eliminated

def test_tc14_bankruptcy_full_failure(clean_game):
    """TC-14: Bankruptcy (Full Failure)."""
    alice = clean_game.players[0]
    bob = clean_game.players[1]
    med = clean_game.resources["board"].get_property_at(39)
    med.owner = bob
    alice.balance = 10
    
    # Needs to pay $50. No assets.
    with patch.object(med, 'get_rent', return_value=50), \
         patch('moneypoly.ui.confirm', return_value=False):
        clean_game.pay_rent(alice, med)
        clean_game._check_bankruptcy(alice)
        
    assert alice.is_eliminated is True
