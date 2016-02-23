#ifndef GRAPH_H
#define GRAPH_H

#include <qwt_plot.h>
#include <qwt_plot_curve.h>

#include <list>

#include "graphobservable.h"
#include "models/components/abstractwidgethandler.h"
#include "models/components/abstractwidgetcontroller.h"

class Graph: public QwtPlot, public GraphObservable, public AbstractWidgetHandler
{
    Q_OBJECT
public:    
    Graph();

    void setData(double x[], double y[], int length);


signals:

private slots:

private:
    QwtPlotCurve* curve1;
};

#endif // GRAPH_H
