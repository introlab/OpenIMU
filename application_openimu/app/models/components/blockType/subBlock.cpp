#include "subBlock.h"
#include "../block.h"
#include <iostream>
#include <vector>
#include "../inputnode.h"
#include "../outputnode.h"

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

    std::vector<int> in1 = Block::GetInput("input1")->Get();
    std::vector<int> in2 = Block::GetInput("input2")->Get();
    out1=in1;
    out2=in2;
    for(int i = 0; i<in1.size(); i++){
        out1[i] -= in2[i];
        out2[i] -= in1[i];
    }

    Block::GetOutput("output1")->Send(out1);
    Block::GetOutput("output2")->Send(out2);
}
