#include "graph.h"


Graph::Graph():QwtPlot()
{
    this->curve1 = new QwtPlotCurve();
    this->curve1->attach(this);

    double x[] = {1,2,3,4,5,6,7,8,9};
    double y[] = {9,8,7,6,5,4,3,2,1};

    this->setData(x,y,9);
}

void Graph::setData(double x[], double y[], int length)
{
    this->curve1->setSamples(x,y,length);
    this->replot();
}


