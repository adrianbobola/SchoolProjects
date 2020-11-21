---
title: "HW02 ASCII Art"
layout: "homework"
list-of-files: ["asciiart.c"]
publish: now
deadline-early: 2019-03-23 24:00
deadline-final: 2019-03-26 24:00
authors:
  - Milan Fabian: milan.fabian@mail.muni.cz
editors:
  - xpiatka
  - xkurcik
  - xgorta
---

Doplnění zadání:

**2019-03-13 10:10**
: Definovanie výstupu pre prázdny vstup

## Predstavenie úlohy

Určite sa každý z vás už stretol s [ASCII Art](http://cs.wikipedia.org/wiki/ASCII_art),
vykresľovaním rôznej grafiky na terminál pomocou ASCII znakov.
V tejto úlohe si vyskúšate jednoduchý prevod textu a jeho vykreslenie na terminál.

## Zadanie

Vytvorte kompletný spustiteľný program, ktorý zo štandardného vstupu načíta text, prevedie ho na ASCII Art a vypíše ho na štandardný výstup.

V kostre úlohy nájdete súbor `asciifont.h` so zadefinovým fontom 8x8, ktorý použijete na vykresľovanie. Tento hlavičkový súbor nijako neupravujte, vaše riešenie bude skompilované s rovnakou verziou hlavičkového súboru ako je v kostre. Úlohu riešte v súbore `asciiart.c`.

## Formát fontu

Font je definovaný ako dvojrozmerné pole `char[128][8]` v hlavičkovom súbore `asciifont.h`.
Prvá súradnica označuje číslo znaku v ASCII (viď [článok](http://en.wikipedia.org/wiki/ASCII#ASCII_printable_characters) na Wikipédii), druhá súradnica označuje riadok. Stĺpec získate vymaskovaním. Tam kde získate vymaskovaním 1 bude čierny bod, kde získate 0 nebude nič. Názorná ukážka pre znak A (ASCII hodnota 65) je na obrázku:

![A](ascii_art_a.png)

## Požiadavky

  * Program sa bude spúštať `./asciiart length`, teda s jedným parametrom.
  * Parameter `length` bude celé číslo, ktoré označuje maximálny počet znakov, ktoré sa majú vypísať do jedného riadku (= maximálna šírka terminálu). Pozor, ide o reálny počet vypísaných znakov na štandardný výstup, čo je počet zadaných znakov od používateľa x 8.
  * Ak používateľ zadá iný počet parametrov, ako je požadované, alebo zadaný parameter nebude celé kladné číslo väčšie __alebo rovné__ ako 8, program o tom vypíše hlášku na štandardný **chybový** výstup a skončí s **nenulovým** návratovým kódom.
  * Používateľ následne zadá na štandardný vstup jeden riadok textu, ukončený znakom nového riadku. Povolené sú len hodnoty znakov od 0 do 127 (ktoré sú definované v hlavičkovom súbore `asciifont.h`). V prípade, kedy používateľ zadá znak mimo zadaného rozsahu ASCII, vypíšete hlášku na štandardný **chybový** výstup a skončí s **nenulovým** návratovým kódom. Maximálny počet znakov na vstupe je 100, vyšší počet sa testovať nebude.
  * Program na štandardný výstup vypíše text prevedený do ASCII Art. Čierny bod fontu vykreslíte ako znak `#`, biely bod ako medzeru.
  * Maximálny počet znakov (`#` alebo medzera) na jeden riadok sa bude rovnať parametru length zadanému pri spustení. Zároveň je potrebné na jeden riadok vypísať čo najväčší počet znakov v ASCII art. Každý znak musí byť len na jednom riadku, nesmie byť rozdelený na dva.
  * Medzi znakmi nepridávajte žiadne horizontálne ani vertikálne medzery. Použitý font je pripravený tak, aby medzery neboli potrebné.
  * Ak vychádza na koniec riadku znak medzery (z používateľského vstupu), je potrebné vypísať biele miesta presne podla fontu. Automatická kontrola pri odovzdaní kontroluje aj medzery.
  * Po vypísaní celého textu program korektne skončí.
  * *V prípade prázdneho vstupu program nevypisuje nič a korektne skončí.*{: class="add"}

## Príklad práce s programom

```
login@aisa$ ./asciiart 80
FI MUNI rulezz!

 ######   ####           ##   ## ##  ##  ##   ##  ####
 ##        ##            ### ### ##  ##  ###  ##   ##
 ##        ##            ####### ##  ##  #### ##   ##            #####   ##  ##
 #####     ##            ## # ## ##  ##  ## ####   ##            ##  ##  ##  ##
 ##        ##            ##   ## ##  ##  ##  ###   ##            ##  ##  ##  ##
 ##        ##            ##   ## ##  ##  ##   ##   ##            ##      ##  ##
 ##       ####           ##   ##  #####  ##   ##  ####           ##       #####

   ##                              ##
   ##                             ####
   ##     ####    ####    ####    ####
   ##    ##  ##     ##      ##     ##
   ##    ######    ##      ##      ##
   ##    ##       ##      ##
   ##     ####    ####    ####     ##
```

## Poznámky

  * Program prekladajte nasledovne: `gcc -std=c99 -Wall -Wextra -Werror -pedantic -o asciiart asciiart.c`.
  * Na výpis na **štandardný chybový výstup** použite volanie `fprintf(stderr, FORMAT, PARAMS...)`, pričom táto funkcia sa správa
    podobne ako `printf(FORMAT, PARAMS...)`.
  * Počet parametrov programu dostane funkcia `main` v argumente `argc`, ich hodnoty v poli `argv`.
    Prvý parameter je vždy názov spúšťaného programu.
  * Vzorové riešenie si môžete vyskúšať na Aise: `/home/kontr/pb071/hw02/asciiart`. Využite možnosť porovnať výsledok vašeho riešenia s výsledkom vzorového riešenia pomocou príkazu `diff`.
