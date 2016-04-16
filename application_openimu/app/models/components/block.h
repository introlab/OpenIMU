#ifndef BLOCK_H
#define BLOCK_H

#include <iostream>
#include <vector>
#include "abstractinputnode.h"
#include "abstractoutputnode.h"
#include "inputnode.h"
#include "outputnode.h"
#include "observer.h"
#include <iostream>

class Block : public Observer
{
public:
    Block();

    ~Block();
    virtual void Notify(std::string inputID);
    void AddInput(AbstractInputNode* input);
    void AddOutput(AbstractOutputNode* output);

    AbstractInputNode* GetInput(std::string inputID){
        for ( std::vector<AbstractInputNode*>::iterator it = inputs.begin() ; it != inputs.end(); ++it)
        {
            if(inputID == (*it)->GetStringID()) return *it;
        }
        return 0; //nullptr
    }
    //To cast it in the right child
    template <class T>
    InputNode<T>* GetInput(std::string inputID){
        return (InputNode<T>*)GetInput(inputID);
    }

    AbstractOutputNode* GetOutput(std::string outputID){
        for ( std::vector<AbstractOutputNode*>::iterator it = outputs.begin() ; it != outputs.end(); ++it)
        {
            if((*it)->GetStringID() == outputID) return *it;
        }
        return 0; //nullptr
    }
    //To cast it in the right child
    template <class T>
    OutputNode<T>*GetOutput(std::string outputID){
        return (OutputNode<T>*)GetOutput(outputID);
    }

    std::string GetStringID();
    void SetStringID(const std::string value);


private:
    std::string stringID;

    //Temp
    std::string blockType;
    int inputSemaphore;

protected:
    virtual void work();
    std::vector<AbstractInputNode*> inputs;
    std::vector<AbstractOutputNode*> outputs;

};

#endif // BLOCK_H
