#include "comp/scomp.h"
#include <string>
#include <vector>
#include "mpqtypes.h"


std::string applyWaveCompression(const BlockTableEntry& blockEntry, const std::string& blockContent) {
	const size_t sectorSize = 4096;
	const size_t sectorCount = (blockEntry.fileSize + sectorSize - 1) / sectorSize;

	// Read sector offset table
	std::vector<uint32_t> sectorOffsetTable(sectorCount + 1);
	memcpy(sectorOffsetTable.data(), blockContent.data(), sizeof(uint32_t) * (sectorCount + 1));

	std::vector<std::string> sectorTable;
	for (size_t i = 0; i < sectorCount; i++) {
		// Prepare compressed data
		const size_t thisSectorSize =
			(i < sectorCount - 1) ? sectorSize
			: (blockEntry.fileSize - 1) % sectorSize + 1;
		const size_t sectorOffset = sectorOffsetTable[i];
		const size_t compressedSize = sectorOffsetTable[i + 1] - sectorOffsetTable[i];

		std::vector<char> sectorData(
			blockContent.data() + sectorOffsetTable[i],
			blockContent.data() + sectorOffsetTable[i + 1]
		);

		// Not compressed -> feed as-is
		if(compressedSize == thisSectorSize)
		{
			sectorTable.push_back(std::string(sectorData.begin(), sectorData.end()));
			continue;
		}

		// Not wav-compressed : feed as-is
		uint8_t compType = sectorData[0];
		if(!(compType & (MAFA_COMPRESS_WAVECOMP_MONO | MAFA_COMPRESS_WAVECOMP_STEREO)))
		{
			sectorTable.push_back(std::string(sectorData.begin(), sectorData.end()));
			continue;
		}

		// Decompress
		DWORD dcmpSize = thisSectorSize;
		sectorData.resize(thisSectorSize);
		if(!SCompDecompress(sectorData.data(), &dcmpSize, sectorData.data(), compressedSize))
		{
			throw std::runtime_error("Cannot decompress data");
		}

		// Recompress
		DWORD cmpSize = thisSectorSize;
		if(!SCompCompress(sectorData.data(), &cmpSize, sectorData.data(), thisSectorSize, compType, 0, 3))
		{
			throw std::runtime_error("Recompression failed");
		}

		if(cmpSize >= compressedSize)
		{
			sectorTable.push_back(std::string(
				blockContent.data() + sectorOffsetTable[i],
				blockContent.data() + sectorOffsetTable[i + 1]
			));
		}
		else {
			// Add to table
			sectorTable.push_back(std::string(
				sectorData.data(),
				sectorData.data() + cmpSize
			));
		}
	}

	// Reconfigure sectorOffsetTable
	size_t newSectorCursor = sizeof(uint32_t) * (sectorCount + 1);
	for(size_t i = 0 ; i < sectorCount ; i++)
	{
		sectorOffsetTable[i] = newSectorCursor;
		newSectorCursor += sectorTable[i].size();
	}
	sectorOffsetTable[sectorCount] = newSectorCursor;
	const auto newBlockSize = newSectorCursor;

	// Rebuild table
	std::string newBlockData(newBlockSize, 0);
	char* p = const_cast<char*>(newBlockData.data());
	memcpy(p, sectorOffsetTable.data(), 4 * (sectorCount + 1));
	p += sizeof(uint32_t) * (sectorCount + 1);
	for (size_t i = 0; i < sectorCount; i++)
	{
		memcpy(p, sectorTable[i].data(), sectorTable[i].size());
		p += sectorTable[i].size();
	}

	// Rewrite blockEntry
	return newBlockData;
}
