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
    ${CMAKE_CURRENT_SOURCE_DIR}/TestBenchmark.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/../../applicationOpenimu/app/CustomQmlScene.cpp
    )

SET(headers
    ${CMAKE_CURRENT_SOURCE_DIR}/TestBenchmark.h
    ${CMAKE_CURRENT_SOURCE_DIR}/../../applicationOpenimu/app/CustomQmlScene.h
    )
<<<<<<< HEAD
=======

>>>>>>> 27ad10623e4fd3951298e50afd5c941a4bd5267d
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../../applicationOpenimu/app/core ${CMAKE_CURRENT_BINARY_DIR}/core)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../../applicationOpenimu/app/algorithm ${CMAKE_CURRENT_BINARY_DIR}/algorithm)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../../applicationOpenimu/app/acquisition ${CMAKE_CURRENT_BINARY_DIR}/acquisition)


include_directories(
    ../../applicationOpenimu/app/core/json
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
