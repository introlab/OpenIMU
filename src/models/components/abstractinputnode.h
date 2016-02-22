#ifndef ABSTRACTINPUTNODE_H
#define ABSTRACTINPUTNODE_H

#include "observer.h"

class AbstractInputNode
{
public:
    AbstractInputNode();
    virtual void* Get() = 0;
    virtual void SetObserver(Observer* newObserver){observer = newObserver;}
    virtual std::string GetID(){return "";}

    void SetStringID(const std::string value);
    std::string GetStringID();
    void SetActive(bool active);
protected:
    Observer* observer;
    std::string stringID;

    bool isActive;
    void Notify();
};

#endif // ABSTRACTINPUTNODE_H
