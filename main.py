from cards import Card, default_deck, dataclass, values
from collections import deque
from random import shuffle

class Deck:
    # creates queue of cards
    def __init__(self):
        tmp_deque = default_deck.copy()
        shuffle(tmp_deque)
        self.cards = deque(tmp_deque)
        self.trump = self.get_trump()
    
    def get_trump(self):
        return self.cards[0]
    
    def draw_one(self) -> Card:
        if not self.cards:
            raise Exception("Cannot draw a card from empty deck")
        return self.cards.pop()
    
    def draw(self, n=6):
        return [self.draw_one() for _ in range(n)]

    def __repr__(self):
        return str(self.cards)
    
    
    
@dataclass
class Player:
    # player has hand with cards and ability to play game
    hand: list[Card]

    def put_card(self, ind=0):
        if ind > len(self.hand) - 1 or ind < 0:
            raise Exception("Index of player's hand out of range")
        card = self.hand[ind]
        del self.hand[ind]
        return card
    
    def get_full_hand(self, d: Deck):
        while len(self.hand) < 6:
            try:
                self.hand.append(d.draw_one())
            except:
                return
        


class Game:
    def __init__(self, players: int = 3):
        if players > 6 or players < 2:
            raise Exception("Cannot create game with that player amount")
        self.deck = Deck()
        self.players = [Player(self.deck.draw()) for _ in range(players)]
        self.table = []
        self.player_to_move: int
    
    def has_smallest_trump(self):
        # updats index of player who's first to move
        trump = self.deck.get_trump().suit
        min_val = [len(values) for _ in range(len(self.players))]
        for ind, player in enumerate(self.players):
            for card in player.hand:
                if card.suit == trump:
                    min_val[ind] = min(values.index(card.value), min_val[ind])
        print(min_val)
        def find_min(array: list[int]):
            min = array[0]
            ind = 0
            for i, elem in enumerate(array):
                if elem < min:
                    min = elem
                    ind = i       
            return ind
        
        self.player_to_move = find_min(min_val)
    
    def values_can_be_popped(self) -> list[str]:
        # defines which cards can be popped if table not empty
        pass 

    def pop_card_on_table(self, player1: Player, player2: Player, card: Card):
        # updates table
        pass

    def cover_card():
        # updates table
        pass

    def logic(self):
        pass

g = Game()
print(g.deck.get_trump().suit)
g.has_smallest_trump()
print(g.player_to_move)
for p in g.players:
    print(p.hand)



# h = g.players[0].hand
# print(h)
# for card1 in h:
#     for card2 in h:
#         if card1.beats(card2, trump_suit="Spades"):
#             print(1, end=" ")
#         else:
#             print(0, end=" ")
#     print()

