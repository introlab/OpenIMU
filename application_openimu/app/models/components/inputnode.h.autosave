#ifndef INPUTNODE_H
#define INPUTNODE_H
#include "observer.h"

#include <iostream>

#ifndef MAX_ARRAY_SIZE
#define MAX_ARRAY_SIZE 0x08
#endif

class InputNode
{
public:
    InputNode(){
        for(int i=0; i<MAX_ARRAY_SIZE;i++) valueBuf[i] = 0;
        observer=0;
    }

    void SetObserver(Observer* newObserver){observer = newObserver;}

    int *Get();
    virtual void Put(int value[]);

    void SetStringID(const std::string value);
    std::string GetStringID();

protected:
    int valueBuf[MAX_ARRAY_SIZE];
    std::string stringID;

private:
    Observer* observer;

    void Notify();
};

#endif // INPUTNODE_H
