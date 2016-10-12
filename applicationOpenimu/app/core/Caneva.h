#ifndef CANEVA_H
#define CANEVA_H

#include <string>
#include "json/json/json.h"
#include "components/Block.h"
#include "../CustomQmlScene.h"
#include "../acquisition/wimuacquisition.h"

class Caneva
{

public:
    Caneva(std::string filename, CustomQmlScene* scene);
    
    ~Caneva();
    Block* getBlock(std::string ID);

    void test();
    void testSteps(WimuAcquisition& acceleroData);
    void testActivity(std::string filename);
    void test_slider_chart();
    void setSliderLimitValues(int min, int max);
    void setGraphData(std::string filePath);

private:

    void loadFile(std::string filename);
    void createBlocks();
    void createVBlocks(CustomQmlScene *scene);
    void createInputs(Block *block, Json::Value inputs);
    void createOutputs(Block *block, Json::Value outputs);
    void makeConnections();

    std::vector<Block*> blocks;
    Json::Reader reader;
    std::string filename;
    Json::Value root;
};

#endif // CANEVA_H
