from treys import Card, Evaluator
from utils import *
from node import Node


class GameState:

    def __init__(self):
        self.deck = Deck()
        self.evaluator = Evaluator()
        self.hands = []
        self.community_cards = []
        self.betting_percents = {'IP': 0.5, 'OOP': 0.5}

    
    def create_new_flop(self, card1, card2, card3):
        if card1 == card2 or card1 == card3 or card2 == card3:  
            raise ValueError("Community cards must be unique")
        self.community_cards = [card1, card2, card3]
        
        # self.deck.remove(card1)
        # self.deck.remove(card2)
        # self.deck.remove(card2)

    def add_card(self):
        new_card = self.deck.draw(1)
        self.community_cards.append(self.deck.draw(1))
    
    def __copy__(self):
        new_state = GameState()
        new_state.deck = self.deck.copy()
        new_state.evaluator = self.evaluator
        new_state.hands = self.hands.copy()
        new_state.community_cards = self.community_cards.copy()
        new_state.betting_percents = self.betting_percents.copy()
        return new_state


game_state = GameState()
flop_cards = [Card.new('2d'), Card.new('3h'), Card.new('4s')]
game_state.create_new_flop(flop_cards[0], flop_cards[1], flop_cards[2])
root = Node(game_state, 'OOP', 'action')
root.generate_children(2)
print(root.to_string_tree())