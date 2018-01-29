#TOOD add files.

include_directories(${GTEST_INCLUDES})

add_executable(sample_test sample_test.cpp)
target_link_libraries(sample_test ${GTEST_LIBS})
add_test(AllTests sample_test)

