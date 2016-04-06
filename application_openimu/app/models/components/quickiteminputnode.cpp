#include "quickiteminputnode.h"

QuickItemInputNode::QuickItemInputNode(): InputNode()
{
    id = "";
    valueBuf = 0;
}


void QuickItemInputNode::Put(int value)
{
    valueBuf = value;
    emit valueBufChanged(valueBuf);
}
