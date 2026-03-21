"""
Exhaustive Workflow Test for MoneyPoly (Part 1.3)
Focus: Super Workflow hitting remaining nodes (Tax, Cards, Houses, Monopoly)
"""
import pytest
from unittest.mock import patch, MagicMock
from moneypoly.game import Game
from moneypoly.config import INCOME_TAX_AMOUNT, HOUSE_COST, HOUSE_RENT_BONUS

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
    
    # 1. LAND ON INCOME TAX (Pos 4)
    # Alice starts at 0, rolls 4.
    with patch('moneypoly.dice.Dice.roll', return_value=4), \
         patch('moneypoly.dice.Dice.is_doubles', return_value=False):
        clean_game.play_turn()
    
    assert alice.position == 4
    assert alice.balance == 1500 - INCOME_TAX_AMOUNT # 1300
    
    # 2. LAND ON CHANCE (Pos 7)
    # Alice at 4, rolls 3.
    # Mock a "receive" card for $200.
    receive_card = {"description": "Bank Error", "action": "collect", "value": 200}
    
    with patch('moneypoly.dice.Dice.roll', return_value=3), \
         patch('moneypoly.dice.Dice.is_doubles', return_value=False), \
         patch('moneypoly.cards.Deck.draw', return_value=receive_card):
        clean_game.current_player_idx = 0 # Ensure it's Alice's turn again
        clean_game.play_turn()
        
    assert alice.position == 7
    # 1300 + 200 = 1500
    assert alice.balance == 1500
    
    # 3. MONOPOLY AND HOUSES (Nodes 48-52)
    # Logic: Alice acquires Med Ave (1) and Baltic Ave (3).
    med = clean_game.resources["board"].get_property_at(1)
    baltic = clean_game.resources["board"].get_property_at(3)
    
    med.owner = alice
    baltic.owner = alice
    alice.properties.extend([med, baltic])
    
    # Verify group ownership
    assert med.group.all_owned_by(alice) is True
    
    # Alice builds a house.
    # Menu flow: Choice 7 (Build), Choice 1 (Med Ave), default (and exit)
    with patch('moneypoly.ui.safe_int_input', side_effect=[7, 1, 0]):
        clean_game._offer_pre_roll_options(alice)
        
    assert med.houses == 1
    assert alice.balance == 1500 - HOUSE_COST # 1400
    
    # 4. RENT VERIFICATION WITH HOUSES
    # Bob lands on Med Ave (Pos 1).
    # Normal rent: 2. Monopoly rent: 4. House bonus: 50. Total: 54.
    initial_bob_balance = bob.balance
    initial_alice_balance = alice.balance
    
    clean_game.pay_rent(bob, med)
    
    assert bob.balance == initial_bob_balance - 54
    assert alice.balance == initial_alice_balance + 54
    
    print("\n[EXHAUSTIVE] Super Workflow Verified: Tax, Cards, Houses, and Monopoly Rent.")

def test_tc16_luxury_tax(clean_game):
    """TC-16: Luxury Tax Tile (Pos 38) - Node 18a, 18b branch."""
    alice = clean_game.players[0]
    from moneypoly.config import LUXURY_TAX_AMOUNT
    
    with patch('moneypoly.dice.Dice.roll', return_value=38), \
         patch('moneypoly.dice.Dice.is_doubles', return_value=False):
        clean_game.play_turn()
        
    assert alice.position == 38
    assert alice.balance == 1500 - LUXURY_TAX_AMOUNT
