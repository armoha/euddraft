//
// Created by phu54321 on 2016-12-14.
//

#ifndef MPQ_MPQWRITE_H
#define MPQ_MPQWRITE_H

#include <cstddef>
#include <cstdint>
#include <string>
#include "mpqread.h"

std::string createEncryptedMPQ(MpqReadPtr mr);

// SC:R hard limit on the inflated block table entry count. freeze writes
// header.blockTableEntryCount as "real block table position / 16 + block
// count + 2" so the in-game keycalc buffer (blockEntryCount * 16 bytes)
// spans the whole archive, including the compressed scenario.chk that sits
// before the real block table. A count over 2^18 (262144 * 16 B = 4 MiB)
// makes SC:R refuse the map with "Scenario Damaged".
const uint32_t kMaxBlockTableEntryCount = 262144u;

// Compute freeze's inflated block table entry count and verify it stays
// under the SC:R limit. blockTableOffset must already be 16-byte aligned.
// Throws std::runtime_error when the count would exceed the limit.
uint32_t freezeBlockTableEntryCount(size_t blockTableOffset, size_t blockDataCount);

#endif //MPQ_MPQWRITE_H
