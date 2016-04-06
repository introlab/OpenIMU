#ifndef OUTPUT_H
#define OUTPUT_H

#include "inputnode.h"
#include <vector>

class OutputNode
{
public:
    OutputNode();
    ~OutputNode();
    void Send(int value);
    void AddDest(InputNode *input);
    virtual std::string GetID(){return "";}
    void SetStringID(const std::string value);
    std::string GetStringID();
    int getValueBuf() const;
    void setValueBuf(int value);
	
protected:
    int valueBuf;

private:
    void NotifyAll();
    std::vector<InputNode*> inputs;
    std::string stringID;
};

#endif // OUTPUT_H
