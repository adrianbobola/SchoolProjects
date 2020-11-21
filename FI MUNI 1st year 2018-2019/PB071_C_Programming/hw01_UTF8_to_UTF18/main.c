#include <stdio.h>
#include "utfconvert.h"

int main(void) {
    int decadicNumber;
    if ((scanf("%d", &decadicNumber) != 1) || (decadicNumber < 0)) {
        printf("Invalid input!\n");
        return 1;
    }

    for (int i = 0; i < decadicNumber; i++) {
        unsigned int input = 0;

        if (scanf("%X", &input) != 1) {
            printf("Invalid input!\n");
            return 1;
        }

        int result = chceckValidUniRemoveHeaders(input);

        if (result == -1) {
            printf("Invalid input!\n");
            return 1;
        }

        input = result;
        unsigned int unicode = utf8ToUni(input);

        if (validUni(unicode) == false) {
            printf("Invalid input!\n");
            return 1;
        }

        unsigned int lowerByte = 0;
        unsigned int UpperByte = 0;
        uniToUtf16(unicode, &lowerByte, &UpperByte);

        if (unicode <= 0xFFFF) {
            printf("%03d%03d 0x%02X%02X\n", UpperByte, lowerByte, UpperByte, lowerByte);

        } else {
            unsigned int lowerLowerByte = 0;
            unsigned int lowerUpperByte = 0;
            unsigned int upperUpperByte = 0;
            unsigned int upperLowerByte = 0;

            lowerUpperByte = lowerByte & 0xFF;
            lowerByte = lowerByte >> 8;
            lowerLowerByte = lowerByte & 0xFF;

            upperUpperByte = UpperByte & 0xFF;
            UpperByte = UpperByte >> 8;
            upperLowerByte = UpperByte & 0xFF;

            printf("%03d%03d%03d%03d 0x%02X%02X%02X%02X\n", upperLowerByte, upperUpperByte, lowerLowerByte,
                   lowerUpperByte, upperLowerByte, upperUpperByte, lowerLowerByte, lowerUpperByte);
        }
    }
    return 0;
}
