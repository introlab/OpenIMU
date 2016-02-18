#pragma once
#include "AccelerometerDataPerHour.h"
#include <vector>

class AccelerometerDataPerDay
{
public:
	AccelerometerDataPerDay(void);
	~AccelerometerDataPerDay(void);
	void setDayNumber(int x);
	int getDayNumer();
	vector<AccelerometerDataPerHour> getDataPerDay();
	void addHourData(AccelerometerDataPerHour x);
	
private:
	int dayNumber;
	vector<AccelerometerDataPerHour> data;
};

