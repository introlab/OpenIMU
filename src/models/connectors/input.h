#ifndef IFILTER_H
#define IFILTER_H
#include "models/connectors/iconnector.h"
#include "models/observer.h"

#include <iostream>

template <class T>
class Input: public IConnector
{
public:
    Input(Observer* newObserver);
    ~Input();
    void Put(T value);
    void SetActive(bool active);

    std::string getStringID() const;
    void setStringID(const std::string &value);

private:
    T valueBuf;
    Observer* observer;
    bool isActive;
    std::string stringID;

    void Notify();
};

#endif // IFILTER_H
