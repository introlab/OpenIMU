#ifndef IALGO_H
#define IALGO_H

#include <iostream>
#include <vector>
#include "connectors/input.h"
#include "connectors/output.h"
#include "observer.h"

class IAlgo : public Observer
{
public:
    IAlgo();
    ~IAlgo();
    void Notify(std::string inputID);
    template<typename T>
    void AddInput(Input<T> *input);
    template<typename T>
    void AddOutput(Output<T>* output);

protected:
    template<typename T>
    Input<T>* GetInput(std::string inputID);
    template<typename T>
    Output<T>* GetOutput(std::string outputID);


    template<typename T>
    std::vector<Input<T> *> inputs;
    template<typename T>
    std::vector<Output<T> *> outputs;
    virtual void work() = 0;

};

#endif // IALGO_H
