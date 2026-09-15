#pragma once

#include <cstddef>
#include <cstdint>

#include "mpqtypes.h"

// Bit-exact counterpart of freeze/keycalc.py + freeze/crypt.py.
// All arithmetic is mod 2**32; dwData is the whole archive viewed as
// little-endian u32 words. Throws std::invalid_argument on null/implausible
// inputs instead of invoking undefined behavior.
void keycalc(
	const uint32_t seedKey[4],
	const uint32_t destKey[4],
	uint32_t fileCursor,
	uint32_t outputKeys[4],

	// Auxilarry data
	const uint32_t* dwData,
	const MPQHeader& header,
	uint32_t hashEntryCount,
	uint32_t hashTableOffset,
	uint32_t blockEntryCount,
	uint32_t initialBlockIndex,
	const BlockTableEntry& chkBlockEntry,
	size_t sectorSize
);
