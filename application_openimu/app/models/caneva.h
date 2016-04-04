#ifndef CANEVA_H
#define CANEVA_H

#include <string>
#include <json/json.h>
#include "components/block.h"

class Caneva
{
public:

    static Caneva* getInstance();
    ~Caneva();
    Block* getBlock(std::string ID);

protected:
    Caneva();
private:
    static Caneva* _instance;
    Caneva(std::string filename);


    void loadFile(std::string filename);
    void createBlocks();
    void createInputs(Block *block, Json::Value inputs);
    void createOutputs(Block *block, Json::Value outputs);
    void makeConnections();


    std::vector<Block*> blocks;

    Json::Reader reader;
    std::string filename;
    Json::Value root;
};

#endif // CANEVA_H
