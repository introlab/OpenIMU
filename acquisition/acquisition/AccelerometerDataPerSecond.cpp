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
void AccelerometerDataPerSecond:: displayDataPerSecond(){
	printf("TIMESTAMP %X \n",timestamp);

	for(int i =0;i<x_Axis.size();++i ){
		printf("Acceleration X: %d, Y: %d, Z: %d   \n",x_Axis.at(i), y_Axis.at(i),z_Axis.at(i));
	}
	
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