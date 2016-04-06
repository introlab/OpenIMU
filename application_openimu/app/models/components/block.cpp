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


void Block::Notify(std::string inputID)
{
    inputSemaphore--;
    if(inputSemaphore == 0){
        work();
        inputSemaphore = inputs.size();
    }
}

void Block::work()
{

}

void Block::AddInput(InputNode* input)
{
    if(!input) return;
    inputs.push_back(input);
    input->SetObserver(this);
    inputSemaphore++;
}

void Block::AddOutput(OutputNode* output)
{
    if(!output) return;
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

