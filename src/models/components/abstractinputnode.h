#ifndef ABSTRACTINPUTNODE_H
#define ABSTRACTINPUTNODE_H

#include "observer.h"

class AbstractInputNode
{
public:
    AbstractInputNode();
    virtual void Put(void* data) = 0;
    virtual void* Get() = 0;
    virtual void SetObserver(Observer* newObserver){observer = newObserver;}
    virtual std::string GetID(){return "";}

protected:
    Observer* observer;
};

#endif // ABSTRACTINPUTNODE_H
