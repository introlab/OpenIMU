#pragma once
#include "SensorReader.h"

class MagnetometerReader : public SensorReader
{
public:
	MagnetometerReader(void);
	~MagnetometerReader(void);
	MagnetometerReader(string s): SensorReader(s,"MAG"){}
};

