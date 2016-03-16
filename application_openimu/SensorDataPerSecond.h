#pragma once
#include <vector>

using namespace std;

class SensorDataPerSecond
{
public:
	SensorDataPerSecond(void);
	~SensorDataPerSecond(void);
	
	void setTimestamp(int value);
	int getTimestamp();

	void setXAxisValue(signed short int xvalue);
	void setYAxisValue(signed short int yvalue);
	void setZAxisValue(signed short int zvalue);

	void displayDataPerSecond();

	vector<signed short int> getXAxisValues();
	vector<signed short int> getYAxisValues();
	vector<signed short int> getZAxisValues();


private:
	int timestamp;
	vector<signed short int> x_Axis;
	vector<signed short int> y_Axis;
	vector<signed short int> z_Axis;

};

