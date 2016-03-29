#include "divBlock.h"

DivBlock::DivBlock(): Block()
{

}

DivBlock::~DivBlock()
{
}

void DivBlock::work()
{
    //out1 = int(in1 / in2)
    //out2 = int(in2 / in1)
    std::cout<<"WORKING ON DIV!\n\n";

    int res1 = Block::GetInput("input1")->Get() / Block::GetInput("input2")->Get();
    int res2 = Block::GetInput("input2")->Get() / Block::GetInput("input1")->Get();

    std::cout<<"div result1: "<<res1<<std::endl;
    std::cout<<"div result2: "<<res2<<std::endl<<std::endl;

    Block::GetOutput("output1")->Send(res1);
    Block::GetOutput("output2")->Send(res2);
}
