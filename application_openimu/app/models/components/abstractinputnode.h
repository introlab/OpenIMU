#ifndef ABSTRACTINPUTNODE_H
#define ABSTRACTINPUTNODE_H
#include "observer.h"

#include <iostream>
#include <vector>

class AbstractInputNode
{
public:
    AbstractInputNode(){
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
    void Notify();

private:
    Observer* observer;

};

#endif // ABSTRACTINPUTNODE_H
