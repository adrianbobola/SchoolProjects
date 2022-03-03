"""Autor: Adrián Bobola, 485641

Prohlašuji, že celý zdrojový kód jsem zpracoval(a) zcela samostatně.
Jsem si vědom(a), že  nepravdivost tohoto tvrzení může být důvodem
k hodnocení F v předmětu IB111 a k disciplinárnímu řízení.
"""

from turtle import Turtle


# Známé nedostatky: žiadne
# Styl: Snáď v poriadku
def sequence(n):
    """
    Vypise prvnich n nasobku cisla 3, kde kazdy 5. prvek bude cislo 2. Tedy
    následujici posloupnost 3, 6, 9, 12, 2, 18, 21, 24, 27, 2, 33, 36, ...

    :param n: prirozene cislo vetsi rovno 1 udavajici, kolik prvku posloupnosti
              se ma vypsat

    >>> sequence(12)
    3, 6, 9, 12, 2, 18, 21, 24, 27, 2, 33, 36
    """
    for i in range(1, n+1):
        if (i == n):
            if (i % 5 == 0):
                print("2", end=" ")
            else:
                print(i*3, end=" ")
        else:
            if (i % 5 == 0):
                print("2", end=", ")
            else:
                print(i*3, end=", ")


# Známé nedostatky: žiadne
# Styl: Veľa krát použitá funkcia for. Nevedel som to inak upraviť, keďže kažé for vypisuje inú vec
def remainder_table(n):
    """
    Funkce pro zadane n vypise tabulku velikosti nxn (+ popisne radky a
    sloupce), kde v sloupci s a radku r bude T, prave tehdy kdyz zbytek po
    deleni cisla s cislem r je vetsi nez 2.

    :param n: prirozene cislo mezi 1 a 9 vcetne

    >>> remainder_table(3)
        1 2 3
        - - -
    1 | F F F
    2 | F F F
    3 | F F F

    >>> remainder_table(5)
        1 2 3 4 5
        - - - - -
    1 | F F F F F
    2 | F F F F F
    3 | F F F F F
    4 | F F T F F
    5 | F F T T F
    """
    for i in range(2):
        print(" ", end=" ")
    for i in range(1, n+1):
        print(i, end=" ")
    print()
    for i in range(2):
        print(" ", end=" ")
    for i in range(1, n+1):
        print("-", end=" ")
    print()
    for s in range(1, n+1):
        print(s, end=" ")
        print("|", end=" ")
        for r in range(1, n+1):
            if (r % s > 2):
                a = "T"
            else:
                a = "F"
            print(a, end=" ")
        print()


# Známé nedostatky: žiadne
# Styl: Snáď v poriadku
def hourglass(size):
    """
    Funkce vykresli prsypaci hodiny pomoci textove grafiky, ktere budou mi
    vysku a sirku rovnou size. Okraje hodin tvori znak #, vnitrek znak . a
    zbytek jsou mezery

    :param size: prirozene cislo vetsi rovno 3 udavajci velikost obrazku

    >>> hourglass(3)
    ###
     #
    ###

    >>> hourglass(5)
    #####
     #.#
      #
     #.#
    #####

    >>> hourglass(10)
    ##########
     #......#
      #....#
       #..#
        ##
        ##
       #..#
      #....#
     #......#
    ##########
    """
    for i in range(0, size):
        for j in range(0, size):
            if(i == j) or (i == 0) or (i == size-1) or (j+1 == size-i):
                print("#", end="")
            elif((j > i) and (j + 1 < size - i) or (j < i) and (j + 1 > size - i)):
                print(".", end="")
            else:
                print(" ", end="")
        print()


# Známé nedostatky: Pri n=párne číslo je stred písmena R posunutý
# Styl: Neprehľadnosť kódu kvôli spájaniu podmienok, ale inak som to nevedel urobiť
def draw_r(size):
    """
    Funkce pomoci textove grafiky vykresli znak velke R.

    :param size: prirozene cislo vetsi rovno 5

    >>> draw_r(5)
    ####
    #   #
    ####
    #  #
    #   #

    >>> draw_r(10)
    #########
    #        #
    #        #
    #        #
    #########
    #    #
    #     #
    #      #
    #       #
    #        #
    """
    for i in range(0, size):
        for j in range(0, size):
            if(i == 0)and(j < size - 1) or (j == 0) or (i == size//2)and(j < size - 1) or ((i < size//2)and(j == size-1)and(i > 0)) or ((i > size//2)and(i == j)):
                print("#", end="")
            else:
                print(" ", end="")
        print()


# Známé nedostatky: posun o pár stupňov medzi jednotlivými kvetmi.
# Styl: Snáď v poriadku
def flowers():
    """
    Funkce vykresli pomoci zelvi grafiky 7 sousedicich kyticek (viz obrazek
    v zadani)
    """
    turtle = Turtle()
    for k in range(6):
        turtle.penup()
        turtle.right(11)
        turtle.forward(115)
        turtle.pendown()
        turtle.left(11)
        for j in range(3):
            turtle.forward(50)
            turtle.left(60)
            for i in range(3):
                turtle.forward(25)
                turtle.left(60)
            turtle.forward(50)
        turtle.left(60)
        for j in range(3):
            turtle.forward(50)
            turtle.left(60)
            for i in range(3):
                turtle.forward(25)
                turtle.left(60)
            turtle.forward(50)
    turtle.penup()
    turtle.left(50)
    turtle.forward(115)
    turtle.pendown()
    turtle.left(10.5)
    for k in range(2):
        for j in range(3):
            turtle.forward(50)
            turtle.left(60)
            for i in range(3):
                turtle.forward(25)
                turtle.left(60)
            turtle.forward(50)
        turtle.left(60)


# Známé nedostatky: žiadne
# Styl: Snáď v poriadku
def snowflake():
    """
    Funkce vykresli pomoci zelvi grafiky snehovou vlocku (viz obrazek v zadani)
    """
    turtle = Turtle()
    turtle.pensize(3)
    turtle.pencolor("skyblue")
    for k in range(8):
        turtle.left(45)
        turtle.forward(100)
        for l in range(5):
            turtle.left(45)
            turtle.forward(100/5)
            turtle.backward(100/5)
            turtle.right(90)
            turtle.forward(100/5)
            turtle.backward(100/5)
            turtle.left(45)
            turtle.backward(100/5)
