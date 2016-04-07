#include "addBlock.h"
#include "../block.h"
#include <iostream>
#include <vector>
#include "../inputnode.h"
#include "../outputnode.h"

 AddBlock::AddBlock() : Block()
 {
 }

 AddBlock::~AddBlock()
 {
 }

void AddBlock::work()
{
    // out = in1 + in2

    std::vector<int> in1 = Block::GetInput("input1")->Get();
    std::vector<int> in2 = Block::GetInput("input2")->Get();
    out=in1;
    for(int i = 0; i<in1.size(); i++) out[i] += in2[i];
    Block::GetOutput("output1")->Send(out);
}

