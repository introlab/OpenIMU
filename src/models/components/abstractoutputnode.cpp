#include "abstractoutputnode.h"

AbstractOutputNode::AbstractOutputNode()
{

}

void AbstractOutputNode::SetStringID(const std::string value)
{
    stringID = value;
}

std::string AbstractOutputNode::GetStringID()
{
    return stringID;
}
