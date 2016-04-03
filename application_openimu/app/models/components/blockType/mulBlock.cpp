#include "mulBlock.h"

MulBlock::MulBlock(): Block()
{
}

MulBlock::~MulBlock()
{
}

void MulBlock::work()
{
    // out = in1 + in2
    std::cout<<"WORKING ON MUL!\n";

    int product = Block::GetInput("input1")->Get() * Block::GetInput("input2")->Get();

    std::cout<<"mul result: "<<product<<std::endl<<std::endl;

    Block::GetOutput("output1")->Send(product);
}
