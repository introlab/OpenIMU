#include "abstractinputnode.h"

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
    //@TODO REMOVE this line is ugly!!!
    if(observer)
    observer->Notify(stringID);
}
