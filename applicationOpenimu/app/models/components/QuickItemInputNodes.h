#ifndef QUICKITEMINPUTNODES_H
#define QUICKITEMINPUTNODES_H

#include "InputNode.h"
#include "QuickItemInputNodesHandles.h"

class QuickItemInputNodeInt: public InputNode<int>
{
public:
    QuickItemInputNodeInt(QuickItemInputNodeIntHandle* h){
        handle = h;
    }

    void Put(std::vector<int> value){
        handle->Put(value);
    }

private:
    QuickItemInputNodeIntHandle* handle;

};

class QuickItemInputNodeDouble: public InputNode<double>
{
public:
    QuickItemInputNodeDouble(QuickItemInputNodeDoubleHandle* h){
        handle = h;
    }

    void Put(std::vector<double> value){
        handle->Put(value);
    }

private:
    QuickItemInputNodeDoubleHandle* handle;

};

class QuickItemInputNodeString: public InputNode<std::string>
{
public:
    QuickItemInputNodeString(QuickItemInputNodeStringHandle* h){
        handle = h;
    }

    void Put(std::vector<std::string> value){
         handle->Put(value);
    }

private:
    QuickItemInputNodeStringHandle* handle;

};

#endif // QUICKITEMINPUTNODES_H
