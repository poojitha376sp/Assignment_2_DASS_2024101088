"""
White Box Test Suite for MoneyPoly (Part 1.3)
Focus: Special Movement & Bankruptcy (TC-11 to TC-14)
"""
import pytest
from unittest.mock import patch
from moneypoly.game import Game
from moneypoly.config import BOARD_SIZE, JAIL_POSITION

@pytest.fixture
def clean_game():
    """Fixture to provide a clean game instance with two players."""
    return Game(["Alice", "Bob"])

def test_tc12_movement_go_to_jail(clean_game):
    """
    TC-12: Movement (Go To Jail Tile) - Node 18 in CFG.
    Verify player is moved to Jail and state updated when landing on Go To Jail.
    """
    player = clean_game.players[0]
    clean_game.current_player_idx = 0
    
    # Mock dice to land exactly on Pos 30 (Go To Jail)
    with patch('moneypoly.dice.Dice.roll', return_value=30), \
         patch('moneypoly.dice.Dice.is_doubles', return_value=False):
        clean_game.play_turn()
        
    assert player.position == JAIL_POSITION
    assert player.jail_info["in_jail"] is True

def test_tc13_movement_third_double(clean_game):
    """
    TC-13: Movement (3rd Double Rule) - Logical Branch.
    Verify player is sent to Jail after 3 consecutive doubles.
    """
    player = clean_game.players[0]
    clean_game.current_player_idx = 0
    
    # Mock random.randint to produce three consecutive doubles (1+1, 2+2, 3+3)
    with patch('random.randint', side_effect=[1, 1, 2, 2, 3, 3]), \
         patch.object(clean_game, '_handle_property_tile'):
        clean_game.play_turn()
        clean_game.play_turn()
        clean_game.play_turn()
        
    assert player.position == JAIL_POSITION
    assert player.jail_info["in_jail"] is True

def test_tc11_bankruptcy_mortgage_recovery(clean_game):
    """
    TC-11: Bankruptcy (Mortgage Recovery) - Node 37-41 in CFG.
    Verify player can avoid bankruptcy by mortgaging properties.
    """
    alice = clean_game.players[0]
    bob = clean_game.players[1]
    prop = clean_game.resources["board"].get_property_at(1) # Med Ave
    
    prop.owner = bob
    alice.balance = 20
    
    # Alice owns Oriental Ave (Mortgage value 50)
    oriental = clean_game.resources["board"].get_property_at(6)
    oriental.owner = alice
    alice.properties.append(oriental)
    
    # Alice needs to pay $50 rent -> balance -30.
    # Choice 1: Mortgage property
    # Choice 1: Select Oriental Ave
    # Choice 0: Continue (now has balance 20)
    with patch.object(prop, 'get_rent', return_value=50), \
         patch('moneypoly.ui.safe_int_input', side_effect=[1, 1, 0]):
        clean_game.pay_rent(alice, prop)
        clean_game._check_bankruptcy(alice)
        
    assert oriental.is_mortgaged is True
    assert alice.balance == 20
    assert not alice.is_eliminated

def test_tc14_bankruptcy_full_failure(clean_game):
    """
    TC-14: Bankruptcy (Full Failure) - Node 42 in CFG.
    Verify player is eliminated when they cannot pay after selling everything.
    """
    alice = clean_game.players[0]
    bob = clean_game.players[1]
    prop = clean_game.resources["board"].get_property_at(39) # Boardwalk
    
    prop.owner = bob
    alice.balance = 10 
    alice.properties = [] # Nothing to sell
    
    with patch.object(prop, 'get_rent', return_value=50), \
         patch('moneypoly.ui.safe_int_input', return_value=0):
        clean_game.pay_rent(alice, prop)
        clean_game._check_bankruptcy(alice)
        
    assert alice.is_eliminated is True
    assert alice not in clean_game.players
