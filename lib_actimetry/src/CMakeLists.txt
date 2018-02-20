#TOOD add files.

include_directories(${GTEST_INCLUDES})
include_directories(${KFR_INCLUDES})
include_directories(${LIQUIDDSP_INCLUDES})
include_directories(${GSL_INCLUDES})

add_executable(sample_test sample_test.cpp)
target_link_libraries(sample_test ${GTEST_LIBS} ${GSL_LIBS})
add_test(AllTests sample_test)

