"""
White Box Test Suite for MoneyPoly (Part 1.3)
Focus: Property and Auction Branches (TC-05 to TC-07) + Refined TC-04
"""
import pytest
from unittest.mock import patch, MagicMock
from moneypoly.game import Game
from moneypoly.config import STARTING_BALANCE, JAIL_FINE

@pytest.fixture
def clean_game():
    """Fixture to provide a clean game instance with two players."""
    return Game(["Alice", "Bob"])

def test_tc04_jail_three_turn_limit_refined(clean_game):
    """
    TC-04: Jail (3rd Turn Forced Fine) - Node 12 in CFG.
    Refined to avoid side effects from card draws.
    """
    player = clean_game.players[0]
    player.go_to_jail()
    player.jail_info["turns"] = 2 # Already spent 2 turns
    
    # Mock input to choose 'n' for paying fine, then failing doubles
    # Mock _apply_card to do nothing (prevents balance changes from cards)
    with patch('moneypoly.ui.confirm', return_value=False), \
         patch('builtins.input', return_value='s'), \
         patch('moneypoly.dice.Dice.roll', return_value=7), \
         patch('moneypoly.dice.Dice.is_doubles', return_value=False), \
         patch.object(clean_game, '_apply_card'):
        clean_game._handle_jail_turn(player)
        
    assert player.jail_info["in_jail"] is False
    assert player.balance == STARTING_BALANCE - JAIL_FINE
    assert player.jail_info["turns"] == 0

def test_tc05_purchase_normal(clean_game):
    """
    TC-05: Purchase (Normal) - Node 24 in CFG.
    Verify a player can buy an unowned property.
    """
    player = clean_game.players[0]
    # Move Alice to Mediterranean Ave (Pos 1, Price 60)
    prop = clean_game.resources["board"].get_property_at(1)
    initial_balance = player.balance
    
    # Mock input to choose 'b' for buy
    with patch('builtins.input', return_value='b'):
        clean_game._handle_property_tile(player, prop)
        
    assert prop.owner == player
    assert player.balance == initial_balance - prop.financials["price"]
    assert prop in player.properties

def test_tc06_auction_winning_bid(clean_game):
    """
    TC-06: Auction (Winning Bid) - Node 28 in CFG.
    Verify a property is transferred to the highest bidder in an auction.
    """
    alice = clean_game.players[0]
    bob = clean_game.players[1]
    prop = clean_game.resources["board"].get_property_at(3) # Baltic Ave
    
    # Mock inputs:
    # 1. Tile choice: 'a' (Auction)
    # 2. Alice bid: 10
    # 3. Bob bid: 50
    # 4. Alice bid: 0 (dropout)
    with patch('builtins.input', side_effect=['a']), \
         patch('moneypoly.ui.safe_int_input', side_effect=[10, 50, 0]):
        clean_game._handle_property_tile(alice, prop)
        
    assert prop.owner == bob
    assert bob.balance == STARTING_BALANCE - 50
    assert prop in bob.properties
    assert prop not in alice.properties

def test_tc07_auction_no_bidders(clean_game):
    """
    TC-07: Auction (No Bidders) - Node 27 in CFG.
    Verify the property remains unowned if no one bids.
    """
    alice = clean_game.players[0]
    prop = clean_game.resources["board"].get_property_at(3)
    
    # Mock inputs:
    # 1. Tile choice: 'a' (Auction)
    # 2. All players bid 0
    with patch('builtins.input', side_effect=['a']), \
         patch('moneypoly.ui.safe_int_input', side_effect=[0, 0]):
        clean_game._handle_property_tile(alice, prop)
        
    assert prop.owner is None
    assert alice.balance == STARTING_BALANCE
    assert prop not in alice.properties
