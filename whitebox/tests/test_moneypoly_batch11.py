"""
White Box Test Suite for MoneyPoly (Part 1.3)
Focus: Remaining Movement, Bank, Deck, and Board Helper Branches
"""
import pytest
from unittest.mock import patch
from moneypoly.game import Game
from moneypoly.bank import Bank
from moneypoly.cards import CardDeck
from moneypoly.property import Property, PropertyGroup
from moneypoly.config import BANK_STARTING_FUNDS, GO_SALARY, BOARD_SIZE, STARTING_BALANCE


@pytest.fixture
def clean_game():
    return Game(["Alice", "Bob"])


def test_tc46_move_exactly_to_go_awards_salary():
    """TC-46: Landing exactly on Go should award the salary."""
    player = Game(["Alice"]).players[0]
    player.position = 10

    new_position = player.move(BOARD_SIZE - 10)

    assert new_position == 0
    assert player.balance == STARTING_BALANCE + GO_SALARY


def test_tc47_bank_pay_out_overdraft_raises():
    """TC-47: The bank should refuse payouts larger than its reserves."""
    bank = Bank()

    with pytest.raises(ValueError):
        bank.pay_out(BANK_STARTING_FUNDS + 1)


def test_tc48_board_tile_types_for_special_and_blank_positions(clean_game):
    """TC-48: Board tile classification should distinguish special, property, and blank tiles."""
    board = clean_game.resources["board"]

    assert board.get_tile_type(0) == "go"
    assert board.get_tile_type(4) == "income_tax"
    assert board.get_tile_type(1) == "property"
    assert board.get_tile_type(2) == "community_chest"
    assert board.get_tile_type(6) == "property"
    assert board.get_tile_type(10) == "jail"
    assert board.get_tile_type(12) == "blank"
    assert board.is_special_tile(12) is False
    assert board.is_special_tile(0) is True


def test_tc49_carddeck_reshuffle_resets_index(clean_game):
    """TC-49: Reshuffling should reset the deck index and keep the same cards."""
    deck = CardDeck([
        {"action": "collect", "value": 10},
        {"action": "pay", "value": 5},
        {"action": "jail", "value": 0},
    ])
    deck.draw()
    deck.draw()

    with patch('random.shuffle', side_effect=lambda items: items.reverse()):
        deck.reshuffle()

    assert deck.index == 0
    assert deck.peek() == {"action": "jail", "value": 0}
    assert deck.cards_remaining() == 3


def test_tc50_property_group_counts_multiple_owners():
    """TC-50: Property group owner counting should track each owner correctly."""
    group = PropertyGroup("Test", "test")
    prop_a = Property("A", 1, {"price": 60, "rent": 2}, group)
    prop_b = Property("B", 3, {"price": 60, "rent": 4}, group)
    owner_one = type("Owner", (), {"name": "Alice"})()
    owner_two = type("Owner", (), {"name": "Bob"})()

    prop_a.owner = owner_one
    prop_b.owner = owner_two

    counts = group.get_owner_counts()

    assert counts[owner_one] == 1
    assert counts[owner_two] == 1
    assert group.size() == 2
