#if (defined(_WIN32) || defined(WIN32)) && !defined(NO_WINDOWS_H)
// Do nothing
#else

#include <memory.h>

void CopyMemory(void* destination, const void* source, size_t length) {
    memcpy(destination, source, length);
}

void ZeroMemory(void* destination, size_t length) {
    memset(destination, 0, length);
}

#endif