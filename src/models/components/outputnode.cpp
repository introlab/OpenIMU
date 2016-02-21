#include "outputnode.h"

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

