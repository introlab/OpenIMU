#include "outputnode.h"

OutputNode::OutputNode()
{

}

OutputNode::~OutputNode()
{

}

void OutputNode::Send(int value)
{
    valueBuf = value;
    NotifyAll();
}

void OutputNode::AddDest(InputNode* input)
{
    inputs.push_back(input);
}

void OutputNode::NotifyAll()
{
    for (typename std::vector<InputNode*>::iterator it = inputs.begin() ; it != inputs.end(); ++it)
    {
        (*it)->Put(valueBuf);
    }
}

void OutputNode::SetStringID(const std::string value)
{
    stringID = value;
}

std::string OutputNode::GetStringID()
{
    return stringID;
}
