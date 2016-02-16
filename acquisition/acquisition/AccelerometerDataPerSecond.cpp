#include "AccelerometerDataPerSecond.h"


AccelerometerDataPerSecond::AccelerometerDataPerSecond(void)
{
}


AccelerometerDataPerSecond::~AccelerometerDataPerSecond(void)
{
}

void AccelerometerDataPerSecond:: setTimestamp(int value){
	timestamp = value;
}
int AccelerometerDataPerSecond:: getTimestamp(){
	return timestamp;
}
void AccelerometerDataPerSecond::setXAxisValue(signed short int xvalue){
	x_Axis.push_back(xvalue);
}
void AccelerometerDataPerSecond::setYAxisValue(signed short int yvalue){
	y_Axis.push_back(yvalue);
}
void AccelerometerDataPerSecond::setZAxisValue(signed short int zvalue){
	z_Axis.push_back(zvalue);
}
vector<signed short int> AccelerometerDataPerSecond:: getXAxisValues(){
	return x_Axis;
}
vector<signed short int> AccelerometerDataPerSecond:: getYAxisValues(){
	return y_Axis;
}
vector<signed short int> AccelerometerDataPerSecond:: getZAxisValues(){
	return z_Axis;
}