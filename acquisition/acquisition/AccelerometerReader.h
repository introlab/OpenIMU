#pragma once
#include "SensorReader.h"
#include <iostream>

class AccelerometerReader: public SensorReader
{
public:
	AccelerometerReader(void);
	~AccelerometerReader(void);
	AccelerometerReader(string s) :SensorReader(s,"ACC"){}
};

