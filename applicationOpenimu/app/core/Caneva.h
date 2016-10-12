#ifndef CANEVA_H
#define CANEVA_H

#include <string>
#include "json/json/json.h"
#include "components/Block.h"
#include "../CustomQmlScene.h"

class Caneva
{
public:
    Caneva(std::string filename, CustomQmlScene* scene);
    
    ~Caneva();
    Block* getBlock(std::string ID);

    void test();
    void testSteps(std::string filePath);
    void testActivity(std::string filename);
    void test_slider_chart();
    void setSliderLimitValues(int min, int max);
    void setGraphData(std::string filePath);
    void testPythonActivity(std::string filePath);
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
