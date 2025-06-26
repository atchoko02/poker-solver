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

hands = [Hand([Card.new('Qd'), Card.new('Qh')]), Hand([Card.new('Ad'), Card.new('Kc')]), Hand([Card.new('5h'), Card.new('2d')])]
for hand in hands:
    solver.IPRange.add_hand(hand)
hands2 = [Hand([Card.new('Ac'), Card.new('3d')]), Hand([Card.new('Jd'), Card.new('2s')])]
for hand in hands2:
    solver.OOPRange.add_hand(hand)

solver.game_state.add_ranges(solver.IPRange, solver.OOPRange)
solver.game_state.generate_default_freqs(solver.IPRange, solver.OOPRange)
solver.game_state.create_new_flop(solver.flop_cards[0], solver.flop_cards[1], solver.flop_cards[2])
solver.game_state.add_turn_and_river(Card.new('7d'), Card.new('8h'))
root = Node(solver.game_state.__copy__(), 'OOP', 'action')
root.generate_children(3)


for i in range(100):
    root.calc_values()
    root.calc_new_strat('OOP')
    root.calc_values()
    root.calc_new_strat('IP')

print("\n")
print(f"OOP regret: {root.gamestate.OOPRegret}")
print(f"OOP stratagy: {root.gamestate.OOPfreqs}")
print(f"OOP values: {root.gamestate.OOPvalues}")
print(f"IP values: {root.gamestate.IPvalues}")

raise_node = root.children[1]
print("\n OOP rause \n")

print(f"IP regret: {raise_node.gamestate.IPRegret}")
print(f"IP stratagy: {raise_node.gamestate.IPfreqs}")


# sampletree = Node(solver.game_state, 'OOP', 'action')
# fold_node = Node(solver.game_state.__copy__(), 'IP', 'terminal')
# fold_node.isFold = True
# sampletree.children.append(fold_node)

# raise_state = solver.game_state.__copy__()
# raise_state.contribution['OOP'] += 50
# raise_state.pot += 50
# raise_node = Node(raise_state, 'IP', 'reaction')
# sampletree.children.append(raise_node)

# terminal1 = Node(solver.game_state.__copy__(), 'IP', 'terminal')
# sampletree.children.append(terminal1)

# for i in range(3):
#     call_state = raise_state.__copy__()
#     call_state.contribution['IP'] += 50
#     call_state.pot += 50
#     raise_node.children.append(Node(call_state, 'OOP', 'terminal'))

# sampletree.calc_values()
# print(f"OOP values: {sampletree.gamestate.OOPvalues}")
# print(f"OOP regret: {sampletree.gamestate.OOPRegret}")



