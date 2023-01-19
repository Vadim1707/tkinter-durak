from __future__ import annotations
from itertools import product

from constants import VALUES_DICT, SUITS


class Card:
    def __init__(self, value, suit) -> None:
        self.__value = value
        self.__suit = suit
    

    def beats(self, card2: Card, trump_suit: str) -> bool:
        # checks if first (callable) card can beat second card (card2)
        if self.__suit == card2.__suit:
            if VALUES_DICT[self.get_value()] > VALUES_DICT[card2.get_value()]:
                return True
        elif self.__suit == trump_suit:
            return True
        return False
    
    def get_value(self):
        return self.__value
    
    def get_suit(self):
        return self.__suit

    def __str__(self):
        return self.__value + " of " + self.__suit
    def __repr__(self):
        return self.__value + " of " + self.__suit

# unshuffled deck with 36 cards
DEFAULT_DECK = [0 for _ in range(len(VALUES_DICT)*len(SUITS))]
_ = 0
for c in product(VALUES_DICT, SUITS):
    DEFAULT_DECK[_] = Card(*c)
    _ += 1
del _