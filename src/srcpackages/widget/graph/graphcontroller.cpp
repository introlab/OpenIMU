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
    int a = *(int*)((InputNode<int>*)this->Input("a"))->Get();
    //((Graph*)this->widget)->SetText(a);
}
