#include "AccelerometerDataPerDay.h"


AccelerometerDataPerDay::AccelerometerDataPerDay(void)
{
}


AccelerometerDataPerDay::~AccelerometerDataPerDay(void)
{
}

void AccelerometerDataPerDay:: setDayNumber(int x)
{
	dayNumber = x;
}
int AccelerometerDataPerDay:: getDayNumer()
{
	return dayNumber;
}
vector<AccelerometerDataPerHour> AccelerometerDataPerDay:: getDataPerDay()
{
	return data;
}
void AccelerometerDataPerDay::addHourData(AccelerometerDataPerHour x)
{
	data.push_back(x);
}
