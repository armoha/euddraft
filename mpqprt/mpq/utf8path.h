#ifndef MPQ_UTF8PATH_H
#define MPQ_UTF8PATH_H

#include <cstdio>
#include <string>

#ifdef _WIN32
#include <windows.h>

inline std::wstring utf8ToWide(const std::string& utf8) {
    if (utf8.empty()) return {};
    int len = MultiByteToWideChar(CP_UTF8, 0, utf8.c_str(), (int)utf8.size(), nullptr, 0);
    std::wstring wide(len, 0);
    MultiByteToWideChar(CP_UTF8, 0, utf8.c_str(), (int)utf8.size(), &wide[0], len);
    return wide;
}

inline FILE* fopenUtf8(const std::string& path, const char* mode) {
    std::wstring wpath = utf8ToWide(path);
    std::wstring wmode(mode, mode + strlen(mode));
    return _wfopen(wpath.c_str(), wmode.c_str());
}

#else

inline FILE* fopenUtf8(const std::string& path, const char* mode) {
    return std::fopen(path.c_str(), mode);
}

#endif

#endif // MPQ_UTF8PATH_H
