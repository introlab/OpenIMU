#include "wimuacquisition.h"
#include <fstream>
#include <math.h>
#include <windows.h>
#include <sys/types.h>
#include <sys/stat.h>
std::vector<frame> WimuAcquisition::getData()
{
    return data;
}

void WimuAcquisition::setData(std::vector<frame> value)
{
    data = value;
}

WimuAcquisition::WimuAcquisition()
{

}
WimuAcquisition::~WimuAcquisition()
{

}
long WimuAcquisition::getFileSize(FILE *file)
{
    long lCurPos, lEndPos;
    lCurPos = ftell(file);
    fseek(file, 0, 2);
    lEndPos = ftell(file);
    fseek(file, lCurPos, 0);
    return lEndPos;
}
WimuAcquisition::WimuAcquisition(std::string filename,int freq)
{
    const char *filePath = filename.c_str();
    BYTE *fileBuf;			// Pointer to our buffered data
    FILE *file = NULL;		// File pointer

    // Open the file in binary mode using the "rb" format string
    // This also checks if the file exists and/or can be opened for reading correctly
    if ((file = fopen(filePath, "rb")) == NULL)
        std::cout << "Could not open specified file" << std::endl;
    else
        std::cout << "File opened successfully" << std::endl;

    // Get the size of the file in bytes
    long fileSize = getFileSize(file);

    // Allocate space in the buffer for the whole file
    fileBuf = new BYTE[fileSize];

    // Read the file in to the buffer
    fread(fileBuf, fileSize, 1, file);
    int numberOfSecondsInFile = fileSize/304;
    for(int i=0; i< numberOfSecondsInFile ; i++)
    {
        std::vector<frame> b=readSensorDataSecond(fileBuf,i*304,freq);
        data.insert(data.end(), b.begin(), b.end());
    }
}

 std::vector<frame> WimuAcquisition::readSensorDataSecond(BYTE* fileBuf, int start,int freq)
{
    std::vector<frame> tmp;
    int time=0;
    for (int i = start; i < start+4; i++)
    {
        time+=fileBuf[i]*pow(0x100,i-start);
    }

    time*=1000;
    for (int i = 0; i < freq; i++)
    {
        frame leFrame;
        leFrame.timestamp=time+i*(1000/freq);
        leFrame.x=(fileBuf[start+4+2*i+1]*0x100+fileBuf[start+4+2*i]);
        leFrame.y=(fileBuf[start+4+2*freq+2*i+1]*0x100+fileBuf[start+4+2*freq+2*i]);
        leFrame.z=(fileBuf[start+4+4*freq+2*i+1]*0x100+fileBuf[start+4+4*freq+2*i]);
        tmp.push_back(leFrame);
    }
    return tmp;
}
