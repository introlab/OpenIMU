#ifndef OUTPUTNODE_H
#define OUTPUTNODE_H

#include "abstractoutputnode.h"

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


protected:
    std::vector<T> valueBuf;
};

#endif // OUTPUTNODE_H
