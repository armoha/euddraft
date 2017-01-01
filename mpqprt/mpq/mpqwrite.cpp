//
// Created by phu54321 on 2016-12-14.
//

#include "mpqtypes.h"
#include "mpqwrite.h"
#include "mpqcrypt.h"
#include <vector>
#include <cstring>
#include <assert.h>
#include <utility>

using HashTable = std::vector<HashTableEntry>;
using BlockTable = std::vector<BlockTableEntry>;
using BlockDataTable = std::vector<std::string>;

extern bool bEnableMpaq;

// Hashers

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

std::string applyWaveCompression(const BlockTableEntry& blockEntry, const std::string& blockContent);

std::string createEncryptedMPQ(MpqReadPtr mr) {
    // Generate new hash table
    auto hashEntryCount = mr->getHashEntryCount();
    HashTable hashTable;
    for(int i = 0 ; i < hashEntryCount ; i++) {
        auto hashEntry = mr->getHashEntry(i);
        // remove (keyfile)
        if(hashEntry->hashA == 0x1A3398DE && hashEntry->hashB == 0xFEAAAFAA) {
            HashTableEntry deletedEntry;
            memset(&deletedEntry, 0, sizeof(HashTableEntry));
            deletedEntry.blockIndex = 0xFFFFFFFE;
            hashTable.push_back(deletedEntry);
        }
        else hashTable.push_back(*hashEntry);
    }

    // Get blocks & block data
    BlockTable blockTable;
    BlockDataTable blockDataTable;
    for(auto& hashEntry: hashTable) {
        if(hashEntry.blockIndex >= 0xFFFFFFFE) continue;
        auto blockEntry = mr->getBlockEntry(hashEntry.blockIndex);
		std::string blockData = mr->getBlockContent(blockEntry);
        auto newBlockEntry = *blockEntry;

		if(bEnableMpaq) blockData = applyWaveCompression(newBlockEntry, blockData);
		newBlockEntry.blockSize = blockData.size();

    	blockDataTable.push_back(blockData);
		newBlockEntry.fileFlag &= ~(BLOCK_ENCRYPTED | BLOCK_KEY_ADJUSTED);  // No longer encrypted
        blockTable.push_back(newBlockEntry);
        hashEntry.blockIndex = blockTable.size() - 1;
    }

    // Place scenario.chk block at the top
    int firstBlockHashEntry = -1;
    for(int i = 0 ; i < hashEntryCount ; i++) {
        auto& entry = hashTable[i];
        if(entry.blockIndex == 0) firstBlockHashEntry = i;
        // staredit\scenario.chk
        if(entry.hashA == 0xB701656E && entry.hashB == 0xFCFB1EED) {
            if(i != firstBlockHashEntry) {
                auto chkBlockIndex = entry.blockIndex;
                std::swap(blockTable[0], blockTable[chkBlockIndex]);
                std::swap(blockDataTable[0], blockDataTable[chkBlockIndex]);
                hashTable[i].blockIndex = 0;
                hashTable[firstBlockHashEntry].blockIndex = chkBlockIndex;
            }
            break;
        }
    }

    // Get file size & prepare buffer for it
    size_t newArchiveSize = sizeof(MPQHeader);
    uint32_t hashTableOffset, blockTableOffset;
    {
        for (size_t i = 0 ; i < blockDataTable.size() ; i++) {
            blockTable[i].blockOffset = newArchiveSize;
            newArchiveSize += blockDataTable[i].size();
        }

        hashTableOffset = newArchiveSize;
        newArchiveSize += hashTable.size() * 16;
        newArchiveSize = (newArchiveSize + 0xF) & ~0xF;  // round up by 16 : block table should starts from 0!!

        blockTableOffset = newArchiveSize;
        newArchiveSize += (blockDataTable.size() + 2) * 16;  // Extra 2 entries for block data table
    }

    // Adjust hash table
    for(auto& hashEntry : hashTable) {
        if(hashEntry.blockIndex <= 0xFFFFFFFE) hashEntry.blockIndex += (blockTableOffset >> 4);
    }

    // Prepare buffer
    std::vector<char> archiveBuffer(newArchiveSize);
    size_t cursor = 32;

    // Write mpq header
    MPQHeader header;
    header.magic = 0x1A51504D;
    header.headerSize = 32;
    header.mpqSize = newArchiveSize;
    header.mpqVersion = 0;
    header.sectorSizeShift = 3;
    header.unused0 = 0;
    header.hashTableOffset = hashTableOffset;
    header.blockTableOffset = 0;
    header.hashTableEntryCount = hashTable.size();
    header.blockTableEntryCount = newArchiveSize >> 4;
    memcpy(archiveBuffer.data(), &header, sizeof(MPQHeader));

    // Write file data
    for(const auto& blockData : blockDataTable) {
        memcpy(archiveBuffer.data() + cursor, blockData.data(), blockData.size());
        cursor += blockData.size();
    }

    // Write hash data
    const uint32_t hashTableKey = HashString("(hash table)", MPQ_HASH_FILE_KEY);
    for(const auto& hashEntry: hashTable) {
        memcpy(archiveBuffer.data() + cursor, &hashEntry, sizeof(hashEntry));
        cursor += sizeof(hashEntry);
    }
    EncryptData(
            archiveBuffer.data() + cursor - 16 * hashTable.size(),
            16 * hashTable.size(),
            hashTableKey);

    // Write block table data
    cursor = (cursor + 0xF) & ~0xF;
    const uint32_t blockTableKey = HashString("(block table)", MPQ_HASH_FILE_KEY);
    DecryptData(archiveBuffer.data(), cursor, blockTableKey);
    for(const auto& blockEntry : blockTable) {
        memcpy(archiveBuffer.data() + cursor, &blockEntry, sizeof(blockEntry));
        cursor += sizeof(blockEntry);
    }

    // Write decrypted data
    EncryptData(archiveBuffer.data(), cursor, blockTableKey);
    memcpy(archiveBuffer.data() + cursor, "freeze02 protect", 16);
    cursor += 16;
    DecryptData(archiveBuffer.data(), cursor, blockTableKey);

    // Output hash data here
    uint32_t outputDwords[4] = {0};
    {
        // Read map keys
        uint32_t keyDwords[9];
        auto keyFileEntry = mr->getBlockEntry("(keyfile)");
        if(keyFileEntry == nullptr) throw std::runtime_error("No keyfile");
        auto keyFile = mr->getBlockContent(keyFileEntry);
        if(keyFile.size() != 8 + 36) {   // 8 : sectorshifttable
            throw std::runtime_error("Key not sufficiently random : " + std::to_string(keyFile.size()));
        }
        memcpy(keyDwords, keyFile.data() + 8, 36);

        auto feedSample = [&](uint32_t sample) {
            keyDwords[0] = mix(keyDwords[0], sample);
            keyDwords[1] = mix(keyDwords[1], keyDwords[0]);
            keyDwords[2] = mix(keyDwords[2], keyDwords[1]);
            keyDwords[3] = mix(keyDwords[3], keyDwords[2]);
        };

        const uint32_t* dwData = reinterpret_cast<uint32_t*>(archiveBuffer.data());

        // 1. Feed MPQ header - 8 operationM
        for(int i = 0 ; i < 8 ; i++) {
            feedSample(reinterpret_cast<uint32_t*>(&header)[i]);
        }
        for(int i = 0 ; i < 8 ; i++) {
            feedSample(dwData[i]);
        }

        // 2. Feed HET - 1024 operation
        for(int i = 0 ; i < hashEntryCount ; i++) {
            feedSample(dwData[hashTableOffset / 4 + i * 4 + 3]);
        }

        // 3. Feed BET - maybe ~60 operation
        for(size_t i = 0 ; i < blockTable.size() ; i++) {
            feedSample(dwData[blockTableOffset / 4 + i * 4]);
        }

        // 4. Feed scenario.chk sectorOffsetTable
        auto& chkBlockEntry = blockTable[0];
        auto chkSectorNum = (chkBlockEntry.fileSize + 4095) / 4096;
        for(size_t i = 0 ; i < chkSectorNum + 1 ; i += 3) {
            feedSample(dwData[8 + i]);
        }

        // 5. Feed entire mpq file
        const int SAMPLEN = 2048;
        int mpqDwordN = header.mpqSize / 4 - 4;
        uint32_t fileCursor = keyDwords[8];
        for(int i = 0 ; i < 4 ; i++) {
            for(uint32_t j = 0 ; j < SAMPLEN / 4 ; j++) {
                keyDwords[i] = keyDwords[i] * 3 + dwData[fileCursor % mpqDwordN];
                fileCursor = mix(fileCursor, j);
            }
        }

        // 6. Final feedback
        for(int i = 0 ; i < 64 ; i++) {
            keyDwords[0] = mix(keyDwords[0], keyDwords[3]);
            keyDwords[1] = mix(keyDwords[1], keyDwords[0]);
            keyDwords[2] = mix(keyDwords[2], keyDwords[1]);
        }

        // 7. Great! calculate outputDwords
        outputDwords[0] = unmix_ch(keyDwords[4], keyDwords[0]);
        outputDwords[1] = unmix_ch(keyDwords[5], keyDwords[1]);
        outputDwords[2] = unmix_ch(keyDwords[6], keyDwords[2]);
        outputDwords[3] = unmix_ch(keyDwords[7], keyDwords[3]);
    }
    memcpy(archiveBuffer.data() + cursor, outputDwords, 16);
    cursor += 16;
    EncryptData(archiveBuffer.data(), cursor, blockTableKey);

    return std::string(archiveBuffer.begin(), archiveBuffer.end());
}
