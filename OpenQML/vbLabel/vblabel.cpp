#include "vblabel.h"
#include <QSGSimpleRectNode>

VBLabel::VBLabel()
{
    // By default, QQuickItem does not draw anything. If you subclass
    // QQuickItem to create a visual item, you will need to uncomment the
    // following line and re-implement updatePaintNode()

    setFlag(ItemHasContents, true);
}

VBLabel::~VBLabel()
{
}

QSGNode *VBLabel::updatePaintNode(QSGNode *oldNode, QQuickItem::UpdatePaintNodeData *)
{
    auto node = static_cast<QSGSimpleRectNode*>(oldNode);
    if(!node)
        node =  new QSGSimpleRectNode(boundingRect(), Qt::green);
    node->setRect(boundingRect());
    return node;
}
