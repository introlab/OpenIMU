#ifndef IALGO_H
#define IALGO_H

#include <iostream>
#include <vector>
#include "inputnode.h"
#include "outputnode.h"
#include "observer.h"

class Block : public Observer
{
public:
    Block();

    //Temp
    Block(std::string blockType);

    ~Block();
    void Notify(std::string inputID);
    void AddInput(InputNode* input);
    void AddOutput(OutputNode* output);
    InputNode* GetInput(std::string inputID);
    OutputNode* GetOutput(std::string inputID);

    std::string GetStringID();
    void SetStringID(const std::string value);

private:

    std::vector<InputNode*> inputs;
    std::vector<OutputNode*> outputs;
    void work();

    std::string stringID;

    //Temp
    std::string blockType;
    int inputSemaphore;

};

#endif // IALGO_H
