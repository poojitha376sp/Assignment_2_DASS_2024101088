"""
White Box Test Suite for MoneyPoly (Part 1.3)
Focus: UI, Bank Accounting, and Invalid Trade Inputs
"""
import pytest
from moneypoly.game import Game
from moneypoly.bank import Bank
from moneypoly import ui
from moneypoly.config import BANK_STARTING_FUNDS, STARTING_BALANCE


@pytest.fixture
def clean_game():
    return Game(["Alice", "Bob"])


def test_tc32_bank_collect_ignores_negative_values():
    """TC-32: Negative bank collections should not reduce bank funds."""
    bank = Bank()
    before = bank.get_balance()

    bank.collect(-100)

    assert bank.get_balance() == before


def test_tc33_print_board_ownership_does_not_crash(clean_game, capsys):
    """TC-33: Printing board ownership should work for a normal board state."""
    ui.print_board_ownership(clean_game.resources["board"])
    captured = capsys.readouterr()

    assert "Property Register" in captured.out
    assert "Mediterranean Avenue" in captured.out


def test_tc34_trade_rejects_negative_cash(clean_game):
    """TC-34: Trade should reject a negative cash amount instead of raising."""
    seller = clean_game.players[0]
    buyer = clean_game.players[1]
    prop = clean_game.resources["board"].get_property_at(1)
    prop.owner = seller
    seller.add_property(prop)

    result = clean_game.trade(seller, buyer, prop, -25)

    assert result is False
    assert prop.owner == seller
    assert seller.balance == STARTING_BALANCE
    assert buyer.balance == STARTING_BALANCE


def test_tc35_buy_property_rejects_negative_price(clean_game):
    """TC-35: Buying should reject a property with invalid negative pricing."""
    buyer = clean_game.players[0]
    prop = clean_game.resources["board"].get_property_at(3)
    prop.financials["price"] = -10

    result = clean_game.buy_property(buyer, prop)

    assert result is False
    assert prop.owner is None
    assert buyer.balance == STARTING_BALANCE
