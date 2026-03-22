"""
White Box Test Suite for MoneyPoly (Part 1.3)
Focus: Bankruptcy Triggered by Card Payments
"""
import pytest
from moneypoly.game import Game


@pytest.fixture
def clean_game():
    return Game(["Alice", "Bob", "Charlie"])


def test_tc51_collect_from_all_eliminates_bankrupt_opponent(clean_game):
    """TC-51: A player who falls below zero from a group-payment card should be removed."""
    alice, bob, charlie = clean_game.players
    bob.balance = 20
    charlie.balance = 100

    clean_game._apply_card(alice, {"action": "collect_from_all", "value": 50})

    assert bob not in clean_game.players
    assert bob.is_eliminated is True
    assert charlie in clean_game.players


def test_tc52_birthday_card_eliminates_bankrupt_opponent(clean_game):
    """TC-52: Birthday card payments should also eliminate players who go bankrupt."""
    alice, bob, charlie = clean_game.players
    bob.balance = 5
    charlie.balance = 100

    clean_game._apply_card(alice, {"action": "birthday", "value": 10})

    assert bob not in clean_game.players
    assert bob.is_eliminated is True
    assert charlie in clean_game.players
