#include "SensorDataPerDay.h"


SensorDataPerDay::SensorDataPerDay(void)
{
}


SensorDataPerDay::~SensorDataPerDay(void)
{
}

void SensorDataPerDay:: setDayNumber(int x)
{
	dayNumber = x;
}
int SensorDataPerDay:: getDayNumer()
{
	return dayNumber;
}
vector<SensorDataPerHour> SensorDataPerDay:: getDataPerDay()
{
	return data;
}
void SensorDataPerDay::addHourData(SensorDataPerHour x)
{
	data.push_back(x);
}
