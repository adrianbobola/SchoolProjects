"""Autor: Adrián Bobola, 485641

Prohlašuji, že celý zdrojový kód jsem zpracoval(a) zcela samostatně.
Jsem si vědom(a), že  nepravdivost tohoto tvrzení může být důvodem
k hodnocení F v předmětu IB111 a k disciplinárnímu řízení."""

import random


def arg_min(matrix):
    """
    Funkce pro zadanou matici (2D seznam) cisel vrati pozici (dvojici indexu
    (radek, sloupec)), na ktere se nachazi nejmensi cislo. Pro jednoduchost
    predpokladej, ze v matici je vzdy prave jedno minimalni (a tedy nejmensi)
    cislo.

    :param matrix: 2D seznam realnych cisel velikosti alespon 1x1
    :return: dvojice indexu, kde se nachazi nejmensi cislo

    >>> print(arg_min([[0]]))
    (0, 0)

    >>> print(arg_min([[10, 1], [8, 9]]))
    (0, 1)

    >>> print(arg_min([[0, 1 ,10], [8, 9, -10], [3, 1, 2]]))
    (1, 2)
    """
    min = matrix[0][0]
    if len(matrix) > 1:
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if matrix[i][j] < min:
                    min = matrix[i][j]
                    sur_i = i
                    sur_j = j
    else:
        sur_i = 0
        sur_j = 0
    return sur_i, sur_j

#print(arg_min([[0, 1 ,10], [8, 9, -10], [3, 1, 2]]))

def even_sum(n):
    """
    Funkce pro zadane n *rekurzivne* spocita soucet vsech sudych prirozenych
    cisel mensich nebo rovnych n.

    :param n: prirozene cislo
    :return: soucet vsech sudych prirozenych cisel mensich nebo rovnych n

    >>> print(even_sum(0))
    0

    >>> print(even_sum(5))
    6

    >>> print(even_sum(6))
    12
    """
    if n%2 != 0:
        a = []
        for i in range(1, n+1):
            if i%2 == 0:
                a.append(i)
                sum = sum + i
    else:
        even_sum(n)


def chceck_3times(my_dictionary):
    times = []
    stop = 0
    for i in range(1,7):
        times.append(my_dictionary.get(i))
    for time in times:
        if time == 3:
            return False
    return True


def three_strikes_law():
    my_dictionary = {}
    """
    Funkce simuluje hod kostkou tak dlouho, dokud nektere cislo nepadne
    trikrat. Nasledne vytiskne analyzu, kolikrat ktere cislo padlo. Funkce
    nic nevraci.

    Priklad vystupu:
    Value 1 was rolled 3 times.
    Value 2 was rolled 1 times.
    Value 3 was rolled 2 times.
    Value 4 was rolled 0 times.
    Value 5 was rolled 1 times.
    Value 6 was rolled 1 times.
    """
    number = random.randint(1, 6)
    my_dictionary[number] = 1

    while chceck_3times(my_dictionary) is True:
        number = random.randint(1, 6)
        if number not in my_dictionary:
            my_dictionary[number] = 1
        else:
            my_dictionary[number] += 1

    for i in range(1, 7):
        time = 0
        if my_dictionary.get(i) == None:
            time = 0
        else:
            time = my_dictionary.get(i)
        print("Value", i, "was rolled", time, "times")


#three_strikes_law()

def trending_hashtags(data, k):
    """
    Funkce pro zadana data napocita cetnosti hastagu a vypise k nejcastejsich
    hashtagu. Data je retezec tvaru:
    #hashtag1,#hashtag2,#hashtag3;...

    Data muze by i prazdny retezec.

    :param data: neprazdny retezec s daty (hashtagy)
    :param k: prorozene cislo vetsi rovno 1

    >>> trending_hashtags("#auto;#auto;#summer", 1)
    #auto

    >>> trending_hashtags("#auto;#auto;#summer", 3)
    #auto
    #summer

    >>> trending_hashtags("#nofilter,#bff,#party;#nofilter,#party;#nofilter", 2)
    #nofilter
    #party
    """
    my_dictionary = {}
    data = data.split(";")
    a = []
    for i in range(len(data)):
        if data[i] not in my_dictionary:
            my_dictionary[data[i]] = 1
        else:
            my_dictionary[data[i]] += 1

    sorted_dict = sorted(my_dictionary, key=lambda data: my_dictionary[data], reverse=True)[:k]

    for text in sorted_dict:
        a.append(text)
    print(a)

#trending_hashtags("#auto;#auto;#summer", 1)

class Student:
    def __init__(self, uco, name):
        self.uco = uco
        self.name = name

    def __str__(self):
        return "Student: {name} ({uco})".format(name=self.name, uco=self.uco)


class Course:
    def __init__(self, code, credit_value):
        self.code = code
        self.credits = credit_value
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def print_students(self):
        i = 1
        for s in self.students:
            print(str(i) + ".", str(s.uco), s.name, sep="\t")
            i += 1

    def __str__(self):
        return "Course: {code}".format(code=self.code)


def shall_pass(student, courses):
    """
    Funkce pro zadaného studenta overi (vrati True nebo False) zda ma zapsane
    predmety za alespon 20 kreditu.
    :param student: objekt typu Student
    :param courses: seznam objektu typu Course
    :return: True pokud student ma zapsane predmety za alespon 20 kr. jinak
             vrati False

    >>> test_can_pass()
    OK
    """
    sum_kredity = 0


    if sum_kredity >= 20:
        return True
    else:
        return False

def test_can_pass():
    """
    Funkce slouzi ciste k otestovani funkcionality funkce can_pass.
    """
    s1 = Student(1, "Hozna")  # 10 + 2 = 12 kr. - nesplnuje
    s2 = Student(2, "Pepa")  # 10 + 12 = 22 kr. - splnuje
    s3 = Student(3, "Karel")  # 30 kr. - splnuje
    s4 = Student(4, "Jarda")  # 2 kr. - nesplnuje
    s5 = Student(5, "Kvido")  # 0 kr. - nesplnuje

    c1 = Course('IB000', 10)
    c2 = Course('MB101', 12)
    c3 = Course('IB111', 30)
    c4 = Course('IA073', 2)

    c1.add_student(s1)
    c1.add_student(s2)

    c2.add_student(s2)

    c3.add_student(s3)

    c4.add_student(s4)
    c4.add_student(s1)

    courses = [c1, c2, c3, c4]

    assert not shall_pass(s1, courses), "Student {s} nemá dost kreditů".format(s=s1)
    assert shall_pass(s2, courses), "Student {s} má dost kreditů".format(s=s2)
    assert shall_pass(s3, courses), "Student {s} má dost kreditů".format(s=s3)
    assert not shall_pass(s4, courses), "Student {s} nemá dost kreditů".format(s=s4)
    assert not shall_pass(s5, courses), "Student {s} nemá dost kreditů".format(s=s4)

    print('OK')
