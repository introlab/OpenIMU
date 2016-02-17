#include "AccelerometerDataPerHour.h"


AccelerometerDataPerHour::AccelerometerDataPerHour(void)
{
}


AccelerometerDataPerHour::~AccelerometerDataPerHour(void)
{
}

vector<AccelerometerDataPerSecond> AccelerometerDataPerHour:: getAccelerometerDataPerHour()
{
  return data;
}

void AccelerometerDataPerHour::addAccelerometerDataSecond(AccelerometerDataPerSecond x)
{
	if(data.size()>0 && x.getTimestamp() == data.back().getTimestamp()){
		x.setTimestamp(x.getTimestamp()+1);
	}
		data.push_back(x);
}
void AccelerometerDataPerHour::displayDataPerHour()
{
	for (int i=0; i<data.size(); ++i)
	{
		data.at(i).displayDataPerSecond();
	}
}