#ifndef OUTPUT_H
#define OUTPUT_H

#include "inputnode.h"
#include "abstractoutputnode.h"
#include <vector>

template <class T>
class OutputNode: public AbstractOutputNode
{
public:
    OutputNode();
    ~OutputNode();
    void Send(T value);
    void AddDest(InputNode<T> *input);

private:
    T valueBuf;
    std::vector<InputNode<T> * > inputs;
    void NotifyAll();
};

#endif // OUTPUT_H
