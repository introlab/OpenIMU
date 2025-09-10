#Look for minimum cmake version
cmake_minimum_required(VERSION 3.21)

PROJECT (OpenIMU LANGUAGES NONE)

set(CMAKE_VERBOSE_MAKEFILE ON)

#Python
add_subdirectory(python)
