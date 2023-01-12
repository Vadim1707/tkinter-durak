from classes import Card, Deck, Player, values
from time import sleep


class Game:
    def __init__(self, players: int = 3):
        if players > 6 or players < 2:
            raise Exception(f"Cannot create game with that player amount ({players})")
        self.deck = Deck()
        self.players = [Player(self.deck.draw()) for _ in range(players)]
        self.table = []
        self.trump = self.deck.trump
        self.player_to_move = self.has_smallest_trump()
        self.discard_pile = []
        for i in range(1, players):
            self.players[i].is_bot = True
        
    
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

        # if player.is_bot:
        #     for i in range(len(player.hand)):
        #         try:
        #             if player.hand[i].value in possible_card_values or not possible_card_values:
        #                 card = player.put_card(card_ind)
        #                 self.table.append(card)
        #         except:
        #             pass
        #         else:
        #             return card

        
        if player.hand[card_ind].value in possible_card_values or not possible_card_values:
            card = player.put_card(card_ind)
            self.table.append(card)
        else:
            raise Exception(f"Cannot put {card} on board")
        
        return card
        
    # TODO those two functions can be merged into one with adding one extra paramether (if he moves or beats)

    def cover_card(self, card_to_cover: Card, player: Player, card_ind: int):
        # updates table
        card = player.hand[card_ind]

        if card.beats(card_to_cover, trump_suit=self.trump):
            card = player.put_card(card_ind)
            self.table.append(card)
        else:
            raise Exception(f"Cannot beat previous card {card_to_cover} with this one {card}")
        
        return card

    def has_cards_to_pop(self, player_ind: int):
        p = self.players[player_ind]
        if len(p.hand) > 0:
            for val in p.get_values():
                if val in self.values_can_be_popped():
                    return True
        return False
    
    def can_beat(self, player: Player, card: Card):
        for cp in player.hand:
            if cp.beats(card):
                return True
        return False
    
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

    def stats(self, history = []): #prints but can turn it to string in future if needed for frontend
        print("trump: ", self.trump, "\nplayer to move: ", self.player_to_move)
        for i, p in enumerate(self.players):
            print(f"p{i}: ", p.hand)
        print("Table: ", self.table)
        print("Discard pile: ", self.discard_pile)
        print("history: ", history)

            
    
    def move(self, is_first_move=False):
        # Unfinished: bugs are possible
        # pre: table clear, all players have enough cards
        # post: table clear, players have not enough cards
        # TODO: bots! and some logic function enhancements
        max_table = 10 if is_first_move else 12
        history = []
        i_beat = False
        initiated_move = False
        player_who_beats = (self.player_to_move + 1) % len(self.players)
        
        while len(self.players[player_who_beats].hand) and max_table - len(self.table):
            
            is_bot = self.players[player_who_beats].is_bot if i_beat else self.players[self.player_to_move].is_bot

            if is_bot:

                print("table: ", self.table)
                self.stats(history)

                if self.end_of_move(history):
                    self.finish_move(player_who_beats)
                    break
                
                if not i_beat:
                    has_put = False
                    ind = 0
                    while ind < len(self.players[self.player_to_move].hand):
                        try:
                            self.pop_card_on_table(self.players[self.player_to_move], ind)
                            has_put = True
                            break
                        except:
                            pass
                        ind += 1
                    if not has_put:
                        self.next_player(self.player_to_move, player_who_beats)
                        continue
                    else:
                        history.append(ind)
                        i_beat = not i_beat
                        continue
                elif i_beat:
                    has_put = False
                    ind = 0
                    while ind < len(self.players[self.player_to_move].hand):
                        try:
                            self.cover_card(self.table[-1], self.players[self.player_to_move], ind)
                            has_put = True
                            break
                        except:
                            pass
                        ind += 1
                    if not has_put:
                        self.take_table_cards(self.players[player_who_beats])
                        self.player_to_move = (player_who_beats + 1) % len(self.players)
                        break
                    else:
                        history.append(ind)
                        i_beat = not i_beat
                        continue

                # i_beat = not i_beat

            if not self.players[self.player_to_move].hand:
                history.append('q')
                if self.end_of_move(history):
                    self.finish_move(player_who_beats)
                    break
                continue

            s1 = "Hand of guy who's gonna beat: " + str(self.players[player_who_beats].hand)
            s2 = "Hand of the guy who pops cards: " + str(self.players[self.player_to_move].hand)
            print("table: ", self.table)
            print("putting\n", s2) if not i_beat else print("beating\n", s1)

            
            ind_of_card = input("Which card to put? (type index of card starting from 0-1-2-etc, q to stop, t to take hand, s to show stats)")
            if ind_of_card == 'q' or ind_of_card.isnumeric():
                history.append(ind_of_card)

            # stop moving (for player who puts)

            if ind_of_card == 's':
                self.stats()
                continue

            if ind_of_card == 'q':
                if not initiated_move:
                    print("Put one card on table to continue")
                    continue

                self.player_to_move = self.next_player(self.player_to_move, player_who_beats)

                if len(history) >= len(self.players) - 1:
                    if self.end_of_move(history):
                        self.finish_move(player_who_beats)
                        break
                       
            if ind_of_card == 't' and i_beat:
                if not initiated_move:
                    continue
                # take cards
                self.take_table_cards(self.players[player_who_beats])
                self.player_to_move = (player_who_beats + 1) % len(self.players)
                break

            try:

                if not i_beat:
                    self.pop_card_on_table(self.players[self.player_to_move], int(ind_of_card)) 
                elif i_beat:
                    self.cover_card(self.table[-1], self.players[player_who_beats], int(ind_of_card))
                
                i_beat = not i_beat
                initiated_move = True

            except Exception as e:
                print(str(e))


    def logic(self):
        # move order: 0-1-2-0 etc
        lengths = [len(self.players[i].hand) for i in range(len(self.players))]
        is_first_move = True
        while any(lengths):
            print("---New Move---")
            print("trump: ", g.trump)
            
            self.move(is_first_move)
            if len(self.discard_pile) > 0:
                is_first_move = False
            
            for player in self.players:
                player.get_full_hand(self.deck)

            
            
        

            
        
        pass

g = Game(players=3)
print(g.trump, g.player_to_move)
for p in g.players:
    print(p.hand)
g.logic()
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

