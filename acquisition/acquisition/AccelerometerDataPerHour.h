#pragma once
#include<vector>
#include "AccelerometerDataPerSecond.h"

class AccelerometerDataPerHour
{
public:
	
	AccelerometerDataPerHour(void);
	~AccelerometerDataPerHour(void);

	vector<AccelerometerDataPerSecond> getAccelerometerDataPerHour();
	void addAccelerometerDataSecond(AccelerometerDataPerSecond x);
	void displayDataPerHour();

private:
	vector<AccelerometerDataPerSecond> data;

};

