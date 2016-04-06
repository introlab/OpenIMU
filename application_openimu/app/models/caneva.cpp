#include "caneva.h"

#include <fstream>
#include <iostream>
#include "components/blockType/blockFactory.h"

Caneva::Caneva(std::string filename, CustomQmlScene *scene)
{
    loadFile(filename);

    createBlocks();
    createVBlocks(scene);

    makeConnections();
}

Caneva::~Caneva()
{
    for(auto it = blocks.begin() ; it != blocks.end() ; it++)
        delete(*it);
}

void Caneva::test()
{
    //testing
    int asd[] =  {10,20,11,-2,0,-20,-10,-20};
    getBlock("adder")->GetInput("input1")->Put(asd);
    getBlock("adder")->GetInput("input2")->Put(asd);
    getBlock("subber")->GetInput("input2")->Put(asd);

    setSliderLimitValues(0,10);
}

void Caneva::setSliderLimitValues(int min, int max){
    int a[] = {min};
    int b[] = {max};
    getBlock("slider")->GetInput("inputSliderMinimumValue")->Put(a);
    getBlock("slider")->GetInput("inputSliderMaximumValue")->Put(b);
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
    BlockFactory* blockFactory = new BlockFactory();
    for(Json::ValueIterator it = root["ListBlock"].begin() ; it != root["ListBlock"].end() ; it++)
    {
        Block* block = new Block();
        block = blockFactory->createBlockType((*it)["type"].asString());
        block->SetStringID((*it)["ID"].asString());

        createInputs(block,(*it)["inputs"]);
        createOutputs(block,(*it)["outputs"]);

        blocks.push_back(block);
    }
}

void Caneva::createVBlocks(CustomQmlScene *scene)
{
    for(Json::ValueIterator it = root["ListVBlock"].begin() ; it != root["ListVBlock"].end() ; it++)
    {
        Block* block = new Block();
        block->SetStringID((*it)["ID"].asString());

        // get inputs
        for(Json::ValueIterator in = (*it)["inputs"].begin() ; in != (*it)["inputs"].end() ; in++)
        {
            block->AddInput(scene->getInputNode((*it)["ID"].asString().c_str(),(*in)["ID"].asString().c_str()));
        }

        // get outputs
        for(Json::ValueIterator out = (*it)["outputs"].begin() ; out != (*it)["outputs"].end() ; out++)
        {
            block->AddOutput(scene->getOutputNode((*it)["ID"].asString().c_str(),(*out)["ID"].asString().c_str()));
        }

        blocks.push_back(block);
    }
}

void Caneva::createInputs(Block* block, Json::Value inputs)
{
    for(Json::ValueIterator it = inputs.begin() ; it != inputs.end() ; it++)
    {
        InputNode* input = new InputNode();
        input->SetStringID((*it)["ID"].asString());
        block->AddInput(input);
    }
}

void Caneva::createOutputs(Block *block, Json::Value outputs)
{
    for(Json::ValueIterator it = outputs.begin() ; it != outputs.end() ; it++)
    {
        OutputNode* output = new OutputNode();
        output->SetStringID((*it)["ID"].asString());
        block->AddOutput(output);
    }
}

void Caneva::makeConnections()
{
    for(Json::ValueIterator it = root["ListConnection"].begin() ; it != root["ListConnection"].end() ; it++)
    {
        //getBlock((*it)["from"].asString())->GetOutput((*it)["out"].asString())->AddDest(getBlock((*it)["to"].asString())->GetInput((*it)["in"].asString()));
        Block* from = getBlock((*it)["from"].asString());
        if(!from) return;
        OutputNode* out = from->GetOutput((*it)["out"].asString());
        if(!out) return;
        Block* to = getBlock((*it)["to"].asString());
        if(!to) return;
        InputNode* in = to->GetInput((*it)["in"].asString());
        if(!in) return;
        out->AddDest(in);
    }
}

Block *Caneva::getBlock(std::string ID)
{
    for ( auto it = blocks.begin() ; it != blocks.end(); ++it)
    {
        if((*it)->GetStringID() == ID) return *it;
    }
    return 0; //nullptr
}
