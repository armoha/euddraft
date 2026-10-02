#include "../doctest.h"

#include <cstdint>
#include <stdexcept>

#include "../mpqwrite.h"

TEST_CASE("freezeBlockTableEntryCount computes the inflated count") {
  // count = blockTableOffset/16 + blockDataCount + 2 (2 extra BET entries).
  CHECK(freezeBlockTableEntryCount(0, 0) == 2u);
  CHECK(freezeBlockTableEntryCount(16, 0) == 3u);
  CHECK(freezeBlockTableEntryCount(0, 3) == 5u);
  CHECK(freezeBlockTableEntryCount(16 * 100, 3) == 105u);
  // Offset must be 16-byte aligned already; floor division matches >> 4.
  CHECK(freezeBlockTableEntryCount(16 * 100 + 8, 3) == 105u);
}

TEST_CASE("freezeBlockTableEntryCount enforces the SC:R 4 MiB limit") {
  // 262144 entries is the last acceptable value ("Scenario Damaged" starts
  // at 262145).
  CHECK(freezeBlockTableEntryCount(16 * 262141u, 1u) == 262144u);
  CHECK_THROWS_AS(freezeBlockTableEntryCount(16 * 262142u, 1u),
                  std::runtime_error);
  // A large block count pushes the inflated count over the limit too.
  CHECK_THROWS_AS(freezeBlockTableEntryCount(0, 262143u),
                  std::runtime_error);
}