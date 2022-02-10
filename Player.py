def does_player_have_card(player, value):
    for i in range(len(player.cards)):
        if not i+1 == len(player.cards):
            if player.cards[i, 1] == value:
                return True
    return False
def does_player_have_colour(player, value):
    for i in range(len(player.cards)):
        if not i+1 == len(player.cards):
            if player.cards[i, 0] == value:
                return True
    return False

import numpy as np
class Player():
    def __init__(self):
        self.size_of_hand = 0
        self.cards = np.empty((0, 2), str)
        self.debt = 0
        self.reds = 0
        self.greens = 0
        self.blues = 0
        self.yellows = 0
        self.a_cards = 0
        self.r_cards = 0
        self.w_cards = 0
    def add_card(self, deck):
        self.cards = np.append(self.cards, [deck.get_next_card()], axis=0)
        self.size_of_hand += 1
        
    def play_card(self, card, cardind, other_player, is_wild, colour, pile, is_player_turn, deck):
        if pile[0] == card[0] or pile[1] == card[1] and not is_wild:
            if card[1] == '@':                    
                if does_player_have_card(other_player, '@'):
                    is_player_turn = not is_player_turn
                other_player.debt += self.debt + 2
                self.debt = 0
            elif card[1] != 'S' and card[1] != 'r':
                is_player_turn = not is_player_turn
            self.cards = np.delete(self.cards, cardind-1,axis=0)
            pile[0] = card[0]
            pile[1] = card[1]
        elif is_wild:
            if card[1] == '$':
                if does_player_have_card(other_player, '$'):
                    is_player_turn = not is_player_turn
                other_player.debt += self.debt + 4
                self.debt = 0
            else:
                is_player_turn = not is_player_turn
            self.cards = np.delete(self.cards, cardind-1,axis=0)
            pile[0] = colour
            pile[1] = card[1]
        else:
            print("You can't play that card")
            
        if other_player.debt:
            if not does_player_have_card(other_player, '@') and pile[1] == '@' or not does_player_have_card(other_player, '$') and pile[1] == '$':
                for i in range(other_player.debt):
                    other_player.add_card(deck)
                other_player.debt = 0
        return is_player_turn
    def pick_ideal_colour(self):
        colour_switcher = {
            0: "R",
            1: "G",
            2: "B",
            3: "Y"
        }
        colours = [self.reds, self.greens, self.blues, self.yellows]
        most_amount_of_colours = "B"

        if self.reds > self.blues and self.reds > self.yellows and self.reds > self.greens:
            return 'R'
        elif self.greens > self.reds and self.greens > self.blues and self.greens > self.yellows:
            return 'G'
        elif self.blues > self.greens and self.blues > self.reds and self.blues > self.yellows:
            return 'B'
        elif self.yellows > self.reds and self.yellows > self.blues and self.yellows > self.greens:
            return 'Y'
        else:
            for i in range(len(colours)):
                if i != len(colours)-1:
                    if colours[i] > colours[i+1]:
                        most_amount_of_colours = i
                    else:
                        most_amount_of_colours = i+1
            return colour_switcher.get(most_amount_of_colours, "B")
    def can_player_play(self, pile):
        if self.size_of_hand != 0:
            for i in range(len(self.cards)):
                if self.cards[i, 0] == pile[0] or self.cards[i, 1] == pile[1] or self.cards[i, 0] == 'W' or self.cards[i, 0] == '+':
                    return True
        return False