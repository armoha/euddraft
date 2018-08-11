cmake_minimum_required(VERSION 3.6)
project(euddraft_freeze_project)

if (WIN32)
    # set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} -s")
    # set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -s")
endif()

set(CMAKE_CXX_STANDARD 11)
set(SOURCE_FILES
    mpq/cmpdcmp.cpp
    mpq/keycalc.cpp
    mpq/modchk.cpp
    mpq/mpqcrypt.cpp
    mpq/mpqread.cpp
    mpq/mpqwrite.cpp
    mpq/comp/huffman.cpp
    mpq/comp/scomp.cpp
    mpq/comp/serr.cpp
    mpq/comp/smem.cpp
    mpq/comp/wave.cpp
    mpq/comp/winfuncs.c
    mpq/comp/exp.c
    mpq/comp/imp.c
    mpq/comp/zlib/adler32.c
    mpq/comp/zlib/compress.c
    mpq/comp/zlib/crc32.c
    mpq/comp/zlib/deflate.c
    mpq/comp/zlib/gzclose.c
    mpq/comp/zlib/gzlib.c
    mpq/comp/zlib/gzread.c
    mpq/comp/zlib/gzwrite.c
    mpq/comp/zlib/infback.c
    mpq/comp/zlib/inffast.c
    mpq/comp/zlib/inflate.c
    mpq/comp/zlib/inftrees.c
    mpq/comp/zlib/trees.c
    mpq/comp/zlib/uncompr.c
    mpq/comp/zlib/zutil.c
)

add_executable(euddraft_freeze ${SOURCE_FILES} mpq/main.cpp)

add_subdirectory(pybind11)
pybind11_add_module(freeze_pyext ${SOURCE_FILES} mpq/pybindmain.cpp)

# Multi threaded DLL -> Multi threaded in msvc
foreach(flag_var
        CMAKE_CXX_FLAGS CMAKE_CXX_FLAGS_DEBUG CMAKE_CXX_FLAGS_RELEASE
        CMAKE_CXX_FLAGS_MINSIZEREL CMAKE_CXX_FLAGS_RELWITHDEBINFO)
    if(${flag_var} MATCHES "/MD")
        string(REGEX REPLACE "/MD" "/MT" ${flag_var} "${${flag_var}}")
    endif(${flag_var} MATCHES "/MD")
endforeach(flag_var)

if (CMAKE_BUILD_TYPE MATCHES "Release")
    message("release mode - static linked")
    if (WIN32)
        target_link_libraries(euddraft_freeze -static)
        add_custom_command(TARGET euddraft_freeze POST_BUILD
                COMMAND "${CMAKE_COMMAND}" -E copy "$<TARGET_FILE:euddraft_freeze>" "C:/gitclones/euddraft/mpq.exc"
                COMMENT "Copying to main project")
    endif()
endif()
