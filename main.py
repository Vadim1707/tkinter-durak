from cards import Card, default_deck, dataclass, values
# from functions import equal_arrays
from collections import deque
from random import shuffle

class Deck:
    # creates queue of cards
    def __init__(self):
        tmp_deque = default_deck.copy()
        shuffle(tmp_deque)
        self.cards = deque(tmp_deque)
        self.trump = self.get_trump().suit
    
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
    
    def get_values(self):
        values = set()
        for card in self.hand:
            values.append(card.value)
        return values

        


class Game:
    def __init__(self, players: int = 3):
        if players > 6 or players < 2:
            raise Exception("Cannot create game with that player amount")
        self.deck = Deck()
        self.players = [Player(self.deck.draw()) for _ in range(players)]
        self.table = []
        self.trump = self.deck.trump
        self.player_to_move = self.has_smallest_trump()
        
    
    def has_smallest_trump(self):
        # updats index of player who's first to move
        # trump = self.deck.get_trump().suit
        min_val = [len(values) for _ in range(len(self.players))]
        for ind, player in enumerate(self.players):
            for card in player.hand:
                if card.suit == self.trump:
                    min_val[ind] = min(values.index(card.value), min_val[ind])
        # print(min_val)
        def find_min(array: list[int]):
            min = array[0]
            ind = 0
            for i, elem in enumerate(array):
                if elem < min:
                    min = elem
                    ind = i       
            return ind
        
        return find_min(min_val)
    
    def values_can_be_popped(self) -> list[str]:
        # defines which cards can be popped if table not empty
        # ineffective. should be updated after each popping of card on table

        if not self.table:
            return []
        possible_values = []
        for card in self.table:
            possible_values.append(card.value)

        return possible_values 

    def pop_card_on_table(self, player: Player, card_ind: int = 0):
        # updates table
        # pre: card is puttable, card index is legit and logic of the game doesn't break
        
        possible_card_values = self.values_can_be_popped()
        
        if player.hand[card_ind].value in possible_card_values or not possible_card_values:
            card = player.put_card(card_ind)
            self.table.append(card)
        else:
            raise Exception("Cannot put this card on board")
        
        return card
        
    # TODO those two functions can be merged into one with adding one extra paramether (if he moves or beats)

    def cover_card(self, card_to_cover: Card, player: Player, card_ind: int):
        # updates table
        card = player.hand[card_ind]

        if card.beats(card_to_cover, trump_suit=self.trump):
            card = player.put_card(card_ind)
            self.table.append(card)
        else:
            raise Exception("Cannot beat previous card with this one")
        
        return card

    def has_cards_to_pop(self, player_ind: int):
        p = self.players[player_ind]
        if len(p.hand) > 0:
            for val in p.get_values():
                if val in self.values_can_be_popped():
                    return True
        return False
            
    
    def move(self, is_first_all_clear=False):
        # maybe change some functions and refactor before beginning
        # Unfinished
        # TODO: should always put at least one card on board
        max_table = 12 if is_first_all_clear else 10
        history = []
        i_beat = False
        player_who_beats = (self.player_to_move + 1) % len(self.players)
        while len(self.players[player_who_beats].hand) and max_table - len(self.table):
            print("Hand of guy who's gonna beat: ", self.players[player_who_beats].hand)
            print("Hand of the guy who pops cards: ", self.players[self.player_to_move].hand)
            ind_of_card = input("Which card to put? (type index of card starting from 0, or q to stop)")
            history.append(ind_of_card)
            if ind_of_card == 'q':

                
                print(history)
                self.player_to_move = (self.player_to_move + 1) % len(self.players)
                if self.player_to_move == player_who_beats:
                    self.player_to_move = (self.player_to_move + 1) % len(self.players)

                if len(history) >= len(self.players) - 1:
                    print(history[-len(self.players) + 1:])
                    print(['q' for _ in range(len(self.players) - 1)])
                    if history[-len(self.players) + 1:] == ['q' for _ in range(len(self.players) - 1)]:
                        break
                        # then move ends
            if ind_of_card == 't':
                # take card
                break
            try:

                if not i_beat:
                    print("putting")
                    self.pop_card_on_table(self.players[self.player_to_move], int(ind_of_card))
                    i_beat = True
                    print(self.table)
                elif i_beat:
                    print("beating")
                    self.cover_card(self.table[-1], self.players[player_who_beats], int(ind_of_card))
                    i_beat = False
                    print(self.table)


            except Exception:
                print("Can't put this card on table")


    def logic(self):
        # move order: 0-1-2-0 etc
        
        pass

g = Game(players=3)
print(g.trump, g.player_to_move)
for p in g.players:
    print(p.hand)
g.move()
print(g.table)
# # print(g.deck.get_trump().suit)
# g.has_smallest_trump()
# mv = g.player_to_move
# for p in g.players:
#     print(p.hand)


# # try:
# card_to_beat = g.pop_card_on_table(g.players[mv])
# print(g.table)
# print(g.trump)
# for i in range(6):
#     try:
#         g.cover_card(card_to_beat, g.players[(mv+1) % len(g.players)], i)
#         break
#     except Exception as e:
#         print('Ошибка:\n', e.with_traceback(None))

# except:
#     print(g.players[mv].hand[i-len(g.table)], " card cannot be put")

    



# h = g.players[0].hand
# print(h)
# for card1 in h:
#     for card2 in h:
#         if card1.beats(card2, trump_suit="Spades"):
#             print(1, end=" ")
#         else:
#             print(0, end=" ")
#     print()

