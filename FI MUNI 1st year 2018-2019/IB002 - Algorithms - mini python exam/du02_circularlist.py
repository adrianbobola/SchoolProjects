#!/usr/bin/env python3

# IB002 Domaci uloha 2.
#
# Jednosmerne spojovany seznam uz znate - jde o zretezeny seznam uzlu (Node),
# kde kazdy uzel ukazuje na sveho naslednika. V tomto prikladu nemame first
# (ani last), seznam je zadany "prvnim" ze svych uzlu.
# Seznamy v teto uloze nikdy nebudou prazdne, tj. vzdy muzete predpokladat,
# ze na vstupu je objekt typu Node.
#
# Tato uloha pracuje se dvema typy jednosmerne spojovanych seznamu:
# Linearni seznam - kde posledni prvek seznamu ukazuje na None.
# Kruhovy seznam - kde posledni prvek seznamu ukazuje zpet na prvni prvek.
#
# Pro vsechny funkce muzete predpokladat, ze seznam na vstupu je linearni,
# nebo kruhovy, tj. nemusite napriklad osetrovat situaci, kdy naslednikem
# "posledniho" v seznamu je "druhy".
#
# Podobne jako u minule ulohy, smyslem je vyzkouset si praci s odkazy.
# I v teto uloze je tedy zakazano pouzivat seznamy (list), slovniky (dict)
# a mnoziny (set).
# Rovnez nejsou povoleny zadne Pythonovske knihovny.
# (Pokud chcete tyto veci pouzivat pro vlastni testovani, nezapomente je
#  pred odevzdanim vymazat nebo zakomentovat.)
#
# Ve vystupu vyhodnocovaci sluzby znazornujeme jednosmerne spojovane seznamy
# podobne jako u minuleho ukolu:
#
# Toto je linearni seznam o trech prvcich:
# linearni seznam: -> 7 -> 42 -> 17
# Toto je kruhovy seznam o trech prvcich:
# kruhovy seznam: -> 7 -> 42 -> 17 -> zpet na zacatek
#
# Do definice tridy Node nijak nezasahujte.


class Node:
    """Trida Node reprezentujici prvek ve spojovanem seznamu

    Atributy:
        key        klic daneho uzlu (cele cislo)
        next       odkaz na dalsi prvek seznamu
        opposite   odkaz na protejsi prvek seznamu, viz ukol 3.
    """

    __slots__ = ('key', 'next', 'opposite')

    def __init__(self):
        self.key = 0
        self.next = None
        self.opposite = None
        
# Ukol 1.
# Implementujte funkci is_circular, ktera dostane prvni uzel seznamu
# a otestuje, zda je zadany zretezeny seznam kruhovy.

def is_circular(node):
    """
    vstup: 'node' prvni uzel seznamu, ktery je linearni, nebo kruhovy
    vystup: True, pokud je seznam z uzlu 'node' kruhovy
            False, jinak
    casova slozitost: O(n), kde 'n' je pocet prvku seznamu
    """    
    helper = node
    while (helper.next != None) and (helper.next != node):
        helper = helper.next
        
    if helper.next == node:
        return True
    else:
        return False

# Ukol 2.
# Implementujte funkci get_length, ktera vrati delku (tj. pocet uzlu)
# linearniho nebo kruhoveho zretezeneho seznamu zacinajiciho v zadanem uzlu.

def get_length(node):
    """
    vstup: 'node' prvni uzel seznamu, ktery je linearni, nebo kruhovy
    vystup: pocet prvku v zadanem seznamu
    casova slozitost: O(n), kde 'n' je pocet prvku seznamu
    """
    
    helper = node
    pocet = 1
    while (helper.next != None) and (helper.next != node):
        pocet += 1
        helper = helper.next
    return pocet


# Ukol 3.
# Implementujte funkci calculate_opposites, ktera korektne naplni atributy
# "opposite" v uzlech kruhoveho seznamu sude delky. Tj. pro kruhove seznamy
# delky 2n naplni u kazdeho uzlu atribut opposite uzlem, ktery je o n kroku
# dale (tedy v kruhu je to uzel "naproti").
#
# Napriklad v kruhovem seznamu 1 -> 2 -> 3 -> 4 (-> 1) je opposite
# uzlu 1 uzel 3, uzlu 2 uzel 4, uzlu 3 uzel 1 a uzlu 4 uzel 2.
#
# Pokud vstupni seznam neni kruhovy nebo ma lichou delku, tak funkce
# calculate_opposites seznam neupravuje.
#
# Pozor na casovou a prostorovou slozitost vaseho algoritmu!

def calculate_opposites(node):
    """
    vstup: 'node' prvni uzel seznamu, ktery je linearni, nebo kruhovy
    vystup: nic, kokretne doplni atribut opposite pro kruhovy seznam sude delky
    casova slozitost: O(n), kde 'n' je pocet prvku seznamu
    """
    length = get_length(node)
    step = length // 2
    if (is_circular(node) == True) and (length % 2 == 0):
        helper = node
        for i in range(step):
            helper = helper.next
            
        for i in range(length):
            node.opposite = helper
            helper = helper.next
            node = node.next
