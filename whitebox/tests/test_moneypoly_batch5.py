"""
White Box Test Suite for MoneyPoly (Part 1.3)
Focus: Edge Cases, Card Payouts, and Branch Completeness
"""
import pytest
from moneypoly.game import Game


@pytest.fixture
def clean_game():
    return Game(["Alice", "Bob"])


def test_tc17_purchase_exact_balance(clean_game):
    """TC-17: Buying with exactly the listed price should still succeed."""
    player = clean_game.players[0]
    prop = clean_game.resources["board"].get_property_at(1)
    player.balance = prop.financials["price"]

    result = clean_game.buy_property(player, prop)

    assert result is True
    assert prop.owner == player
    assert player.balance == 0