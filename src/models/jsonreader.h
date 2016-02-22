#ifndef LAYOUTREADER_H
#define LAYOUTREADER_H

#include <json/json.h>
#include <iostream>

class JsonReader
{
public:
    JsonReader();

    void loadFile(std::string str);
    void save();

    Json::Value getNextWidget();
    bool hasWidget();
    Json::Value getNextAlgo();
    bool hasAlgo();
    Json::Value getNextInput();
    bool hasInput();
    Json::Value getNextOutput();
    bool hasOutput();

private:
    std::string filename;
    bool fileLoaded;
    Json::Value root;
    Json::Value widgetList;
    Json::ArrayIndex widgetIndex;
};

#endif // LAYOUTREADER_H
