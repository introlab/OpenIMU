#include "SensorDataPerSecond.h"


SensorDataPerSecond::SensorDataPerSecond(void)
{
}


SensorDataPerSecond::~SensorDataPerSecond(void)
{
}

void SensorDataPerSecond:: setTimestamp(int value){
	timestamp = value;
}
int SensorDataPerSecond:: getTimestamp(){
	return timestamp;
}
void SensorDataPerSecond::setXAxisValue(signed short int xvalue){
	x_Axis.push_back(xvalue);
}
void SensorDataPerSecond::setYAxisValue(signed short int yvalue){
	y_Axis.push_back(yvalue);
}
void SensorDataPerSecond::setZAxisValue(signed short int zvalue){
	z_Axis.push_back(zvalue);
}
void SensorDataPerSecond:: displayDataPerSecond(){
//	printf("TIMESTAMP %X \n",timestamp);

	for(int i =0;i<x_Axis.size();++i ){
//		printf("Acceleration X: %d, Y: %d, Z: %d   \n",x_Axis.at(i), y_Axis.at(i),z_Axis.at(i));
	}
	
}
vector<signed short int> SensorDataPerSecond:: getXAxisValues(){
	return x_Axis;
}
vector<signed short int> SensorDataPerSecond:: getYAxisValues(){
	return y_Axis;
}
vector<signed short int> SensorDataPerSecond:: getZAxisValues(){
	return z_Axis;
}
