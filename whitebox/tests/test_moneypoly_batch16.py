"""
White Box Test Suite for MoneyPoly (Part 1.3)
Focus: List Mutation During Card-Payment Bankruptcy Cleanup
"""
import pytest
from moneypoly.game import Game


@pytest.fixture
def clean_game():
    return Game(["Alice", "Bob", "Charlie", "Dana"])


def test_tc60_collect_from_all_cleans_multiple_bankrupt_players(clean_game):
    """TC-60: Removing one bankrupt player should not skip the next one."""
    alice, bob, charlie, dana = clean_game.players
    bob.balance = 20
    charlie.balance = 10
    dana.balance = 100

    clean_game._apply_card(alice, {"action": "collect_from_all", "value": 50})

    assert bob not in clean_game.players
    assert charlie not in clean_game.players
    assert bob.is_eliminated is True
    assert charlie.is_eliminated is True
    assert dana in clean_game.players
