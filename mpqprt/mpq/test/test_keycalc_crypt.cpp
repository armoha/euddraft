#include "../doctest.h"

#include <cstdint>
#include <cstring>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>

#include "../keycalc.h"
#include "../mpqcrypt.h"
#include "../mpqtypes.h"

extern uint32_t T(uint32_t x);
extern uint32_t mix(uint32_t seed, uint32_t ch);
extern uint32_t unmix_ch(uint32_t seed, uint32_t seed0);
extern void garbagifyHashTable(std::vector<HashTableEntry>& hashTable,
                               int maxBlockIndex, std::mt19937& gen);

TEST_CASE("T and mix known answers") {
  // T(0) = 0*(...) + 0x8ADA4053 by definition.
  CHECK(T(0u) == 0x8ADA4053u);
  // mix(0,0) = T(0) + 0 + 0x10F874F3 mod 2**32.
  CHECK(mix(0u, 0u) == 0x9BD2B546u);
  // Determinism.
  CHECK(T(0x12345678u) == T(0x12345678u));
  CHECK(mix(1u, 2u) == mix(1u, 2u));
}

TEST_CASE("mix/unmix roundtrip") {
  const uint32_t seeds[] = {0u, 1u, 0x12345678u, 0xFFFFFFFFu, 0x8ADA4053u};
  const uint32_t chs[] = {0u, 1u, 0x10F874F3u, 0xDEADBEEFu, 0xFFFFFFFFu};
  for (uint32_t s : seeds) {
    for (uint32_t c : chs) {
      CHECK(unmix_ch(mix(s, c), s) == c);
    }
  }
}

TEST_CASE("HashString basics") {
  // Empty string falls through to the initial seed.
  CHECK(HashString("", MPQ_HASH_TABLE_OFFSET) == 0x7FED7FEDu);
  // Names are case-insensitive.
  CHECK(HashString("(hash table)", MPQ_HASH_FILE_KEY) ==
        HashString("(HASH TABLE)", MPQ_HASH_FILE_KEY));
  CHECK(HashString("staredit\\scenario.chk", MPQ_HASH_NAME_A) ==
        HashString("STAREDIT\\SCENARIO.CHK", MPQ_HASH_NAME_A));
  // FILE_KEY hashes strip directory prefixes.
  CHECK(HashString("dir\\file.chk", MPQ_HASH_FILE_KEY) ==
        HashString("file.chk", MPQ_HASH_FILE_KEY));
}

TEST_CASE("Encrypt/Decrypt roundtrip") {
  std::vector<uint32_t> plain = {0x12345678u, 0u, 0xFFFFFFFFu, 0x9B82B546u,
                                 0x00000001u, 0x80000000u};
  const uint32_t keys[] = {0u, 1u, 0xEEEEEEEEu, 0xFFFFFFFFu};
  for (uint32_t key : keys) {
    std::vector<uint32_t> buf = plain;
    EncryptData(buf.data(), (uint32_t)(buf.size() * 4), key);
    // Ciphertext must differ from plaintext for non-trivial input.
    CHECK(buf != plain);
    DecryptData(buf.data(), (uint32_t)(buf.size() * 4), key);
    CHECK(buf == plain);
  }
}

TEST_CASE("GetFileDecryptKey recovers key") {
  // Build a plausible offset table and encrypt it, then recover.
  std::vector<uint32_t> table = {12u, 20u, 36u};
  const uint32_t key = 0x12345678u;
  std::vector<uint32_t> encrypted = table;
  EncryptData(encrypted.data(), (uint32_t)(encrypted.size() * 4), key);
  uint32_t recovered = GetFileDecryptKey(
      encrypted.data(), (uint32_t)(encrypted.size() * 4), table[0],
      [&](const void* decrypted) {
        return memcmp(decrypted, table.data(), table.size() * 4) == 0;
      });
  CHECK(recovered == key);
  // Garbage that matches nothing yields the not-found sentinel.
  std::vector<uint32_t> noise = {0xDEADBEEFu, 0xCAFEBABEu};
  CHECK(GetFileDecryptKey(noise.data(), (uint32_t)(noise.size() * 4),
                           0x12345678u,
                           [](const void*) { return false; }) == 0xFFFFFFFFu);
  CHECK(GetFileDecryptKey(nullptr, 0, 0, [](const void*) { return true; }) ==
        0xFFFFFFFFu);
}

TEST_CASE("keycalc determinism and guards") {
  MPQHeader header = {};
  header.magic = 0x1A51504D;
  header.headerSize = 32;
  header.sectorSizeShift = 3;
  header.hashTableOffset = 64;
  header.blockTableOffset = 0;
  header.hashTableEntryCount = 4;
  header.blockTableEntryCount = 8;

  std::vector<uint32_t> dw(64, 0);
  for (size_t i = 0; i < dw.size(); i++) dw[i] = (uint32_t)(i * 0x9E3779B1u);

  BlockTableEntry chkEntry = {};
  chkEntry.fileSize = 4096;

  const uint32_t seed[4] = {1u, 2u, 3u, 4u};
  const uint32_t dest[4] = {5u, 6u, 7u, 8u};
  uint32_t out1[4] = {};
  uint32_t out2[4] = {};
  keycalc(seed, dest, 0xABCDEF01u, out1, dw.data(), header, 4, 64, 8, 2,
          chkEntry, 4096);
  keycalc(seed, dest, 0xABCDEF01u, out2, dw.data(), header, 4, 64, 8, 2,
          chkEntry, 4096);
  CHECK(memcmp(out1, out2, sizeof(out1)) == 0);

  // Different seeds must (overwhelmingly likely) change the output.
  const uint32_t seedB[4] = {9u, 2u, 3u, 4u};
  uint32_t out3[4] = {};
  keycalc(seedB, dest, 0xABCDEF01u, out3, dw.data(), header, 4, 64, 8, 2,
          chkEntry, 4096);
  CHECK(memcmp(out1, out3, sizeof(out1)) != 0);

  CHECK_THROWS_AS(
      keycalc(nullptr, dest, 0, out1, dw.data(), header, 4, 64, 8, 2, chkEntry,
              4096),
      std::invalid_argument);
  CHECK_THROWS_AS(
      keycalc(seed, dest, 0, out1, nullptr, header, 4, 64, 8, 2, chkEntry,
              4096),
      std::invalid_argument);
  CHECK_THROWS_AS(
      keycalc(seed, dest, 0, out1, dw.data(), header, 4, 64, 1, 2, chkEntry,
              4096),
      std::invalid_argument);
  CHECK_THROWS_AS(
      keycalc(seed, dest, 0, out1, dw.data(), header, 4, 64, 8, 2, chkEntry,
              0),
      std::invalid_argument);
}

TEST_CASE("garbagify deterministic overload") {
  HashTableEntry live = {};
  live.hashA = 0x11111111u;
  live.hashB = 0x22222222u;
  live.blockIndex = 3;
  HashTableEntry dead = {};
  dead.hashA = 0xAAAAAAAAu;
  dead.hashB = 0xBBBBBBBBu;
  dead.blockIndex = 0xFFFFFFFEu;

  std::vector<HashTableEntry> t1 = {live, dead};
  std::vector<HashTableEntry> t2 = {live, dead};
  std::mt19937 g1(42), g2(42);
  garbagifyHashTable(t1, 64, g1);
  garbagifyHashTable(t2, 64, g2);
  CHECK(memcmp(t1.data(), t2.data(), t1.size() * sizeof(HashTableEntry)) == 0);

  // Live entry untouched; dead entry remapped into range with fresh hashes.
  CHECK(t1[0].hashA == live.hashA);
  CHECK(t1[0].hashB == live.hashB);
  CHECK(t1[0].blockIndex == live.blockIndex);
  CHECK(t1[1].blockIndex < 64u);
  CHECK(t1[1].hashA != live.hashA);
  CHECK(t1[1].hashA != live.hashB);

  std::vector<HashTableEntry> bad = {dead};
  std::mt19937 g3(1);
  CHECK_THROWS_AS(garbagifyHashTable(bad, 0, g3), std::invalid_argument);
}
