from treys import Card, Deck, Evaluator
from utils import *


class GameState:

    def __init__(self):
        self.deck = Deck()
        self.evaluator = Evaluator()
        self.hands = []
        self.community_cards = []


    
    def create_new_flop(self, card1, card2, card3):
        if card1 == card2 or card1 == card3 or card2 == card3:  
            raise ValueError("Community cards must be unique")
        self.community_cards = [card1, card2, card3]
        
        # self.deck.remove(card1)
        # self.deck.remove(card2)
        # self.deck.remove(card2)

game = GameState()
game.create_new_flop(Card.new('As'), Card.new('Ad'), Card.new('Ah'))
for card in game.community_cards:
    print(Card.int_to_pretty_str(card))

IP_range = Range()
IP_range.add_hand(Hand([Card.new('As'), Card.new('Ad')]))
IP_range.add_hand(Hand([Card.new('Ah'), Card.new('Ac')]))
IP_range.add_hand(Hand([Card.new('Ac'), Card.new('Ah')]))
IP_range.add_hand(Hand([Card.new('Js'), Card.new('Jh')]))

print(IP_range)

    