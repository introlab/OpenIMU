#include <stdio.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <windows.h>
#include "AccelerometerDataPerSecond.h"

using namespace std;
typedef unsigned char BYTE;
const int freq=50;

void LoadAccelerometerdata();
AccelerometerDataPerSecond readAccelerometerDataSecond(BYTE* ,int);

int main( int argc, const char* argv[] )
{
	LoadAccelerometerdata();
	return 0;
}

long getFileSize(FILE *file)
{
	long lCurPos, lEndPos;
	lCurPos = ftell(file);
	fseek(file, 0, 2);
	lEndPos = ftell(file);
	fseek(file, lCurPos, 0);
	return lEndPos;
}

void LoadAccelerometerdata()
{
	const char *filePath = "C:\\ACC_4.DAT";	
	BYTE *fileBuf;			// Pointer to our buffered data
	FILE *file = NULL;		// File pointer

	// Open the file in binary mode using the "rb" format string
	// This also checks if the file exists and/or can be opened for reading correctly
	if ((file = fopen(filePath, "rb")) == NULL)
		cout << "Could not open specified file" << endl;
	else
		cout << "File opened successfully" << endl;

	// Get the size of the file in bytes
	long fileSize = getFileSize(file);

	// Allocate space in the buffer for the whole file
	fileBuf = new BYTE[fileSize];

	// Read the file in to the buffer
	fread(fileBuf, fileSize, 1, file);
	int numberOfSecondsInFile = fileSize/304;
	vector<AccelerometerDataPerSecond> accelerometerDataPerHour;
	for(int i=0; i< numberOfSecondsInFile ; i++)
	{
		accelerometerDataPerHour.push_back(readAccelerometerDataSecond(fileBuf,i*304));
	}
	
	cin.get();
	delete[]fileBuf;
    fclose(file);   // Almost forgot this 
}

//TO DO: CHANGE TO DELETE FILEBUFF
AccelerometerDataPerSecond readAccelerometerDataSecond(BYTE* fileBuf, int start)
{
	AccelerometerDataPerSecond AcceleroData;
	int time=0;
	for (int i = start; i < start+4; i++)
	{
		time+=fileBuf[i]*pow(0x100,i-start);
	}
	printf("TIMESTAMP: %X \n", time);
	AcceleroData.setTimestamp(time);

	for (int i = 0; i < freq; i++)
	{		 
		AcceleroData.setXAxisValue(fileBuf[start+4+2*i+1]*0x100+fileBuf[start+4+2*i]);
	}//TO DO Test if we can use one for condition, performance wise

	for (int i = 0; i < freq; i++)
	{
		AcceleroData.setYAxisValue(fileBuf[start+4+2*freq+2*i+1]*0x100+fileBuf[start+4+2*freq+2*i]);
	}
	for (int i = 0; i < freq; i++)
	{
		AcceleroData.setZAxisValue(fileBuf[start+4+4*freq+2*i+1]*0x100+fileBuf[start+4+4*freq+2*i]);
	}
	//printf("Acceleration X: %d \n",	AcceleroData.getXAxisValues().at(4));
	return AcceleroData;
}