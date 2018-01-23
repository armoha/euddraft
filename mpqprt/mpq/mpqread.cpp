//
// Created by phu54321 on 2016-12-12.
//

#include <stdexcept>
#include "mpqread.h"
#include "mpqtypes.h"
#include "mpqcrypt.h"
#include "cmpdcmp.h"
#include <vector>
#include <set>
#include <sstream>
#include <fstream>


using std::min;


class MpqReadImpl;


class MpqReadImpl {
public:
    MpqReadImpl(const std::string& mpqName);
    ~MpqReadImpl();

    int getFileCount() const {
        return fileCount;
    }

    int getHashEntryCount() const;
    int getBlockEntryCount() const;

	const HashTableEntry* getHashEntry(int index) const;
	const HashTableEntry* getHashEntry(const std::string& fname) const;
    const BlockTableEntry* getBlockEntry(int index) const;
    std::string getDecryptedBlockContent(const HashTableEntry* hte, const BlockTableEntry *blockEntry) const;

private:
    MPQHeader header;
	mutable std::set<std::string> knownFileNames;
    std::vector<HashTableEntry> hashTable;
    std::vector<BlockTableEntry> blockTable;
    size_t fileCount;
    mutable std::ifstream is;
};

///////

template <typename T>
void readTable(std::istream& is, size_t tableOffset, size_t entryCount, const char* tableKeyString, std::vector<T>& output) {
    // Read data
    std::vector<char> tableData;
    size_t tableSize = entryCount * sizeof(T);
    tableData.resize(tableSize);
    is.seekg(tableOffset, std::ios_base::beg);
    is.read(tableData.data(), tableSize);

    // Decrypt data
    const auto hashTableKey = HashString(tableKeyString, MPQ_HASH_FILE_KEY);
    DecryptData(tableData.data(), tableSize, hashTableKey);

    for (size_t i = 0; i < tableSize >> 4; i++) {
        const auto &hashTableEntry = *(reinterpret_cast<T *>(tableData.data()) + i);
        output.push_back(hashTableEntry);
    }

}

MpqReadImpl::MpqReadImpl(const std::string &mpqName) {
    // Read header
    try {
        is.exceptions(std::ifstream::failbit|std::ifstream::badbit);

        is.open(mpqName, std::ios_base::in | std::ios_base::binary);
        is.read(reinterpret_cast<char*>(&header), sizeof(header));

        // Get hash table
        readTable(is, header.hashTableOffset, header.hashTableEntryCount, "(hash table)", hashTable);
        readTable(is, header.blockTableOffset, header.blockTableEntryCount, "(block table)", blockTable);

        fileCount = 0;
        for (auto &entry: blockTable) {
            if (entry.blockSize != 0) fileCount++;
        }

		// Read listfile
		knownFileNames.insert("(listfile)");
		auto listFileHashEntry = getHashEntry("(listfile)");
		if (listFileHashEntry) {
			auto listFileBlockEntry = getBlockEntry(listFileHashEntry->blockIndex);
			auto listFile = getDecryptedBlockContent(listFileHashEntry, listFileBlockEntry);
			if (listFileBlockEntry->fileFlag & BLOCK_COMPRESSED) {
				listFile = decompressBlock(listFileBlockEntry->fileSize, listFile);
			}
			const char* p = listFile.data();
			const char* pend = listFile.data() + listFile.size();
			const char* fnStart = p;
			while (true) {
				if (p == pend || *p == 0 || *p == '\r' || *p == '\n') {
					if (fnStart != p) {
						knownFileNames.insert(std::string(fnStart, p));
					}
					fnStart = p + 1;
				}
				if (p == pend) break;
				p++;
			}
		}
    } catch(std::ifstream::failure e) {
        throw std::runtime_error(std::string("Error reading file : ") + e.what());
    }
}

MpqReadImpl::~MpqReadImpl() {
    is.close();
}

int MpqReadImpl::getHashEntryCount() const {
    return hashTable.size();
}

int MpqReadImpl::getBlockEntryCount() const {
    return blockTable.size();
}

const HashTableEntry* MpqReadImpl::getHashEntry(int index) const {
	return &hashTable[index];
}

const HashTableEntry* MpqReadImpl::getHashEntry(const std::string& _fname) const {
	auto fname = _fname.c_str();
	auto hashA = HashString(fname, MPQ_HASH_NAME_A);
	auto hashB = HashString(fname, MPQ_HASH_NAME_B);
	auto hashKey = HashString(fname, MPQ_HASH_TABLE_OFFSET);
	auto initialFindIndex = hashKey & (hashTable.size() - 1);
	auto index = initialFindIndex;
	do {
		auto hashTableEntry = &hashTable[index];
		if (hashTableEntry->blockIndex == 0xFFFFFFFF) return nullptr;
		else if (hashTableEntry->hashA == hashA && hashTableEntry->hashB == hashB) {
			knownFileNames.insert(_fname);
			return hashTableEntry;
		}
		index = (index + 1) & (hashTable.size() - 1);
	} while (index != initialFindIndex);
	return nullptr;
}


const BlockTableEntry* MpqReadImpl::getBlockEntry(int index) const {
    return &blockTable[index];
}

std::string MpqReadImpl::getDecryptedBlockContent(const HashTableEntry* hashEntry, const BlockTableEntry *blockEntry) const {
    is.seekg(blockEntry->blockOffset, std::ios_base::beg);

    if(!(blockEntry->fileFlag & BLOCK_ENCRYPTED)) {
        // Plain file. just read-as
        std::vector<char> buf(blockEntry->blockSize);
        is.read(buf.data(), blockEntry->blockSize);
        return std::string(buf.begin(), buf.end());
    }
	else {
		// Encrypted file. Should get file key.
		uint32_t fileKey = 0xFFFFFFFF;
		const size_t sectorSize = 512u << header.sectorSizeShift;
		size_t sectorNum = (blockEntry->fileSize + sectorSize - 1) / sectorSize;
		std::vector<uint32_t> encryptedOffsetTable(sectorNum + 1);

		// Get encrypted SectorOffsetTable
		is.read(reinterpret_cast<char*>(encryptedOffsetTable.data()), 4 * (sectorNum + 1));

		for (const auto& s : knownFileNames) {
			if (HashString(s.c_str(), MPQ_HASH_NAME_A) == hashEntry->hashA &&
				HashString(s.c_str(), MPQ_HASH_NAME_B) == hashEntry->hashB) {
				fileKey = HashString(s.c_str(), MPQ_HASH_FILE_KEY);
				if (blockEntry->fileFlag & 0x00020000) {  // File key adjusted
					fileKey = (fileKey + blockEntry->blockOffset) ^ blockEntry->fileSize;
				}
				break;
			}
		}

		if (fileKey == 0xFFFFFFFF) {
			if (blockEntry->fileFlag & (BLOCK_COMPRESSED | BLOCK_IMPLODED)) {
				// Get decryption key
				fileKey = GetFileDecryptKey(encryptedOffsetTable.data(), blockEntry->fileSize, blockEntry->blockSize, sectorSize);
				if (fileKey == 0xFFFFFFFF) throw std::runtime_error("Key-extraction from encrypted block failed!");
			}
			else {
				printf("Cannot get key of non-compressed encrypted block\n");
				printf(" - HASHA %08X, HASHB %08X, BLOCK %08X\n", hashEntry->hashA, hashEntry->hashB, hashEntry->blockIndex);
				throw std::runtime_error("Cannot get key of non-compressed encrypted block");
			}
		}

        // Read entire block
        is.seekg(blockEntry->blockOffset, std::ios_base::beg);
        std::vector<char> buf(blockEntry->blockSize);
        is.read(buf.data(), blockEntry->blockSize);

		// Compressed data have sectorOffsetTable.
		if (blockEntry->fileFlag & (BLOCK_COMPRESSED)) {
			// Decrypt sectorOffsetTable
			DecryptData(buf.data(), 4 * (sectorNum + 1), fileKey - 1);
			uint32_t* sectorOffsetTable = reinterpret_cast<uint32_t*>(buf.data());

			// Decrypt file data
			for (size_t sectorIndex = 0; sectorIndex < sectorNum; sectorIndex++) {
				size_t thisSectorOffset = sectorOffsetTable[sectorIndex];
				size_t thisSectorSize = sectorOffsetTable[sectorIndex + 1] - sectorOffsetTable[sectorIndex];
				DecryptData(buf.data() + thisSectorOffset, thisSectorSize, fileKey + sectorIndex);
			}

			// Return block data
			return std::string(buf.begin(), buf.end());
		}

		// Non-compressed data don't
		else {
			// Decrypt file data
			for (size_t sectorIndex = 0; sectorIndex < sectorNum; sectorIndex++) {
				size_t thisSectorOffset = sectorSize * sectorIndex;
				size_t thisSectorSize = min(sectorSize, blockEntry->fileSize - thisSectorOffset);
				DecryptData(buf.data() + thisSectorOffset, thisSectorSize, fileKey + sectorIndex);
			}

			// Return block data
			return std::string(buf.begin(), buf.end());
		}
	}
}

/////////////////////////////

MpqRead::MpqRead(const std::string &mpqName) : pimpl(new MpqReadImpl(mpqName)) {}
MpqRead::~MpqRead() { delete pimpl; }
int MpqRead::getFileCount() const { return pimpl->getFileCount(); }

int MpqRead::getHashEntryCount() const { return pimpl->getHashEntryCount(); }
int MpqRead::getBlockEntryCount() const { return pimpl->getBlockEntryCount(); }
const HashTableEntry* MpqRead::getHashEntry(int index) const { return pimpl->getHashEntry(index); }
const HashTableEntry* MpqRead::getHashEntry(const std::string &fname) const { return pimpl->getHashEntry(fname); }
const BlockTableEntry* MpqRead::getBlockEntry(int index) const { return pimpl->getBlockEntry(index); }

std::string MpqRead::getBlockContent(const HashTableEntry *hashEntry) const {
	auto blockEntry = pimpl->getBlockEntry(hashEntry->blockIndex);
	return pimpl->getDecryptedBlockContent(hashEntry, blockEntry);
}

std::string MpqRead::getFileContent(const HashTableEntry *hashEntry) const {
	auto blockEntry = pimpl->getBlockEntry(hashEntry->blockIndex);
	std::string content = pimpl->getDecryptedBlockContent(hashEntry, blockEntry);
	if(blockEntry->fileFlag & BLOCK_COMPRESSED)
	{
		content = decompressBlock(blockEntry->fileSize, content);
	}
	return content;
}

/////////////////////////////

MpqReadPtr readMPQ(const std::string& mpqName) {
    return std::make_shared<MpqRead>(mpqName);
}
