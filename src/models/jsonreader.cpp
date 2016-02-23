#include "jsonreader.h"
#include <json/json.h>
#include <iostream>
#include <fstream>

JsonReader::JsonReader()
{
    filename = "";
    fileLoaded = false;
}

void JsonReader::loadFile(std::string str)
{
    filename = str;
    Json::Reader reader;

    std::ifstream file;
    file.open(str.c_str());
    std::string fileContent;
    std::string buf;

    if(file.is_open())
        while(file >> buf)
            fileContent.append(buf);


    bool parsingSuccessful = reader.parse(fileContent, root);
    if ( !parsingSuccessful )
    {
        // report to the user the failure and their locations in the document.
        std::string error = reader.getFormattedErrorMessages();
        std::cout  << "Failed to parse configuration\n"
                   << error;
        return;
    }
    fileLoaded = true;
}

std::string JsonReader::getDisplayName()
{
    return root["DisplayName"].asString();
}

void JsonReader::save()
{

}

Json::Value JsonReader::getNextWidget()
{
    // Get the value of the member of root named 'layout', return a 'null' value if
    // there is no such member.
    if (fileLoaded == false) return 0;

    if (widgetList.isNull())
    {
        widgetList = root["widgets"];
        widgetIndex = 0;
        if(widgetList.size() == 0)return widgetList[0];
    }
    int index = widgetIndex<widgetList.size()?widgetIndex++:widgetIndex++-1;
    return widgetList[index];
}

bool JsonReader::hasWidget()
{
    int listSize = widgetList.size();
    return widgetIndex <= listSize;
}

Json::Value JsonReader::getNextAlgo(){
    return 0;
}
bool JsonReader::hasAlgo(){
    return 0;
}

Json::Value JsonReader::getNextInput(){
    return 0;
}
bool JsonReader::hasInput(){
    return 0;
}

Json::Value JsonReader::getNextOutput(){
    return 0;
}
bool JsonReader::hasOutput(){
    return 0;
}
