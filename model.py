
from random import shuffle

from constants import (
    TREASURE,
    VICTORY,
    ACTION,
)
from base_cards import (
    Estate,
    Copper,
)


class SupplyPile():

    def __init__(self, card):
        self.card = card
        self.remaining = self.card.supply

    def print_pile(self):
        remaining = (
            str(self.remaining) if self.remaining is not None else " "
        ).rjust(2)
        print ("%s %s" % (remaining, self.card.name))


class Supply():

    def __init__(self):
        self.lookup_ordered = []
        self.lookup_by_name = {}

    def add_card(self, card_func):
        pile = SupplyPile(card_func())
        key = pile.card.name.lower()
        self.lookup_ordered.append(pile)
        self.lookup_by_name[key] = pile

    def can_gain(self, card):
        remaining = self.lookup_by_name[card.name.lower()].remaining
        return remaining is None or remaining > 0

    def is_game_over(self):
        empty_piles = 0
        for pile in self.lookup_ordered:
            if pile.remaining is not None and pile.remaining == 0:
                empty_piles += 1
                if pile.name in ["Province", "Colony"]:
                    return True
        return empty_piles >= 3


class GameContext():

    def __init__(self, kingdom_cards):
        self.supply = Supply()
        self.add_kingdom_cards(kingdom_cards)
        self.players = []
        self._current_player = 0
        self.current_turn = None

    def add_kingdom_cards(self, card_funcs):
        for card_func in card_funcs:
            self.add_kingdom_card(card_func)

    def add_kingdom_card(self, card_func):
        self.supply.add_card(card_func)

    def add_player(self, player):
        self.players.append(player)

    def current_player(self):
        return self.players[self._current_player]

    def opponents(self):
        current = self.current_player()
        return [
            player
            for player in self.players
            if player != current
        ]

    def start_game(self):
        self.current_turn = TurnContext(self)

    def end_turn(self):
        self.current_player().end_turn()
        self.current_turn.end()
        if self.supply.is_game_over():
            print ('game over!')
            return
        self._current_player = (
            self._current_player + 1
        ) % len(self.players)
        self.current_turn = TurnContext(self)

    def print_supply(self):
        print ("==========\n # card\n----------")
        for pile in self.supply.lookup_ordered:
            pile.print_pile()

    def play_all_treasure(self):
        to_play = []
        for card in self.current_player().deck.hand:
            if TREASURE in card.types:
                to_play.append(card)
        for card in to_play:
            self.current_turn.play_card(card)

    def handle_input(self, input_str):
        if "play " in input_str:
            input_str = input_str.split("play ")[1]
            self.current_turn.play_str(input_str)
        if "buy " in input_str:
            self.play_all_treasure()
            input_str = input_str.split("buy ")[1]
            self.current_turn.buy_str(input_str)
        if "end" == input_str:
            self.end_turn()

        if self.current_turn.buys == 0:
            # todo assumes we play all treasure
            self.end_turn()


class Deck():

    def __init__(self):
        self.deck = []
        self.discard = []
        self.hand = []
        self.battlefield = []
        for _ in range(3):
            self.gain(Estate())
        for _ in range(7):
            self.gain(Copper())
        self.end_turn()

    def gain(self, card):
        self.discard.append(card)
        print ("Gained: %s" % card.name)

    def draw_one(self):
        if not self.deck:
            self.deck = self.discard
            self.discard = []
            shuffle(self.deck)
        if self.deck:
            card = self.deck.pop()
            self.hand.append(card)

    def draw(self, quantity):
        for _ in range(quantity):
            self.draw_one()
        self.print_hand()

    def discard_one(self):
        # todo user/ai input
        self.discard.append(self.hand.pop())

    def discard_to(self, quantity):
        while len(self.hand) > quantity:
            self.discard_one()
        self.print_hand()

    def play(self, card):
        to_pop = None
        for i in range(len(self.hand)):
            if self.hand[i].id == card.id:
                to_pop = i
        self.battlefield.append(self.hand.pop(to_pop))
        self.print_hand()

    def end_turn(self):
        self.discard.extend(self.hand)
        self.hand = []
        self.discard.extend(self.battlefield)
        self.battlefield = []
        self.draw(5)

    def print_hand(self):
        cards = ", ".join([
            card.name
            for card in self.hand
        ])
        print ("Hand: %s" % cards)
        cards = ", ".join([
            card.name
            for card in self.battlefield
        ])
        print ("Play: %s" % cards)


class Player():

    def __init__(self, name=None):
        self.name = name
        self.deck = Deck()

    def gain(self, card):
        self.deck.gain(card)

    def play(self, card):
        self.deck.play(card)

    def end_turn(self):
        self.deck.end_turn()


class TurnContext():

    def __init__(self, game_ctx):
        self.game_ctx = game_ctx
        self.actions = 1
        self.buys = 1
        self.cash = 0
        self.buy_phase = False
        self.player = self.game_ctx.current_player()
        print ("%s's turn." % self.player.name)
        self.game_ctx.current_player().deck.print_hand()

    def add_cash(self, value):
        self.cash = max(self.cash + value, 0)

    def add_action(self, value):
        self.actions = max(self.actions + value, 0)

    def add_buy(self, value):
        self.buys = max(self.buys + value, 0)

    def add_card(self, value):
        for i in range(0, value):
            self.player_ctx.draw_card()

    def try_gain(self, value):
        # todo with cards that trigger on gaining others
        return True

    def try_trash(self, value):
        # todo with cards that trigger on trashing others
        return True

    def try_play(self, value):
        return self.actions > 0 and not self.buy_phase

    def play_str(self, card_name):
        for card in self.player.deck.hand:
            if card.name.lower() == card_name:
                return self.play_card(card)
        print ("card not found")

    def buy_str(self, card_name):
        for pile in self.game_ctx.supply.lookup_ordered:
            card = pile.card
            if card.name.lower() == card_name:
                return self.buy_card(card)
        print ("card not found")

    def buy_card(self, card):
        exists = self.game_ctx.supply.can_gain(card)
        afford = card.price(self.game_ctx) <= self.cash
        if exists and afford and self.buys > 0:
            self.buys -= 1
            self.player.gain(card)
            card.on_gain(self)
        else:
            print ('cant afford %s' % card.name)
        return

    def play_card(self, card):
        if TREASURE in card.types:
            self.buy_phase = True
        if ACTION in card.types:
            if self.buy_phase:
                raise Exception
            self.actions -= 1
        self.player.play(card)
        card.on_play(self)

    def end(self):
        # todo?
        pass

    def plus_card(self, quantity):
        self.player.deck.draw(quantity)

    def plus_action(self, quantity):
        self.add_action(quantity)

    def plus_cash(self, quantity):
        self.add_cash(quantity)

    def plus_buy(self, quantity):
        self.add_buy(quantity)
