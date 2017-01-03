#include "keycalc.h"
#include <string>
#include <vector>

std::string modChk(
	const std::string& chkContent,
	const uint32_t seedKey[4],
	const uint32_t destKey[4],
	uint32_t fileCursor)
{
	std::vector<char> chk(chkContent.begin(), chkContent.end());

	// Add terminator section
	chk.push_back('S');
	chk.push_back('T');
	chk.push_back('U');
	chk.push_back('B');
	chk.push_back(0x00);
	chk.push_back(0x10);
	chk.push_back(0x00);
	chk.push_back(0x00);

	// Add things
	chk.resize((chk.size() + 0x1F) & ~0xF);

	uint32_t outputDwords[4];

	BlockTableEntry stubBlockEntry = { 0 };
	keycalc(
		seedKey,
		destKey,
		fileCursor,
		outputDwords,

		reinterpret_cast<const uint32_t*>(chk.data()),
		*(reinterpret_cast<const MPQHeader*>(chk.data())),
		chk.size(),
		0,
		0,
		chk.size() / 16,
		chk.size() / 16 - 32,
		stubBlockEntry
	);
	memcpy(chk.data() + chk.size() - 16, outputDwords, 16);
	return std::string(chk.begin(), chk.end());
}
