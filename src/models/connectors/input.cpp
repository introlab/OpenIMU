#include "input.h"

template <class T>
Input<T>::Input(Observer *newObserver)
{
    observer = newObserver;
    isActive = true;
}

template <class T>
Input<T>::~Input()
{

}

template <class T>
void Input<T>::Put(T value)
{
    valueBuf = value;
    if(isActive) Notify();
}

template <class T>
void Input<T>::SetActive(bool active)
{
    isActive = active;
}

template <class T>
std::string Input<T>::getStringID() const
{
    return stringID;
}

template <class T>
void Input<T>::setStringID(const std::string &value)
{
    stringID = value;
}

template <class T>
void Input<T>::Notify()
{
    observer->Notify(stringID);
}

