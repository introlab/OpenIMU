#include "SubBlock.h"
#include "../Block.h"
#include <iostream>
#include <vector>
#include "../AbstractInputNode.h"
#include "../AbstractOutputNode.h"

SubBlock::SubBlock(): Block()
{

}

SubBlock::~SubBlock()
{

}

void SubBlock::work()
{
    //out1 = in1 - in2
    //out2 = in2 - in1

    std::vector<int> in1 = Block::GetInput<int>("input1")->Get();
    std::vector<int> in2 = Block::GetInput<int>("input2")->Get();
    out1=in1;
    out2=in2;
    for(int i = 0; i<in1.size(); i++){
        out1[i] -= in2[i];
        out2[i] -= in1[i];
    }

    Block::GetOutput<int>("output1")->Send(out1);
    Block::GetOutput<int>("output2")->Send(out2);
}
