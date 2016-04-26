#ifndef OUTPUTNODE_H
#define OUTPUTNODE_H

#include "abstractoutputnode.h"
#include "inputnode.h"

template <class T>
class OutputNode: public AbstractOutputNode
{
public:
    OutputNode(): AbstractOutputNode() {}
    void Send(std::vector<T> value){
        valueBuf = value;
        NotifyAll();
    }
    std::vector<T> getValueBuf() const {return valueBuf;}
    void setValueBuf(std::vector<T> value) {valueBuf = value;}

    void NotifyAll(){
        for (typename std::vector<AbstractInputNode*>::iterator it = inputs.begin() ; it != inputs.end(); ++it)
        {
            ((InputNode<T>*)(*it))->Put(valueBuf);
        }
    }

protected:
    std::vector<T> valueBuf;
};

#endif // OUTPUTNODE_H
