#include "quickiteminputnode.h"

QuickItemInputNode::QuickItemInputNode(): InputNode()
{
    id = "";
}


void QuickItemInputNode::Put(std::vector<int> value)
{
    this->value = QList<int>::fromVector(QVector<int>::fromStdVector(value));
    emit valueChanged(this->value);
}
