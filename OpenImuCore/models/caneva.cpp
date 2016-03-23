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
    for(Json::ValueIterator it = root["ListBlock"].begin() ; it != root["ListBlock"].end() ; it++)
    {
        std::cout<<"Block: "<<(*it)["type"].asString()<<std::endl;

        Block* block = new Block((*it)["type"].asString());
        block->SetStringID((*it)["ID"].asString());

        createInputs(block,(*it)["inputs"]);
        createOutputs(block,(*it)["outputs"]);

        blocks.push_back(block);

        block->Notify("");
    }
}

void Caneva::createInputs(Block* block, Json::Value inputs)
{
    std::cout<<"Inputs: ";
    for(Json::ValueIterator it = inputs.begin() ; it != inputs.end() ; it++)
    {
        InputNode* input = new InputNode();
        input->SetStringID((*it)["ID"].asString());
        block->AddInput(input);
        std::cout<<(*it)["ID"].asString()<<", ";
    }
    std::cout<<std::endl;
}

void Caneva::createOutputs(Block *block, Json::Value outputs)
{
    std::cout<<"Outputs: ";
    for(Json::ValueIterator it = outputs.begin() ; it != outputs.end() ; it++)
    {
        OutputNode* output = new OutputNode();
        output->SetStringID((*it)["ID"].asString());
        block->AddOutput(output);
        std::cout<<(*it)["ID"].asString()<<", ";
    }
    std::cout<<std::endl;
}
