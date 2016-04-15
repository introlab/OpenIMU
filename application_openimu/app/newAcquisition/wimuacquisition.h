#ifndef WIMUACQUISITION_H
#define WIMUACQUISITION_H
#include <vector>
#include <iostream>
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
class WimuAcquisition
{
private:
    std::vector<frame> data;
public:
    WimuAcquisition();
    ~WimuAcquisition();
    WimuAcquisition(std::string file,int freq);
    std::vector<frame>readSensorDataSecond(BYTE* fileBuf, int start,int freq);
    long getFileSize(FILE *file);
    std::vector<frame> getData();
    void setData(std::vector<frame> value);
    std::vector<string_timestamp> getDates();
	int getDataSize();
	std::vector<frame> getData(long long start,long long end);
	static string_timestamp maxTime(std::vector<frame> frames);
	static string_timestamp minTime(std::vector<frame> frames);
};

#endif // WIMUACQUISITION_H
