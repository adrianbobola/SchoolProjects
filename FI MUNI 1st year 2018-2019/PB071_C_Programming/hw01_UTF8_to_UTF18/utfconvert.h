#ifndef UTFCONVERT_H
#define UTFCONVERT_H

#include <stdbool.h>

/**
 * Transforms a hexadecimal number representing
 * a UTF-8 encoded character into its Unicode equivalent
 *
 * @param[in] utf8code  UTF-8 code
 * @return Unicode value of the UTF-8 encoded character
 */

unsigned int utf8ToUni(unsigned int input);

/**
 * Encodes a unicode value using UTF-16 coding
 *
 * @param[in] unicode  Unicode value to encode
 * @param[in, out] utf16code, changed variable lower and upperByte
 * @return None
 */

void uniToUtf16(unsigned int unicode, unsigned int *lowerByte, unsigned int *upperByte);

/**
 * Check valid UTF-8 input and then remove UTF-8 headers
 *
 * @param[in] unicode  Unicode value
 * @param[in, out] utf8 code in, utf8 code without header out
 * @return utf8 code to be returned without header or
 * return -1 if input utf8 doesn`t have a right header
 */

int chceckValidUniRemoveHeaders(unsigned int input);

/**
 * Check Unicode code that is right
 *
 * @param[in] unicode  Unicode
 * @param[in, out] unicode code in
 * @return True for valid Unicode, return False for invalid Unicode
 */

bool validUni(unsigned int unicode);

#endif
