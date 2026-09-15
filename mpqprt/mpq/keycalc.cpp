#include "mpqtypes.h"
#include <cstddef>
#include <cstdint>
#include <stdexcept>
#include <string.h>

// NOTE: this file must stay bit-identical with
//   freeze/crypt.py (T/mix) and freeze/keycalc.py (feed order).
// All u32 arithmetic intentionally wraps mod 2**32; do not promote to
// wider/64-bit types (see LP64 hash-table fix in CHANGELOG).

uint32_t T(uint32_t x) {
	auto xsq = x * x;
	return x * (xsq * (xsq * xsq + 1) + 1) + 0x8ada4053;
}


uint32_t mix(uint32_t seed, uint32_t ch) {
	return T(seed) + ch + 0x10f874f3;
}

uint32_t unmix_ch(uint32_t seed, uint32_t seed0) {
	// seed = T(seed0) + ch + C
	// ch = seed - T(seed0) - C
	return seed - T(seed0) - 0x10f874f3;
}

void keycalc(
	const uint32_t seedKey[4],
	const uint32_t destKey[4],
	uint32_t fileCursor,
	uint32_t outputKeys[4],

	// Auxiliary data
	const uint32_t* dwData,
	const MPQHeader& header,
	uint32_t hashEntryCount,
	uint32_t hashTableOffset,
	uint32_t blockEntryCount,
	uint32_t initialBlockIndex,
	const BlockTableEntry& chkBlockEntry,
	size_t sectorSize
) {
	if (dwData == nullptr || seedKey == nullptr || destKey == nullptr ||
	    outputKeys == nullptr) {
		throw std::invalid_argument("keycalc: null pointer argument");
	}
	if (blockEntryCount < 2) {
		throw std::invalid_argument("keycalc: blockEntryCount too small");
	}
	if (sectorSize == 0) {
		throw std::invalid_argument("keycalc: sectorSize must be non-zero");
	}
	uint32_t keyDwords[4];
	keyDwords[0] = seedKey[0];
	keyDwords[1] = seedKey[1];
	keyDwords[2] = seedKey[2];
	keyDwords[3] = seedKey[3];

	auto feedSample = [&](uint32_t sample) {
		keyDwords[0] = mix(keyDwords[0], sample);
		keyDwords[1] = mix(keyDwords[1], keyDwords[0]);
		keyDwords[2] = mix(keyDwords[2], keyDwords[1]);
		keyDwords[3] = mix(keyDwords[3], keyDwords[2]);
	};

	// 1. Feed MPQ header - 8 operationM
	for (size_t i = 0; i < 8; i++)
		feedSample(reinterpret_cast<const uint32_t*>(&header)[i]);

	for (size_t i = 0; i < 8; i++)
		feedSample(dwData[i]);

	// 2. Feed HET - 1024 operation
	for (size_t i = 0; i < hashEntryCount; i++)
		feedSample(dwData[hashTableOffset / 4 + i * 4 + 3]);

	// 3. Feed BET - maybe ~60 operation
	for (size_t i = 0; i < blockEntryCount - initialBlockIndex - 2; i++)
		feedSample(dwData[initialBlockIndex * 4 + i * 4]);

	// 4. Feed scenario.chk sectorOffsetTable
	auto chkSectorNum = (chkBlockEntry.fileSize + sectorSize - 1) / sectorSize;
	for (size_t i = 0; i < chkSectorNum + 1; i += 3)
		feedSample(dwData[8 + i]);

	// 5. Feed entire mpq file
	const int SAMPLEN = 2048;
	// int64 to keep the valid-input range well-defined;
	// guarded >= 2 above so this stays positive.
	const int64_t mpqDwordN =
	    static_cast<int64_t>(blockEntryCount) * 4 - 4;
	for (size_t i = 0; i < 4; i++) {
		for (uint32_t j = 0; j < SAMPLEN / 4; j++) {
			const size_t sampleIdx =
			    static_cast<size_t>(fileCursor % mpqDwordN);
			keyDwords[i] = keyDwords[i] * 3 + dwData[sampleIdx];
			fileCursor = mix(fileCursor, j);
		}
	}

	// 6. Final feedback
	for (size_t i = 0; i < 64; i++) {
		keyDwords[0] = mix(keyDwords[0], keyDwords[3]);
		keyDwords[1] = mix(keyDwords[1], keyDwords[0]);
		keyDwords[2] = mix(keyDwords[2], keyDwords[1]);
	}

	for (int i = 0; i < 4; i++) {
		outputKeys[i] = unmix_ch(destKey[i], keyDwords[i]);
	}
}
