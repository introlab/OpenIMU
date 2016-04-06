#pragma once
#include <string>
#include "SensorDataPerDay.h"

using namespace std;
typedef unsigned char BYTE;
const int freq=50;

class SensorReader
{
public:
	SensorReader(void);
	~SensorReader(void);
	SensorReader(string x, string y);
	
	SensorDataPerHour GetOneHourSensorData(string x);
	vector<SensorDataPerDay> GetAccelerometerData();
    void LoadSensorData(bool cond);
	SensorDataPerSecond readSensorDataSecond(BYTE* fileBuf, int start);

	long getFileSize(FILE *file);
	void findpaths();
	vector<string> listFiles(string x);

protected:
	string folderPath;
	vector<SensorDataPerDay> data;
	vector<string> subdirs;
	string sensorType;
};

