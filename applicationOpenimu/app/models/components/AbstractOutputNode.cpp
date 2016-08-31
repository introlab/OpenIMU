#include "AbstractOutputNode.h"

AbstractOutputNode::AbstractOutputNode()
{

}

void AbstractOutputNode::Send(std::vector<int> value)
{
    valueBuf = value;
    NotifyAll();
}

void AbstractOutputNode::AddDest(AbstractInputNode* input)
{
    inputs.push_back(input);
}

void AbstractOutputNode::SetStringID(const std::string value)
{
    stringID = value;
}

std::string AbstractOutputNode::GetStringID()
{
    return stringID;
}

std::vector<int> AbstractOutputNode::getValueBuf() const
{
    return valueBuf;
}

void AbstractOutputNode::setValueBuf(std::vector<int> value)
{
    valueBuf = value;
}
