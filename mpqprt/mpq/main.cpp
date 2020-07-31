#include "mpqread.h"
#include "mpqwrite.h"
#include <fstream>
#include <cstring>

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
    catch (std::runtime_error e) {
        puts(e.what());
		return -2;
    }
    return 0;
}
