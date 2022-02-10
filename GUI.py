# import pygame module in this program
from cgi import test
import pygame
import numpy as np
from Player import Player
from Deck import Deck
from random import seed, randint
from AI import *
import time
seed(randint(0, 9999999999999999))
# DECK_SIZE = 108
suits = ['R', 'G', 'B', 'Y']
# is_player_turn = True
# is_game_over = False
# is_player_winner = False
deck = Deck("deck")
deck.fill_new(suits)
deck.shuffle()
pile = ['','']
DECK_SIZE = 108
suits = ['R', 'G', 'B', 'Y']
is_player_turn = True
is_game_over = False
is_game_started = True
is_player_winner = False
# is_player_winner = False
deck = Deck("deck")
deck.fill_new(suits)
deck.shuffle()
pile = ['','']
while deck.arr[DECK_SIZE-1, 0] == '+' or deck.arr[DECK_SIZE-1, 0] == 'W' or deck.arr[DECK_SIZE-1, 1] == '@' or deck.arr[DECK_SIZE-1, 1] == 'r' or deck.arr[DECK_SIZE-1, 1] == 'S':
    deck.shuffle()
pile = deck.get_next_card()
Chase = Player()
Computer = Player()

# activate the pygame library
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()
carryOn = True

# Rect((left, top), (width, height))

# define the RGB value for white,
# green, blue colour .
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
red = (255, 0, 0)
yellow = (242, 255, 0)
black = (0, 0, 0)
grey = (117, 117, 116)

# assigning values to X and Y variable
X = 800
Y = 600

# create the display surface object
# of specific dimension..e(X, Y).
screen = pygame.display.set_mode((X, Y))

# set the pygame window name
pygame.display.set_caption('Uno')

# Assigning Clock
clock = pygame.time.Clock()

# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.SysFont('system', 30)

# create a text surface object,
# on which text is drawn on it.
text = font.render('The Current card is a: ', True, black)

# Card Values
card_width = 70
card_height = 100

# create a rectangular object for the
# text surface object
textRect = text.get_rect()

# Drawing Rectangle
# pygame.display.flip()

# set the center of the rectangular object.
textRect.center = (200, Y // 2)

colour_switcher = {
    "R": red,
    "G": green,
    "B": blue,
    "Y": yellow,
    "+": grey,
    "W": grey
}
number_switcher = {
    "0": " 0",
    "1": " 1",
    "2": " 2",
    "3": " 3",
    "4": " 4",
    "5": " 5",
    "6": " 6",
    "7": " 7",
    "8": " 8",
    "9": " 9",
    "@": "+2",
    "r": " R",
    "S": " S",
    "$": "+4",
    "C": " W"
}
is_wild_switcher = {
    "C": True,
    "$": True
}
colour_switch = {
    0: "R",
    1: "G",
    2: "B",
    3: "Y"
}
player_coords = np.empty((0,2), int)
player_y_has_changed = 0
player_y = 30

def create_player_coords(y, n, times_y_has_changed, coords):
    x_pos = 0
    for i in range(n):
        if i%9 == 0 and times_y_has_changed < 4:
            y += card_height + 5
            times_y_has_changed += 1
            x_pos = 20
        coords = np.append(coords, [[x_pos, y]],axis=0)
        x_pos += 85
    return coords

def draw_pile_card(colour, card):
    pygame.draw.rect(screen, colour_switcher.get(colour, (0, 0, 0)), [239, 5, card_width, card_height],3, 3)
    text_to_display = font.render(number_switcher.get(card), True, colour_switcher.get(colour, (0, 0, 0)))
    textToDisplayRect = text_to_display.get_rect()
    textToDisplayRect.center = (260, (card_height/2)-3)
    screen.blit(text_to_display, (260, (card_height/2)-3))

def computer_cards(n):
    text_to_display = font.render(f'The Computer has {n} cards', True, black)
    text_rect = text_to_display.get_rect()
    text_rect.center = (X-314, 15)
    screen.blit(text_to_display, (X-314, 15))
    
def draw_player_cards(coords, cards):
    arr = []
    if len(cards) < 36:
        arr = range(len(cards))
    else:
        arr = range(len(cards)-36, len(cards))
    x = 0
    for i in arr:
        pygame.draw.rect(screen, colour_switcher.get(cards[i,0], (0,0,0)), [coords[x,0], coords[x, 1], card_width, card_height], 3,3)
        card_info_text = font.render(number_switcher.get(cards[i, 1]), True, colour_switcher.get(cards[i, 0], (0, 0, 0)))
        card_info_rect = card_info_text.get_rect()
        card_info_rect.center = (coords[x,0]+22, coords[x,1]+((card_height/2)-7))
        screen.blit(card_info_text, (coords[x,0]+22, coords[x,1]+((card_height/2)-7)))
        x += 1

def check_if_card_touching(pos, coords):
    is_on_card = False
    card_selected = 0
    for i in range(len(Chase.cards)):
        if pos[0] > coords[i, 0] and pos[0] < coords[i, 0] + card_width and pos[1] > coords[i, 1] and pos[1] < coords[i, 1] + card_height:
            is_on_card = True
            card_selected = i
    return [is_on_card, card_selected]

def show_situation(player, computer, pile, is_player_turn):
    player_coords = np.empty((0,2), int)
    player_coords = create_player_coords(player_y, len(player.cards), player_y_has_changed, player_coords)
    screen.blit(text, (5, Y-(Y-(card_height/2))))
    pygame.draw.line(screen, black, (X//2-50, 3), (X//2-50, 110), 3)
    pygame.draw.line(screen, black, (X//2+70, 3), (X//2+70, 110), 3)
    pygame.draw.rect(screen, black, [X//2-25, 5, card_width, card_height], 3, 3)
    draw_card_text = font.render("Draw",True, black)
    draw_card_rect = draw_card_text.get_rect()
    draw_card_rect.center = (X//2-19, 45)
    screen.blit(draw_card_text, (X//2-19, 45))
    draw_pile_card(pile[0], pile[1])
    computer_cards(len(computer.cards))
    draw_player_cards(player_coords, player.cards)
    pygame.draw.rect(screen, black, [X-255, 45, 175, 45], 3, 3)
    restart_text = font.render("Restart", True, black)
    restart_rect = restart_text.get_rect()
    restart_rect.center = (X-200, 57)
    screen.blit(restart_text, (X-200, 57))

colour_coords = np.empty((0,2), int)
def show_colour_switcher(coords, i):
    colour_coords = np.array([[coords[i, 0], coords[i, 1]],[coords[i,0]+50, coords[i,1]],[coords[i,0], coords[i,1]+50],[coords[i,0]+50, coords[i,1]+50]], int)
    return colour_coords

def draw_colour_s(colour_coords):
    pygame.draw.rect(screen,red, [colour_coords[0, 0], colour_coords[0, 1], 50, 50], 0)
    pygame.draw.rect(screen,green, [colour_coords[1, 0], colour_coords[1, 1], 50, 50], 0)
    pygame.draw.rect(screen,blue, [colour_coords[2, 0], colour_coords[2, 1], 50, 50], 0)
    pygame.draw.rect(screen,yellow, [colour_coords[3, 0], colour_coords[3, 1], 50, 50], 0)
    pygame.draw.rect(screen, black, [colour_coords[0,0], colour_coords[0,1], 100, 100], 3)
    pygame.draw.line(screen, black,(colour_coords[1, 0], colour_coords[1, 1]),(colour_coords[1,0], colour_coords[1, 1]+97),2)
    pygame.draw.line(screen, black,(colour_coords[2, 0], colour_coords[2, 1]),(colour_coords[2, 0]+97, colour_coords[2, 1]),2)

player_coords = np.empty((0,2), int)
player_coords = create_player_coords(player_y, len(Chase.cards), player_y_has_changed, player_coords)
# infinite loop
while carryOn:
    # --- Main event loop
    if not is_game_over:
        
        if is_game_started:
            has_to_draw = False
            player_coords = np.empty((0,2), int)
            player_y_has_changed = 0
            player_y = 30
            seed(randint(0, 9999999999999999))
            # DECK_SIZE = 108
            suits = ['R', 'G', 'B', 'Y']
            is_player_turn = True
            is_game_over = False
            is_player_winner = False
            deck = Deck("deck")
            deck.fill_new(suits)
            deck.shuffle()
            pile = ['','']
            DECK_SIZE = 108
            suits = ['R', 'G', 'B', 'Y']
            is_player_turn = True
            is_game_over = False
            is_player_winner = False
            deck = Deck("deck")
            deck.fill_new(suits)
            deck.shuffle()
            pile = ['','']
            while deck.arr[DECK_SIZE-1, 0] == '+' or deck.arr[DECK_SIZE-1, 0] == 'W' or deck.arr[DECK_SIZE-1, 1] == '@' or deck.arr[DECK_SIZE-1, 1] == 'r' or deck.arr[DECK_SIZE-1, 1] == 'S':
                deck.shuffle()
            pile = deck.get_next_card()
            Chase = Player()
            Computer = Player()
            Chase.cards = np.empty((0,2), str)
            Computer.cards = np.empty((0,2), str)
            show_situation(Chase, Computer, pile, is_player_turn)
            for i in range(7):
                Chase.add_card(deck)
                Computer.add_card(deck)
            is_game_started = False
            is_player_choice = False
            player_choice_ind = 0
            show_situation(Chase, Computer, pile, is_player_turn)
            restart_game = False
            r_ind = 0
            has_drawn = False
        if is_player_turn:
            show_situation(Chase, Computer, pile, is_player_turn)
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    carryOn = False # Flag that we are done so we can exit the while loop
                # handle MOUSEBUTTONUP
                if event.type == pygame.MOUSEBUTTONUP and not is_player_choice:
                    show_situation(Chase, Computer, pile, is_player_turn)
                    player_coords = np.empty((0,2), int)
                    player_coords = create_player_coords(player_y, len(Chase.cards), player_y_has_changed, player_coords)
                    # print(player_coords)
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    is_card = check_if_card_touching(pos, player_coords)
                    if is_card[0]:
                        player_coords = np.empty((0,2), int)
                        player_coords = create_player_coords(player_y, len(Chase.cards), player_y_has_changed, player_coords)
                        print(f"Touching {Chase.cards[is_card[1], 0]} {number_switcher.get(Chase.cards[is_card[1], 1])}")
                        colour_choice = "B"
                        wild_switcher = {
                            "+": True,
                            "W": True
                        }
                        card = [Chase.cards[is_card[1], 0], Chase.cards[is_card[1], 1]]
                        is_wild = wild_switcher.get(card[0], False)
                        if is_wild:
                            is_player_choice = True
                            player_choice_ind = is_card[1]
                            show_situation(Chase, Computer, pile, is_player_turn)
                            # colour_choice = input("What colour would you like to play?(R,B,G,Y): ")
                        else:
                            is_player_turn = Chase.play_card(card, is_card[1]+1, Computer, is_wild, colour_choice, pile, is_player_turn, deck)
                            show_situation(Chase, Computer, pile, is_player_turn)
                    elif pos[0] > X-200 and pos[0] < X-200+175 and pos[1] > 57 and pos[1] < 57+45:
                        is_game_started = True
                        is_game_over = True
                        is_player_winner = True
                    if pos[0] > X//2-25 and pos[0] < X//2-25 + card_width and pos[1] > 5 and pos[1] < 5 + card_height:
                        print("You are drawing.")
                        Chase.add_card(deck)
                        player_coords = np.empty((0,2), int)
                        player_coords = create_player_coords(player_y, len(Chase.cards), player_y_has_changed, player_coords)
                        print(player_coords)
                        show_situation(Chase, Computer, pile, is_player_turn)
                        if Chase.cards[len(Chase.cards)-1, 0] != pile[0] and Chase.cards[len(Chase.cards)-1, 1] != pile[1] and Chase.cards[len(Chase.cards)-1, 1] != '$' and Chase.cards[len(Chase.cards)-1, 1] != 'C':
                            is_player_turn = not is_player_turn
                        
                    else:
                        print("Not touching card")
                    show_situation(Chase, Computer, pile, is_player_turn)
                    if len(Chase.cards) == 0:
                        time.sleep(2)
                        is_game_over = True
                        is_player_winner = True
                elif is_player_choice:
                    has_to_draw = True
                    # print(f"Success {player_choice_ind}")
                    player_coords = np.empty((0,2), int)
                    player_coords = create_player_coords(player_y, len(Chase.cards), player_y_has_changed, player_coords)
                    pos = pygame.mouse.get_pos()
                    # show_situation(Chase, Computer, pile, is_player_turn)
                    colour_coords = show_colour_switcher(player_coords, player_choice_ind)
                    # red_s = pygame.Rect(colour_coords[0,0], colour_coords[0,1], 50, 50)
                    # pygame.draw.rect(screen, red, red_s, 0, 3)
                    # print(colour_coords)
                    colour_choice_ind = 0
                    chosen = False
                    draw_colour_s(colour_coords)
                    clicked_colour = False
                    if event.type == pygame.MOUSEBUTTONUP:
                        draw_colour_s(colour_coords)
                        pos = pygame.mouse.get_pos()
                        
                        for i in range(4):
                            if pos[0] > colour_coords[i, 0] and pos[0] < colour_coords[i, 0]+50 and pos[1] > colour_coords[i, 1] and pos[1] < colour_coords[i, 1]+50:
                                colour_choice_ind = i
                                chosen = True
                                has_to_draw = False
                                clicked_colour = True
                                show_situation(Chase, Computer, pile, is_player_turn)                            
                        if not clicked_colour:
                            chosen = False
                            show_situation(Chase, Computer, pile, is_player_turn)
                            is_player_choice = False
                            player_choice_ind = 0
                            clicked_colour = False
                            has_to_draw = False
                    if chosen:
                        clicked_colour = False
                        card = [Chase.cards[player_choice_ind, 0], Chase.cards[player_choice_ind, 1]]
                        is_player_turn = Chase.play_card(card, player_choice_ind+1, Computer, is_wild, colour_switch.get(colour_choice_ind, "B"), pile, is_player_turn, deck)
                        chosen = False
                        show_situation(Chase, Computer, pile, is_player_turn)
                        is_player_choice = False
                        player_choice_ind = 0
        else:
            if Computer.can_player_play(pile):
                available_cards = get_available_cards(Computer, pile)
                get_card_colours(Computer)
                get_card_cata(Computer, available_cards)
                highest_value_card_ind = get_card_values(Computer, pile, available_cards)
                card = [Computer.cards[highest_value_card_ind, 0], Computer.cards[highest_value_card_ind, 1]]
                print("Computer is playing a:", Computer.cards[highest_value_card_ind, 0], Computer.cards[highest_value_card_ind, 1])
                is_player_turn = Computer.play_card(card, highest_value_card_ind+1, Chase, is_wild_switcher.get(card[1], False), Computer.pick_ideal_colour(), pile, is_player_turn, deck)
                show_situation(Chase, Computer, pile, is_player_turn)
                time.sleep(1.5)
            else:
                print("Computer is drawing.")
                Computer.add_card(deck)
                show_situation(Chase, Computer, pile, is_player_turn)
                if Computer.cards[len(Computer.cards)-1, 0] != pile[0] and Computer.cards[len(Computer.cards)-1, 1] != pile[1] and Computer.cards[len(Computer.cards)-1, 1] != '$' and Computer.cards[len(Computer.cards)-1, 1] != 'C':
                            is_player_turn = not is_player_turn
                time.sleep(0.5)
            if len(Computer.cards) == 0:
                time.sleep(2)
                is_game_over = True
                is_player_winner = False
        
        # --- Game logic should go here
    

    # --- Drawing code should go here
    # First, clear the screen to white. 
    screen.fill(white)
    #The you can draw different shapes and lines or add text to your background stage.
    if not is_game_over:
        show_situation(Chase, Computer, pile, is_player_turn)
    if has_to_draw:
        colour_coords = show_colour_switcher(player_coords, player_choice_ind)
        draw_colour_s(colour_coords)
    
    if is_game_over and is_player_winner:
        result = font.render("Congrats! You won!", True, black)
        result_rect = result.get_rect()
        result_rect.center = (X//2-50, Y//2)
        screen.blit(result, (X//2-50,Y//2))
        r_ind += 1
    elif is_game_over and not is_player_winner:
        result = font.render("Sorry. You lost", True, black)
        result_rect = result.get_rect()
        result_rect.center = (X//2-50, Y//2)
        screen.blit(result, (X//2-50,Y//2))
        r_ind += 1
    
    if r_ind == 180:
        is_game_over = False
        is_game_started = True
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    
    # --- Limit to 60 frames per second
    clock.tick(60)
pygame.quit()