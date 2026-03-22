"""
White Box Test Suite for MoneyPoly (Part 1.3)
Focus: Helper Methods and Boundary State
"""
import pytest
from moneypoly.game import Game
from moneypoly.cards import CardDeck
from moneypoly.property import Property


@pytest.fixture
def clean_game():
    return Game(["Alice", "Bob"])


def test_tc41_board_purchasable_state_matrix(clean_game):
    """TC-41: Purchasable status should reflect ownership and mortgage state."""
    board = clean_game.resources["board"]
    prop = board.get_property_at(1)

    assert board.is_purchasable(1) is True

    prop.owner = clean_game.players[0]
    assert board.is_purchasable(1) is False

    prop.owner = None
    prop.is_mortgaged = True
    assert board.is_purchasable(1) is False

    assert board.is_purchasable(0) is False


def test_tc42_card_deck_cycles_and_counts():
    """TC-42: Card decks should cycle and report remaining cards correctly."""
    deck = CardDeck([
        {"action": "collect", "value": 10},
        {"action": "pay", "value": 5},
    ])

    first = deck.draw()
    second = deck.draw()
    third = deck.draw()

    assert first["action"] == "collect"
    assert second["action"] == "pay"
    assert third == first
    assert deck.cards_remaining() == 1


def test_tc43_net_worth_ignores_mortgaged_property(clean_game):
    """TC-43: Mortgaged properties should not count toward net worth."""
    player = clean_game.players[0]
    prop = clean_game.resources["board"].get_property_at(3)
    prop.owner = player
    player.add_property(prop)
    base_worth = player.net_worth()

    prop.is_mortgaged = True

    assert player.net_worth() == base_worth - prop.financials["price"]


def test_tc44_find_winner_with_no_players_returns_none():
    """TC-44: A game with no players should not have a winner."""
    game = Game([])

    assert game.find_winner() is None


def test_tc45_board_owner_lists_reflect_state(clean_game):
    """TC-45: Owned and unowned property lists should match board state."""
    board = clean_game.resources["board"]
    alice = clean_game.players[0]
    prop = board.get_property_at(1)
    prop.owner = alice
    alice.add_property(prop)

    owned = board.properties_owned_by(alice)
    unowned = board.unowned_properties()

    assert prop in owned
    assert prop not in unowned
    assert len(owned) == 1
