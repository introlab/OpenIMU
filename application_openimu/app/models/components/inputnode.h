#ifndef INPUTNODE_H
#define INPUTNODE_H
#include "observer.h"

#include <iostream>
#include <vector>

class InputNode
{
public:
    InputNode(){
        observer=0;
    }

    void SetObserver(Observer* newObserver){observer = newObserver;}

    std::vector<int> Get();
    virtual void Put(std::vector<int> value);

    void SetStringID(const std::string value);
    std::string GetStringID();

protected:
    std::vector<int> valueBuf;
    std::string stringID;

private:
    Observer* observer;

    void Notify();
};

#endif // INPUTNODE_H
