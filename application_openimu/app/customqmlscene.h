#ifndef CUSTOMQMLSCENE_H
#define CUSTOMQMLSCENE_H

#include <QWidget>
#include "models/components/quickiteminputnodes.h"
#include "models/components/quickitemoutputnodes.h"

class CustomQmlScene: public QWidget
{
public:
    CustomQmlScene(std::string filename, QWidget *parent);

    AbstractInputNode* getInputNode(QString blockId, QString inputId);
    template <class T>
    InputNode<T>* getInputNode(QString blockId, QString inputId)
    {
        return (InputNode<T>*)getInputNode(blockId,inputId);
    }

    AbstractOutputNode* getOutputNode(QString blockId, QString inputId);
    template <class T>
    OutputNode<T>* getOutputNode(QString blockId, QString inputId)
    {
        return (OutputNode<T>*)getOutputNode(blockId,inputId);
    }

private:
    QQuickItem* container;
};

#endif // CUSTOMQMLSCENE_H
