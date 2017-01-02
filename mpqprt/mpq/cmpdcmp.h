#pragma once

#include <string>
#include "mpqtypes.h"
#include "comp/scomp.h"

std::string decompressBlock(size_t fileSize, const std::string& blockContent);
std::string compressToBlock(const std::string& fileContent, uint8_t cmpType1, uint8_t cmpType2);
