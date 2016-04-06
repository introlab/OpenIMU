#include "outputnode.h"

OutputNode::OutputNode()
{

}

void OutputNode::Send(int value[])
{
    for(int i = 0; i<MAX_ARRAY_SIZE; i++) valueBuf[i] = value[i];
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

int *OutputNode::getValueBuf() const
{
    return (int *)valueBuf;
}

void OutputNode::setValueBuf(int value[])
{
    for(int i = 0; i<MAX_ARRAY_SIZE; i++) valueBuf[i] = value[i];
}
