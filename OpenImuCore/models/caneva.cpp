#include "caneva.h"

#include <fstream>
#include <iostream>

Caneva::Caneva(std::string filename)
{
    loadFile(filename);

    createBlocks();
}

Caneva::~Caneva()
{
    for(auto it = blocks.begin() ; it != blocks.end() ; it++)
        delete(*it);
}

void Caneva::loadFile(std::string filename)
{
    this->filename = filename;

    std::ifstream file;
    file.open(filename.c_str());
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
    }
}

void Caneva::createBlocks()
{
    for(Json::ValueIterator itr = root["ListBlock"].begin() ; itr != root["ListBlock"].end() ; itr++)
    {
        std::cout<<(*itr)["type"].asString()<<std::endl;

        Block* block = new Block((*itr)["type"].asString());

        blocks.push_back(block);

        block->Notify("");
    }
}

