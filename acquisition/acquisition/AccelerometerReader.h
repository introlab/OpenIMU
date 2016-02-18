#pragma once
#include <string>
#include "AccelerometerDataPerDay.h"

using namespace std;
typedef unsigned char BYTE;
const int freq=50;

class AccelerometerReader
{
public:
	AccelerometerReader(void);
	~AccelerometerReader(void);
	AccelerometerReader(string x);
	
	AccelerometerDataPerHour GetOneHourAccelerometerData(string x);
	void LoadAccelerometerData();
	long getFileSize(FILE *file);
	void findpaths();
	vector<string> listFiles(string x);
	AccelerometerDataPerSecond readAccelerometerDataSecond(BYTE* fileBuf, int start);

private:
	string folderPath;
	vector<AccelerometerDataPerDay> data;
	vector<string> subdirs;
};

