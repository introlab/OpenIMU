#include "inputnode.h"

void InputNode::Put(int value){
    valueBuf = value;
    Notify();
}

int InputNode::Get(){
    return valueBuf;
}

void InputNode::SetStringID(const std::string value)
{
    stringID = value;
}

std::string InputNode::GetStringID()
{
    return stringID;
}

void InputNode::Notify()
{
    //@TODO REMOVE this line is ugly!!!
    if(observer)
    observer->Notify(stringID);
}
