#include "builder.h"
#include "srcpackages/algorithm/incrementer/incrementer.h"
#include "components/inputnode.h"
#include "components/outputnode.h"

Builder::Builder()
{
    displayBuilder = new DisplayBuilder();
}

Display *Builder::load(std::string layoutFile)
{
    this->jsonReader = new JsonReader();
    jsonReader->loadFile(layoutFile);
    displayName = jsonReader->getDisplayName();
    this->CreateItems();

    return displayBuilder->GetDisplay();
}

std::string Builder::getDisplayName()
{
    return this->displayName;
}

void Builder::CreateItems(){
    for(Json::Value widgetDesc = jsonReader->getNextWidget(); jsonReader->hasWidget(); widgetDesc = jsonReader->getNextWidget())
    {
        std::string widgetName = widgetDesc["widget"].asString();
        int xPos = widgetDesc["pos"]["x"].asInt();
        int yPos = widgetDesc["pos"]["y"].asInt();
        AbstractWidgetController* node = this->displayBuilder->CreateWidget(widgetName, xPos, yPos);
        this->controllerList.push_back(node);
        //CreateInputsAndOutputs(node);
    }
/*
    for(Json::Value algoDesc = jsonReader->getNextAlgo(); jsonReader->hasAlgo(); algoDesc = jsonReader->getNextAlgo())
    {
        std::string algoName = algoDesc["algo"].asString();
        std::string algoID = algoDesc["ID"].asString();

        this->algorithmList.push_back(this->CreateAlgo(algoName, algoID));
    }

    this->CreateConnections();
*/
}

AbstractAlgorithm *Builder::CreateAlgo(std::string algoName, std::string algoID)
{
    AbstractAlgorithm* algorithm;
    if(algoName == "Incrementer")
    {
        algorithm = new Incrementer();
    }

    algorithm->SetStringID(algoID);

    CreateInputsAndOutputs(algorithm);

    return algorithm;
}

void Builder::CreateInputsAndOutputs(AbstractAlgorithm* node)
{
    for(Json::Value inputDesc = jsonReader->getNextInput(); jsonReader->hasInput(); inputDesc = jsonReader->getNextInput())
    {
        std::string inputID = inputDesc["ID"].asString();
        bool inputActive = inputDesc["active"].asBool();
        std::string inputType = inputDesc["dataType"].asString();

        this->inputNodeList.push_back(this->CreateInput(inputID, inputActive, inputType, node));
    }

    for(Json::Value outputDesc = jsonReader->getNextOutput(); jsonReader->hasOutput(); outputDesc = jsonReader->getNextOutput())
    {
        std::string outputID = outputDesc["ID"].asString();
        std::string outputType = outputDesc["dataType"].asString();

        this->outputNodeList.push_back(this->CreateOutput(outputID, outputType, node));
    }
}

AbstractInputNode *Builder::CreateInput(std::string inputID, bool inputActive, std::string inputType, AbstractAlgorithm *node)
{
    AbstractInputNode * inputNode;

    if(inputType == "int")
    {
        inputNode = new InputNode<int>();
    }

    inputNode->SetStringID(inputID);
    inputNode->SetActive(inputActive);

    node->AddInput(inputNode);

    return inputNode;
}

AbstractOutputNode *Builder::CreateOutput(std::string outputID, std::string outputType, AbstractAlgorithm *node)
{
    AbstractOutputNode * outputNode;

    if(outputType == "int")
    {
        outputNode = new OutputNode<int>();
    }

    outputNode->SetStringID(outputID);

    node->AddOutput(outputNode);

    return outputNode;
}

void Builder::CreateConnections(){

}

void Builder::Clear()
{
    this->displayBuilder->Clear();
}
