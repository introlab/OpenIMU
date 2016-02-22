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

template<class T>
OutputNode<T>::OutputNode()
{

}

template <class T>
OutputNode<T>::~OutputNode()
{

}

template<class T>
void OutputNode<T>::Send(T value)
{
    valueBuf = value;
    NotifyAll();
}

template<class T>
void OutputNode<T>::AddDest(InputNode<T>* input)
{
    inputs.push_back(input);
}

template<class T>
void OutputNode<T>::NotifyAll()
{
    for (typename std::vector<InputNode<T>*>::iterator it = inputs.begin() ; it != inputs.end(); ++it)
    {
        (*it)->Put(valueBuf);
    }
}

#endif // OUTPUT_H
