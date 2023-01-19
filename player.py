from dataclasses import dataclass

from card import Card
from deck import Deck

@dataclass
class Player:
    # player has hand with cards and ability to play game
    hand: list[Card]
    is_bot: bool = True

    def put_card(self, ind=0):
        if ind > len(self.hand) - 1 or ind < 0:
            raise Exception("Index of player's hand out of range")
        card = self.hand[ind]
        del self.hand[ind]
        return card
    
    def get_full_hand(self, d: Deck):
        while len(self.hand) < 6:
            card = d.draw_one()
            if card is not None:
                self.hand.append(card)
            else:
                break
    
    def get_values(self):
        values = set()
        for card in self.hand:
            values.append(card.get_value())
        return values
    