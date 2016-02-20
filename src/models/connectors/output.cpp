#include "output.h"

template<class T>
Output<T>::Output()
{

}

template <class T>
Output<T>::~Output()
{

}

template<class T>
void Output<T>::Send(T value)
{
    valueBuf = value;
    Notify();
}

template<class T>
void Output<T>::AddDest(Input<T>* input)
{
    inputs.push_back(input);
}

template<class T>
void Output<T>::Notify()
{
    for (typename std::vector<Input<T>*>::iterator it = inputs.begin() ; it != inputs.end(); ++it)
    {
        (*it)->Put(valueBuf);
    }
}

