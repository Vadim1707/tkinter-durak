from __future__ import annotations
from dataclasses import dataclass
from itertools import product




values = ["6","7","8","9","10","Jack","Queen","King","Ace"]
suits = ["Spades", "Hearts", "Dimonds", "Clubs"]


@dataclass
class Card:
    value: str
    suit: str

    def beats(self, card2: Card, trump_suit: str) -> bool:
        num, num2 = 0, 0
        for i, val in enumerate(values):
            if self.value == val:
                num = i
            if card2.value == val:
                num2 = i
        
        if self.suit == card2.suit:
            if num > num2:
                return True
        elif self.suit == trump_suit:
            return True
        return False
            

                

    def __str__(self):
        return self.value + " of " + self.suit
    def __repr__(self):
        return self.value + " of " + self.suit



default_deck = [0 for _ in range(len(values)*len(suits))]
_ = 0
for c in product(values, suits):
    default_deck[_] = Card(*c)
    _ += 1

    