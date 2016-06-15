
from model import (
    GameContext,
    Player,
)
from base_cards import *
from sets import *

sample_kingdom = [
    Copper,
    Silver,
    Gold,
    Estate,
    Duchy,
    Province,
    Smithy,
    Village,
    Laboratory,
    Woodcutter,
    Militia,
]


def game():
    g = GameContext(sample_kingdom)
    g.print_supply()
    g.add_player(Player("Marin"))
    g.start_game()
    while True:
        input_str = input().strip()
        g.handle_input(input_str)

game()
