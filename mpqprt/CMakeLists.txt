cmake_minimum_required(VERSION 3.6)
project(euddraft_freeze_project)

if (WIN32)
    if(MSVC)
        set(CMAKE_C_FLAGS_DEBUG_INIT "/D_DEBUG /MTd /Zi /Ob0 /Od /RTC1")
        set(CMAKE_C_FLAGS_MINSIZEREL_INIT     "/MT /O1 /Ob1 /D NDEBUG")
        set(CMAKE_C_FLAGS_RELEASE_INIT        "/MT /O2 /Ob2 /D NDEBUG")
        set(CMAKE_C_FLAGS_RELWITHDEBINFO_INIT "/MT /Zi /O2 /Ob1 /D NDEBUG")
        set(CMAKE_CXX_FLAGS_DEBUG_INIT "/D_DEBUG /MTd /Zi /Ob0 /Od /RTC1")
        set(CMAKE_CXX_FLAGS_MINSIZEREL_INIT     "/MT /O1 /Ob1 /D NDEBUG")
        set(CMAKE_CXX_FLAGS_RELEASE_INIT        "/MT /O2 /Ob2 /D NDEBUG")
        set(CMAKE_CXX_FLAGS_RELWITHDEBINFO_INIT "/MT /Zi /O2 /Ob1 /D NDEBUG")
    else()
        set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} -s -static-libgcc -static")
        set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -s -static-libgcc -static-libstdc++ -static")
    endif()
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

add_subdirectory(pybind11)
pybind11_add_module(freeze_pyext ${SOURCE_FILES} mpq/pybindmain.cpp)
set_target_properties(freeze_pyext PROPERTIES OUTPUT_NAME "freezeMpq")

option(FREEZE_BUILD_TESTS "Build freeze unit tests" ON)
if (FREEZE_BUILD_TESTS)
    enable_testing()
    add_executable(mpq_unit_tests
        ${SOURCE_FILES}
        mpq/test_main.cpp
        mpq/test/test_cmpdcmp.cpp
        mpq/test/test_keycalc_crypt.cpp
    )
    target_include_directories(mpq_unit_tests PRIVATE mpq)
    add_test(NAME mpq_unit_tests COMMAND mpq_unit_tests)
endif()

# Copy the built extension into euddraft's lib/ directory so that the
# frozen application can `import freezeMpq`. Extension suffix is .pyd on
# Windows and .so on Linux / macOS.
if (WIN32)
    set(FREEZEMPQ_EXT "pyd")
else()
    set(FREEZEMPQ_EXT "so")
endif()
if (NOT FREEZEMPQ_OUTPUT_DIR)
    set(FREEZEMPQ_OUTPUT_DIR "${CMAKE_SOURCE_DIR}/../lib")
endif()

add_custom_command(TARGET freeze_pyext POST_BUILD
        COMMAND "${CMAKE_COMMAND}" -E copy_if_different "$<TARGET_FILE:freeze_pyext>" "${FREEZEMPQ_OUTPUT_DIR}/freezeMpq.${FREEZEMPQ_EXT}"
        COMMENT "Copying freezeMpq.${FREEZEMPQ_EXT} to ${FREEZEMPQ_OUTPUT_DIR}")
