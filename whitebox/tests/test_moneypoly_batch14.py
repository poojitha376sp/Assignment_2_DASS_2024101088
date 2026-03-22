"""
White Box Test Suite for MoneyPoly (Part 1.3)
Focus: Mortgage Bank Accounting Regression
"""
import pytest
from moneypoly.game import Game
from moneypoly.config import BANK_STARTING_FUNDS, STARTING_BALANCE


@pytest.fixture
def clean_game():
    return Game(["Alice", "Bob"])


def test_tc55_mortgage_reduces_bank_balance(clean_game):
    """TC-55: Mortgaging a property should reduce the bank's cash reserves."""
    player = clean_game.players[0]
    prop = clean_game.resources["board"].get_property_at(1)
    prop.owner = player
    player.add_property(prop)

    before = clean_game.resources["bank"].get_balance()
    result = clean_game.mortgage_property(player, prop)

    assert result is True
    assert clean_game.resources["bank"].get_balance() == before - prop.financials["mortgage"]
    assert player.balance == STARTING_BALANCE + prop.financials["mortgage"]


def test_tc56_mortgage_does_not_change_bank_when_rejected(clean_game):
    """TC-56: Failed mortgage attempts should leave the bank balance unchanged."""
    player = clean_game.players[0]
    prop = clean_game.resources["board"].get_property_at(3)
    before = clean_game.resources["bank"].get_balance()

    result = clean_game.mortgage_property(player, prop)

    assert result is False
    assert clean_game.resources["bank"].get_balance() == before
    assert player.balance == STARTING_BALANCE
