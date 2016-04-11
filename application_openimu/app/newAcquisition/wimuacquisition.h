#ifndef WIMUACQUISITION_H
#define WIMUACQUISITION_H
#include <vector>
#include <iostream>
typedef unsigned char BYTE;

struct frame {
  int x;
  int y;
  int z;
  int timestamp; //en ms
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
};

#endif // WIMUACQUISITION_H
