#ifndef BUILDER_H
#define BUILDER_H

#include <QWidget>
#include <string>
#include "views/display.h"
#include "displaybuilder.h"
#include "jsonreader.h"
#include "components/abstractalgorithm.h"
#include "components/abstractinputnode.h"
#include "components/abstractoutputnode.h"
#include "components/abstractwidgetcontroller.h"


class Builder
{
public:
    Builder();
    Display* load(std::string layoutFile);
    void Clear();

private:
    void CreateItems();
    AbstractAlgorithm* CreateAlgo(std::string algoName, std::string algoID);
    void CreateInputsAndOutputs(AbstractAlgorithm *node);
    AbstractInputNode* CreateInput(std::string inputID, bool inputActive, std::string inputType, AbstractAlgorithm* node);
    AbstractOutputNode *CreateOutput(std::string outputID, std::string outputType, AbstractAlgorithm* node);
    void CreateConnections();

    JsonReader* jsonReader;
    DisplayBuilder* displayBuilder;

    std::list<AbstractWidgetController*> controllerList;
    std::list<AbstractInputNode*> inputNodeList;
    std::list<AbstractOutputNode*> outputNodeList;
    std::list<AbstractAlgorithm*> algorithmList;
};

#endif // BUILDER_H
