#include "graph.h"


Graph::Graph():QwtPlot()
{
    this->curve1 = new QwtPlotCurve();
    this->curve1->attach(this);

    double x[] = {1,2,3,4,5,6,7,8,9,10};
    double y[] = {0.8,0.4,-0.9,0.1,-0.5,-0.4,1.3,0.2,-0.1,0.3};

    this->setData(x,y,10);
}

void Graph::setData(double x[], double y[], int length)
{
    this->curve1->setSamples(x,y,length);
    this->replot();
}


