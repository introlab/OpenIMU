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

    int* in1 = Block::GetInput("input1")->Get();
    int* in2 = Block::GetInput("input2")->Get();
    for(int i = 0; i<MAX_ARRAY_SIZE; i++){
        out1[i] = in1[i]-in2[i];
        out2[i] = in2[i]-in1[i];
    }

    Block::GetOutput("output1")->Send(out1);
    Block::GetOutput("output2")->Send(out2);
}
