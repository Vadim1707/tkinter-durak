from collections import deque
from random import shuffle

from card import Card, DEFAULT_DECK

class Deck:
    # creates queue of cards
    def __init__(self):
        tmp_deque = DEFAULT_DECK.copy()
        shuffle(tmp_deque)
        self.__cards = deque(tmp_deque)

        # # tool for testing
        # for _ in range(23):
        #     self.cards.pop()
    
    def get_trump(self):
        return self.__cards[0].get_suit()
    
    def draw_one(self) -> Card:
        if not self.__cards:
            return None
        return self.__cards.pop()
    
    def draw(self, n=6):
        return [self.draw_one() for _ in range(n)]

    def __repr__(self):
        return str(self.__cards)