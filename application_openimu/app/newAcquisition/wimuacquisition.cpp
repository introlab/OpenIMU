#include "wimuacquisition.h"
#include <fstream>
#include <math.h>
#ifdef WIN32
//Needed???
#include <windows.h>
#endif
#include <sys/types.h>
#include <sys/stat.h>
#include <time.h>
#include <ctime>

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
    long long time=0;
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
std::vector<string_timestamp> WimuAcquisition::getDates()
{
	std::vector<string_timestamp> result;
    long long lastTimestamp = -1;
	for (int i=0;i<data.size();i++)
    {
		long long t = data.at(i).timestamp/1000;
		int day =t/86400;
		int lastday=lastTimestamp/86400;
		if(lastTimestamp==-1 || day!=lastday)
        {
			string_timestamp tmp;
            /*__time64_t ltime = t;
			
			tmp.date = _ctime64( &ltime );
			tmp.date.erase(tmp.date.size() - 1);
			tmp.timestamp = data.at(i).timestamp;*/
			std::time_t _time =(time_t) t;
			//ctime(_time);
			char buffer[32];
			// Format: Mo, 15.06.2009 20:20:00
			tmp.timestamp = data.at(i).timestamp;
			std::strftime(buffer, 32, "%d %B %Y", gmtime (&_time));
			tmp.date = buffer;
			result.push_back(tmp);
        }
        lastTimestamp = t;
    }
	return result;
}
int WimuAcquisition::getDataSize()
{
	return data.size();
}
std::vector<frame> WimuAcquisition::getData(long long start,long long end)
{
	std::vector<frame> result;
	for (frame _frame : data)
	{
		if(_frame.timestamp<=end && _frame.timestamp>=start)
			result.push_back(_frame);
	}
	return result;
}
string_timestamp WimuAcquisition::maxTime(std::vector<frame> _frames)
{
	long long max = 0;
	string_timestamp result;
	for (int i=_frames.size()-1;i>=0;i--)
	{
		if (_frames.at(i).timestamp>max)
			max = _frames.at(i).timestamp;
	}
	result.timestamp=max;
	std::time_t _time =(time_t) max/1000;
	char buffer[32];
	std::strftime(buffer, 32, "%H:%M", gmtime (&_time));
	result.date = buffer;
	return result;
}
string_timestamp WimuAcquisition::minTime(std::vector<frame> _frames)
{
	long long min=-1;
	string_timestamp result;
	for (frame _frame : _frames)
	{
		if (_frame.timestamp<min || min ==-1)
			min = _frame.timestamp;
	}
	result.timestamp=min;
	std::time_t _time =(time_t) min/1000;
	char buffer[32];
	std::strftime(buffer, 32, "%H:%M", gmtime (&_time));
	result.date = buffer;
	return result;
}
