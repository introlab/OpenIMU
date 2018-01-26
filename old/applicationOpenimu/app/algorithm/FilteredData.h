#ifndef FILTEREDDATA_H
#define FILTEREDDATA_H

#include <vector>
#include <iostream>
#include "../acquisition/IJsonSerializable.h"
#include "../acquisition/WimuAcquisition.h"
#include "../core/json/json/json.h"

using namespace std;

// Object mapping frequency filter json

class FilteredData : public IJsonSerializable
{
public:

    FilteredData();
    ~FilteredData();
    virtual void Serialize( Json::Value& root, RecordInfo recordInfo, std::string& output);
    virtual void Deserialize( Json::Value& root);

    string m_recordId;
    string m_runtime;
    int m_cutoff;
    int m_transition;
    string m_uuid;
    string m_filename;
    std::vector<frame> m_dataAccelerometer;
};

#endif // FILTEREDDATA_H
