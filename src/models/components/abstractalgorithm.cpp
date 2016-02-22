#include "abstractalgorithm.h"

AbstractAlgorithm::AbstractAlgorithm()
{

}

AbstractAlgorithm::~AbstractAlgorithm()
{

}

void AbstractAlgorithm::SetStringID(const std::string value)
{
    stringID = value;
}

std::string AbstractAlgorithm::GetStringID()
{
    return stringID;
}


void AbstractAlgorithm::Notify(std::string inputID)
{
    work();
}

void AbstractAlgorithm::AddInput(AbstractInputNode* input)
{
    inputs.push_back(input);
}

void AbstractAlgorithm::AddOutput(AbstractOutputNode* output)
{
    outputs.push_back(output);
}

AbstractInputNode* AbstractAlgorithm::Input(std::string inputID)
{
    for ( std::vector<AbstractInputNode*>::iterator it = inputs.begin() ; it != inputs.end(); ++it)
    {
        if((*it)->GetID() == inputID) return *it;
    }
    return 0; //nullptr
}

AbstractOutputNode* AbstractAlgorithm::Output(std::string outputID)
{
    for ( std::vector<AbstractOutputNode*>::iterator it = outputs.begin() ; it != outputs.end(); ++it)
    {
        if((*it)->GetID() == outputID) return *it;
    }
    return 0; //nullptr
}
