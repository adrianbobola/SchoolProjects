#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "asciifont.h"

#define MAX_bitsArray 100

bool validStr(const char *inputString) {
    if (inputString == NULL) {
        return true;
    }
    unsigned int i = 0;
    while (inputString[i] != '\0') {
        if ((int) inputString[i] < 0) {
            return false;
        }
        i += 1;
    }
    return true;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "No parameters given\n");
        return 1;
    }
    long inputNumber = strtol(argv[1], NULL, 10);

    if (inputNumber < 8) {
        fprintf(stderr, "Parameter is lower than 8\n");
        return 1;
    }

    unsigned int bitsArray[8] = {0};
    bitsArray[0] = 128;
    bitsArray[1] = 64;
    bitsArray[2] = 32;
    bitsArray[3] = 16;
    bitsArray[4] = 8;
    bitsArray[5] = 4;
    bitsArray[6] = 2;
    bitsArray[7] = 1;

    char inputString[MAX_bitsArray] = {0};
    unsigned int i = 0;
    unsigned int lenStr = 0;
    int ch;
    while ((ch = getchar()) != EOF && ch != '\n') {
        if (i < MAX_bitsArray) {
            inputString[i++] = (char) ch;
            lenStr += 1;
        }
    }
    inputString[i] = '\0';

    if (validStr(inputString) == false) {
        fprintf(stderr, "Input contains non-valid ASCII character\n");
        return 1;
    }

    long charInRow = inputNumber / 8;
    unsigned int printedChar = 0;

    while (printedChar < lenStr) {
        for (int strCol = 0; strCol < 8; strCol++) {
            for (int strOneRow = 0; strOneRow < charInRow; strOneRow++) {
                if (printedChar + strOneRow >= lenStr) {
                    break;
                }

                for (int bitsNumber = 0; bitsNumber < 8; bitsNumber++) {
                    int ascii_value = (int) inputString[printedChar + strOneRow];

                    if ((FONT_DATA[ascii_value][strCol] & bitsArray[bitsNumber]) == bitsArray[bitsNumber]) {
                        printf("#");
                    } else {
                        printf(" ");
                    }
                }
            }
            printf("\n");
        }
        printedChar += charInRow;
    }
    return 0;
}
