#ifndef WIMUACQUISITION_H
#define WIMUACQUISITION_H

#include <vector>
#include <iostream>
#include"IJsonSerializable.h"
#include"../core/json/json/json.h"

typedef unsigned char BYTE;


struct frame {
  signed short int x;
  signed short int y;
  signed short int z;
  long long timestamp; //in ms
};
struct string_timestamp{
	long long timestamp;
	std::string date;
};

class WimuAcquisition: public IJsonSerializable
{
private:
    std::vector<frame> data;
    std::vector<frame> dataGyro;
    std::vector<frame> dataMagneto;

public:
    WimuAcquisition();
    ~WimuAcquisition();
    virtual void Serialize( Json::Value& root, RecordInfo record,  std::string date,std::string& output );
    virtual void Deserialize( Json::Value& root);

    void initialize();
    void clearData();
    void extractAcceleroData();
    void extractGyrometerData();
    void extractMagnetomer();

    WimuAcquisition(std::string filenameAccelero, std::string filenameGyro,std::string filenameMagneto, int frequence);
    std::vector<frame>readSensorDataSecond(BYTE* fileBuf, int start,int freq);
    long getFileSize(FILE *file);
    void setData(std::vector<frame> value);
	int getDataSize();
    std::vector<frame> getData()const;
    std::vector<string_timestamp> getDates()const;
    std::vector<frame> getData(long long start,long long end)const;
	static string_timestamp maxTime(std::vector<frame> frames);
	static string_timestamp minTime(std::vector<frame> frames);

    std::string fileAcc;
    std::string fileGyro;
    std::string fileMagneto;
    int freq;
};

#endif // WIMUACQUISITION_H
