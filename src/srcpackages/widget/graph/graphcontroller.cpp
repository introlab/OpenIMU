#include "graphcontroller.h"
#include "models/components/outputnode.h"

GraphController::GraphController(Graph *graph)
{
    graph->SetObserver(this);
}

void GraphController::Notify(std::string inputID)
{
    work();
}

void GraphController::work()
{
    double* x = (double*)(((InputNode<double*>*)this->Input("CoorX"))->Get());
    double* y = (double*)(((InputNode<double*>*)this->Input("CoorY"))->Get());
    int length = (int)((InputNode<int>*)this->Input("Length"))->Get();

    ((Graph*)this->widget)->setData(x,y,length);
}
