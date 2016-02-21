#ifndef LAYOUTREADER_H
#define LAYOUTREADER_H

#include <json/json.h>
#include <iostream>

class LayoutReader
{
public:
    LayoutReader();

    void loadFile(std::string str);
    void save();
    Json::Value getNextWidget();
    bool hasWidget();

private:
    std::string filename;
    bool fileLoaded;
    Json::Value root;
    Json::Value widgetList;
    Json::ArrayIndex widgetIndex;
};

#endif // LAYOUTREADER_H
