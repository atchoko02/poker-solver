from treys import Card, Evaluator
import copy
from random import Random

class Range:
    # class to represent a range of poker hands
    def __init__(self):
        self.hands = set() # Using a set to avoid duplicates
    
    # Adds a card to the range
    def add_hand(self, card):
        if isinstance(card, Hand):
            self.hands.add(card)
        else:
            raise ValueError("Expected a Hand instance")
    
    # Removes a card from the range
    def remove_hand(self, hand):
        # Ensure card is a Card instance
        if not isinstance(hand, Hand):
            raise ValueError("Expected a Hand instance")

        # check if card is in the range
        if hand in self.hands:
            self.hands.remove(hand)
        else:
            raise ValueError("Hand not found in range")
    
    def __str__(self):
        return ", ".join(str(hand) for hand in self.hands)

class Hand:
    # class to represent a poker hand
    def __init__(self, cards):
        if len(cards) != 2:
            raise ValueError("A hand must consist of exactly two cards")
        if cards[0] == cards[1]:
            raise ValueError("A hand cannot consist of two identical cards")


        self.cards = set() # using a set to avoid duplicates and for comparison without order
        for card in cards:
            self.cards.add(card)
            
    def __eq__(self, other):
        if isinstance(other, Hand):
            return self.cards == other.cards
        return False
    
    def __repr__(self):
        return f"Hand: {', '.join(Card.int_to_pretty_str(card) for card in self.cards)}"
    
    def __hash__(self):
        hash_value = 1
        for card in self.cards:
            hash_value *= card
        return hash_value

# def add_pocket_pairs():

class Deck:
    def __init__(self, cards=[]):
        if len(cards) > 0:
            self.cards = cards
        else:
            self.cards = [Card.new(f"{rank}{suit}") for rank in '23456789TJQKA' for suit in 'cdhs']
        self.random = Random()
        self.random.shuffle(self.cards)
    
    def draw(self, num=1):
        if num < 1 or num > len(self.cards):
            raise ValueError("Invalid number of cards to draw")
        drawn_cards = self.cards[:num]
        self.cards = self.cards[num:]
        return drawn_cards if num > 1 else drawn_cards[0]

    def copy(self):
        new_deck = Deck(copy.deepcopy(self.cards))
        return new_deck

class GameState:

    def __init__(self):
        self.deck = Deck()
        self.evaluator = Evaluator()
        self.IPfreqs = {}
        self.OOPfreqs = {}
        self.IPRegret = {}
        self.OOPRegret = {}
        self.community_cards = []
        self.contribution = {'IP': 0, 'OOP': 0}  # Contribution to the pot by each player

        # NEED TO ADD A WAY TO CHANGE THESE DEFAULTS
        self.pot = 50 # dault pot size
        self.betting_percents = {'IP': 0.5, 'OOP': 0.5}  # Default betting percentages for IP and OOP
        self.inital_pot = self.pot  # Store the initial pot size for reference

    
    def create_new_flop(self, card1, card2, card3):
        if card1 == card2 or card1 == card3 or card2 == card3:  
            raise ValueError("Community cards must be unique")
        self.community_cards = [card1, card2, card3]
    
    def generate_default_freqs(self, IPRange, OOPRange):
        for hand in IPRange.hands:
            self.IPfreqs[hand] = [0.33, 0.33, 0.33]  # Default frequencies
        
        for hand in OOPRange.hands:
            self.OOPfreqs[hand] = [0.33, 0.33, 0.33]


    def add_card(self):
        new_card = self.deck.draw(1)
        self.community_cards.append(self.deck.draw(1))
    
    def __copy__(self):
        new_state = GameState()
        new_state.deck = self.deck.copy()
        new_state.evaluator = self.evaluator
        new_state.community_cards = copy.deepcopy(self.community_cards)
        new_state.IPfreqs = copy.deepcopy(self.IPfreqs)
        new_state.OOPfreqs = copy.deepcopy(self.OOPfreqs)
        new_state.IPRegret = copy.deepcopy(self.IPRegret)
        new_state.OOPRegret = copy.deepcopy(self.OOPRegret)
        new_state.betting_percents = copy.deepcopy(self.betting_percents)
        new_state.contribution = copy.deepcopy(self.contribution)
        new_state.pot = self.pot
        new_state.inital_pot = self.inital_pot
        return new_state
    