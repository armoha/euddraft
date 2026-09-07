#include "mpqread.h"
#include "mpqwrite.h"
#include "utf8path.h"
#include <fstream>
#include <cstring>
#include <pybind11/pybind11.h>

int applyFreezeMpqModification(
        const std::string& ifname,
        const std::string& ofname
) {

    try {
        auto hMPQ = readMPQ(ifname);
        std::string data = createEncryptedMPQ(hMPQ);
        hMPQ = nullptr;  // Close hMPQ, so close file handler
#ifdef _WIN32
        std::wstring wpath = utf8ToWide(ofname);
        std::ofstream os(wpath.c_str(), std::ios_base::binary);
#else
        std::ofstream os(ofname, std::ios_base::binary);
#endif
        os.write(data.data(), data.size());
        os.close();
    }
    catch (std::runtime_error e) {
        puts(e.what());
        return -2;
    }
    return 0;
}

PYBIND11_MODULE(freezeMpq, m, pybind11::mod_gil_not_used()) {
    m.def("applyFreezeMpqModification", &applyFreezeMpqModification, "Apply freeze");
}