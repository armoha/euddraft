//
// Created by phu54321 on 2016-12-12.
//

#include <cctype>
#include <cassert>
#include <cstring>
#include <vector>
#include "mpqcrypt.h"

unsigned long dwCryptTable[0x500];

// The encryption and hashing functions use a number table in their procedures. This table must be initialized before the functions are called the first time.
void InitializeCryptTable()
{
    static bool inited = false;
    if(inited) return;
    inited = true;

    unsigned long seed   = 0x00100001;
    unsigned long index1 = 0;
    unsigned long index2 = 0;
    int   i;

    for (index1 = 0; index1 < 0x100; index1++)
    {
        for (index2 = index1, i = 0; i < 5; i++, index2 += 0x100)
        {
            unsigned long temp1, temp2;

            seed  = (seed * 125 + 3) % 0x2AAAAB;
            temp1 = (seed & 0xFFFF) << 0x10;

            seed  = (seed * 125 + 3) % 0x2AAAAB;
            temp2 = (seed & 0xFFFF);

            dwCryptTable[index2] = (temp1 | temp2);
        }
    }
}

void EncryptData(void *lpbyBuffer, unsigned long dwLength, unsigned long dwKey)
{
    InitializeCryptTable();
    assert(lpbyBuffer);

    unsigned long *lpdwBuffer = (unsigned long *)lpbyBuffer;
    unsigned long seed = 0xEEEEEEEE;
    unsigned long ch;

    dwLength /= sizeof(unsigned long);

    while(dwLength-- > 0)
    {
        seed += dwCryptTable[0x400 + (dwKey & 0xFF)];
        ch = *lpdwBuffer ^ (dwKey + seed);

        dwKey = ((~dwKey << 0x15) + 0x11111111) | (dwKey >> 0x0B);
        seed = *lpdwBuffer + seed + (seed << 5) + 3;

        *lpdwBuffer++ = ch;
    }
}

void DecryptData(void *lpbyBuffer, unsigned long dwLength, unsigned long dwKey)
{
    InitializeCryptTable();
    assert(lpbyBuffer);

    unsigned long *lpdwBuffer = (unsigned long *)lpbyBuffer;
    unsigned long seed = 0xEEEEEEEEL;
    unsigned long ch;

    dwLength /= sizeof(unsigned long);

    while(dwLength-- > 0)
    {
        seed += dwCryptTable[0x400 + (dwKey & 0xFF)];
        ch = *lpdwBuffer ^ (dwKey + seed);

        dwKey = ((~dwKey << 0x15) + 0x11111111L) | (dwKey >> 0x0B);
        seed = ch + seed + (seed << 5) + 3;

        *lpdwBuffer++ = ch;
    }

}
// Different types of hashes to make with HashString

// Based on code from StormLib.
unsigned long HashString(const char *lpszString, unsigned long dwHashType)
{
    InitializeCryptTable();
    assert(lpszString);
    assert(dwHashType <= MPQ_HASH_FILE_KEY);

    if (dwHashType==MPQ_HASH_FILE_KEY)
        while (strchr(lpszString,'\\') != NULL) lpszString = strchr(lpszString,'\\') + 1;


    unsigned long  seed1 = 0x7FED7FEDL;
    unsigned long  seed2 = 0xEEEEEEEEL;
    int    ch;

    while (*lpszString != 0)
    {
        ch = toupper(*lpszString++);

        seed1 = dwCryptTable[(dwHashType * 0x100) + ch] ^ (seed1 + seed2);
        seed2 = ch + seed1 + seed2 + (seed2 << 5) + 3;
    }
    return seed1;
}



//////////////////////////////////////

uint32_t GetFileDecryptKey(const uint32_t* encryptedOffsetTable, uint32_t fileSize, uint32_t blockSize, uint32_t sectorSize) {
    const size_t sectorNum = (fileSize + (sectorSize - 1)) / sectorSize;
    const uint32_t offsetTableLength = 4 * (sectorNum + 1);
    std::vector<uint32_t> decryptedOffsetTable(sectorNum + 1);
    if(offsetTableLength > blockSize) return 0xFFFFFFFF; // Unsupported, mpq-protected map

    // We know that decryptedOffsetTable[0] should be offsetTableLength.
    // Exploit storm encryption algorithm with that knowledge.
    for(int dwKeyLobyte = 0 ; dwKeyLobyte < 256 ; dwKeyLobyte++) {
        // seed += dwCryptTable[0x400 + (dwKey & 0xFF)];
        // ch = *lpdwBuffer ^ (dwKey + seed);

        // range of dwKey & 0xFF  :  00 ~ FF - Can be brute-forced
        // dwKey = (ch ^ *lpdwBuffer) - seed0
        // Check if this equation holds.
        const uint32_t seed = 0xEEEEEEEE + dwCryptTable[0x400 + dwKeyLobyte];
        const uint32_t dwKey = (encryptedOffsetTable[0] ^ offsetTableLength) - seed;
        if((dwKey & 0xff) == dwKeyLobyte) {  // Viable candidate
            // Do full decryption and check if decrypted offset table is valid.
            memcpy(decryptedOffsetTable.data(), encryptedOffsetTable, offsetTableLength);
            DecryptData(decryptedOffsetTable.data(), offsetTableLength, dwKey);

            // Last table
			if (decryptedOffsetTable[0] != offsetTableLength) continue;
			if (decryptedOffsetTable[sectorNum] != blockSize) continue;
            for(size_t i = 0 ; i < sectorNum ; i++)
                if(decryptedOffsetTable[i] > decryptedOffsetTable[i + 1]) return 0xFFFFFFFF;

            // SectorOffsetKey is encrypted using (fileKey - 1), so key we've got is one less from file's original key
            return dwKey + 1;
        }
    }

    // Cannot find viable candidate.
    return 0xFFFFFFFF;
}
