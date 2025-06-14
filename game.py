from treys import Card, Evaluator
from utils import *
from node import Node


class Solver:
    def __init__(self):
        self.game_state = GameState()
        self.flop_cards = []
        self.IPRange = Range()
        self.OOPRange = Range()
        self.betting_percents = {'IP': 0.5, 'OOP': 0.5}



# game_state = GameState()
# flop_cards = [Card.new('2d'), Card.new('3h'), Card.new('4s')]
# game_state.create_new_flop(flop_cards[0], flop_cards[1], flop_cards[2])
# root = Node(game_state, 'OOP', 'action')
# root.generate_children(1)
# print(root.to_string_tree())

solver = Solver()
solver.flop_cards = [Card.new('2d'), Card.new('3h'), Card.new('4s')]
hands = [Hand([Card.new('2d'), Card.new('3h')]), Hand([Card.new('4s'), Card.new('5c')])]
for hand in hands:
    solver.IPRange.add_hand(hand)
    solver.OOPRange.add_hand(hand)
solver.game_state.generate_default_freqs(solver.IPRange, solver.OOPRange)
print(solver.game_state.IPfreqs)
print(solver.game_state.OOPfreqs)
