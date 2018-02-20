#Add googletest library
add_subdirectory(googletest)
set(GTEST_INCLUDES ${CMAKE_CURRENT_SOURCE_DIR}/googletest/include CACHE INTERNAL "doc string")
set(GTEST_LIBS gtest gmock gtest_main CACHE INTERNAL "doc string")

#Add liquid-dsp wrapper
#Does not build with MSVC2017
#add_subdirectory(liquid-dsp)

add_subdirectory(kfr)
set(KFR_INCLUDES ${CMAKE_CURRENT_SOURCE_DIR}/kfr/include CACHE INTERNAL "doc string")


set(GSL_DISABLE_TESTS TRUE)
add_subdirectory(gsl)
#GSL includes are all generated to build directory/gsl
set(GSL_INCLUDES ${CMAKE_CURRENT_BINARY_DIR}/gsl CACHE INTERNAL "doc string")
set(GSL_LIBS gsl gslcblas CACHE INTERNAL "doc string")
