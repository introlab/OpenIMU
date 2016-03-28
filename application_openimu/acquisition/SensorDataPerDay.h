#pragma once
#include "SensorDataPerHour.h"
#include <vector>

class SensorDataPerDay
{
public:
	SensorDataPerDay(void);
	~SensorDataPerDay(void);
	void setDayNumber(int x);
	int getDayNumer();
	vector<SensorDataPerHour> getDataPerDay();
	void addHourData(SensorDataPerHour x);
	
private:
	int dayNumber;
	vector<SensorDataPerHour> data;
};

