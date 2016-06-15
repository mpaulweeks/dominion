
from constants import (
    TREASURE,
    VICTORY,
    ACTION,
)


class _Card():

    name = None
    types = set()
    cost = 0
    supply = 10
    vp = 0

    @property
    def id(self):
        return self.name

    def name(self, ctx):
        pass

    def on_trash(self, ctx):
        pass

    def on_play(self, ctx):
        pass

    def on_gain(self, ctx):
        pass

    def gain(self, ctx):
        if ctx.try_gain(self):
            self.on_gain(ctx)

    def trash(self, ctx):
        if ctx.try_trash(self):
            self.on_trash(ctx)

    def play(self, ctx):
        if ctx.try_play(self):
            ctx.play_card(self)

    def price(self, ctx):
        return self.cost


class Copper(_Card):

    name = 'Copper'
    types = [TREASURE]
    cost = 0
    supply = None

    def on_play(self, ctx):
        ctx.add_cash(1)


class Silver(_Card):

    name = 'Silver'
    types = [TREASURE]
    cost = 3
    supply = None

    def on_play(self, ctx):
        ctx.add_cash(2)


class Gold(_Card):

    name = 'Gold'
    types = [TREASURE]
    cost = 6
    supply = None

    def on_play(self, ctx):
        ctx.add_cash(3)


class Estate(_Card):

    name = 'Estate'
    types = [VICTORY]
    cost = 2
    supply = 8
    vp = 1


class Duchy(_Card):

    name = 'Duchy'
    types = [VICTORY]
    cost = 5
    supply = 8
    vp = 3


class Province(_Card):

    name = 'Province'
    types = [VICTORY]
    cost = 8
    supply = 8
    vp = 6
