from software_design_patterns.behavioral.state_pattern import *


def test_state_heads_or_tails():
    player_heads = Player("Alice", 20)
    player_tails = Player("Bob", 20)
    game = HeadsOrTails(player_heads, player_tails, 10)

    print("\n")
    game.play()

    assert game.winner is not None
    assert game.winner.balance == player_heads.balance + player_tails.balance
    assert game.state == State.END
