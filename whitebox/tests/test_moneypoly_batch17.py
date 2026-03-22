"""
White Box Test Suite for MoneyPoly (Part 1.3)
Focus: Menu Trade Branch, Jail Fine Safety, and Mortgage Redemption Rounding
"""
import pytest
from unittest.mock import patch

from moneypoly.game import Game
from moneypoly.property import Property
from moneypoly.config import STARTING_BALANCE


@pytest.fixture
def clean_game():
    return Game(["Alice", "Bob"])


def test_tc61_menu_trade_executes_valid_trade(clean_game):
    """TC-61: The trade menu should be able to complete a valid trade."""
    alice, bob = clean_game.players
    prop = clean_game.resources["board"].get_property_at(1)
    prop.owner = alice
    alice.add_property(prop)

    with patch("moneypoly.ui.safe_int_input", side_effect=[5, 1, 1, 100, 0]):
        clean_game.interactive_menu(alice)

    assert prop.owner == bob
    assert prop in bob.properties
    assert prop not in alice.properties
    assert alice.balance == STARTING_BALANCE + 100
    assert bob.balance == STARTING_BALANCE - 100


def test_tc62_jail_fine_bankruptcy_still_eliminates_player(clean_game):
    """TC-62: Paying the jail fine should still eliminate a bankrupt player safely."""
    player = clean_game.players[0]
    player.go_to_jail()
    player.balance = 40

    with patch("moneypoly.ui.confirm", return_value=True), \
         patch("moneypoly.dice.Dice.roll", return_value=1), \
         patch("builtins.input", return_value="s"):
        clean_game._handle_jail_turn(player)

    assert player not in clean_game.players
    assert player.is_eliminated is True


def test_tc63_property_unmortgage_rounds_cost_upward():
    """TC-63: Unmortgaging should round the repayment up rather than down."""
    prop = Property("Park Place", 37, {"price": 350, "rent": 35}, None)
    prop.mortgage()

    cost = prop.unmortgage()

    assert cost == 193
    assert prop.is_mortgaged is False


def test_tc64_game_unmortgage_rounds_cost_upward(clean_game):
    """TC-64: Game-level unmortgaging should also round the cost up."""
    player = clean_game.players[0]
    prop = clean_game.resources["board"].get_property_at(37)
    prop.owner = player
    player.add_property(prop)
    prop.mortgage()
    player.balance = 193

    result = clean_game.unmortgage_property(player, prop)

    assert result is True
    assert prop.is_mortgaged is False
    assert player.balance == 0