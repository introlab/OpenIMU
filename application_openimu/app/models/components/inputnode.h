#ifndef INPUTNODEINT_H
#define INPUTNODEINT_H

#include "abstractinputnode.h"

template <class T>
class InputNode: public AbstractInputNode
{
public:
    InputNode():AbstractInputNode() {}
    virtual void Put(std::vector<T> value){std::cout<<"WTF4";
        valueBuf= value;
        Notify();
    }
    std::vector<int> Get(){return valueBuf;}

protected:
    std::vector<T> valueBuf;
};

#endif // INPUTNODEINT_H
