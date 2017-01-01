//
// Created by phu54321 on 2016-12-12.
//

#ifndef MPQ_MPQTYPES_H
#define MPQ_MPQTYPES_H

#include <cstdint>

#include <packon.h>

typedef struct {
	uint32_t magic; //0x1A51504D
	uint32_t headerSize; // >= 32
	uint32_t mpqSize; //Don't matter
	uint16_t mpqVersion; //0
	uint8_t sectorSizeShift; //3
	uint8_t unused0; //0

	uint32_t hashTableOffset;
	uint32_t blockTableOffset;
	uint32_t hashTableEntryCount;
	uint32_t blockTableEntryCount;
} MPQHeader;

typedef struct {
	uint32_t hashA;
	uint32_t hashB;
    uint16_t language;
    uint8_t platform;
    uint8_t unused0;
	uint32_t blockIndex;
}HashTableEntry;



const uint32_t BLOCK_KEY_ADJUSTED  = 0x00020000;
const uint32_t BLOCK_ENCRYPTED     = 0x00010000;
const uint32_t BLOCK_COMPRESSED    = 0x00000200;
const uint32_t BLOCK_IMPLODED      = 0x00000100;

typedef struct {
	uint32_t blockOffset;
	uint32_t blockSize;
	uint32_t fileSize;
	uint32_t fileFlag;
}BlockTableEntry;

#include <packoff.h>

static_assert(sizeof(MPQHeader) == 32, "header size mismatch");
static_assert(sizeof(HashTableEntry) == 16, "het size mismatch");
static_assert(sizeof(BlockTableEntry) == 16, "bet size mismatch");

#endif //MPQ_MPQTYPES_H
