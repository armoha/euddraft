#include "comp/scomp.h"
#include <string>
#include <vector>
#include "mpqtypes.h"


std::string decompressBlock(size_t fileSize, const std::string& blockContent) {
	const size_t sectorSize = 4096;
	const size_t sectorCount = (fileSize + sectorSize - 1) / sectorSize;

	// Read sector offset table
	std::vector<uint32_t> sectorOffsetTable(sectorCount + 1);
	memcpy(sectorOffsetTable.data(), blockContent.data(), sizeof(uint32_t) * (sectorCount + 1));

	// Output
	std::vector<char> output(fileSize);

	for (size_t i = 0; i < sectorCount; i++) {
		char* outp = output.data() + sectorSize * i;

		// Prepare compressed data
		const size_t thisSectorSize =
			(i < sectorCount - 1) ? sectorSize
			: (fileSize - 1) % sectorSize + 1;
		const size_t sectorOffset = sectorOffsetTable[i];
		const size_t compressedSize = sectorOffsetTable[i + 1] - sectorOffsetTable[i];

		// Decompress
		DWORD dcmpSize = thisSectorSize;
		std::vector<char> sectorData(thisSectorSize);
		if(!SCompDecompress(
			sectorData.data(), &dcmpSize,
			blockContent.data() + sectorOffset, compressedSize))
		{
			throw std::runtime_error("Cannot decompress data");
		}
		memcpy(outp, sectorData.data(), sectorData.size());
	}

	return std::string(output.begin(), output.end());
}




std::string compressToBlock(const std::string& fileContent, uint8_t cmpType1, uint8_t cmpType2) {
	const size_t fileSize = fileContent.size();
	const size_t sectorSize = 4096;
	const size_t sectorCount = (fileSize + sectorSize - 1) / sectorSize;

	uint8_t cmpType = cmpType1;

	// Output
	std::vector<char> output(fileSize + 4 * (sectorCount + 1));
	char* outp = output.data() + 4 * (sectorCount + 1);
	uint32_t* p_sot = reinterpret_cast<uint32_t*>(output.data());
	for (size_t i = 0; i < sectorCount; i++) {
		*(p_sot++) = outp - output.data();

		// Prepare compressed data
		const size_t thisSectorSize =
			(i < sectorCount - 1) ? sectorSize
			: (fileSize - 1) % sectorSize + 1;

		// Recompress
		DWORD cmpSize = thisSectorSize;
		if (!SCompCompress(
			outp, &cmpSize,
			fileContent.data() + sectorSize * i, thisSectorSize,
			cmpType, 0, 3))
		{
			throw std::runtime_error("Recompression failed");
		}

		outp += cmpSize;
		cmpType = cmpType2;
	}

	*p_sot = outp - output.data();
	return std::string(output.data(), outp);
}



#include "doctest.h"

TEST_CASE("Compression")
{
	
}