#include "SensorReader.h"
#include <stdio.h>
#include <iostream>
#include <fstream>
#ifdef WIN32
//Needed???
#include <windows.h>
#endif
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <math.h>
struct stat info;


SensorReader::SensorReader(void)
{
}


SensorReader::~SensorReader(void)
{
}


SensorReader::SensorReader(string x, string y)
{
    folderPath = x;
    sensorType = y;
}


long SensorReader::getFileSize(FILE *file)
{
    long lCurPos, lEndPos;
    lCurPos = ftell(file);
    fseek(file, 0, 2);
    lEndPos = ftell(file);
    fseek(file, lCurPos, 0);
    return lEndPos;
}

vector<string> SensorReader::listFiles(string x)
{
    vector<string> paths;
    DIR *dir;
    struct dirent *ent;
    if ((dir = opendir (x.c_str())) != NULL) {
        /* print all the files and directories within directory */
        while ((ent = readdir (dir)) != NULL ) {
            if (/*ent->d_type == 0x8000 &&*/  string(ent->d_name).find(sensorType)!=std::string::npos )
            {
                //printf ("%s \n",x+"\\"+string(ent->d_name));
                if(string(ent->d_name)!= "." && string(ent->d_name) != ".." )
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
vector<SensorDataPerDay> SensorReader::GetAccelerometerData()
{
    return data;
}
SensorDataPerHour SensorReader:: GetOneHourSensorData(string x)
{
    const char *filePath = x.c_str();
    BYTE *fileBuf;			// Pointer to our buffered data
    FILE *file = NULL;		// File pointer

    // Open the file in binary mode using the "rb" format string
    // This also checks if the file exists and/or can be opened for reading correctly
    if ((file = fopen(filePath, "rb")) == NULL)
        cout << "Could not open specified file" << endl;
    else{
        cout << "File opened successfully" << endl;

        // Get the size of the file in bytes
        long fileSize = getFileSize(file);

        // Allocate space in the buffer for the whole file
        fileBuf = new BYTE[fileSize];

        // Read the file in to the buffer
        fread(fileBuf, fileSize, 1, file);
        int numberOfSecondsInFile = fileSize/304;
        SensorDataPerHour accelerometerDataForOneHour;
        for(int i=0; i< numberOfSecondsInFile ; i++)
        {
            accelerometerDataForOneHour.addAccelerometerDataSecond(readSensorDataSecond(fileBuf,i*304));
        }
        //accelerometerDataForOneHour.displayDataPerHour();
        delete[]fileBuf;
        fclose(file);
        return accelerometerDataForOneHour;
    }
    SensorDataPerHour obj;
    return obj;
}
SensorDataPerSecond SensorReader::readSensorDataSecond(BYTE* fileBuf, int start)
{
    SensorDataPerSecond AcceleroData;
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

void SensorReader:: LoadSensorData(bool cond){
    if(cond){
        findpaths();
        for(string i : subdirs)
        {
            SensorDataPerDay x;
            std::size_t found = i.find_last_of("/\\");
            int dayNumber = stoi(i.substr(found+1)) ;
            std::cout << " num: " << dayNumber << '\n';
            x.setDayNumber(dayNumber);
            vector<string> files = listFiles(i);
            for (string j : files)
            {
                x.addHourData(GetOneHourSensorData(j));
            }
            data.push_back(x);
        }
    }
    else{
        SensorDataPerDay x;
        //std::size_t found = folderPath.find_last_of("/\\");
        //int dayNumber = stoi(folderPath.substr(found+1)) ;
        // std::cout << " num: " << dayNumber << '\n';
        // x.setDayNumber(dayNumber);
        // vector<string> files = listFiles(folderPath);
        // for (string j : files)
        // {
        x.addHourData(GetOneHourSensorData(folderPath));
        // }
        data.push_back(x);
    }
}

void SensorReader::findpaths()
{
    DIR *dir;
    struct dirent *ent;
    if ((dir = opendir (folderPath.c_str())) != NULL) {
        /* print all the files and directories within directory */
        while ((ent = readdir (dir)) != NULL ) {
            if (/*ent->d_type == 0x4000 &&*/ string(ent->d_name)!="."&& string(ent->d_name)!="..")
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
