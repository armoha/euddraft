//
// Created by phu54321 on 2016-12-12.
//

#include <stdexcept>
#include "mpqread.h"
#include "mpqtypes.h"
#include "mpqcrypt.h"
#include <vector>
#include <fstream>

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
    const BlockTableEntry* getBlockEntry(const std::string& fname) const;
    const BlockTableEntry* getBlockEntry(int index) const;
    std::string getDecryptedBlockContent(const BlockTableEntry *blockEntry) const;

private:
    MPQHeader header;
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


const BlockTableEntry* MpqReadImpl::getBlockEntry(const std::string& _fname) const {
    auto fname = _fname.c_str();
    auto hashA = HashString(fname, MPQ_HASH_NAME_A);
    auto hashB = HashString(fname, MPQ_HASH_NAME_B);
    auto hashKey = HashString(fname, MPQ_HASH_TABLE_OFFSET);
    auto initialFindIndex = hashKey & (hashTable.size() - 1);
    auto index = initialFindIndex;
    do {
        const auto& hashTableEntry = hashTable[index];
        if(hashTableEntry.blockIndex == 0xFFFFFFFF) return nullptr;
        else if(hashTableEntry.hashA == hashA && hashTableEntry.hashB == hashB) {
            return &blockTable[hashTableEntry.blockIndex];
        }
        index = (index + 1) & (hashTable.size() - 1);
    }while(index != initialFindIndex);
	return nullptr;
}

const BlockTableEntry* MpqReadImpl::getBlockEntry(int index) const {
    return &blockTable[index];
}

std::string MpqReadImpl::getDecryptedBlockContent(const BlockTableEntry *blockEntry) const {
    is.seekg(blockEntry->blockOffset, std::ios_base::beg);

    if(!(blockEntry->fileFlag & BLOCK_ENCRYPTED)) {
        // Plain file. just read-as
        std::vector<char> buf(blockEntry->blockSize);
        is.read(buf.data(), blockEntry->blockSize);
        return std::string(buf.begin(), buf.end());
    }
    else {
        // Encrypted file. Should get file key.
        if(!(blockEntry->fileFlag & (BLOCK_COMPRESSED | BLOCK_IMPLODED))) {
            throw std::runtime_error("Cannot get key of non-compressed encrypted block");
        }
        // Get encrypted SectorOffsetTable
        const size_t sectorSize = 512u << header.sectorSizeShift;
        size_t sectorNum = (blockEntry->fileSize + sectorSize - 1) / sectorSize;
        std::vector<uint32_t> encryptedOffsetTable(sectorNum + 1);
        is.read(reinterpret_cast<char*>(encryptedOffsetTable.data()), 4 * (sectorNum + 1));

        // Get decryption key
        const auto fileKey = GetFileDecryptKey(encryptedOffsetTable.data(), blockEntry->fileSize, blockEntry->blockSize, sectorSize);
        if(fileKey == 0xFFFFFFFF) throw std::runtime_error("Key-extraction from encrypted block failed!");

        // Read entire block
        is.seekg(blockEntry->blockOffset, std::ios_base::beg);
        std::vector<char> buf(blockEntry->blockSize);
        is.read(buf.data(), blockEntry->blockSize);

        // Decrypt sectorOffsetTable
        DecryptData(buf.data(), 4 * (sectorNum + 1), fileKey - 1);
        uint32_t* sectorOffsetTable = reinterpret_cast<uint32_t*>(buf.data());

        // Decrypt file data
        for(size_t sectorIndex = 0 ; sectorIndex < sectorNum ; sectorIndex++) {
            size_t thisSectorOffset = sectorOffsetTable[sectorIndex];
            size_t thisSectorSize = sectorOffsetTable[sectorIndex + 1] - sectorOffsetTable[sectorIndex];
            DecryptData(buf.data() + thisSectorOffset, thisSectorSize, fileKey + sectorIndex);
        }

        // Return block data
        return std::string(buf.begin(), buf.end());
    }
}

/////////////////////////////

MpqRead::MpqRead(const std::string &mpqName) : pimpl(new MpqReadImpl(mpqName)) {}
MpqRead::~MpqRead() { delete pimpl; }
int MpqRead::getFileCount() const { return pimpl->getFileCount(); }

int MpqRead::getHashEntryCount() const { return pimpl->getHashEntryCount(); }
int MpqRead::getBlockEntryCount() const { return pimpl->getBlockEntryCount(); }
const HashTableEntry* MpqRead::getHashEntry(int index) const { return pimpl->getHashEntry(index); }
const BlockTableEntry* MpqRead::getBlockEntry(int index) const { return pimpl->getBlockEntry(index); }
const BlockTableEntry* MpqRead::getBlockEntry(const std::string &fname) const { return pimpl->getBlockEntry(fname); }

std::string MpqRead::getBlockContent(const BlockTableEntry *blockEntry) const {
    return pimpl->getDecryptedBlockContent(blockEntry);
}

/////////////////////////////

MpqReadPtr readMPQ(const std::string& mpqName) {
    return std::make_shared<MpqRead>(mpqName);
}
