#pragma once
#include "SensorReader.h"

class GyroscopeReader : public SensorReader
{
public:
	GyroscopeReader(void);
	~GyroscopeReader(void);
	GyroscopeReader(string s) :SensorReader(s,"GYR"){}
};

