#include "../doctest.h"
#include <stdlib.h>
#include "../cmpdcmp.h"
#include "../doctest.h"

TEST_CASE("Compression & decompression")
{
	// Generate binary data
	const int s_size = 1024;
	char s[s_size] = {0};
	std::string data(s, s + s_size);

	std::string cmp = compressToBlock(data, MAFA_COMPRESS_STANDARD, MAFA_COMPRESS_STANDARD, 4096);
	std::string dcmp = decompressBlock(s_size, cmp, 4096);
	CHECK(dcmp == data);
}
