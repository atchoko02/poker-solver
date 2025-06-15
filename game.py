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

hands = [Hand([Card.new('Ad'), Card.new('Kh')]), Hand([Card.new('Qs'), Card.new('Jc')])]
for hand in hands:
    solver.IPRange.add_hand(hand)
hands2 = [Hand([Card.new('Ac'), Card.new('Kc')]), Hand([Card.new('Qd'), Card.new('Js')])]
for hand in hands2:
    solver.OOPRange.add_hand(hand)

solver.game_state.add_ranges(solver.IPRange, solver.OOPRange)
solver.game_state.generate_default_freqs(solver.IPRange, solver.OOPRange)
solver.game_state.create_new_flop(solver.flop_cards[0], solver.flop_cards[1], solver.flop_cards[2])
root = Node(solver.game_state, 'OOP', 'action')
root.generate_children(1)
root.calc_values()
print(solver.game_state.IPvalues)
print(solver.game_state.OOPvalues)

