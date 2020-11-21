"""Autor: Adrián Bobola, 485641

Prohlašuji, že celý zdrojový kód jsem zpracoval(a) zcela samostatně. Jsem si vědom(a),
že  nepravdivost tohoto tvrzení může být důvodem k hodnocení F v předmětu IB111 a k disciplinárnímu řízení.
"""
from random import randint
from typing import List


def player_input():
    print("Zadaj suradnice bodu v tvare X,Y: ", end="")
    sur = input().split(',')
    for i in range(len(sur)):
        if sur[i].isdigit():
            sur[i] = int(sur[i])
    return sur


def print_state(state):
    for i in range(2):
        print(" ", end=" ")
    for i in range(0, len(state)):
        print(i, end=" ")
    print()
    for i in range(2):
        print(" ", end=" ")
    for i in range(0, len(state)):
        print("-", end=" ")
    print()

    for s in range(0, len(state)):
        print(s, end=" ")
        print("|", end=" ")
        for j in range(len(state[0])):
            print(state[s][j], end=" ")
        print()


def is_winner(state):
    items_main_diagonal = []  # all items in the main diagonal
    items_second_diagonal = []  # all items in the second diagonal
    for i in range(len(state)):
        items_col = []  # all items in coll
        items_main_diagonal.append(state[i][i])
        items_second_diagonal.append(state[i][-1 - i])
        for j in range(len(state)):
            items_col.append(state[j][i])

        if o_count(state[i]) == 5:  # check in row
            return True
        elif x_count(state[i]) == 5:
            return True
        elif o_count(items_col) == 5:  # check in col
            return True
        if x_count(items_col) == 5:
            return True
    if o_count(items_main_diagonal) == 5:  # check in diagonal
        return True
    if x_count(items_main_diagonal) == 5:
        return True
    if o_count(items_second_diagonal) == 5:
        return True

    if x_count(items_second_diagonal) == 5:
        return True
    else:
        return False


def x_count(array):
    count = 0
    allcounts = []
    pos = -5  # default for pos
    for i in range(len(array)):
        if array[i] == 'X' and i - pos > 1:
            allcounts.append(count)
            count = 1
            pos = i
        elif array[i] == 'X' and i - pos == 1:
            count += 1
            pos += 1
    allcounts.append(count)
    return max(allcounts)


def o_count(array):
    count = 0
    allcounts = []
    pos = -5  # default for pos
    for i in range(len(array)):
        if array[i] == 'O' and i - pos > 1:
            allcounts.append(count)
            count = 1
            pos = i
        elif array[i] == 'O' and i - pos == 1:
            count += 1
            pos += 1
    allcounts.append(count)
    return max(allcounts)


# Funkcia change_mark funguje len pre riadky s parametrom size=5. Všeobecné riešenie pre size=n a stĺpce má nenapadlo.
def change_mark(state):
    for i in range(len(state)):
        if (state[i][0] == "X" and state[i][-1] == "X") and (state[i][1] == "X" or state[i][1] == "O") and (
                state[i][2] == "X" or state[i][2] == "O") and (state[i][3] == "X" or state[i][3] == "O"):
            for j in range(1, len(state)):
                state[i][j] = "X"
        elif (state[i][0] == "O" and state[i][len(state) - 1] == "O") and (
                state[i][1] == "X" or state[i][1] == "O") and (
                state[i][2] == "X" or state[i][2] == "O") and (state[i][3] == "X" or state[i][3] == "O"):
            for j in range(1, 4):
                state[i][j] = "O"
    return state


def valid_move(state, position):
    if (state[int(position[0])][int(position[1])] == "X") or (state[int(position[0])][int(position[1])] == "O"):
        return False
    else:
        return True


def check_mark_row(state, mark):
    helper = []
    mark_in_row = []
    mark_in_number_row = []

    for i in range(len(state)):
        helper.append(state[i])
    if mark == "X":
        for i in range(len(helper)):
            mark_in_row.append(x_count(helper[i]))
            mark_in_number_row.append(i)
    elif mark == "O":
        for i in range(len(helper)):
            mark_in_row.append(o_count(helper[i]))
            mark_in_number_row.append(i)

    for i in range(len(mark_in_row)):
        if mark_in_row[i] == 4:
            return mark_in_number_row[i]
    return False


def check_mark_col(state, mark):
    helper = []
    mark_in_col = []
    mark_in_number_col = []

    state_inverse: List[List[str]] = []
    for j in range(len(state)):
        state_inverse.append([" " for i in range(len(state))])

    for i in range(len(state_inverse)):
        for j in range(len(state_inverse)):
            state_inverse[i][j] = state[j][i]

    for i in range(len(state_inverse)):
        helper.append(state_inverse[i])

    if mark == "X":
        for i in range(len(helper)):
            mark_in_col.append(x_count(helper[i]))
            mark_in_number_col.append(i)
    elif mark == "O":
        for i in range(len(helper)):
            mark_in_col.append(o_count(helper[i]))
            mark_in_number_col.append(i)

    for i in range(len(mark_in_col)):
        if mark_in_col[i] == 4:
            return mark_in_number_col[i]
    return False


# Známé nedostatky: Samotná funkcia strategy by mala byť v poriadku.
# Styl: Asi v poriadku.
def strategy(state, mark):
    """
    Funkce, ktera pro zadany stav vrarati tah, ktery se ma zahrat.
    :param state: hraci plocha reprezentovana seznamen seznamu obsahujicich
                  znaky ' ', 'X' nebo 'O'.
    :param mark: znacka ('X' nebo 'O'), pro kterou ma funkce najit vhodne
                 misto pro umisteni na hernim planu
    :return: dvojice (radek, sloupc) popisujici tah.
    """
    if check_mark_row(state, mark):
        x = int(check_mark_row(state, mark))
        y = 0
        default = [x, y]
        while not (valid_move(state, default)):
            y += 1
            default = [x, y]
        return (x, y)

    elif check_mark_col(state, mark):
        x = 0
        y = int(check_mark_col(state, mark))
        default = [x, y]
        while not (valid_move(state, default)):
            x += 1
            default = [x, y]
        return (x, y)

    else:
        x = randint(0, len(state) - 1)
        y = randint(0, len(state) - 1)
        default = [x, y]
        while not (valid_move(state, default)):
            x = randint(0, len(state) - 1)
            y = randint(0, len(state) - 1)
            default = [x, y]
        return (x, y)


# Známé nedostatky: Ak je size=n, tak nefunguje reverzia znakov, pre n=5 funguje iba v riadku.
# Styl: Neprehľadnosť kódu.
def play(size, human_starts=True):
    """
    Funkce pro simulaci hry jednoho hrace s pocitacem.
    :param size: prirozene cislo vetsi rovno 5 udavajici velikost herniho
                 planu
    :param human_starts: booleovsky prepinach udavajici, zda ma zacinat hrac
    """

    state: List[List[str]] = []
    for j in range(size):
        state.append([" " for i in range(size)])

    repeat = False
    computer = "X"
    human = "O"
    player_turn = False

    if human_starts:
        computer = "O"
        human = "X"
        player_turn = True
        print("Zacinas a preto tvoj znak je: ", human)

    while is_winner(state) is False:
        print_state(state)
        print()
        if player_turn:
            print("Na tahu: hrac")
            sur = player_input()
            change_mark(state)

            if int(max(sur)) < size:
                if valid_move(state, sur):
                    state[int(sur[0])][int(sur[1])] = human
                    change_mark(state)
                    player_turn = False
                else:
                    repeat = True
            else:
                repeat = True

            while repeat is True:
                sur = player_input()
                if int(max(sur) < size):
                    if valid_move(state, sur):
                        state[int(sur[0])][int(sur[1])] = human
                        player_turn = False
                        repeat = False
                    else:
                        repeat = True
                else:
                    repeat = True
            if is_winner(state) is True:
                print_state(state)
                print("Player win.")
        else:
            print("Na tahu: pocitac")
            position = strategy(state, computer)
            state[position[0]][position[1]] = computer

            if is_winner(state) is True:
                change_mark(state)
                print_state(state)
                print("Computer win.")

                break
            player_turn = True
            
