"""
White Box Test Suite for MoneyPoly (Part 1.3)
Focus: Trade, Mortgage, and Jail Card Branches
"""
import pytest
from unittest.mock import patch
from moneypoly.game import Game
from moneypoly.config import STARTING_BALANCE


@pytest.fixture
def clean_game():
    return Game(["Alice", "Bob"])


def test_tc22_jail_free_card_release(clean_game):
    """TC-22: A jail-free card should release the player and consume the card."""
    player = clean_game.players[0]
    player.go_to_jail()
    player.jail_info["cards"] = 1

    with patch('moneypoly.ui.confirm', return_value=True), \
         patch('moneypoly.dice.Dice.roll', return_value=4), \
         patch('builtins.input', return_value='s'):
        clean_game._handle_jail_turn(player)

    assert player.jail_info["in_jail"] is False
    assert player.jail_info["cards"] == 0
    assert player.position == 14


def test_tc23_trade_success(clean_game):
    """TC-23: A valid trade should move the property and cash between players."""
    seller = clean_game.players[0]
    buyer = clean_game.players[1]
    prop = clean_game.resources["board"].get_property_at(1)
    prop.owner = seller
    seller.add_property(prop)

    result = clean_game.trade(seller, buyer, prop, 100)

    assert result is True
    assert prop.owner == buyer
    assert prop in buyer.properties
    assert prop not in seller.properties
    assert seller.balance == STARTING_BALANCE + 100
    assert buyer.balance == STARTING_BALANCE - 100


def test_tc24_trade_rejected_for_low_cash(clean_game):
    """TC-24: Trade must fail when the buyer cannot afford the agreed cash."""
    seller = clean_game.players[0]
    buyer = clean_game.players[1]
    prop = clean_game.resources["board"].get_property_at(3)
    prop.owner = seller
    seller.add_property(prop)
    buyer.balance = 20

    result = clean_game.trade(seller, buyer, prop, 50)

    assert result is False
    assert prop.owner == seller
    assert prop in seller.properties
    assert prop not in buyer.properties
    assert buyer.balance == 20


def test_tc25_mortgage_and_unmortgage_success(clean_game):
    """TC-25: Mortgaging and then unmortgaging should update balances correctly."""
    player = clean_game.players[0]
    prop = clean_game.resources["board"].get_property_at(6)
    prop.owner = player
    player.add_property(prop)

    mortgage_result = clean_game.mortgage_property(player, prop)
    mortgage_value = prop.financials["mortgage"]
    unmortgage_cost = int(mortgage_value * 1.1)

    assert mortgage_result is True
    assert prop.is_mortgaged is True
    assert player.balance == STARTING_BALANCE + mortgage_value

    player.balance = unmortgage_cost
    unmortgage_result = clean_game.unmortgage_property(player, prop)

    assert unmortgage_result is True
    assert prop.is_mortgaged is False
    assert player.balance == 0


def test_tc26_mortgage_rejected_for_wrong_owner(clean_game):
    """TC-26: A player cannot mortgage a property they do not own."""
    alice = clean_game.players[0]
    bob = clean_game.players[1]
    prop = clean_game.resources["board"].get_property_at(9)
    prop.owner = bob
    bob.add_property(prop)

    result = clean_game.mortgage_property(alice, prop)

    assert result is False
    assert prop.is_mortgaged is False
    assert alice.balance == STARTING_BALANCE
    assert bob.balance == STARTING_BALANCE