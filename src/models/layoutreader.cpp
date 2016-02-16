#include "layoutreader.h"
#include <json/json.h>
#include <iostream>
#include <fstream>

LayoutReader::LayoutReader()
{
    filename = "";
    fileLoaded = false;
}

void LayoutReader::loadFile(std::string str)
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

void LayoutReader::save()
{

}

Json::Value LayoutReader::getNextWidget()
{
    // Get the value of the member of root named 'layout', return a 'null' value if
    // there is no such member.
    if (fileLoaded == false) return 0;

    if (widgetList.isNull())
    {
        widgetList = root["layout"];
        widgetIndex = 0;
    }
    int index = widgetIndex<widgetList.size()?widgetIndex++:widgetIndex++-1;
    return widgetList[index];
}

bool LayoutReader::hasWidget()
{
    int listSize = widgetList.size();
    return widgetIndex <= listSize;
}
