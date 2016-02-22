#ifndef GRAPH_H
#define GRAPH_H

#include <QLabel>
#include "graphobservable.h"
#include "models/components/abstractwidgethandler.h"
#include "models/components/abstractwidgetcontroller.h"

class Graph: public QLabel, public GraphObservable, public AbstractWidgetHandler
{
    Q_OBJECT
public:
    Graph();

signals:

private slots:

};

#endif // GRAPH_H
