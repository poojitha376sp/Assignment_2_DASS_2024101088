"""
Exhaustive Workflow Test for MoneyPoly (Part 1.3)
Focus: Super Workflow hitting remaining nodes (Tax, Cards, Houses, Monopoly)
"""
import pytest
from unittest.mock import patch
from moneypoly.game import Game
from moneypoly.config import INCOME_TAX_AMOUNT, HOUSE_COST, LUXURY_TAX_AMOUNT

@pytest.fixture
def clean_game():
    return Game(["Alice", "Bob"])

def test_tc15_full_game_workflow(clean_game):
    """
    TC-15: Super Workflow.
    Verifies the remaining statement nodes:
    - Tax Tiles (18a, 18b)
    - Card Draw (18c-h)
    - House Building & Monopoly (48-52)
    """
    alice = clean_game.players[0]
    bob = clean_game.players[1]
    
    # Global mocks for input/confirm to avoid blocked stdin
    with patch('builtins.input', return_value='s'), \
         patch('moneypoly.ui.confirm', return_value=True):
        
        # 1. LAND ON INCOME TAX (Pos 4)
        with patch('moneypoly.dice.Dice.roll', return_value=4), \
             patch('moneypoly.dice.Dice.is_doubles', return_value=False):
            clean_game.play_turn()
        
        assert alice.position == 4
        assert alice.balance == 1500 - INCOME_TAX_AMOUNT
        
        # 2. LAND ON CHANCE (Pos 7)
        receive_card = {"description": "Bank Error", "action": "collect", "value": 200}
        with patch('moneypoly.dice.Dice.roll', return_value=3), \
             patch('moneypoly.dice.Dice.is_doubles', return_value=False), \
             patch('moneypoly.cards.CardDeck.draw', return_value=receive_card):
            # Correct attribute for turn index is turn_info["index"]
            clean_game.turn_info["index"] = 0
            clean_game.play_turn()
            
        assert alice.position == 7
        assert alice.balance == 1500
        
        # 3. MONOPOLY AND HOUSES
        med = clean_game.resources["board"].get_property_at(1)
        baltic = clean_game.resources["board"].get_property_at(3)
        med.owner = alice
        baltic.owner = alice
        alice.properties.extend([med, baltic])
        
        # Choice 7 (Build), Choice 1 (Med Ave), 0 (Back)
        with patch('moneypoly.ui.safe_int_input', side_effect=[7, 1, 0]):
            clean_game.interactive_menu(alice)
            
        assert med.houses == 1
        assert alice.balance == 1500 - HOUSE_COST
        
        # 4. RENT VERIFICATION (50 + 4 = 54)
        initial_bob_balance = bob.balance
        clean_game.pay_rent(bob, med)
        assert bob.balance == initial_bob_balance - 54

def test_tc16_luxury_tax(clean_game):
    """TC-16: Luxury Tax Tile (Pos 38)."""
    alice = clean_game.players[0]
    with patch('moneypoly.dice.Dice.roll', return_value=38), \
         patch('moneypoly.dice.Dice.is_doubles', return_value=False):
        clean_game.play_turn()
    assert alice.position == 38
    assert alice.balance == 1500 - LUXURY_TAX_AMOUNT
