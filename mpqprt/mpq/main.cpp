#include "mpqread.h"
#include "mpqwrite.h"
#include <cstdio>
#include <cstring>
#include <exception>
#include <fstream>

int main(int argc, char** argv) {
    if(argc != 2) return -1;

	std::string ifname = argv[1];
	std::string ofname = ifname;

	try {
		auto hMPQ = readMPQ(ifname);
		std::string data = createEncryptedMPQ(hMPQ);
		hMPQ = nullptr;  // Close hMPQ, so close file handler
		std::ofstream os(ofname, std::ios_base::binary);
		os.write(data.data(), data.size());
		os.close();
	}
    catch (const std::exception& e) {
        puts(e.what());
		return -2;
    }
    return 0;
}
