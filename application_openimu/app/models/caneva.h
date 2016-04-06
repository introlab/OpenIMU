#ifndef CANEVA_H
#define CANEVA_H

#include <string>
#include <json/json.h>
#include "components/block.h"
#include "customqmlscene.h"

class Caneva
{
public:
    Caneva(std::string filename, CustomQmlScene* scene);
    ~Caneva();

    void test();

private:
    void loadFile(std::string filename);
    void createBlocks();
    void createVBlocks(CustomQmlScene *scene);
    void createInputs(Block *block, Json::Value inputs);
    void createOutputs(Block *block, Json::Value outputs);
    void makeConnections();

    Block* getBlock(std::string ID);
    std::vector<Block*> blocks;

    Json::Reader reader;
    std::string filename;
    Json::Value root;
};

#endif // CANEVA_H
