#include "SensorDataPerHour.h"


SensorDataPerHour::SensorDataPerHour(void)
{
}


SensorDataPerHour::~SensorDataPerHour(void)
{
}

vector<SensorDataPerSecond> SensorDataPerHour:: getAccelerometerDataPerHour()
{
  return data;
}

void SensorDataPerHour::addAccelerometerDataSecond(SensorDataPerSecond x)
{
	if(data.size()>0 && x.getTimestamp() == data.back().getTimestamp()){
		x.setTimestamp(x.getTimestamp()+1);
	}
		data.push_back(x);
}
vector<double> SensorDataPerHour:: computeNormOfAcceleration(){

}
void SensorDataPerHour::displayDataPerHour()
{
	for (int i=0; i<data.size(); ++i)
	{
		data.at(i).displayDataPerSecond();
	}
}