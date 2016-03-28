#ifndef INPUTNODE_H
#define INPUTNODE_H
#include "observer.h"

#include <iostream>

class InputNode
{
public:
    InputNode(){valueBuf=0;}
    ~InputNode(){}
    void SetObserver(Observer* newObserver){observer = newObserver;}

    int Get();
    void Put(int value);

    void SetStringID(const std::string value);
    std::string GetStringID();

private:
    int valueBuf;
    Observer* observer;
    std::string stringID;

    void Notify();
};

#endif // INPUTNODE_H
