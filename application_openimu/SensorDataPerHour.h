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
	vector<double> computeNormOfAcceleration();
	void displayDataPerHour();

private:
	vector<SensorDataPerSecond> data;

};

