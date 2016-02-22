#include "abstractinputnode.h"

AbstractInputNode::AbstractInputNode()
{

}

void AbstractInputNode::SetStringID(const std::string value)
{
    stringID = value;
}

std::string AbstractInputNode::GetStringID()
{
    return stringID;
}

void AbstractInputNode::SetActive(bool active)
{
    isActive = active;
}

void AbstractInputNode::Notify()
{
    observer->Notify(stringID);
}
