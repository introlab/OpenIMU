#include "graph.h"


Graph::Graph():QwtPlot()
{
    curve1 = new QwtPlotCurve();
    curve1->attach(this);
}
