#include "abstractinputnode.h"

void AbstractInputNode::Put(std::vector<int> value){
    std::cout<<"WTF5";
    valueBuf= value;
    Notify();
}

std::vector<int> AbstractInputNode::Get(){
    return valueBuf;
}

void AbstractInputNode::SetStringID(std::string* value)
{
    std::cout<<"ptr value before: "<<stringID<<std::endl;
    delete stringID;
    stringID = value;
    std::cout<<"ptr value after: "<<stringID<<std::endl;

}

std::string* AbstractInputNode::GetStringID()
{
    //return stringID;
    return (std::string*)(*((void**)((void*)this+0x14)));
}

void AbstractInputNode::Notify()
{
    //@TODO REMOVE this line is ugly!!!
    if(observer)
    observer->Notify(stringID);
}
