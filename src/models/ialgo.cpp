#include "ialgo.h"

IAlgo::IAlgo()
{
    std::cout<<"asd";
}

IAlgo::~IAlgo()
{

}

void IAlgo::Notify(std::string inputID)
{
    work();
}

void IAlgo::AddInput(Input* input)
{
    inputs.push_back(input);
}

void IAlgo::AddOutput(Output* output)
{
    outputs.push_back(output);
}

IConnector* IAlgo::Input(std::string inputID)
{
    for (typename std::vector<Input*>::iterator it = inputs.begin() ; it != inputs.end(); ++it)
    {
        /*if(*it.GetID() == inputID)*/ return *it;
    }
}

IConnector* IAlgo::Output(std::string outputID)
{
    for (typename std::vector<Output*>::iterator it = outputs.begin() ; it != outputs.end(); ++it)
    {
        if((*it)->GetID() == outputID) return *it;
    }
}
