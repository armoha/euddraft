#include "mpqread.h"
#include "mpqwrite.h"
#include <fstream>

extern bool bEnableMpaq;

int main(int argc, char** argv) {
    // if(argc != 2 && argc != 3) return -1;

	std::string ifname = argv[1];
	std::string ofname = ifname;

	if (argc == 3) {
		if (strcmp(argv[2], "mpaq") == 0) bEnableMpaq = true;
		else return -1;  // Invalid argument
	}

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
