from treys import Card, Evaluator
from tree.utils import *
from tree.node import Node


class Solver:
    def __init__(self):
        self.game_state = GameState()
        self.flop_cards = [Card.new('3d'), Card.new('Jh'), Card.new('As')]
        self.game_state.create_new_flop(self.flop_cards[0], self.flop_cards[1], self.flop_cards[2])
        self.game_state.add_turn_and_river(Card.new('7d'), Card.new('8h'))
        self.IPRange = Range()
        self.OOPRange = Range()
        self.betting_percents = {'IP': 0.5, 'OOP': 0.5}
        self.root = None