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
