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

std::vector<frame> WimuAcquisition::getDataAccelerometer() const
{
    return m_dataAccelerometer;
}

void WimuAcquisition::setDataAccelerometer(std::vector<frame> value)
{
    m_dataAccelerometer = value;
}

WimuAcquisition::WimuAcquisition()
{

}
WimuAcquisition::~WimuAcquisition()
{

}

void WimuAcquisition::Serialize( Json::Value& root, RecordInfo recordInfo, std::string& output)
{
   // serialize
   Json::Value mainRoot;
   Json::Value init(Json::objectValue);
   init["name"] = recordInfo.m_recordName;
   init["format"] = recordInfo.m_imuType;
   init["position"] = recordInfo.m_imuPosition;
   init["comment"] = recordInfo.m_recordDetails;
   init["parent_id"] = recordInfo.m_parentId;

   //Accelerometer
   Json::Value accJsonValues(Json::arrayValue);
   for (size_t j = 0; j != m_dataAccelerometer.size(); j++)
   {
       Json::Value accObj(Json::objectValue);
       accObj["x"] = m_dataAccelerometer.at(j).x;
       accObj["y"] = m_dataAccelerometer.at(j).y;
       accObj["z"] = m_dataAccelerometer.at(j).z;
       accObj["t"] = m_dataAccelerometer.at(j).timestamp;
       accJsonValues.append(accObj);
   }

   //Gyrometer
   Json::Value gyrJsonValues(Json::arrayValue);
   for (size_t j = 0; j != m_dataGyro.size(); j++)
   {
       Json::Value gyrObj(Json::objectValue);
       gyrObj["x"] = m_dataGyro.at(j).x;
       gyrObj["y"] = m_dataGyro.at(j).y;
       gyrObj["z"] = m_dataGyro.at(j).z;
       gyrObj["t"] = m_dataGyro.at(j).timestamp;
       gyrJsonValues.append(gyrObj);
   }

   //Magnetometer
   Json::Value magJsonValues(Json::arrayValue);
   for (size_t j = 0; j != m_dataMagneto.size(); j++)
   {
       Json::Value magObj(Json::objectValue);
       magObj["x"] = m_dataMagneto.at(j).x;
       magObj["y"] = m_dataMagneto.at(j).y;
       magObj["z"] = m_dataMagneto.at(j).z;
       magObj["t"] = m_dataMagneto.at(j).timestamp;
       magJsonValues.append(magObj);
   }
   mainRoot["record"]= init;
   if(accJsonValues.size()!= 0)
   {
        mainRoot["accelerometres"]= accJsonValues;
   }
   if(gyrJsonValues.size()!= 0)
   {
        mainRoot["gyrometres"]= gyrJsonValues;
   }
   if(magJsonValues.size()!= 0)
   {
        mainRoot["magnetometres"]= magJsonValues;
   }

   Json::StyledWriter writer;
   output = writer.write(mainRoot);
}

void WimuAcquisition::Deserialize( Json::Value& root )
{
   // deserialize primitives

    Json::Value accJsonValues = root.get("accelerometres", "");
    for(int i =0; i<accJsonValues.size(); i++)
    {
        frame value;
        value.timestamp = accJsonValues[i].get("t", "").asLargestInt();
        value.x = accJsonValues[i].get("x", "").asInt();
        value.y = accJsonValues[i].get("y", "").asInt();
        value.z = accJsonValues[i].get("z", "").asInt();

        m_dataAccelerometer.push_back(value);
    }

    Json::Value gyrJsonValues = root.get("gyrometres", "");
    for(int i =0; i<gyrJsonValues.size(); i++)
    {
        frame value;
        value.timestamp = gyrJsonValues[i].get("t", "").asLargestInt();
        value.x = gyrJsonValues[i].get("x", "").asInt();
        value.y = gyrJsonValues[i].get("y", "").asInt();
        value.z = gyrJsonValues[i].get("z", "").asInt();

        m_dataGyro.push_back(value);
    }

    Json::Value magJsonValues = root.get("magnetometres", "");
    for(int i =0; i<magJsonValues.size(); i++)
    {
        frame value;
        value.timestamp = magJsonValues[i].get("t", "").asLargestInt();
        value.x = magJsonValues[i].get("x", "").asInt();
        value.y = magJsonValues[i].get("y", "").asInt();
        value.z = magJsonValues[i].get("z", "").asInt();

        m_dataMagneto.push_back(value);
    }

}

void WimuAcquisition::initialize()
{
    if(!m_filepathAcc.empty())
    {
         extractAcceleroData();
    }
    if(!m_filepathGyro.empty())
    {
        extractGyrometerData();
    }
    if(!m_filepathMagneto.empty())
    {
        extractMagnetomer();
    }
}

void WimuAcquisition::clearData()
{
    m_dataAccelerometer.clear();
    m_dataMagneto.clear();
    m_dataGyro.clear();
    m_filepathAcc = "";
    m_filepathGyro = "";
    m_filepathMagneto = "";
}

void WimuAcquisition::extractAcceleroData()
{
    BYTE *fileBuf;			// Pointer to our buffered data
    FILE *file = NULL;		// File pointer

    // Get the size of the file in bytes
    long fileSize = getFileSize(file);

    // Allocate space in the buffer for the whole file
    fileBuf = new BYTE[fileSize];

    // Read the file in to the buffer
    fread(fileBuf, fileSize, 1, file);
    int numberOfSecondsInFile = fileSize/304;
    for(int i=0; i< numberOfSecondsInFile ; i++)
    {
        std::vector<frame> buffer=readSensorDataSecond(fileBuf,i*304,m_wimuFrequency);
        m_dataAccelerometer.insert(m_dataAccelerometer.end(), buffer.begin(), buffer.end());
    }
}

void WimuAcquisition::extractGyrometerData()
{
    BYTE *fileBuf;			// Pointer to our buffered data
    FILE *file = NULL;		// File pointer
    // Get the size of the file in bytes
    long fileSize = getFileSize(file);

    // Allocate space in the buffer for the whole file
    fileBuf = new BYTE[fileSize];

    // Read the file in to the buffer
    fread(fileBuf, fileSize, 1, file);
    int numberOfSecondsInFile = fileSize/304;
    for(int i=0; i< numberOfSecondsInFile ; i++)
    {
        std::vector<frame> buffer=readSensorDataSecond(fileBuf,i*304,m_wimuFrequency);
        m_dataGyro.insert(m_dataGyro.end(), buffer.begin(), buffer.end());
    }
}

void WimuAcquisition::extractMagnetomer()
{
    BYTE *fileBuf;			// Pointer to our buffered data
    FILE *file = NULL;		// File pointer
    // Get the size of the file in bytes
    long fileSize = getFileSize(file);

    // Allocate space in the buffer for the whole file
    fileBuf = new BYTE[fileSize];

    // Read the file in to the buffer
    fread(fileBuf, fileSize, 1, file);
    int numberOfSecondsInFile = fileSize/304;
    for(int i=0; i< numberOfSecondsInFile ; i++)
    {
        std::vector<frame> buffer=readSensorDataSecond(fileBuf,i*304,m_wimuFrequency);
        m_dataMagneto.insert(m_dataMagneto.end(), buffer.begin(), buffer.end());
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
    this->m_filepathAcc = filenameAccelero;
    this->m_filepathGyro = filenameGyro;
    this->m_filepathMagneto = filenameMagneto;
    this->m_wimuFrequency = frequence;

}

 std::vector<frame> WimuAcquisition::readSensorDataSecond(BYTE* fileBuf, int start,int freq)
{
    std::vector<frame> outputFrame;
    long long time=0;
    for (int i = start; i < start+4; i++)
    {
        time+=fileBuf[i]*pow(0x100,i-start);
    }

    time*=1000;
    for (int i = 0; i < freq; i++)
    {
        frame partialFrame;
        partialFrame.timestamp=time+i*(1000/freq);
        partialFrame.x=(fileBuf[start+4+2*i+1]*0x100+fileBuf[start+4+2*i]);
        partialFrame.y=(fileBuf[start+4+2*freq+2*i+1]*0x100+fileBuf[start+4+2*freq+2*i]);
        partialFrame.z=(fileBuf[start+4+4*freq+2*i+1]*0x100+fileBuf[start+4+4*freq+2*i]);
        outputFrame.push_back(partialFrame);
    }
    return outputFrame;
}
std::vector<string_timestamp> WimuAcquisition::getDates() const
{
	std::vector<string_timestamp> result;
    long long lastTimestamp = -1;
    for (int i=0;i<m_dataAccelerometer.size();i++)
    {
        long long t = m_dataAccelerometer.at(i).timestamp/1000;
		int day =t/86400;
		int lastday=lastTimestamp/86400;
		if(lastTimestamp==-1 || day!=lastday)
        {
            string_timestamp s_timestamp;
                        std::time_t _time =(time_t) t;
			char buffer[32];
			// Format: Mo, 15.06.2009 20:20:00
            s_timestamp.timestamp = m_dataAccelerometer.at(i).timestamp;
            std::strftime(buffer, 32, "%F %T", gmtime (&_time));
            s_timestamp.date = buffer;
            result.push_back(s_timestamp);
        }
        lastTimestamp = t;
    }
	return result;
}
int WimuAcquisition::getDataSize()
{
    return m_dataAccelerometer.size();
}
 std::vector<frame> WimuAcquisition::getDataAccelerometer(long long start,long long end) const
{
	std::vector<frame> result;
    for (frame _frame : m_dataAccelerometer)
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
