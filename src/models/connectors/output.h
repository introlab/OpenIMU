#ifndef OUTPUT_H
#define OUTPUT_H

#include "models/connectors/input.h"
#include <vector>

template <class T>
class Output: public IConnector
{
private:
    T valueBuf;
    std::vector<Input<T> * > inputs;
    void Notify();

public:
    Output();
    ~Output();
    void Send(T value);
    void AddDest(Input<T> *input);
};

#endif // OUTPUT_H
