#!/usr/bin/env python3

# Povolene knihovny: math
# (Poznamka: "povolene" neznamena "nutne"; ukol je mozno snadno vyresit i bez
#  jakychkoli knihoven.)

# IB002 Domaci uloha 3.
#
# Vasi ulohou bude s vyuzitim principu binarniho vyhledavani implementovat
# dve funkce, find_first_occurrence a find_first_greater. V obou pripadech
# musi casova slozitost vaseho algoritmu byt nejhure logaritmicka, tedy byt
# v O(log n). (Pozor, iterovani v poli a slicing a[x:y] ma linearni slozitost.)
# Funkce nesmi modifikovat vstupni pole.


# Ukol 1.
# Implementujte funkci find_first_occurrence, ktera vrati index prvniho
# vyskytu prvku key v serazenem poli numbers. Pokud se prvek v poli
# nevyskytuje, vrati -1.
#
# Priklady vstupu a vystupu:
# find_first_occurrence(2, [1, 2, 2, 2, 4]) -->  1
# find_first_occurrence(3, [1, 2, 4, 5])    --> -1

def find_first_occurrence(key, numbers):
    """
    vstup: 'key' hodnota hledaneho cisla, 'numbers' serazene pole cisel
    vystup: index prvniho vyskytu hodnoty 'key' v poli 'numbers',
            -1, pokud se tam tato hodnota nevyskytuje
    casova slozitost: O(log n), kde 'n' je pocet prvku pole 'numbers'
    """
    minimum = 0
    maximum = len(numbers)-1
    while minimum <= maximum:
        middle = (minimum + maximum) // 2
        if numbers[middle] == key:
            if (numbers[middle - 1] == key):
                maximum = middle-1
            else:
                return middle
            
        elif numbers[middle] > key:
            maximum = middle - 1
        else:
            minimum = middle + 1
    if len(numbers) != 0:
        if numbers[middle] == key:
            return middle
        else:
            return -1
    else:
        return -1
    

# Ukol 2.
# Implementujte funkci find_first_greater modifikaci predchozi funkce
# find_first_occurrence tak, ze find_first_greater vrati index prvniho prvku
# v poli vetsiho nez key. Neni-li v poli zadny takovy, vrati -1.
#
# Priklady vstupu a vystupu:
# find_first_greater(2, [1, 2, 4, 5]) -->  2
# find_first_greater(3, [1, 2, 4, 5]) -->  2
# find_first_greater(3, [1, 2, 3])    --> -1
def find_first_greater(key, numbers):
    """
    vstup: 'key' hodnota hledaneho cisla, 'numbers' serazene pole cisel
    vystup: index prvniho vyskytu prvku vetsiho nez hodnota 'key',
            -1, pokud tam zadny takovy prvek neni
    casova slozitost: O(log n), kde 'n' je pocet prvku pole 'numbers'
    """
    if len(numbers) > 0:
        minimum = 0
        maximum = len(numbers) - 1
    else:
        return -1
        
    while minimum <= maximum:
        middle = (minimum + maximum) // 2
        if numbers[middle] == key:
            if ((middle + 1 != len(numbers)) and (numbers[middle + 1] == key)):
                minimum = middle + 1
            elif ((middle + 1 != len(numbers)) and (numbers[middle + 1] != key)):
                return middle + 1
            else:
                return -1
        elif numbers[middle] < key:
            minimum = middle + 1
        else:
            maximum = middle - 1
    if (key < numbers[middle]):
        return middle
    elif (middle == len(numbers)-1 and key >= numbers[middle]):
        return -1
    else:
        return middle + 1
