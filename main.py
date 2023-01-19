from time import time
import sys

from constants import VALUES_DICT
from card import Card
from deck import Deck
from player import Player



class Game:
    def __init__(self, players: int = 3):
        if players > 6 or players < 2:
            raise Exception(f"Cannot create game with that player amount ({players})")
        self.deck = Deck()
        self.players = [Player(self.deck.draw()) for _ in range(players)]
        self.table = []
        self.trump = self.deck.get_trump()
        self.player_to_move = self.has_smallest_trump()
        self.discard_pile = []
        self.time = str(time())
        for i in range(1, players):
            self.players[i].is_bot = True
        
    
    def has_smallest_trump(self):
        ind_player, smallest_trump = 0, 100
        for i, player in enumerate(self.players):
            for card in player.hand:
                if card.get_suit() == self.trump and VALUES_DICT[card.get_value()] < smallest_trump:
                    ind_player = i
                    smallest_trump = VALUES_DICT[card.get_value()]
        return ind_player

    
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
            raise Exception(f"Cannot put {card} on board")
        
        return card

    def cover_card(self, card_to_cover: Card, player: Player, card_ind: int):
        # updates table
        card = player.hand[card_ind]

        if card.beats(card_to_cover, trump_suit=self.trump):
            card = player.put_card(card_ind)
            self.table.append(card)
        else:
            raise Exception(f"Cannot beat previous card {card_to_cover} with this one {card}")
        
        return card

    # def has_cards_to_pop(self, player_ind: int):
    #     p = self.players[player_ind]
    #     if len(p.hand) > 0:
    #         for val in p.get_values():
    #             if val in self.values_can_be_popped():
    #                 return True
    #     return False
    
    # def can_beat(self, player: Player, card: Card):
    #     for cp in player.hand:
    #         if cp.beats(card):
    #             return True
    #     return False
    
    def take_table_cards(self, player: Player):
        player.hand.extend(self.table)
        self.table = []

    def next_player(self, currently_moves: int, currently_beats: int):
        a = (currently_moves + 1) % len(self.players)
        if a == currently_beats:
            a = (a + 1) % len(self.players)
        return a
    
    def end_of_move(self, history) -> bool:
        return history[-len(self.players) + 1:] == ['q' for _ in range(len(self.players) - 1)]
    
    def finish_move(self, next_to_move: int):
        self.discard_pile.extend(self.table)
        self.table = []
        self.player_to_move = next_to_move

    def stats(self, history=None, p=False):  # prints but can turn it to string in future if needed for frontend    
        if p:
            print("trump: ", self.trump, "\nplayer to move: ", self.player_to_move)
            for i, p in enumerate(self.players):
                print(f"p{i}: ", p.hand)
            print("Table: ", self.table)
            print("Discard pile: ", self.discard_pile)
            print("history: ", history)

        original_stdout = sys.stdout

        with open('stats1.txt', 'a') as f: # f'stats\\stats1-{self.time}'
            sys.stdout = f # Change the standard output to the file we created.
            print("trump: ", self.trump, "\nplayer to move: ", self.player_to_move)
            for i, p in enumerate(self.players):
                print(f"p{i}: ", p.hand)
            print("Table: ", self.table)
            print("Discard pile: ", self.discard_pile)
            print("history: ", history)
            sys.stdout = original_stdout
    
    # def delete_empty_player(self, history):
    #     if  not self.players[self.player_to_move].hand and not self.deck:
    #         del self.players[self.player_to_move]
    #         print(f"player-{self.player_to_move} has won. Congrats!")
    #         self.stats(history, p=True)
    #         if self.player_to_move > len(self.players):
    #             self.player_to_move = 0

    def take_cards(self):
        pass
    
    def put_cards_to_take(self):
        pass

        

            
    
    def move(self, is_first_move=False):

        # create move order
        p = len(self.players)
        BEATING_PLAYER = (self.player_to_move + 1) % p
        players_moving = [i for i in range(p) if i != BEATING_PLAYER]
        i = players_moving.index(self.player_to_move)
        players_moving = players_moving[i:] + players_moving[:i]
        move_order = [0 for _ in range(2*p-2)]
        for i in range(len(move_order)):
            if i%2==1:
                move_order[i] = BEATING_PLAYER
            else:
                move_order[i] = players_moving[i // 2]

        history = []
        # first move
        card_to_put = -1
        while 0 > card_to_put or card_to_put > len(self.players[move_order[0]].hand) - 1:
            card_to_put = input("Please, put card on table to start a move (0,1,...) or s for stats: ")
            if card_to_put == 's':
                self.stats(history, p=True)
            try:
                card_to_put = int(card_to_put)
            except:
                card_to_put = -1

        self.table.append(self.players[move_order[0]].hand.pop(card_to_put))
        print(self.table)
        move_order = move_order[1:] + move_order[:1]
        history = [card_to_put]

        # second move
        card_to_put = -1
    
        while 0 > card_to_put or card_to_put > len(self.players[move_order[0]].hand) - 1:
            card_to_put = input("Please, put card on table to start a move (0,1,...), s for stats or t to take: ")
            if card_to_put == 's':
                self.stats(history, p=True)
            if card_to_put == 't':
                self.put_cards_to_take() # currently empty
                self.take_cards()        # currently empty
                if len(self.players) == 2:
                    self.player_to_move = 1 - self.player_to_move
                else:
                    self.player_to_move = (self.player_to_move + 2) % p
                return
            try:
                card_to_put = int(card_to_put)
                if not self.players[move_order[0]].hand[card_to_put].beats(self.table[0], self.trump):
                    print(f'card {self.players[move_order[0]].hand[card_to_put]} doesn\'t beat card {self.table[0]}')
                    card_to_put = -1
                    continue
            except:
                card_to_put = -1

        self.table.append(self.players[move_order[0]].hand.pop(card_to_put))
        print(self.table)
        move_order = move_order[1:] + move_order[:1]
        history.append(card_to_put)

        # third move
        card_to_put = -1
        while 0 > card_to_put or card_to_put > len(self.players[move_order[0]].hand) - 1:
            card_to_put = input("Please, put card on table to start a move (0,1,...), s for stats or q to stop moving: ")
            if card_to_put == 's':
                self.stats(history, p=True)
            if card_to_put == 'q' or len(self.players[move_order[0]].hand) == 0:
                # ask for move from next player
                if len(self.players) == 2 or self.end_of_move(history):
                    self.finish_move(next_to_move=move_order[1])
                    return
                move_order = move_order[2:] + move_order[:2]
                history.append('q')
                card_to_put = -1
                continue
            try:
                card_to_put = int(card_to_put)
                if self.players[move_order[0]].hand[card_to_put] not in self.values_can_be_popped():
                    print(f'card {self.players[move_order[0]].hand[card_to_put]} cannot be put on table')
                    card_to_put = -1
            except:
                card_to_put = -1

        self.table.append(self.players[move_order[0]].hand.pop(card_to_put))
        print(self.table)
        move_order = move_order[1:] + move_order[:1]
        history.append(card_to_put)

        # fourth move
        card_to_put = -1
    
        while 0 > card_to_put or card_to_put > len(self.players[move_order[0]].hand) - 1:
            card_to_put = input("Please, put card on table to start a move (0,1,...), s for stats or t to take: ")
            if card_to_put == 's':
                self.stats(history, p=True)
            if card_to_put == 't':
                self.put_cards_to_take() # currently empty
                self.take_cards()        # currently empty
                if len(self.players) == 2:
                    self.player_to_move = 1 - self.player_to_move
                else:
                    self.player_to_move = (self.player_to_move + 2) % p
                return
            try:
                card_to_put = int(card_to_put)
                if not self.players[move_order[0]].hand[card_to_put].beats(self.table[0], self.trump):
                    print(f'card {self.players[move_order[0]].hand[card_to_put]} doesn\'t beat card {self.table[0]}')
                    card_to_put = -1
                    continue
            except:
                card_to_put = -1

        self.table.append(self.players[move_order[0]].hand.pop(card_to_put))
        print(self.table)
        move_order = move_order[1:] + move_order[:1]
        history.append(card_to_put)

        





        




        
        # a = input("type: s for stats")
        # if a == "s":
        #     self.stats(history, p=True)


    def logic(self):
        self.move()

                    



g = Game(players=3)
g.players[0].is_bot = False
g.stats([], p=True)

print(g.trump, g.player_to_move)
for p in g.players:
    print(p.hand)
g.logic()
# print(g.table)

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

