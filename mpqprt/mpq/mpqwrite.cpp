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

#include "cmpdcmp.h"
#include "keycalc.h"

using HashTable = std::vector<HashTableEntry>;
using BlockTable = std::vector<BlockTableEntry>;
using BlockDataTable = std::vector<std::string>;

bool bEnableMpaq = false;

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

		if (bEnableMpaq) {
			auto fdata = decompressBlock(newBlockEntry.fileSize, blockData);

			// If wave data -> try recompression
			if (memcmp(fdata.data(), "RIFF", 4) == 0 &&
				memcmp(fdata.data() + 8, "WAVE", 4) == 0) {
				auto cmpdata = compressToBlock(fdata,
					MAFA_COMPRESS_STANDARD | MAFA_COMPRESS_WAVECOMP_HUFFMAN,
					MAFA_COMPRESS_WAVE);
				if (cmpdata.size() < blockData.size()) blockData = cmpdata;
			}
		}
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
	auto initialBlockIndex = (blockTableOffset >> 4);
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
    memcpy(archiveBuffer.data() + cursor, "freeze03 protect", 16);
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

		const uint32_t* dwData = reinterpret_cast<uint32_t*>(archiveBuffer.data());

		uint32_t seedKey[4], destKey[4];
		memcpy(seedKey, keyDwords + 0, sizeof(uint32_t) * 4);
		memcpy(destKey, keyDwords + 4, sizeof(uint32_t) * 4);
		uint32_t fileCursor = keyDwords[8];

    	keycalc(
			seedKey,
			destKey,
			fileCursor,
			outputDwords,

			dwData,
			header,
			header.mpqSize,
			header.hashTableEntryCount,
			header.hashTableOffset,
			header.blockTableEntryCount,
			initialBlockIndex,
			blockTable[0]
		);
    }
    memcpy(archiveBuffer.data() + cursor, outputDwords, 16);
    cursor += 16;
    EncryptData(archiveBuffer.data(), cursor, blockTableKey);

    return std::string(archiveBuffer.begin(), archiveBuffer.end());
}
