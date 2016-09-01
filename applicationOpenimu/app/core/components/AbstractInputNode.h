#ifndef ABSTRACTINPUTNODE_H
#define ABSTRACTINPUTNODE_H
#include "Observer.h"

#include <iostream>
#include <vector>

class AbstractInputNode
{
public:
    AbstractInputNode(){
        observer=0;
        stringID = "";
    }

    void SetObserver(Observer* newObserver){
        observer = newObserver;
    }

    std::vector<int> Get();
    virtual void Put(std::vector<int> value);

    void SetStringID(std::string value);
    std::string GetStringID();

protected:
    std::string stringID;
    std::vector<int> valueBuf;

    void Notify();

private:
    Observer* observer;

};

#endif // ABSTRACTINPUTNODE_H
