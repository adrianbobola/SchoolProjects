"""
Autor: Adrián Bobola, 485641

Prohlašuji, že celý zdrojový kód jsem zpracoval(a) zcela samostatně.
Jsem si vědom(a), že  nepravdivost tohoto tvrzení může být důvodem k
hodnocení F v předmětu IB111 a k disciplinárnímu řízení.
"""

import math
from PIL import Image

# Známé nedostatky: Žádné.
# Styl: Chcel som kód kvôli prehľadnosti rozdeliť na funkciu, ktorá bude vraciať hodnoty nového pixelu.
# Pri rozdelení na viac funkcii sa daný obrázok musel otvárať width*height -krát vo funkcii, preto som tento nápad nevyužil, keďže aj samotné rozostrenie obrázka je časovo dosť náročné.
def transform(image_path):  # Funkcia Blur image
    """
    Funkce ztransformuje zadany obrazek a ulozi jej do stejne slozky pod
    stejnym jmenem s pridanym "_modified" na konec jmena souboru pred
    koncovkou.

    :param image_path: string obsahujici cestu k obrazku
    """
    image = Image.open(image_path)
    image.convert("RGB")
    width, height = image.size
    name = image_path[:len(image_path) - 4]
    for x in range(1, width - 1):
        for y in range(1, height - 1):
            sum_r = 0
            sum_g = 0
            sum_b = 0
            for i in range(-1, 2):
                for j in range(-1, 2):  # all pixels around
                    r, g, b = image.getpixel((x + i, y + j))
                    sum_r += r
                    sum_g += g
                    sum_b += b

            new_r = sum_r // 9  # average of all pixels around
            new_g = sum_g // 9
            new_b = sum_b // 9
            image.putpixel((x, y), (new_r, new_g, new_b))
    filename = name + "_modified.jpg"
    image.save(filename)


# Známé nedostatky: Automatické testy na Aise hlásia chybu pri hľadaní rýmu k slovu "xxxxx" - Očakávany výstup má byť zoznam s 5 prvkami.
# Nemyslím si, že je to chyba programu, keďže v zadanom súbore so slovami skutočne neexistuje ani jedno slovo, ktoré by sa rýmovalo s xxxxx. Preto môj program vráti prázdny zoznam.
# Styl: Asi v poriadku.
def rhymes_with(word, file_path):
    """
    Funkce najde 5 nejlepe se rymujicich slov se slovem v parametru "word"
    v souboru slov nachazejicim se na ceste "file_path".
    :param word: string se slovem
    :param file_path: string s cestou k souboru se slovy, soubor obsahuje jedno
                      slovo na jeden radek
    :return: seznam 5 nejlepe se rymujicich slov se zadanym slovem

    >>> print(rhymes_with("kuskus", "ceska_slova.txt"))
    ['meniskus', 'skus', 'abakus', 'autofokus', 'cirkus']

    >>> print(rhymes_with("sedmikráska", "ceska_slova.txt"))
    ['sedmikráska', 'kráska', 'jiráska', 'teráska', 'vráska']
    """
    word_reversed = word[::-1]
    word_len = len(word_reversed)
    output = []
    while len(output) < 5 and word_len > 0:
        with open(file_path, 'r', encoding="utf-8") as file:
            for line in file.readlines():
                line = line.strip()
                line = line[::-1]
                if line[:len(word_reversed)] == word_reversed and line[::-1] not in output:
                    output.append(line[::-1])
                if len(output) == 5:
                    return output
        word_len -= 1
        word_reversed = word_reversed[:word_len]
    return (output)
