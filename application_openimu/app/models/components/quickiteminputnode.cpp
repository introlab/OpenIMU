#include "quickiteminputnode.h"

QuickItemInputNode::QuickItemInputNode(): InputNode()
{
    id = "";
}


void QuickItemInputNode::Put(int value[])
{
    for(int i = 0; i<MAX_ARRAY_SIZE; i++)
    {
        if(i<this->value.count())
            this->value[i] = value[i];
        else
            this->value.append(value[i]);
    }
    emit valueChanged(this->value);
}
