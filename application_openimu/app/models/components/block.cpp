#include "block.h"

Block::Block()
{
    inputSemaphore = 0;
}

Block::~Block()
{
    for(auto it = inputs.begin() ; it != inputs.end() ; it++)
        delete(*it);
    for(auto it = outputs.begin() ; it != outputs.end() ; it++)
        delete(*it);
}

void Block::SetStringID(const std::string value)
{
    stringID = value;
}

std::string Block::GetStringID()
{
    return stringID;
}


void Block::Notify(std::string* inputID)
{
    std::cout<<"WTF3";
    inputSemaphore--;
    if(inputSemaphore == 0){
        work();
        inputSemaphore = inputs.size();
    }
}

void Block::work()
{

}

void Block::AddInput(AbstractInputNode* input)
{
    if(!input) return;
    input->SetObserver(this);
    inputs.push_back(input);
    inputSemaphore++;
}

void Block::AddOutput(AbstractOutputNode* output)
{
    if(!output) return;
    outputs.push_back(output);
}
/*
AbstractInputNode* Block::GetInput(std::string inputID)
{
    for ( std::vector<AbstractInputNode*>::iterator it = inputs.begin() ; it != inputs.end(); ++it)
    {
        if((*it)->GetStringID() == inputID) return *it;
    }
    return 0; //nullptr
}

AbstractOutputNode* Block::GetOutput(std::string outputID)
{
    for ( std::vector<AbstractOutputNode*>::iterator it = outputs.begin() ; it != outputs.end(); ++it)
    {
        if((*it)->GetStringID() == outputID) return *it;
    }
    return 0; //nullptr
}*/

