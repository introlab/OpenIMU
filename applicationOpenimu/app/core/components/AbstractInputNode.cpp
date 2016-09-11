#include "AbstractInputNode.h"

void AbstractInputNode::Put(std::vector<int> value){
    std::cout<<"WTF5";
    valueBuf= value;
    Notify();
}

std::vector<int> AbstractInputNode::Get(){
    return valueBuf;
}

void AbstractInputNode::SetStringID(std::string value)
{
    stringID = value;
}

std::string AbstractInputNode::GetStringID()
{
    return stringID;
}

void AbstractInputNode::Notify()
{
    if(observer)
       observer->Notify(stringID);
}
