
from base_cards import (
    _Card,
)
from constants import (
    TREASURE,
    VICTORY,
    ACTION,
)


class Village(_Card):

    name = 'Village'
    types = [ACTION]
    cost = 3

    def on_play(self, ctx):
        ctx.plus_card(1)
        ctx.plus_action(2)


class Smithy(_Card):

    name = 'Smithy'
    types = [ACTION]
    cost = 4

    def on_play(self, ctx):
        ctx.plus_card(3)


class Laboratory(_Card):

    name = 'Laboratory'
    types = [ACTION]
    cost = 5

    def on_play(self, ctx):
        ctx.plus_card(2)
        ctx.plus_action(1)


class Woodcutter(_Card):

    name = 'Woodcutter'
    types = [ACTION]
    cost = 3

    def on_play(self, ctx):
        ctx.plus_cash(2)
        ctx.plus_buy(1)


class Militia(_Card):

    name = 'Militia'
    types = [ACTION]
    cost = 4

    def on_play(self, ctx):
        ctx.plus_cash(2)
        for player in ctx.opponents():
            player.deck.discard_to(3)
