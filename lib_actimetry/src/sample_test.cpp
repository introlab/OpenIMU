#include "gtest/gtest.h"
#include <string>

namespace {

    //SimpleTest1
    TEST(Sample, SimpleTest1) {
      std::string myString;
      EXPECT_EQ(0, myString.size());
    }
}

