#include "block.h"

Block::Block()
{

}
Block::Block(std::string blockType)
{
    this->blockType = blockType;
}

Block::~Block()
{

}

void Block::SetStringID(const std::string value)
{
    stringID = value;
}

std::string Block::GetStringID()
{
    return stringID;
}


void Block::Notify(std::string inputID)
{
    work();
}

void Block::work()
{
    if(blockType == "add")
    std::cout<<"WORK ADD!\n";

    if(blockType == "sub")
        std::cout<<"WORK SUB!\n";
}

void Block::AddInput(InputNode* input)
{
    inputs.push_back(input);
}

void Block::AddOutput(OutputNode* output)
{
    outputs.push_back(output);
}

InputNode* Block::GetInput(std::string inputID)
{
    for ( std::vector<InputNode*>::iterator it = inputs.begin() ; it != inputs.end(); ++it)
    {
        if((*it)->GetStringID() == inputID) return *it;
    }
    return 0; //nullptr
}

OutputNode* Block::GetOutput(std::string outputID)
{
    for ( std::vector<OutputNode*>::iterator it = outputs.begin() ; it != outputs.end(); ++it)
    {
        if((*it)->GetStringID() == outputID) return *it;
    }
    return 0; //nullptr
}

