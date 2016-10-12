#include "caneva.h"

#include <fstream>
#include <iostream>
#include "components/Block.h"
#include "components/blockType/BlockFactory.h"
#include "components/InputNode.h"
#include "components/OutputNode.h"
#include "components/QuickItemInputNodes.h"

#include "../acquisition/wimuacquisition.h"
#include <QEventLoop>
#include<QNetworkReply>
#include<QNetworkRequest>
#include<QNetworkAccessManager>
#include"../../acquisition/CJsonSerializer.h"

Caneva::Caneva(std::string filename, CustomQmlScene *scene)
{
    loadFile(filename);
    createBlocks();
    createVBlocks(scene);
    makeConnections();
}


Caneva::~Caneva()
{
    for(auto it = blocks.begin() ; it != blocks.end() ; it++)
        delete(*it);
}

void Caneva::test_slider_chart()
{

    std::vector<std::string> arr_str =  {"a","b","c","d","e","f","g","h"};
    std::vector<int> arr_int =  {10,20,11,-2,0,-20,-10,-20};

    getBlock("chart_line")->GetInput<std::string>("labels")->Put(arr_str);
    getBlock("multiplier")->GetInput<int>("input1")->Put(arr_int);
    setSliderLimitValues(0,100);

}

void Caneva::testSteps(WimuAcquisition& acceleroData)
{
    std::vector<std::string> arr_str =  {"Jour 1", "Jour 2","Jour 3","Jour 4","Jour 5"};
    std::vector<int> arr_int =  {10,20,11,2,0,15,-10,-20};

    std::vector<frame> availableData = acceleroData.getData();

    qDebug() << "here utp";
    getBlock("podometer")->GetInput<frame>("accelData")->Put(availableData);

    getBlock("col1.label_title_value")->GetInput<std::string>("inputTitle")->Put(std::vector<std::string>({"Compteur de pas: "}));

    getBlock("col1.row2.col4.label_start_date")->GetInput<std::string>("inputStartDate")->Put(std::vector<std::string>({acceleroData.getDates().back().date}));
    getBlock("col1.row2.col4.label_end_date")->GetInput<std::string>("inputEndDate")->Put(std::vector<std::string>({acceleroData.getDates().back().date}));
    getBlock("col1.row2.col4.label_days")->GetInput<int>("inputDaysAvailable")->Put(std::vector<int>({6}));

    getBlock("col1.row2.col3.chart_step")->GetInput<std::string>("x")->Put(arr_str);

}
void Caneva::testActivity(std::string filePath)
{
    WimuAcquisition* acceleroData = new WimuAcquisition(filePath,"","",50);
    acceleroData->initialize();
    std::vector<frame> availableData = acceleroData->getData();

    getBlock("activity")->GetInput<frame>("accelData")->Put(availableData);
    getBlock("activity")->GetInput<int>("bufferSize")->Put({50*60});
    getBlock("activity")->GetInput<int>("threshold")->Put({300});
    getBlock("activity")->GetInput<int>("normalG")->Put({9000});

    getBlock("col1.label_title_value")->GetInput<std::string>("inputTitle")->Put(std::vector<std::string>({"Temps d'activité: "}));

    getBlock("col1.row2.col4.label_start_date")->GetInput<std::string>("inputStartDate")->Put(std::vector<std::string>({acceleroData->getDates().back().date}));
    getBlock("col1.row2.col4.label_end_date")->GetInput<std::string>("inputEndDate")->Put(std::vector<std::string>({acceleroData->getDates().back().date}));
    getBlock("col1.row2.col4.label_days")->GetInput<int>("inputDaysAvailable")->Put(std::vector<int>({1}));

    getBlock("col1.row2.col4.vtotalLabel")->GetInput<int>("inputvtotal")->Put(std::vector<int>({100}));
    getBlock("col1.row2.col4.vmoyLabel")->GetInput<int>("inputvmoy")->Put(std::vector<int>({10}));
    getBlock("col1.row2.col4.vmaxLabel")->GetInput<int>("inputvmax")->Put(std::vector<int>({15}));
    getBlock("col1.row2.col4.vminLabel")->GetInput<int>("inputvmin")->Put(std::vector<int>({12}));

}

void Caneva::setGraphData(std::string folderPath){
    std::vector<int> time ;
    std::vector<int> xaxis;
    std::vector<int> yaxis;
    std::vector<int> zaxis;

    for(int i = 0; i< 10;i++){
        time.push_back(i);
        xaxis.push_back(i+2);
        yaxis.push_back(i+4);
        zaxis.push_back(i*2);
    }
    //to do: add values from BD
    getBlock("chart_line")->GetInput("inputTimeAxis")->Put(time);
    getBlock("chart_line")->GetInput("inputXAxis")->Put(xaxis);
    getBlock("chart_line")->GetInput("inputYAxis")->Put(yaxis);
    getBlock("chart_line")->GetInput("inputZAxis")->Put(zaxis);

}

void Caneva::setSliderLimitValues(int min, int max){
    getBlock("slider")->GetInput<int>("inputSliderMinimumValue")->Put(std::vector<int>({min}));
    getBlock("slider")->GetInput<int>("inputSliderMaximumValue")->Put(std::vector<int>({max}));
}

void Caneva::loadFile(std::string filename)
{
    this->filename = filename;

    std::ifstream file;
    file.open(filename.c_str());
    std::string fileContent;
    std::string buf;

    if(file.is_open())
        while(file >> buf)
            fileContent.append(buf);


    bool parsingSuccessful = reader.parse(fileContent, root);
    if ( !parsingSuccessful )
    {
        // report to the user the failure and their locations in the document.
        std::string error = reader.getFormattedErrorMessages();
        std::cout  << "Failed to parse configuration\n"
                   << error;
    }
}


void Caneva::createBlocks()
{
    BlockFactory* blockFactory = new BlockFactory();
    for(Json::ValueIterator it = root["ListBlock"].begin() ; it != root["ListBlock"].end() ; it++)
    {
        Block* block = new Block();
        block = blockFactory->createBlockType((*it)["type"].asString());
        block->SetStringID((*it)["ID"].asString());

        createInputs(block,(*it)["inputs"]);
        createOutputs(block,(*it)["outputs"]);

        blocks.push_back(block);
    }
}

void Caneva::createVBlocks(CustomQmlScene *scene)
{
    for(Json::ValueIterator it = root["ListVBlock"].begin() ; it != root["ListVBlock"].end() ; it++)
    {
        Block* block = new Block();
        block->SetStringID((*it)["ID"].asString());

        // get inputs
        for(Json::ValueIterator in = (*it)["inputs"].begin() ; in != (*it)["inputs"].end() ; in++)
        {
            AbstractInputNode* node;
            if((*in)["TYPE"].asString() == "Int")
                node = new QuickItemInputNodeInt(scene->getInputNode<QuickItemInputNodeIntHandle>((*it)["ID"].asString().c_str(),(*in)["ID"].asString().c_str()));
            else if((*in)["TYPE"].asString() == "Double")
                node = new QuickItemInputNodeDouble(scene->getInputNode<QuickItemInputNodeDoubleHandle>((*it)["ID"].asString().c_str(),(*in)["ID"].asString().c_str()));
            else if((*in)["TYPE"].asString() == "String")
                node = new QuickItemInputNodeString(scene->getInputNode<QuickItemInputNodeStringHandle>((*it)["ID"].asString().c_str(),(*in)["ID"].asString().c_str()));
            else //Default int
                node = new QuickItemInputNodeInt(scene->getInputNode<QuickItemInputNodeIntHandle>((*it)["ID"].asString().c_str(),(*in)["ID"].asString().c_str()));
            node->SetStringID((*in)["ID"].asString());
            block->AddInput(node);
        }

        // get outputs
        for(Json::ValueIterator out = (*it)["outputs"].begin() ; out != (*it)["outputs"].end() ; out++)
        {
            AbstractOutputNode* node;
            if((*out)["TYPE"].asString() == "Int")
            {
                QuickItemOutputNodeInt* vNode = scene->getInputNode<QuickItemOutputNodeInt>((*it)["ID"].asString().c_str(),(*out)["ID"].asString().c_str());
                node = new OutputNode<int>();
                vNode->setOutputNode((OutputNode<int>*)node);
            }
            else if((*out)["TYPE"].asString() == "Double")
            {
                QuickItemOutputNodeDouble* vNode = scene->getInputNode<QuickItemOutputNodeDouble>((*it)["ID"].asString().c_str(),(*out)["ID"].asString().c_str());
                node = new OutputNode<double>();
                vNode->setOutputNode((OutputNode<double>*)node);
            }
            else if((*out)["TYPE"].asString() == "String")
            {
                QuickItemOutputNodeString* vNode = scene->getInputNode<QuickItemOutputNodeString>((*it)["ID"].asString().c_str(),(*out)["ID"].asString().c_str());
                node = new OutputNode<std::string>();
                vNode->setOutputNode((OutputNode<std::string>*)node);
            }
            else //Default int
            {
                QuickItemOutputNodeInt* vNode = scene->getInputNode<QuickItemOutputNodeInt>((*it)["ID"].asString().c_str(),(*out)["ID"].asString().c_str());
                node = new OutputNode<int>();
                vNode->setOutputNode((OutputNode<int>*)node);
            }

            node->SetStringID((*out)["ID"].asString());
            block->AddOutput(node);
        }

        blocks.push_back(block);
    }
}

void Caneva::createInputs(Block* block, Json::Value inputs)
{
    for(Json::ValueIterator it = inputs.begin() ; it != inputs.end() ; it++)
    {
        if((*it)["TYPE"].asString() == "Float"){
            AbstractInputNode* input = new InputNode<float>();
            input->SetStringID((*it)["ID"].asString());
            block->AddInput(input);
        }
        else if((*it)["TYPE"].asString() == "LongLong"){
            AbstractInputNode* input = new InputNode<long long>();
            input->SetStringID((*it)["ID"].asString());
            block->AddInput(input);
        }
        else if((*it)["TYPE"].asString() == "SShort"){
            AbstractInputNode* input = new InputNode<signed short>();
            input->SetStringID((*it)["ID"].asString());
            block->AddInput(input);
        }
        else if((*it)["TYPE"].asString() == "UShort"){
            AbstractInputNode* input = new InputNode<unsigned short>();
            input->SetStringID((*it)["ID"].asString());
            block->AddInput(input);
        }
        else if((*it)["TYPE"].asString() == "Frame"){
            AbstractInputNode* input = new InputNode<frame>();
            input->SetStringID((*it)["ID"].asString());
            block->AddInput(input);
        }
        else
        {
            AbstractInputNode* input = new InputNode<int>();
            input->SetStringID((*it)["ID"].asString());
            block->AddInput(input);
        }
    }
}

void Caneva::createOutputs(Block *block, Json::Value outputs)
{
    for(Json::ValueIterator it = outputs.begin() ; it != outputs.end() ; it++)
    {
        if((*it)["TYPE"].asString() == "Float"){
            AbstractOutputNode* output = new OutputNode<float>();
            output->SetStringID((*it)["ID"].asString());
            block->AddOutput(output);
        }
        else if((*it)["TYPE"].asString() == "LongLong"){
            AbstractOutputNode* output = new OutputNode<long long>();
            output->SetStringID((*it)["ID"].asString());
            block->AddOutput(output);
        }
        else if((*it)["TYPE"].asString() == "SShort"){
            AbstractOutputNode* output = new OutputNode<signed short>();
            output->SetStringID((*it)["ID"].asString());
            block->AddOutput(output);
        }
        else if((*it)["TYPE"].asString() == "UShort"){
            AbstractOutputNode* output = new OutputNode<unsigned short>();
            output->SetStringID((*it)["ID"].asString());
            block->AddOutput(output);
        }
        else if((*it)["TYPE"].asString() == "Frame"){
            AbstractOutputNode* output = new OutputNode<frame>();
            output->SetStringID((*it)["ID"].asString());
            block->AddOutput(output);
        }
        else
        {
            AbstractOutputNode* output = new OutputNode<int>();
            output->SetStringID((*it)["ID"].asString());
            block->AddOutput(output);
        }
    }
}

void Caneva::makeConnections()
{
    for(Json::ValueIterator it = root["ListConnection"].begin() ; it != root["ListConnection"].end() ; it++)
    {
        Block* from = getBlock((*it)["from"].asString());
        if(!from) return;
        AbstractOutputNode* out = from->GetOutput((*it)["out"].asString());
        if(!out) return;
        Block* to = getBlock((*it)["to"].asString());
        if(!to) return;
        AbstractInputNode* in = to->GetInput((*it)["in"].asString());
        if(!in) return;
        out->AddDest(in);
    }
}

Block *Caneva::getBlock(std::string ID)
{
    for ( auto it = blocks.begin() ; it != blocks.end(); ++it)
    {
        if((*it)->GetStringID() == ID) return *it;
    }
    return 0; //nullptr
}
