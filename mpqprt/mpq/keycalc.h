#pragma once

#include "mpqtypes.h"

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
	const BlockTableEntry& chkBlockEntry
);
