//
// Created by phu54321 on 2016-12-12.
//

#ifndef MPQ_MPQCRYPT_H
#define MPQ_MPQCRYPT_H

#include "mpqtypes.h"
#include <functional>

void EncryptData(void *lpbyBuffer, unsigned long dwLength, unsigned long dwKey);
void DecryptData(void *lpbyBuffer, unsigned long dwLength, unsigned long dwKey);

#define MPQ_HASH_TABLE_OFFSET	0
#define MPQ_HASH_NAME_A	1
#define MPQ_HASH_NAME_B	2
#define MPQ_HASH_FILE_KEY	3

unsigned long HashString(const char *lpszString, unsigned long dwHashType);
uint32_t GetFileDecryptKey(const void *buffer, uint32_t bufferSize, uint32_t expectedFirstDword,
                           const std::function<bool(const void *)> &validator);

#endif //MPQ_MPQCRYPT_H
