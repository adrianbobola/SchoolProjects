#!/usr/bin/env python3

# Povolene knihovny: math

# IB002 Domaci uloha 6.
#
# V nasledujicim textu pouzivame pojem "halda" ve vyznamu "binarni halda".
#
# Minimova halda je v kanonickem tvaru, pokud pro kazdy jeji prvek se dvema
# potomky plati, ze jeho levy potomek je mensi nez ten pravy nebo se oba
# rovnaji.
#
# Je v kanonickem tvaru | Neni v kanonickem tvaru
#                       |
#       (1)             |           (1)
#      /   \            |          /   \
#    (2)   (3)          |        (3)   (2)


# Trida representujici minimovou haldu. Pro praci s ni muzete s vyhodou pouzit
# funkce, ktere jste implementovali v zakladnim domacim ukolu.
# V teto implementaci indexujte od 0, tj. koren je na pozici heap.array[0].

class MinHeap:
    __slots__ = ("size", "array")

    def __init__(self):
        self.size = 0
        self.array = []


# Ukol 1.
# Vasim prvnim ukolem je implementovat funkci is_canonical_min_heap(heap),
# ktera overi, zda je zadana halda 'heap' korektni minimovou haldou
# v kanonickem tvaru. Pokud ano, vrati True, v opacnem pripade vrati False.
#
# Prazdna nebo jednoprvkova halda je v kanonickem tvaru implicitne. Mejte na
# pameti, ze halda v kanonickem tvaru musi splnovat take pozadavky kladene na
# minimovou haldu.
def left_item(i, heap):
    return (2*i+1)

def right_item(i, heap):
    if heap.size == 3:
        return 2
    return (2*i+2)

def is_canonical_min_heap(heap):
    """
    vstup: 'heap' typu MinHeap
           (je zaruceno, ze heap.size je velikost pole heap.array;
            neni zaruceno, ze prvky heap.array splnuji haldovou podminku
            nebo podminku kanonickeho tvaru)
    vystup: True, pokud je 'heap' minimova halda v kanonickem tvaru
            False, jinak
    casova slozitost: O(n), kde 'n' je pocet prvku 'heap'
    """
    for i in range(heap.size):
        if heap.size < 2:
            return True
        elif heap.size == 2:
            if heap.array[0] > heap.array[1]:
                return False
        else: #su 3 a viac
            if (2*i+2) < heap.size:
                if heap.array[i] > heap.array[left_item(i, heap)] or heap.array[i] > heap.array[right_item(i, heap)]:
                    return False
                if heap.array[left_item(i, heap)] > heap.array[right_item(i, heap)]:
                    return False
                
            elif (2*i+1) < heap.size:
                if heap.array[i] > heap.array[left_item(i, heap)]:
                    return False
    return True


# Ukol 2.
# Druhym ukolem je implementovat funkci canonise_min_heap(heap), ktera zadanou
# minimovou haldu 'heap' prevede na kanonicky tvar. Funkce bude menit primo
# haldu zadanou v argumentu, proto nebude vracet zadnou navratovou hodnotu.
#
# Napoveda:
# Pro algoritmus s linearni casovou slozitosti je potreba postupovat takto:
# - Rekurzivne resime od korene k listum haldy;
# - pro kazdy uzel haldy:
#   + zkontrolujeme, jestli potomci splnuji vlastnost kanonickeho tvaru;
#     pokud ne:
#     * prohodime hodnoty leveho a praveho potomka;
#     * tim se muze pokazit vlastnost haldy v pravem podstrome, proto
#       probublame problematickou hodnotu z korene praveho podstromu
#       tak hluboko, aby uz neporusovala vlastnost haldy (pri tomto bublani
#       opravujeme pouze vlastnost haldy, kanonicky tvar neresime)
#   + mame tedy korektni minimovou haldu, ktera navic splnuje kanonicky
#     tvar od tohoto uzlu smerem nahoru;
#   + pokracujeme v rekurzi vlevo a vpravo.

def helper_heap(heap, i):
  

    if  heap.array[left_item(i, heap)] < heap.array[i]:
        helper = heap.array[i]
        heap.array[i] = heap.array[left_item(i, heap)]
        heap.array[left_item(i, heap)] = helper
        
    elif heap.array[right_item(i, heap)] < heap.array[i]:
        helper = heap.array[i]
        heap.array[i] = heap.array[right_item(i, heap)]
        heap.array[right_item(i, heap)] = helper

    if heap.array[left_item(i, heap)] > heap.array[right_item(i, heap)]:
        helper = heap.array[left_item(i, heap)]
        heap.array[left_item(i, heap)] = heap.array[right_item(i, heap)]
        heap.array[right_item(i, heap)] = helper
        
def canonise_min_heap(heap):
    """
    vstup: 'heap' korektni minimova halda typu MinHeap
    vystup: funkce nic nevraci, vstupni halda 'heap' je prevedena
            do kanonickeho tvaru (pritom obsahuje stejne prvky jako na zacatku)
    casova slozitost: O(n), kde 'n' je pocet prvku 'heap'
    """
    i = 0
    while((2*i+3) <= heap.size):
        helper_heap(heap, i)
        i += 1
        
    if (2*i+2) <= heap.size:
        if heap.array[left_item(i, heap)] < heap.array[i]:
            helper = heap.array[i]
            heap.array[i] = heap.array[left_item(i, heap)]
            heap.array[left_item(i, heap)] = helper

    for i in range(heap.size):
        if ((2*i+3) <= heap.size):
            helper_heap(heap, i)
        if (2*i+2) <= heap.size:
            if heap.array[left_item(i, heap)] < heap.array[i]:
                helper = heap.array[i]
                heap.array[i] = heap.array[left_item(i, heap)]
                heap.array[left_item(i, heap)] = helper
