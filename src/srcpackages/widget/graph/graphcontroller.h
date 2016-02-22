#ifndef GRAPHCONTROLLER_H
#define GRAPHCONTROLLER_H

#include "graphobserver.h"
#include "models/components/abstractwidgetcontroller.h"
#include "graph.h"

class GraphController: public GraphObserver, public AbstractWidgetController
{
public:
    GraphController(Graph *graph);
    void Notify(std::string inputID);
    void work();
};

#endif // GRAPHCONTROLLER_H
