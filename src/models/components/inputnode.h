#ifndef INPUTNODE_H
#define INPUTNODE_H
#include "abstractinputnode.h"
#include "observer.h"

#include <iostream>

template <class T>
class InputNode: public AbstractInputNode
{
public:
    InputNode(){isActive = true;}
    ~InputNode(){}

    //Override
    void Put(T value){
        valueBuf = value;
        if(isActive) Notify();
    }

    //Override
    T* Get(){
        return &valueBuf;
    }

private:
    T valueBuf;
};

#endif // INPUTNODE_H
