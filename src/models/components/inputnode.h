#ifndef INPUTNODE_H
#define INPUTNODE_H
#include "abstractinputnode.h"
#include "observer.h"

#include <iostream>

template <class T>
class InputNode: public AbstractInputNode
{
public:
    InputNode();
    ~InputNode();

    //Override
    void Put(T value);
    T Get();

    void SetActive(bool active);
    void SetStringID(std::string value);
    std::string GetStringID();

private:
    Observer* observer;
    T valueBuf;

    bool isActive;
    std::string stringID;

    void Notify();
};

#endif // INPUTNODE_H
