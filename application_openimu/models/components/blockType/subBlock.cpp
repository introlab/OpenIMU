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
    std::cout<<"WORKING ON SUB!\n\n";

    int res1 = Block::GetInput("input1")->Get() - Block::GetInput("input2")->Get();
    int res2 = Block::GetInput("input2")->Get() - Block::GetInput("input1")->Get();

    std::cout<<"sub result1: "<<res1<<std::endl;
    std::cout<<"sub result2: "<<res2<<std::endl<<std::endl;

    Block::GetOutput("output1")->Send(res1);
    Block::GetOutput("output2")->Send(res2);
}
