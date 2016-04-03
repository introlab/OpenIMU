#pragma once
#include<vector>
#include "SensorDataPerSecond.h"

class SensorDataPerHour
{
public:
	
	SensorDataPerHour(void);
	~SensorDataPerHour(void);

	vector<SensorDataPerSecond> getAccelerometerDataPerHour();
	void addAccelerometerDataSecond(SensorDataPerSecond x);
	void displayDataPerHour();

private:
	vector<SensorDataPerSecond> data;

};

