#include "mpqread.h"
#include "mpqwrite.h"
#include <fstream>
#include <cstring>
#include <pybind11/pybind11.h>

extern bool bEnableMpaq;

int applyFreezeMpqModification(
        const std::string& ifname,
        const std::string& ofname,
        bool enableMpaq
) {
    bEnableMpaq = enableMpaq;

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

PYBIND11_MODULE(freezeMpq, m) {
    m.def("applyFreezeMpqModification", &applyFreezeMpqModification, "Apply freeze");
}