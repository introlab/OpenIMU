#include "caneva.h"

#include <fstream>
#include <iostream>
#include "components/block.h"
#include "components/blockType/blockFactory.h"
#include "acquisition/AccelerometerReader.h"
#include "components/inputnode.h"
#include "components/outputnode.h"
#include "components/quickiteminputnodes.h"
//#include "components/quickitemoutputnodes.h"

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

void Caneva::test()
{
    std::vector<int> steps;
    std::vector<int> in;

    std::vector<std::string> arr_str =  {"a","b","c","d","e","f","g","h"};
    std::vector<int> arr_int =  {10,20,11,-2,0,-20,-10,-20};
    std::vector<double> arr_double=  {-0.3,-0.6,-0.33,0.06,0,0.6,0.3,0.6};
    getBlock("chart_line")->GetInput<std::string>("labels")->Put(arr_str);
    getBlock("chart_line")->GetInput<int>("input1")->Put(arr_int);
    getBlock("chart_line")->GetInput<double>("input2")->Put(arr_double);

    in.push_back(0);
    getBlock("podoBlock")->GetInput("podoTrigger")->Put(in);
    steps= (getBlock("podoBlock")->GetOutput("podoOutput")->getValueBuf());
    getBlock("label_steps")->GetInput("inputStepNumber")->Put(in);
    
    setSliderLimitValues(0,100);
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
            //block->AddOutput(scene->getOutputNode((*it)["ID"].asString().c_str(),(*out)["ID"].asString().c_str()));
        }

        blocks.push_back(block);
    }
}

void Caneva::createInputs(Block* block, Json::Value inputs)
{
    for(Json::ValueIterator it = inputs.begin() ; it != inputs.end() ; it++)
    {
        if((*it)["TYPE"].asString() == "vfloat"){
            AbstractInputNode* input = new InputNode<double>();
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
        if((*it)["TYPE"].asString() == "vfloat"){
            AbstractOutputNode* output = new OutputNode<double>();
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
        //getBlock((*it)["from"].asString())->GetOutput((*it)["out"].asString())->AddDest(getBlock((*it)["to"].asString())->GetInput((*it)["in"].asString()));
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
