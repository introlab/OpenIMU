#include "AccelerometerReader.h"
#include <stdio.h>
#include <iostream>
#include <fstream>
#include <windows.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
struct stat info;

AccelerometerReader::AccelerometerReader(void)
{
}


AccelerometerReader::~AccelerometerReader(void)
{
}


AccelerometerReader::AccelerometerReader(string x)
{
	folderPath = x;
}

AccelerometerDataPerHour AccelerometerReader:: GetOneHourAccelerometerData(string x)
{
	const char *filePath = x.c_str();	
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
	AccelerometerDataPerHour accelerometerDataForOneHour;
	for(int i=0; i< numberOfSecondsInFile ; i++)
	{
		accelerometerDataForOneHour.addAccelerometerDataSecond(readAccelerometerDataSecond(fileBuf,i*304));
	}
	//accelerometerDataForOneHour.displayDataPerHour();
	delete[]fileBuf;
	fclose(file);   // Almost forgot this 
	return accelerometerDataForOneHour;
}
AccelerometerDataPerSecond AccelerometerReader::readAccelerometerDataSecond(BYTE* fileBuf, int start)
{
	AccelerometerDataPerSecond AcceleroData;
	int time=0;
	for (int i = start; i < start+4; i++)
	{
		time+=fileBuf[i]*pow(0x100,i-start);
	}

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
long AccelerometerReader::getFileSize(FILE *file)
{
	long lCurPos, lEndPos;
	lCurPos = ftell(file);
	fseek(file, 0, 2);
	lEndPos = ftell(file);
	fseek(file, lCurPos, 0);
	return lEndPos;
}
void AccelerometerReader::findpaths()
{

	DIR *dir;
	struct dirent *ent;
	if ((dir = opendir (folderPath.c_str())) != NULL) {
		/* print all the files and directories within directory */
		while ((ent = readdir (dir)) != NULL ) {
			if (ent->d_type == 0x4000 && string(ent->d_name)!="."&& string(ent->d_name)!="..")
			{
				subdirs.push_back(folderPath+"\\"+ent->d_name);
				printf ("%s \n", ent->d_name);
				listFiles(subdirs.back());
			}
		}
		closedir (dir);
	} else {
		/* could not open directory */
		perror ("");
		return ;
	}
	
}
vector<string> AccelerometerReader::listFiles(string x)
{
	vector<string> paths;
	DIR *dir;
	struct dirent *ent;
	if ((dir = opendir (x.c_str())) != NULL) {
		/* print all the files and directories within directory */
		while ((ent = readdir (dir)) != NULL ) {
			if (ent->d_type == 0x8000 && string(ent->d_name).find("ACC")!=std::string::npos )
			{
				printf ("%s \n",x+"\\"+string(ent->d_name));
				paths.push_back(x+"\\"+ent->d_name);
			}
		}
		closedir (dir);
	} else {
		/* could not open directory */
		perror ("");
	}
	return paths;
}
void AccelerometerReader:: LoadAccelerometerData(){
	findpaths();
	for(string i : subdirs) 
	{
		AccelerometerDataPerDay x;
		std::size_t found = i.find_last_of("/\\");
		int dayNumber = stoi(i.substr(found+1)) ;
		std::cout << " num: " << dayNumber << '\n';
		x.setDayNumber(dayNumber);
		vector<string> files = listFiles(i);
		for (string j : files)
		{
			x.addHourData(GetOneHourAccelerometerData(j));
		}
		data.push_back(x);
	}
}