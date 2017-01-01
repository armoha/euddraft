// SComp.h - Header for main compression/decompression routines
// License information for this code is in license.txt

#ifndef S_COMP_INCLUDED
#define S_COMP_INCLUDED

#if (defined(_WIN32) || defined(WIN32)) && !defined(NO_WINDOWS_H)
#include <windows.h>
#else
#include "wintypes.h"
#endif

#ifdef __cplusplus
extern "C" {
#endif

#define MAFA_COMPRESS_WAVECOMP_STEREO  0x80 //Main compressor for standard wave compression
#define	MAFA_COMPRESS_WAVECOMP_MONO    0x40 //Main compressor for unused wave compression
#define MAFA_COMPRESS_WAVECOMP_HUFFMAN 0x01 //Secondary compressor for wave compression


extern const unsigned int UNSUPPORTED_COMPRESSION;
extern const unsigned int UNSUPPORTED_DECOMPRESSION;

BOOL WINAPI SCompCompress(LPVOID lpvDestinationMem, LPDWORD lpdwCompressedSize, LPVOID lpvSourceMem, DWORD dwDecompressedSize, DWORD dwCompressionType, DWORD dwCompressionSubType, DWORD dwCompressLevel);
BOOL WINAPI SCompDecompress(LPVOID lpvDestinationMem, LPDWORD lpdwDecompressedSize, LPVOID lpvSourceMem, DWORD dwCompressedSize);

void __fastcall Implode(LPVOID lpvDestinationMem, LPDWORD lpdwCompressedSize, LPVOID lpvSourceMem, DWORD dwDecompressedSize, LPDWORD lpdwCompressionSubType, DWORD dwCompressLevel);
void __fastcall CompressWaveMono(LPVOID lpvDestinationMem, LPDWORD lpdwCompressedSize, LPVOID lpvSourceMem, DWORD dwDecompressedSize, LPDWORD lpdwCompressionSubType, DWORD dwCompressLevel);
void __fastcall CompressWaveStereo(LPVOID lpvDestinationMem, LPDWORD lpdwCompressedSize, LPVOID lpvSourceMem, DWORD dwDecompressedSize, LPDWORD lpdwCompressionSubType, DWORD dwCompressLevel);
void __fastcall HuffmanCompress(LPVOID lpvDestinationMem, LPDWORD lpdwCompressedSize, LPVOID lpvSourceMem, DWORD dwDecompressedSize, LPDWORD lpdwCompressionSubType, DWORD dwCompressLevel);

void __fastcall DecompressWaveMono(LPVOID lpvDestinationMem, LPDWORD lpdwDecompressedSize, LPVOID lpvSourceMem, DWORD dwCompressedSize);
void __fastcall DecompressWaveStereo(LPVOID lpvDestinationMem, LPDWORD lpdwDecompressedSize, LPVOID lpvSourceMem, DWORD dwCompressedSize);
void __fastcall HuffmanDecompress(LPVOID lpvDestinationMem, LPDWORD lpdwDecompressedSize, LPVOID lpvSourceMem, DWORD dwCompressedSize);
void __fastcall Explode(LPVOID lpvDestinationMem, LPDWORD lpdwDecompressedSize, LPVOID lpvSourceMem, DWORD dwCompressedSize);

#ifdef __cplusplus
};  // extern "C"
#endif

#endif


