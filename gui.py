from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea, QSizePolicy, QGridLayout
)
from game import Solver
from node import Node
from utils import *

class StrategyWindow(QWidget):
    def __init__(self, freqs, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Strategy Frequencies")
        layout = QGridLayout()
        if isinstance(freqs, dict):
            hands = list(freqs.items())
            columns = 3  # Number of columns you want
            for idx, (hand, freq_list) in enumerate(hands):
                row = idx // columns
                col = idx % columns
                layout.addWidget(QLabel(f"{hand}: {freq_list}"), row, col)
        else:
            layout.addWidget(QLabel(str(freqs)), 0, 0)
        self.setLayout(layout)
        self.resize(600, 600)

class RangeWindow(QWidget):
    def __init__(self, rng, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Range")
        layout = QGridLayout()
        if hasattr(rng, "hands"):
            hands = list(rng.hands)
            columns = 3  # Number of columns you want
            for idx, hand in enumerate(hands):
                row = idx // columns
                col = idx % columns
                layout.addWidget(QLabel(str(hand)), row, col)
        else:
            layout.addWidget(QLabel(str(rng)), 0, 0)
        self.setLayout(layout)
        self.resize(400, 400)

class NodeProperties(QWidget):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Position: {self.node.position}"))
        layout.addWidget(QLabel(f"Type: {self.node.type}"))
        layout.addWidget(QLabel(f"Number of Cards: {len(self.node.gamestate.community_cards)}"))
        layout.addWidget(QLabel(f"Pot: {getattr(self.node.gamestate, 'pot', 'N/A')}"))
        layout.addWidget(QLabel(f"Raise Level: {getattr(self.node, 'raise_level', 'N/A')}"))
        layout.addWidget(QLabel(f"OOP Current Contribution: {self.node.gamestate.contribution['OOP']}"))
        layout.addWidget(QLabel(f"IP Current Contribution: {self.node.gamestate.contribution['IP']}"))
        # Show Range button
        range_btn = QPushButton("Show Range")
        range_btn.clicked.connect(self.show_range_window)
        layout.addWidget(range_btn)
        # Show Strategy button
        strat_btn = QPushButton("Show Strategy")
        strat_btn.clicked.connect(self.show_strategy_window)
        layout.addWidget(strat_btn)
        self.setLayout(layout)

    def show_range_window(self):
        # Show the correct range based on node position
        if self.node.position == 'OOP':
            rng = self.node.gamestate.OOPRange
        else:
            rng = self.node.gamestate.IPRange
        self.range_window = RangeWindow(rng)
        self.range_window.show()

    def show_strategy_window(self):
        # Show the correct frequencies based on node position
        if self.node.position == 'OOP':
            freqs = self.node.gamestate.OOPfreqs
        else:
            freqs = self.node.gamestate.IPfreqs
        self.strat_window = StrategyWindow(freqs)
        self.strat_window.show()

class TreeButtonBranch(QWidget):
    def __init__(self, node, on_node_clicked, parent=None):
        super().__init__(parent)
        self.node = node
        self.on_node_clicked = on_node_clicked
        self.expanded = False
        self.child_widgets = []
        self.children_layout = None
        self.init_ui()

    def init_ui(self):
        self.outer_layout = QHBoxLayout()
        self.inner_layout = QVBoxLayout()
        self.button = QPushButton(f"{self.node.position}, {self.node.type}")
        self.button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.button.clicked.connect(self.handle_click)
        self.inner_layout.addWidget(self.button)
        self.outer_layout.addLayout(self.inner_layout)
        self.setLayout(self.outer_layout)

    def handle_click(self):
        self.on_node_clicked(self.node)
        if not self.expanded:
            self.expand_children()
        else:
            # If already expanded, and this is the root node, reset children
            if self.parentWidget() is None or isinstance(self.parentWidget(), QScrollArea):
                self.reset_children()

    def expand_children(self):
        self.collapse_children()
        if self.node.children:
            self.children_layout = QHBoxLayout()
            for child in self.node.children:
                child_widget = TreeButtonBranch(child, self.child_clicked)
                self.child_widgets.append(child_widget)
                self.children_layout.addWidget(child_widget)
            self.inner_layout.addLayout(self.children_layout)
        self.expanded = True

    def collapse_children(self):
        for child_widget in self.child_widgets:
            child_widget.setParent(None)
        self.child_widgets = []
        if self.children_layout:
            while self.children_layout.count():
                item = self.children_layout.takeAt(0)
                if item.widget():
                    item.widget().setParent(None)
                elif item.layout():
                    self.clear_layout(item.layout())
            self.inner_layout.removeItem(self.children_layout)
            self.children_layout = None
        self.expanded = False

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
            elif item.layout():
                self.clear_layout(item.layout())

    def child_clicked(self, node):
        # Remove all siblings and only show the clicked child
        if self.children_layout:
            for i, child_widget in enumerate(self.child_widgets):
                if child_widget.node == node:
                    for j, other_widget in enumerate(self.child_widgets):
                        if i != j:
                            other_widget.setParent(None)
                    for j in reversed(range(self.children_layout.count())):
                        item = self.children_layout.itemAt(j)
                        if item.widget() and item.widget().node != node:
                            w = item.widget()
                            self.children_layout.removeWidget(w)
                            w.setParent(None)
                    child_widget.expand_children()
                    break
        self.on_node_clicked(node)

    def reset_children(self):
        self.collapse_children()
        self.expand_children()

class TreeExplorer(QWidget):
    def __init__(self, root_node):
        super().__init__()
        self.root_node = root_node
        self.selected_node = root_node

        self.setWindowTitle("Poker Tree Explorer")
        self.resize(1200, 800)

        main_layout = QHBoxLayout()
        # Left: Tree area
        self.tree_area = QScrollArea()
        self.tree_area.setWidgetResizable(True)
        self.tree_content = QWidget()
        self.tree_layout = QVBoxLayout()
        self.tree_content.setLayout(self.tree_layout)
        self.tree_area.setWidget(self.tree_content)
        main_layout.addWidget(self.tree_area, 3)

        # Right: Properties area
        self.prop_area = QScrollArea()
        self.prop_area.setWidgetResizable(True)
        self.prop_content = QWidget()
        self.prop_layout = QVBoxLayout()
        self.prop_content.setLayout(self.prop_layout)
        self.prop_area.setWidget(self.prop_content)
        main_layout.addWidget(self.prop_area, 1)

        self.setLayout(main_layout)
        self.tree_root = TreeButtonBranch(self.root_node, self.show_properties)
        self.tree_layout.addWidget(self.tree_root)
        self.show_properties(self.root_node)

    def show_properties(self, node):
        # Show properties
        for i in reversed(range(self.prop_layout.count())):
            widget = self.prop_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.prop_layout.addWidget(NodeProperties(node))

        # If root node is clicked, reset its children
        if node is self.root_node:
            self.tree_root.reset_children()

if __name__ == "__main__":
    import sys
    from node import Node
    from utils import GameState

    app = QApplication(sys.argv)
    solver = Solver()
    solver.flop_cards = [Card.new('3d'), Card.new('Jh'), Card.new('As')]

    for i in range(9, 15):
        solver.IPRange.add_pocket_pair(str(i))
        solver.OOPRange.add_pocket_pair(str(i))


    solver.game_state.add_ranges(solver.IPRange, solver.OOPRange)
    solver.game_state.generate_default_freqs(solver.IPRange, solver.OOPRange)
    solver.game_state.create_new_flop(solver.flop_cards[0], solver.flop_cards[1], solver.flop_cards[2])
    solver.game_state.add_turn_and_river(Card.new('7d'), Card.new('8h'))
    root = Node(solver.game_state.__copy__(), 'OOP', 'action')
    root.generate_children(3)

    def get_current_ev(position):
        if position == 'OOP':
            value = 0
            for hand in root.gamestate.OOPvalues:
                value += root.gamestate.OOPvalues[hand]
            return value / len(root.gamestate.OOPvalues)
        elif position == 'IP':
            value = 0
            for hand in root.gamestate.IPvalues:
                value += root.gamestate.IPvalues[hand]
            return value / len(root.gamestate.IPvalues)


    for i in range(100):
        root.calc_values()
        OOP_sarting_ev = get_current_ev('OOP')
        IP_sarting_ev = get_current_ev('IP')
        root.calc_new_strat()
        root.remove_folded_hands(set(), set())
        root.calc_values()
        OOP_new_ev = get_current_ev('OOP')
        IP_new_ev = get_current_ev('IP')
        print(f"OOP EV: {OOP_new_ev}")
        print(f"IP EV: {IP_new_ev}")
        if OOP_new_ev == OOP_sarting_ev and IP_new_ev == IP_sarting_ev:
            break

    explorer = TreeExplorer(root)
    explorer.show()
    sys.exit(app.exec_())