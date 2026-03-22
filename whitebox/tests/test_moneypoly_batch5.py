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


def test_tc18_collect_from_all_card():
    """TC-18: Chance card that collects from every other player."""
    game = Game(["Alice", "Bob", "Charlie"])
    alice, bob, charlie = game.players
    alice.balance = 100
    bob.balance = 60
    charlie.balance = 40

    game._apply_card(alice, {"action": "collect_from_all", "value": 10})

    assert alice.balance == 120
    assert bob.balance == 50
    assert charlie.balance == 30


def test_tc19_birthday_card():
    """TC-19: Community Chest birthday card charges every opponent."""
    game = Game(["Ann", "Bill", "Cara"])
    ann, bill, cara = game.players
    ann.balance = 200
    bill.balance = 50
    cara.balance = 80

    game._apply_card(ann, {"action": "birthday", "value": 10})

    assert ann.balance == 220
    assert bill.balance == 40
    assert cara.balance == 70


def test_tc20_free_parking_no_effect(clean_game):
    """TC-20: Landing on Free Parking leaves balance unchanged."""
    player = clean_game.players[0]
    player.position = 19
    before = player.balance

    clean_game._move_and_resolve(player, 1)

    assert player.position == 20
    assert player.balance == before


def test_tc21_landing_on_own_property(clean_game):
    """TC-21: No rent is collected when the player lands on their own property."""
    player = clean_game.players[0]
    prop = clean_game.resources["board"].get_property_at(1)
    prop.owner = player
    player.properties.append(prop)
    before = player.balance

    clean_game._handle_property_tile(player, prop)

    assert player.balance == before