//
// Created by phu54321 on 2016-12-12.
//

#ifndef MPQ_MPQREAD_H
#define MPQ_MPQREAD_H

#include <memory>
#include <string>
#include "mpqtypes.h"

class MpqReadImpl;

class MpqRead {
public:
    MpqRead(const std::string& mpqName);
    ~MpqRead();

    int getFileCount() const;
    int getHashEntryCount() const;
    int getBlockEntryCount() const;
    const HashTableEntry* getHashEntry(int index) const;
    const BlockTableEntry* getBlockEntry(const std::string& fname) const;
    const BlockTableEntry* getBlockEntry(int index) const;
	std::string getBlockContent(const BlockTableEntry *blockEntry) const;
	std::string getFileContent(const BlockTableEntry *blockEntry) const;

private:
    MpqReadImpl* pimpl;
};

using MpqReadPtr = std::shared_ptr<MpqRead>;
MpqReadPtr readMPQ(const std::string& mpqName);

#endif //MPQ_MPQREAD_H
