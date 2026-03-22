"""
White Box Test Suite for MoneyPoly (Part 1.3)
Focus: Monopoly Rent with Mortgaged Properties
"""
import pytest
from moneypoly.game import Game


@pytest.fixture
def clean_game():
    return Game(["Alice", "Bob"])


def test_tc53_mortgaged_property_breaks_monopoly_rent(clean_game):
    """TC-53: A mortgaged property should prevent full-group double rent."""
    alice = clean_game.players[0]
    med = clean_game.resources["board"].get_property_at(1)
    baltic = clean_game.resources["board"].get_property_at(3)

    med.owner = alice
    baltic.owner = alice
    alice.add_property(med)
    alice.add_property(baltic)
    baltic.is_mortgaged = True

    rent = med.get_rent()

    assert rent == med.financials["rent"]


def test_tc54_unmortgaging_restores_group_rent_only_when_full_group_is_free(clean_game):
    """TC-54: Double rent should return only after the whole group is free of mortgages."""
    alice = clean_game.players[0]
    med = clean_game.resources["board"].get_property_at(1)
    baltic = clean_game.resources["board"].get_property_at(3)

    med.owner = alice
    baltic.owner = alice
    alice.add_property(med)
    alice.add_property(baltic)
    baltic.is_mortgaged = True

    assert med.get_rent() == med.financials["rent"]

    baltic.unmortgage()

    assert med.get_rent() == med.financials["rent"] * 2
