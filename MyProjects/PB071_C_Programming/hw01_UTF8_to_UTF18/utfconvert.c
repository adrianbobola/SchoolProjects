#include "utfconvert.h"
#include <stdbool.h>

int chceckValidUniRemoveHeaders(unsigned int input) {
    if (input <= 0xFF) {
        if (input == (input & 0x7F)) {
            return (input & 0x7F);
        }
    } else if ((input > 0xFF) && (input <= 0xFFFF)) {
        if ((input & 0xE0C0) == (0xC080)) {
            return (input & 0x1F3F);
        }
    } else if ((input > 0xFFFF) && (input <= 0xFFFFFF)) {
        if ((input & 0xF0C0C0) == (0xE08080)) {
            return (input & 0xF3F3F);
        }
    } else if ((input > 0xFFFFFF) && (input <= 0xFFFFFFFF)) {
        if ((input & 0xF8C0C0C0) == (0xF0808080)) {
            return (input & 0x73F3F3F);
        }
    }
    return -1;
}

bool validUni(unsigned int unicode) {
    return ((unicode <= 0xD7FF) || ((unicode >= 0xE000) && (unicode <= 0x10FFFF)));
}

unsigned int utf8ToUni(unsigned int input) {
    unsigned int firstByte = 0;
    unsigned int secondByte = 0;
    unsigned int thirdByte = 0;
    unsigned int fourthByte = 0;

    firstByte = input & 0xFF;
    input = input >> 8;
    secondByte = input & 0xFF;
    input = input >> 8;
    thirdByte = input & 0xFF;
    input = input >> 8;
    fourthByte = input & 0xFF;

    secondByte = firstByte + (secondByte << 6);
    thirdByte = secondByte + (thirdByte << 12);
    fourthByte = thirdByte + (fourthByte << 18);

    unsigned int unicode = fourthByte;
    return unicode;
}

void uniToUtf16(unsigned int unicode, unsigned int *lowerByte, unsigned int *upperByte) {
    if (unicode > 0xFFFF) {
        unicode = unicode - 0x10000;
        unsigned int low = 0;
        unsigned int upper = 0;

        low = ((unicode & 0x3FF) + 0xDC00);
        unicode = unicode >> 10;
        upper = ((unicode & 0x3FF) + 0xD800);
        *lowerByte = low;
        *upperByte = upper;
        return;
    }

    unsigned int low = 0;
    unsigned int upper = 0;

    low = unicode & 0xFF;
    unicode = unicode >> 8;
    upper = unicode & 0xFF;
    *lowerByte = low;
    *upperByte = upper;
}
