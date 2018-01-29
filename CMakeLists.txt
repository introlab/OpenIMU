PROJECT (OpenIMU)

SET(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS TRUE)
SET(BUILD_SHARED_LIBS TRUE)

include(CTest)
include(CheckFunctionExists)

#Look for minimum cmake version
cmake_minimum_required(VERSION 3.0.2)

#First, let's compile our dependencies
add_subdirectory(third_party)

#Then, compile our actimetry library
add_subdirectory(lib_actimetry)
