"""
White Box Test Suite for MoneyPoly (Part 1.3)
Focus: Idempotent State Changes and Hard Boundaries
"""
import pytest
from moneypoly.game import Game
from moneypoly.bank import Bank
from moneypoly.property import Property
from moneypoly.config import BANK_STARTING_FUNDS, STARTING_BALANCE


@pytest.fixture
def clean_game():
    return Game(["Alice", "Bob"])


def test_tc36_bank_loan_rejects_overdraft():
    """TC-36: A loan larger than the bank's balance should be rejected."""
    bank = Bank()
    with pytest.raises(ValueError):
        bank.give_loan(type("P", (), {"name": "Alice", "add_money": lambda self, amount: None})(), BANK_STARTING_FUNDS + 1)


def test_tc37_bank_pay_out_zero_is_noop():
    """TC-37: Paying out zero should do nothing and return zero."""
    bank = Bank()
    before = bank.get_balance()

    result = bank.pay_out(0)

    assert result == 0
    assert bank.get_balance() == before


def test_tc38_property_mortgage_is_idempotent():
    """TC-38: Mortgaging the same property twice should not pay twice."""
    prop = Property("Test", 99, {"price": 100, "rent": 10}, None)

    first = prop.mortgage()
    second = prop.mortgage()

    assert first == 50
    assert second == 0
    assert prop.is_mortgaged is True


def test_tc39_property_unmortgage_without_mortgage_is_noop():
    """TC-39: Unmortgaging an un-mortgaged property should do nothing."""
    prop = Property("Test", 99, {"price": 100, "rent": 10}, None)

    result = prop.unmortgage()

    assert result == 0
    assert prop.is_mortgaged is False


def test_tc40_property_group_owner_counts_ignore_none_owner(clean_game):
    """TC-40: Owner counts should skip unowned properties and count real owners."""
    board = clean_game.resources["board"]
    alice = clean_game.players[0]
    med = board.get_property_at(1)
    baltic = board.get_property_at(3)
    med.owner = alice
    alice.add_property(med)
    counts = med.group.get_owner_counts()

    assert counts[alice] == 1
    assert counts.get(None) is None
    assert baltic.group is med.group