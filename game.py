from treys import Card, Evaluator
from utils import *
from node import Node


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



# game_state = GameState()
# flop_cards = [Card.new('2d'), Card.new('3h'), Card.new('4s')]
# game_state.create_new_flop(flop_cards[0], flop_cards[1], flop_cards[2])
# root = Node(game_state, 'OOP', 'action')
# root.generate_children(1)
# print(root.to_string_tree())

# solver = Solver()
# solver.flop_cards = [Card.new('3d'), Card.new('Jh'), Card.new('As')]

# for i in range(9, 15):
#     solver.IPRange.add_pocket_pair(str(i))
#     solver.OOPRange.add_pocket_pair(str(i))

# for i in range(10, 15):
#     for j in range(10, 15):
#         if i != j:
#             solver.IPRange.add_suited_hand(str(i), str(j))
#             solver.OOPRange.add_suited_hand(str(i), str(j))

# solver.game_state.add_ranges(solver.IPRange, solver.OOPRange)
# solver.game_state.generate_default_freqs(solver.IPRange, solver.OOPRange)
# solver.game_state.create_new_flop(solver.flop_cards[0], solver.flop_cards[1], solver.flop_cards[2])
# solver.game_state.add_turn_and_river(Card.new('7d'), Card.new('8h'))
# root = Node(solver.game_state.__copy__(), 'OOP', 'action')
# print('starting tree')
# root.generate_children(3)
# print('ended tree')

# def get_current_ev(position):
#     if position == 'OOP':
#         value = 0
#         for hand in root.gamestate.OOPvalues:
#             value += root.gamestate.OOPvalues[hand]
#         return value / len(root.gamestate.OOPvalues)
#     elif position == 'IP':
#         value = 0
#         for hand in root.gamestate.IPvalues:
#             value += root.gamestate.IPvalues[hand]
#         return value / len(root.gamestate.IPvalues)


# for i in range(100):
#     root.calc_values()
#     OOP_starting_ev = get_current_ev('OOP')
#     print(f"Iteration {i+1} - OOP EV: {OOP_starting_ev}")
#     IP_starting_ev = get_current_ev('IP')
#     print(f"Iteration {i+1} - IP EV: {IP_starting_ev}")
#     root.calc_new_strat()
#     root.calc_values()
    


# print("\n")
# print(f"OOP regret: {root.gamestate.OOPRegret}")
# print(f"OOP stratagy: {root.gamestate.OOPfreqs}")
# print(f"OOP values: {root.gamestate.OOPvalues}")
# print(f"IP values: {root.gamestate.IPvalues}")

# raise_node = root.children[1]
# print("\n OOP raise \n")

# print(f"IP regret: {raise_node.gamestate.IPRegret}")
# print(f"IP stratagy: {raise_node.gamestate.IPfreqs}")


