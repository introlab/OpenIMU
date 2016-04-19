cmake_minimum_required(VERSION 2.8.11)
project(test_benchmark)

find_package(Qt5Core    REQUIRED)
find_package(Qt5Gui     REQUIRED)
find_package(Qt5Widgets REQUIRED)
find_package(Qt5Quick   REQUIRED)
find_package(Qt5Charts	REQUIRED)


#MINGW COMPILE FLAGS
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -std=c++11")

enable_testing(true)

SET(srcs
    ${CMAKE_CURRENT_SOURCE_DIR}/testbenchmark.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/../../application_openimu/app/customqmlscene.cpp
    )

SET(headers
    ${CMAKE_CURRENT_SOURCE_DIR}/testbenchmark.h
    ${CMAKE_CURRENT_SOURCE_DIR}/../../application_openimu/app/customqmlscene.h
    )

add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../../application_openimu/app/models ${CMAKE_CURRENT_BINARY_DIR}/models)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../../application_openimu/app/newAcquisition ${CMAKE_CURRENT_BINARY_DIR}/newAcquisition)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../../application_openimu/app/algorithm ${CMAKE_CURRENT_BINARY_DIR}/algorithm)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../../application_openimu/app/acquisition ${CMAKE_CURRENT_BINARY_DIR}/acquisition)


include_directories(
    ../../application_openimu/app/models/json
    )

# Tell CMake to run moc when necessary:
set(CMAKE_AUTOMOC ON)

# As moc files are generated in the binary dir, tell CMake
# to always look for includes there:
set(CMAKE_INCLUDE_CURRENT_DIR ON)

find_package(Qt5Test REQUIRED)

add_executable(test_benchmark main.cpp ${srcs} ${headers})
add_test(test_benchmark test_benchmark)
qt5_use_modules(test_benchmark Sql Core Network Xml XmlPatterns Gui Widgets Quick Charts)

target_link_libraries(test_benchmark Qt5::Test)
