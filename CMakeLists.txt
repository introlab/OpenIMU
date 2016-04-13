PROJECT (OpenIMU)

SET(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS TRUE)
SET(BUILD_SHARED_LIBS TRUE)

include(CTest)
include(CheckFunctionExists)

#Look for minimum cmake version
cmake_minimum_required(VERSION 3.0.2)

#DEFINITIONS POLICY, NEW SINCE 3.0.2
cmake_policy(SET CMP0043 NEW)


########################
# Configurations
########################

# compile in debug or release mode
IF(NOT CMAKE_BUILD_TYPE)
  #SET(CMAKE_BUILD_TYPE Release)
  SET(CMAKE_BUILD_TYPE Debug)
ENDIF(NOT CMAKE_BUILD_TYPE)

#MINGW COMPILE FLAGS
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -std=c++11")
SET(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall")
SET(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wall")

#Install directory
MESSAGE( STATUS "Windows version: " ${CMAKE_SYSTEM})
SET(CMAKE_INSTALL_PREFIX "$ENV{SYSTEMDRIVE}/OpenIMU-${CMAKE_BUILD_TYPE}")
MESSAGE( STATUS "Install directory is : " ${CMAKE_INSTALL_PREFIX})
MESSAGE( STATUS "PROJECT SOURCE DIR is : " ${CMAKE_SOURCE_DIR})
MESSAGE( STATUS "Current Binary Dir : " ${CMAKE_CURRENT_BINARY_DIR})


#This will enable to output everything in the bin directory for testing and debugging...
SET (EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)
SET (LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)

SET(CMAKE_VERBOSE_MAKEFILE ON)


add_subdirectory(application_openimu)
