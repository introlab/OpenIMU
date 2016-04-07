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

    std::vector<int> in1 = Block::GetInput<int>("input1")->Get();
    std::vector<int> in2 = Block::GetInput<int>("input2")->Get();
    out1 = in1;
    out2 = in2;
    for(int i = 0; i<in1.size(); i++){
        out1[i] /= in2[i];
        out2[i] /= in1[i];
    }

    Block::GetOutput<int>("output1")->Send(out1);
    Block::GetOutput<int>("output2")->Send(out2);
}
