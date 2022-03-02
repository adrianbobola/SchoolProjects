"""
Autor: Adrián Bobola, 485641

Prohlašuji, že zdrojový kód jsem zpracoval(a) samostatně, kromě částí, které jsou explicitně označeny ASISTENCE
a doprovozeny vysvětlujícím komentářem. Jsem si vědom(a), že v nepravdivost tohoto tvrzení může být důvodem k
hodnocení F v předmětu IB111 a k disciplinárnímu řízení.
"""


# Známé nedostatky: Žiadne
# Styl: Asi v poriadku.
class Character:
    def __init__(self, name, gender, born, died):
        self.name = name
        self.gender = gender
        self.born = born
        self.died = died
        self.partner = None
        self.childrens = []
        self.mother = None
        self.father = None
        self.house = None

    def add_children(self, children):
        self.childrens.append(children)
        if self.gender == "M":
            children.father = self
        else:
            children.mother = self

    def set_partner(self, partner):
        self.partner = partner

    def add_house(self, house):
        self.house = house


class House:
    def __init__(self, name):
        self.name = name
        self.person = []

    def add_person(self, person):
        self.person.append(person.name)


# Známé nedostatky: Funkcia read_data by mala byť schopná načítať dáta, aj keď sú v súbore rozhadzané oddiely "Characters", "Relationships", "Houses"
#                   Tento problém som veľmi neriešil, keďže v zadaní je uvedené: "Predpokladaj, že vstupný súbor je korektný".
#                   V prípade prehodenia kategórii sa jedná už o nekorektný vstupný súbor.
# Styl: Tento kód sa dal napísať aj krajšie, cez podmienku while a drobnými podprogrammi.
""" ASISTENCE : Nevedel som, ako urobiť "rozdeľovač", ktorý bude zapisovať data z určitých sekcii.
                S nápadom, že by sa to dalo urobiť cez veľký IF cyklus a počítadlom mi pomohla Hana Tokárová, UČO: 484176
"""


def read_data(filename="GoT.txt"):
    """
    Funkce nacte data ze vstupniho souboru, vytvori objekty, nastavi jejich atributy a prida je do slovniku.
    K rozdeleni jednotlivych udaju na radku se ti urcite bude hodit metoda split.
    :param filename: nazev nebo cesta k souboru
    :return: slovnik postav a slovnik objektu
    """
    characters = {}
    houses = {}
    helper = 0
    with open(filename, "r") as my_file:
        for line in my_file.readlines():
            line = line.strip()
            if line[0] != "#":
                if helper == 1:  # If Characters
                    line = line.split(",")
                    name = line[0]
                    gender = line[1]
                    born = int(line[2])
                    died = int(line[3])
                    characters[name] = Character(name, gender, born, died)

                elif helper == 2:  # If Relationships
                    line = line.split("->")
                    line[0] = line[0].split("+")
                    father_name = line[0][0]
                    mother_name = line[0][1]
                    characters[father_name].set_partner(characters[mother_name])
                    characters[mother_name].set_partner(characters[father_name])
                    line[1] = line[1].split(",")
                    for i in range(len(line[1])):
                        if (line[1][i] != ''):
                            characters[father_name].add_children(characters[line[1][i]])
                            characters[mother_name].add_children(characters[line[1][i]])

                elif helper == 3:  # If Houses
                    line = line.split(":")
                    house_name = line[0]
                    houses_people = line[1]
                    houses[house_name] = House(house_name)
                    houses_people = houses_people.split(",")
                    for i in range(len(houses_people)):
                        houses[house_name].add_person(characters[houses_people[i]])
                        characters[houses_people[i]].add_house(house_name)
            else:
                helper += 1

        return characters, houses


# Známé nedostatky: Žiadne
# Styl: Asi v poriadku.
def print_family_tree(character, level=0):
    """
    Funkce vypise rodokmen postavy - jeho manzelku ci manzela a potomky vcetne jejich rodu. Kazdou generaci potomku
    odsadi tolika tabulatory, kolikata je to generace.
    :param character: objekt zadane postavy
    """
    if character.partner is not None:
        print(("    " * level) + character.name + " " + character.house, "+",
              character.partner.name + " " + character.partner.house)
        if len(character.childrens) > 0:
            for children in character.childrens:
                print_family_tree(children, level + 1)
    else:
        print(("    " * level) + character.name + " " + character.house)


def sort_children(children):
    """
    Funkce seradi seznam potomku podle systemu primogenitury, tedy prvni je prvorozeny syn, dale po nejmladsim synovi
    nasleduje nejstarsi dcera a jako posledni je nejmladsi dcera.
    :param children: seznam objektu deti nejake postavy
    :return: serazeny seznam
    """
    male_list = []
    female_list = []

    for child in children:  # Roztridit na muze a zeny - prednost ma nejmladsi syn pred nejstarsi dcerou
        if child.gender == 'M':
            male_list.append(child)
        else:
            female_list.append(child)

    male_list = sorted(male_list, key=lambda x: x.born)
    female_list = sorted(female_list, key=lambda x: x.born)

    children = male_list
    children.extend(female_list)
    return children


# Známé nedostatky: Žiadne
# Styl: Asi v poriadku.
def find_successor(character):
    """
    Funkce projde deti zadane postavy, popripade deti jejich deti a dale, aby nasla naslednika trunu.
    Pokud zadana postava nema zijiciho potomka, nema naslednika.
    Funkce pred hledanim seradi seznam deti podle systemu primogenitury volanim funkce sort_children(children).
    :param character: objekt zadane postavy
    :return: jmeno naslednika, pokud existuje; jinak retezec "Character has no successor among his offsprings."
    """
    sorted_childrens = sort_children(character.childrens)
    if len(sorted_childrens) > 0:
        for child in sorted_childrens:
            if child.died == 0:
                return child.name

        for child in sorted_childrens:
            if child.died == 0:
                return child.name
            elif find_successor(child) != "Character has no successor among his offsprings.":
                return find_successor(child)
    return ("Character has no successor among his offsprings.")


# Známé nedostatky: Automatický test "test_find_eldest" hlási Failed. Nepodarilo sa mi nájsť chybu v mojom kóde.
# Styl: Funkcia by sa dala krajšie zapísať pomocou slovníka a použitím funkcie sort s parametrom key = age.
def find_eldest(house):
    """
    Najde nejstarsiho zijiciho clena zadaneho rodu.
    :param house: objekt zadaneho rodu
    :return: jmeno nejstarsiho zijiciho clena rodu, pokud takovy neexistuje, vrati se
    retezec "There is no living member of the house."
    """
    characters, houses = read_data()
    people_of_house = []
    age_of_people = []
    min_age = 2018
    if len(house.person) != 0:
        for people in house.person:
            if int(characters[people].died) == 0:
                people_of_house.append(people)
                age_of_people.append(int(characters[people].born))
                if int(characters[people].born) < min_age:
                    min_age = int(characters[people].born)
        for i in range(len(age_of_people)):
            if age_of_people[i] == min_age:
                return people_of_house[i]
        if len(age_of_people) == 0:
            return ("There is no living member of the house.")
    else:
        return ("There is no living member of the house.")


# Známé nedostatky:
# Styl:
def could_meet_most(characters):
    """
    Najde postavu, mezi jejimz rokem narozeni a rokem umrti bylo nazivu nejvice ostatnich postav.
    Doporucuju vytvorit si pomocnou funkci pro kontrolu, zda se dve postavy mohly potkat.
    :param characters: slovnik vsech postav
    :return: jmeno hledane postavy
    """


def game_of_thrones_info():
    characters, houses = read_data()

    print("Family tree of Rickard Stark:")
    print_family_tree(characters["Rickard"])
    print()

    print("The successor of Rickard, the Mad King, is: ", end="")
    print(find_successor(characters["Rickard"]))
    print("The successor of Robert Baratheon is: ", end="")
    print(find_successor(characters["Robert"]))

    print("The eldest living member of house Stark is: ", end="")
    print(find_eldest(houses["Stark"]))
    print("The eldest living member of house Tully is: ", end="")
    print(find_eldest(houses["Tully"]))

    print("The character who could meet the most other characters is: ", end="")
    print(could_meet_most(characters))

    print()
