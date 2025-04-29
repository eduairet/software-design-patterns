from enum import Enum, auto
from random import choice


class Player:
    def __init__(self, name: str, balance: int):
        self.name = name
        self.balance = balance


class State(Enum):
    START = auto()
    PLAYING = auto()
    END = auto()


class Coin(Enum):
    HEADS = auto()
    TAILS = auto()


class HeadsOrTails:
    def __init__(self, player_heads: Player, player_tails: Player, bet: int):
        self.player_heads = player_heads
        self.player_tails = player_tails
        self.state = State.START
        self.bet = bet
        self.winner = None

    def play(self):
        if self.state == State.START:
            print(
                f"{self.player_heads.name} and {self.player_tails.name} are ready to play!"
            )
            self.state = State.PLAYING

        while self.state == State.PLAYING:
            self._play_round()

    def _play_round(self):
        player_heads_bet = min(self.bet, self.player_heads.balance)
        player_tails_bet = min(self.bet, self.player_tails.balance)

        round_result = choice([Coin.HEADS, Coin.TAILS])
        print(f"Round result: {round_result.name} |", end=" ")

        if round_result == Coin.HEADS:
            self._update_balances(player_heads_bet, -player_tails_bet)
        else:
            self._update_balances(-player_heads_bet, player_tails_bet)

        self._check_game_over()

    def _update_balances(self, heads_change: int, tails_change: int):
        self.player_heads.balance += heads_change
        self.player_tails.balance += tails_change

    def _check_game_over(self):
        if self.player_heads.balance == 0 or self.player_tails.balance == 0:
            self.winner = (
                self.player_heads
                if self.player_heads.balance > 0
                else self.player_tails
            )
            print(
                f"Game over! Winner is: {self.winner.name} with balance {self.winner.balance}"
            )
            self.state = State.END
        else:
            print(
                f"{self.player_heads.name} balance: {self.player_heads.balance}, "
                f"{self.player_tails.name} balance: {self.player_tails.balance}"
            )
