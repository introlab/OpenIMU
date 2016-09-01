#ifndef INPUTNODE_H
#define INPUTNODE_H

#include "AbstractInputNode.h"

template <class T>
class InputNode: public AbstractInputNode
{
public:
    InputNode():AbstractInputNode() {}
    virtual void Put(std::vector<T> value){
        valueBuf= value;
        Notify();
    }

    std::vector<T> Get(){return valueBuf;}

protected:
    std::vector<T> valueBuf;
};

#endif // INPUTNODE_H
