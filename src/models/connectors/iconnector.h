#ifndef ICONNECTOR_H
#define ICONNECTOR_H


class IConnector
{
public:
    IConnector();
    ~IConnector();
    virtual void Notify() = 0;
    virtual void GetID() = 0;
};

#endif // ICONNECTOR_H
