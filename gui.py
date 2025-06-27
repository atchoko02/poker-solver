import tkinter as tk
from game import Solver
from node import Node
from treys import Card
from utils import *

class GUI:
    def __init__(self, root, solver):
        self.root = root
        self.root.title("Tree viewer GUI")
        self.root.geometry("800x800")

        # Create a button
        self.button = tk.Button(root, text="generate tree", command=self.generate_tree)
        self.button.pack(pady=10)

        # Create an output box (Text widget)
        self.output_box = tk.Text(root, height=30, width=90)
        self.output_box.config(state='disabled')  # Disable editing to make it read-only
        self.output_box.pack(pady=10)

    def generate_tree(self):
        # Handle button click
        self.output_box.config(state='normal')  
        self.output_box.insert(tk.END, "started building tree\n")
        self.output_box.config(state='disabled')
        solver.root = Node(solver.game_state.__copy__(), 'OOP', 'action')
        solver.root.generate_children(3)
        self.output_box.config(state='normal')  
        self.output_box.insert(tk.END, "finished building tree\n")
        self.output_box.config(state='disabled')
        

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    solver = Solver()
    gui = GUI(root, solver)

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
    # solver.root = Node(solver.game_state.__copy__(), 'OOP', 'action')
    # print('starting tree')
    # solver.root.generate_children(3)
    # print('ended tree')



    root.mainloop()


    