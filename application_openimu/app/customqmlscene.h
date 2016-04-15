#ifndef CUSTOMQMLSCENE_H
#define CUSTOMQMLSCENE_H

#include <QWidget>
#include "models/components/quickiteminputnodeshandles.h"
#include "models/components/quickitemoutputnodes.h"

class CustomQmlScene: public QWidget
{
public:
    CustomQmlScene(std::string filename, QWidget *parent);

    QQuickItem* getInputNode(QString blockId, QString inputId, QQuickItem *p_container = 0);
    template <class T>
    T* getInputNode(QString blockId, QString inputId)
    {
        return (T*)getInputNode(blockId,inputId);
    }

    QQuickItem* getOutputNode(QString blockId, QString inputId);
    template <class T>
    T* getOutputNode(QString blockId, QString inputId)
    {
        return (T*)getOutputNode(blockId,inputId);
    }

private:
    QQuickItem* container;
};

#endif // CUSTOMQMLSCENE_H
