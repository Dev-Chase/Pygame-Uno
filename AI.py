def get_card_colours(player):
    player.reds = 0
    player.greens = 0
    player.blues = 0
    player.yellows = 0
    for i in player.cards:
        if i[0] == 'R':
            player.reds += 1
        elif i[0] == 'G':
            player.greens += 1
        elif i[0] == 'B':
            player.blues += 1
        elif i[0] == 'Y':
            player.yellows += 1
            
def get_card_cata(player, arr):
    player.r_cards = 0
    player.a_cards = 0
    player.w_cards = 0
    for i in range(len(arr)):
        if player.cards[arr[i], 0] == 'W' or player.cards[arr[i], 0] == '+':
            player.w_cards += 1
        elif player.cards[arr[i], 1] == '@' or player.cards[arr[i], 1] == 'r' or player.cards[arr[i], 1] == 'S':
            player.a_cards += 1
        else:
            player.r_cards += 1
def get_available_cards(player, pile):
    list_of_card_ind = []
    for i in range(len(player.cards)):
        if player.cards[i, 0] == pile[0] or player.cards[i, 0] == '+' or player.cards[i, 0] == 'W' or player.cards[i, 1] == pile[1]:
            list_of_card_ind.append(i)
    return list_of_card_ind
def get_card_values(player, pile, list_of_card_ind):
    highest_value_card = 0  
    card_values = []
    if player.r_cards + player.a_cards != 0:
        for i in range(len(list_of_card_ind)):
            if player.cards[list_of_card_ind[i], 0] == pile[0] or player.cards[list_of_card_ind[i], 1] == pile[1]:
                if player.cards[list_of_card_ind[i], 1] == 'r' or player.cards[list_of_card_ind[i], 1] == 'S':
                    card_values.append(6)
                elif player.cards[list_of_card_ind[i], 1] == '@':
                    if pile[1] == '@':
                        card_values.append(8)
                    else:
                        card_values.append(4)
                else:
                    card_values.append(2)
            else:
                card_values.append(1)
    elif player.r_cards + player.a_cards == 0 and player.w_cards > 0:
        for i in range(len(list_of_card_ind)):
            if player.cards[list_of_card_ind[i], 1] == 'C':
                card_values.append(4)
            elif player.cards[list_of_card_ind[i], 1] == '$' and pile[1] != '$':
                card_values.append(6)
            elif player.cards[list_of_card_ind[i], 1] == '$' and pile[1] == '$':
                card_values.append(8)
            else:
                card_values.append(2)

    if len(list_of_card_ind) == len(card_values):
        if len(list_of_card_ind) != 1:
            for i in range(len(list_of_card_ind)):
                if i != len(list_of_card_ind)-1:
                    if card_values[i] > card_values[i+1]:
                        highest_value_card = list_of_card_ind[i]
                    else:
                        highest_value_card = list_of_card_ind[i+1]
        elif len(list_of_card_ind) == 1:
            highest_value_card = list_of_card_ind[0]
    else:
        print("What on earth did you do for this to happen?")
    return highest_value_card