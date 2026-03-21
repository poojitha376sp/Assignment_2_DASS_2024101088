"""
White Box Test Suite for MoneyPoly (Part 1.3)
Focus: Financials and Rent Branches (TC-08 to TC-10)
"""
import pytest
from unittest.mock import patch
from moneypoly.game import Game
from moneypoly.config import STARTING_BALANCE

@pytest.fixture
def clean_game():
    """Fixture to provide a clean game instance with two players."""
    return Game(["Alice", "Bob"])

def test_tc08_rent_standard(clean_game):
    """
    TC-08: Rent (Standard) - Node 45 in CFG.
    Verify rent calculation for a single owned property.
    """
    alice = clean_game.players[0]
    bob = clean_game.players[1]
    prop = clean_game.resources["board"].get_property_at(1) # Mediterranean Ave
    
    # Alice buys the property
    prop.owner = alice
    alice.properties.append(prop)
    
    # Bob lands on it
    initial_bob_balance = bob.balance
    initial_alice_balance = alice.balance
    rent = prop.get_rent() # Should be 2 for Med Ave
    
    clean_game._handle_property_tile(bob, prop)
    
    assert bob.balance == initial_bob_balance - rent
    assert alice.balance == initial_alice_balance + rent

def test_tc09_rent_full_group(clean_game):
    """
    TC-09: Rent (Full Group) - Multiplier check.
    Verify rent is doubled when owner has all properties of a color group.
    """
    alice = clean_game.players[0]
    bob = clean_game.players[1]
    # Brown group: Mediterranean (Pos 1) and Baltic (Pos 3)
    prop1 = clean_game.resources["board"].get_property_at(1)
    prop2 = clean_game.resources["board"].get_property_at(3)
    
    # Alice owns both
    prop1.owner = alice
    prop2.owner = alice
    alice.properties.extend([prop1, prop2])
    
    # Rent should be doubled (2 * 2 = 4 for Med Ave)
    rent = prop1.get_rent()
    assert rent == 4
    
    clean_game._handle_property_tile(bob, prop1)
    assert bob.balance == STARTING_BALANCE - 4

def test_tc10_rent_mortgaged(clean_game):
    """
    TC-10: Rent (Mortgaged) - Node 33 in CFG.
    Verify no rent is collected on a mortgaged property.
    """
    alice = clean_game.players[0]
    bob = clean_game.players[1]
    prop = clean_game.resources["board"].get_property_at(1)
    
    prop.owner = alice
    alice.properties.append(prop)
    prop.is_mortgaged = True # Alice mortgages it
    
    clean_game._handle_property_tile(bob, prop)
    
    # Bob should pay nothing
    assert bob.balance == STARTING_BALANCE
    assert alice.balance == STARTING_BALANCE
