"""Autor: Adrián Bobola, 485641

Prohlašuji, že celý zdrojový kód jsem zpracoval(a) zcela samostatně.
Jsem si vědom(a), že  nepravdivost tohoto tvrzení může být důvodem
k hodnocení F v předmětu IB111 a k disciplinárnímu řízení."""

from random import random, randint, seed, choices

# sem prijdou konstanty - napr. pro hodnotu Black Jack
BLACK_JACK = 21
PLAYER_RISK = 0.6  # pravdepodobnost, se kterou hrac riskuje
FAIR_PROB = 1/13  # pravdepodobnost, se kterou je vytahovano eso
ALL_CARDS = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
SPECIAL_CARDS = [10, 'J', 'Q', 'K', 'A']
SUM_SPECIAL_CARDS = [10, 'J', 'Q', 'K']
CARDS_PROB = [FAIR_PROB]

for i in range(12):
    other_cards = (1 - FAIR_PROB)/12
    CARDS_PROB.append(other_cards)


# sem prijdou pomocne funkce - napr. pro vytazeni nahodne karty, vypis jednoho kola hry nebo
#  zkontrolovani, zda prvni dve karty davaji Black Jack
def check_black_jack(cards):
    if (cards[0] in SPECIAL_CARDS) and (cards[1] in SUM_SPECIAL_CARDS):
        return True
    else:
        return False


def sum_cards(cards):
    suma = 0
    for i in cards:
        if(i in SUM_SPECIAL_CARDS):
            suma += 10
        elif(i == 'A'):
            suma += 1
        else:
            suma += i
    return suma


def player_cards():
    return choices(ALL_CARDS, CARDS_PROB)[0]


def final_sum(player_score, croupier_score, output):
    if (player_score > 21) or (player_score < croupier_score):
        if output is True:
            print("Player lost.")
        return 0

    elif player_score is croupier_score:
        if output is True:
            print("It's a tie.")
        return 0

    elif (player_score > croupier_score) and (player_score <= 21):
        if output is True:
            print("Player win.")
        return 1


def after_round(nround, cards, player_score, output):
    if output is True:
        print("************************")
        print("Round: ", nround)
        print("Player cards: ", cards)
        print("Player score: ", player_score)


def begin_game(cards, player_score, output):
    if (output is True):
        print("Game beginning!")
        print("Player cards: ", cards)
        print("Player score: ", player_score)


def end_game(croupier_score, output):
    if output is True:
        print("************************")
        print("Croupier score: ", croupier_score)


def player_turn(player_score, card_prob, risk_prob):
    """
    Funkce simulujici tah hrace: rozhoduje se, zda si vytahnout dalsi kartu. Pokud ma skore mensi
    nez 17, vytahne vzdy, pokud vetsi nebo rovno 17, zariskuje a vytahne s pravdepodobnosti risk_prob.

    :param player_score: aktualni skore hrace
    :param card_prob: pravdepodobnost, se kterou je vytahovano eso (pro volani funkce vybirajici kartu)
    :param risk_prob: pravdepodobnost, se kterou hrac riskuje
    :return: 0 pokud se hrac rozhodl skoncit (nebrat dalsi kartu), jinak ciselna reprezentace nove karty
    """
    if(player_score < 17):
        return choices(ALL_CARDS, CARDS_PROB)[0]
    else:
        probabilty = randint(0, 100)
        if (probabilty < (risk_prob * 100)):
            return choices(ALL_CARDS, CARDS_PROB)[0]
        else:
            return 0


# Známé nedostatky: žiadne
# Styl: Snáď v poriadku
def game(card_prob=FAIR_PROB, risk_prob=PLAYER_RISK, output=True):
    """
    Funkce obsahujici hlavni smycku hry. Na zacatku hrac dostane dve karty a nastavi se jeho skore,
    pricemz se zkontroluje, jestli vytahl Black Jack. Potom hrac tahne tolikrat, dokud se nerozhodne
    skoncit (jakoby vytahne 0) nebo dokud nedosahne skore vetsiho nebo rovneho 21. Na konci se
    porovnanim s krupierovym skore vyhodnoti, zda hrac vyhral.

    :param card_prob: pravdepodobnost, se kterou je vytahovano eso (pri ferovem balicku karet = 1/13)
    :param risk_prob: pravdepodobnost, se kterou hrac riskuje
    :param output: True pokud se ma vypisovat stav hry, False pokud ma pouze probehnout analyza
    :return: 1 kdyz hrac vyhraje, jinak 0 (v pripade remizy i prohry)
    """
    player_score = 0
    croupier_score = 0
    cards = []
    nround = 0
    next_turn = 1

    for i in range(2):
        cards.append(player_cards())

    if check_black_jack(cards) is True:
        player_score = 21
    else:
        player_score = sum_cards(cards)

    begin_game(cards, player_score, output)
    while (player_score < 21):
        cards.append(player_turn(player_score, card_prob, risk_prob))
        nround += 1
        if cards[len(cards)-1] == 0:
            break
        player_score = sum_cards(cards)
        after_round(nround, cards, player_score, output)

    croupier_score = randint(17, 21)
    end_game(croupier_score, output)
    winer = final_sum(player_score, croupier_score, output)
    return winer


# Známé nedostatky: žiadne
# Styl: Snáď v poriadku
def risk_analysis():
    """
    Funkce spusti pro kazdou ze 100 ruznych hodnot pravdepodobnosti riskovani 10 000 her a vypise,
    v kolika procentech her hrac vyhral s danou pravdepodobnosti.
    :return: -
    """
    for i in range(100):
        suma = 0
        for j in range(10000):
            suma += game(card_prob=FAIR_PROB, risk_prob=i/100, output=False)
        print("Risk probability %0.2f -> percent of games won: %0.2f" % (i/100, (suma/j)*100)+'%')
    result2 = (suma/j)*100
    return result2


# Známé nedostatky: Nie som si istý, či to robí to, čo očakaváme od bias analysis
# Styl: Snáď v poriadku
"""
uroven riskovani 0.2 = 0.20
uroven riskovani 0.4 = 0.10
uroven riskovani 0.6 = 0.55
"""


def bias_analysis(risk_prob=PLAYER_RISK):
    """
    Funkce vyzkousi deset ruznych hodnot card_prob(pravdepodobnosti vytazeni esa) - kazdou v 1000
    hrach - a vypise, pri ktere card_prob hrac vyhral nejvickrat.
    :return: -
    """
    results = []
    prob = ['0,10', '0,15', '0,20', '0,25', '0,30', '0,35', '0,40', '0,45', '0,50', '0,55']
    best_prob = 0
    card_prob2 = 0
    for i in range(10):
        suma = 0
        card_prob2 = prob[i]
        for j in range(1000):
            suma += (game(card_prob=card_prob2, risk_prob=risk_prob, output=False))
        results.append(suma)

    best_result = results[0]
    for i in range(len(results)):
        if results[i] > best_result:
            best_result = results[i]

    for i in range(len(results)):
        if results[i] == best_result:
            best_prob = prob[i]

    print("Risk level %0.2f, best biased ace probability:" % risk_prob, best_prob)
