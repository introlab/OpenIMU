#include "WimuAcquisition.h"
#include <fstream>
#include <math.h>
#ifdef WIN32
#include <windows.h>
#endif
#include <sys/types.h>
#include <sys/stat.h>
#include <time.h>
#include <ctime>
#include<QDebug>

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

void WimuAcquisition::Serialize( Json::Value& root,RecordInfo infos,  std::string date,std::string& output )
{
   // serialize
   Json::Value mainRoot;

   Json::Value init(Json::objectValue);
   init["name"] = infos.m_recordName;
   init["format"] = infos.m_imuType;
   init["position"] = infos.m_imuPosition;
   init["comment"] = infos.m_recordDetails;

   //Acc
   Json::Value temp(Json::arrayValue);
   for (size_t j = 0; j != data.size(); j++)
   {
       Json::Value obj(Json::objectValue);
       obj["x"] = data.at(j).x;
       obj["y"] = data.at(j).y;
       obj["z"] = data.at(j).z;
       obj["t"] = data.at(j).timestamp;
       temp.append(obj);
   }

   //Gyr
   Json::Value temp1(Json::arrayValue);
   for (size_t j = 0; j != dataGyro.size(); j++)
   {
       Json::Value obj1(Json::objectValue);
       obj1["x"] = dataGyro.at(j).x;
       obj1["y"] = dataGyro.at(j).y;
       obj1["z"] = dataGyro.at(j).z;
       obj1["t"] = dataGyro.at(j).timestamp;
       temp1.append(obj1);
   }

   //Mag
   Json::Value temp2(Json::arrayValue);
   for (size_t j = 0; j != dataMagneto.size(); j++)
   {
       Json::Value obj2(Json::objectValue);
       obj2["x"] = dataMagneto.at(j).x;
       obj2["y"] = dataMagneto.at(j).y;
       obj2["z"] = dataMagneto.at(j).z;
       obj2["t"] = dataMagneto.at(j).timestamp;
       temp2.append(obj2);
   }
   mainRoot["record"]= init;
   mainRoot["accelerometres"]= temp;
   mainRoot["gyrometres"]= temp1;
   mainRoot["magnetometres"]= temp2;

   Json::StyledWriter writer;
   output = writer.write(mainRoot);
}

void WimuAcquisition::Deserialize( Json::Value& root )
{
   // deserialize primitives

    Json::Value accData = root.get("accelerometres", "");
    for(int i =0; i<accData.size(); i++)
    {
        frame temp;
        temp.timestamp = accData[i].get("t", "").asLargestInt();
        temp.x = accData[i].get("x", "").asInt();
        temp.y = accData[i].get("y", "").asInt();
        temp.z = accData[i].get("z", "").asInt();

        data.push_back(temp);
    }

    Json::Value gyrData = root.get("gyrometres", "");
    for(int i =0; i<gyrData.size(); i++)
    {
        frame temp;
        temp.timestamp = gyrData[i].get("t", "").asLargestInt();
        temp.x = gyrData[i].get("x", "").asInt();
        temp.y = gyrData[i].get("y", "").asInt();
        temp.z = gyrData[i].get("z", "").asInt();

        dataGyro.push_back(temp);
    }

    Json::Value magData = root.get("magnetometres", "");
    for(int i =0; i<magData.size(); i++)
    {
        frame temp;
        temp.timestamp = magData[i].get("t", "").asLargestInt();
        temp.x = magData[i].get("x", "").asInt();
        temp.y = magData[i].get("y", "").asInt();
        temp.z = magData[i].get("z", "").asInt();

        dataMagneto.push_back(temp);
    }
    qDebug() << data.size();

}

void WimuAcquisition::initialize()
{
    if(!fileAcc.empty())
    {
         extractAcceleroData();
    }
    if(!fileGyro.empty())
    {
        extractGyrometerData();
    }
    if(!fileMagneto.empty())
    {
        extractMagnetomer();
    }
}

void WimuAcquisition::extractAcceleroData()
{
    const char *filePath = fileAcc.c_str();
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

void WimuAcquisition::extractGyrometerData()
{
    const char *filePath = fileGyro.c_str();
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
        dataGyro.insert(dataGyro.end(), b.begin(), b.end());
    }
}

void WimuAcquisition::extractMagnetomer()
{
    const char *filePath = fileMagneto.c_str();
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
        dataMagneto.insert(dataMagneto.end(), b.begin(), b.end());
    }
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
WimuAcquisition::WimuAcquisition(std::string filenameAccelero, std::string filenameGyro,std::string filenameMagneto, int frequence)
{
    this->fileAcc = filenameAccelero;
    this->fileGyro = filenameGyro;
    this->fileMagneto = filenameMagneto;
    this->freq = frequence;

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
                        std::time_t _time =(time_t) t;
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
