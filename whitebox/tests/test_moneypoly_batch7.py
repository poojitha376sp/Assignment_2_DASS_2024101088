"""
White Box Test Suite for MoneyPoly (Part 1.3)
Focus: Remaining State-Transition Bugs and Edge Cases
"""
import pytest
from unittest.mock import patch
from moneypoly.game import Game
from moneypoly.bank import Bank
from moneypoly.cards import CardDeck
from moneypoly.dice import Dice
from moneypoly.config import BANK_STARTING_FUNDS, STARTING_BALANCE


@pytest.fixture
def clean_game():
    return Game(["Alice", "Bob"])


def test_tc27_dice_roll_uses_six_sided_dice():
    """TC-27: Dice should roll values from 1 to 6, not 1 to 5."""
    seen_ranges = []

    def fake_randint(low, high):
        seen_ranges.append((low, high))
        return 6

    dice = Dice()
    with patch('random.randint', side_effect=fake_randint):
        total = dice.roll()

    assert seen_ranges == [(1, 6), (1, 6)]
    assert total == 12
    assert dice.is_doubles() is True


def test_tc28_unmortgage_keeps_property_mortgaged_when_funds_low(clean_game):
    """TC-28: Failed unmortgage should not clear the mortgage flag."""
    player = clean_game.players[0]
    prop = clean_game.resources["board"].get_property_at(6)
    prop.owner = player
    player.add_property(prop)
    prop.is_mortgaged = True

    player.balance = 1
    result = clean_game.unmortgage_property(player, prop)

    assert result is False
    assert prop.is_mortgaged is True
    assert player.balance == 1


def test_tc29_loan_reduces_bank_funds():
    """TC-29: Issuing a loan should reduce the bank's cash reserves."""
    bank = Bank()
    player = type("DummyPlayer", (), {"name": "Alice", "add_money": lambda self, amount: None})()
    player.balance = STARTING_BALANCE

    class LoanRecipient:
        def __init__(self):
            self.name = "Alice"
            self.balance = STARTING_BALANCE

        def add_money(self, amount):
            self.balance += amount

    recipient = LoanRecipient()
    bank.give_loan(recipient, 100)

    assert bank.get_balance() == BANK_STARTING_FUNDS - 100
    assert bank.loan_count() == 1
    assert bank.total_loans_issued() == 100
    assert recipient.balance == STARTING_BALANCE + 100


def test_tc30_empty_deck_remaining_and_repr_safe():
    """TC-30: Empty card decks should not crash when queried or printed."""
    deck = CardDeck([])

    assert deck.draw() is None
    assert deck.peek() is None
    assert deck.cards_remaining() == 0
    assert repr(deck) == "CardDeck(0 cards, next=0)"


def test_tc31_buy_property_rejects_existing_owner(clean_game):
    """TC-31: Buying should fail if the property already has an owner."""
    buyer = clean_game.players[0]
    other = clean_game.players[1]
    prop = clean_game.resources["board"].get_property_at(1)
    prop.owner = other
    other.add_property(prop)

    result = clean_game.buy_property(buyer, prop)

    assert result is False
    assert prop.owner == other
    assert prop in other.properties
    assert prop not in buyer.properties
    assert buyer.balance == STARTING_BALANCE