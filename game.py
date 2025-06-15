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
solver.flop_cards = [Card.new('3d'), Card.new('Jh'), Card.new('As')]

hands = [Hand([Card.new('Qd'), Card.new('Qh')]), Hand([Card.new('Ad'), Card.new('Kc')])]
for hand in hands:
    solver.IPRange.add_hand(hand)
hands2 = [Hand([Card.new('Ac'), Card.new('9d')]), Hand([Card.new('5d'), Card.new('2s')])]
for hand in hands2:
    solver.OOPRange.add_hand(hand)

solver.game_state.add_ranges(solver.IPRange, solver.OOPRange)
solver.game_state.generate_default_freqs(solver.IPRange, solver.OOPRange)
solver.game_state.create_new_flop(solver.flop_cards[0], solver.flop_cards[1], solver.flop_cards[2])
solver.game_state.add_turn_and_river(Card.new('7d'), Card.new('8h'))
root = Node(solver.game_state.__copy__(), 'OOP', 'action')
root.generate_children(2)
root.calc_values()

print("\n")
print(f"OOP regret: {root.gamestate.OOPRegret}")

print("\nOOP checks\n")
check_node = root.children[2]
print(f"IP regret: {check_node.gamestate.IPRegret}")

print("\nIP raises\n")
raise_node = check_node.children[1]
print(f"IP contribution: {raise_node.gamestate.contribution}")
print(f"OOP regret: {raise_node.gamestate.OOPRegret}")

print("\nOOP calls\n")
call_node = raise_node.children[2]
print(call_node)
print(f"IP contribtion: {call_node.gamestate.contribution}")
print(f"IP regret: {call_node.gamestate.IPRegret}")

# sampletree = Node(solver.game_state, 'OOP', 'action')
# terminal1 = Node(solver.game_state.__copy__(), 'IP', 'terminal')
# terminal2 = Node(solver.game_state.__copy__(), 'IP', 'terminal')
# terminal3 = Node(solver.game_state.__copy__(), 'IP', 'terminal')

# sampletree.children = [terminal1, terminal2, terminal3]
# sampletree.calc_values()
# print(f"IP values: {sampletree.gamestate.IPvalues}")
# print(f"IP regret: {sampletree.gamestate.IPRegret}")
# print("\n")
# print(f"OOP values: {sampletree.gamestate.OOPvalues}")
# print(f"OOP regret: {sampletree.gamestate.OOPRegret}")



