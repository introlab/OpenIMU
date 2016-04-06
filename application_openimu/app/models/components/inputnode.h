#ifndef INPUTNODE_H
#define INPUTNODE_H
#include "observer.h"

#include <iostream>

class InputNode
{
public:
    InputNode(){valueBuf=0;observer=0;}

    void SetObserver(Observer* newObserver){observer = newObserver;}

    int Get();
    virtual void Put(int value);

    void SetStringID(const std::string value);
    std::string GetStringID();

protected:
    int valueBuf;
    std::string stringID;

private:
    Observer* observer;

    void Notify();
};

#endif // INPUTNODE_H
