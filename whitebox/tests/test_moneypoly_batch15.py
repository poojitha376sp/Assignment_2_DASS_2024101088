"""
White Box Test Suite for MoneyPoly (Part 1.3)
Focus: Empty-Game Safety
"""
import pytest
from moneypoly.game import Game


def test_tc57_current_player_empty_game_raises(clean_game=None):
    """TC-57: Asking for a player in an empty game should fail clearly."""
    game = Game([])

    with pytest.raises(ValueError):
        game.current_player()


def test_tc58_advance_turn_empty_game_is_noop():
    """TC-58: Advancing turns in an empty game should not crash."""
    game = Game([])

    game.advance_turn()

    assert game.turn_info["index"] == 0
    assert game.turn_info["count"] == 0


def test_tc59_play_turn_empty_game_is_noop():
    """TC-59: Playing a turn in an empty game should do nothing."""
    game = Game([])

    game.play_turn()

    assert game.turn_info["count"] == 0
    assert game.players == []
