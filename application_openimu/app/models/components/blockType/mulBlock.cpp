#include "mulBlock.h"

MulBlock::MulBlock(): Block()
{
}

MulBlock::~MulBlock()
{
}

void MulBlock::work()
{
    // out = in1 * in2
    std::vector<int> in1 = Block::GetInput<int>("input1")->Get();
    std::vector<int> in2 = Block::GetInput<int>("input2")->Get();
    out = in1;
    for(int i = 0; i<in1.size(); i++) out[i] *= in2[i];
    Block::GetOutput<int>("output1")->Send(out);
}
