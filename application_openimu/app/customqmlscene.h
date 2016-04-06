#ifndef CUSTOMQMLSCENE_H
#define CUSTOMQMLSCENE_H

#include <QWidget>
#include "models/components/quickiteminputnode.h"
#include "models/components/quickitemoutputnode.h"

class CustomQmlScene: public QWidget
{
public:
    CustomQmlScene(std::string filename, QWidget *parent);
    QuickItemInputNode* getInputNode(QString blockId, QString inputId);
    QuickItemOutputNode* getOutputNode(QString blockId, QString inputId);

private:
    QQuickItem* container;
};

#endif // CUSTOMQMLSCENE_H
