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
  int* in1 = Block::GetInput("input1")->Get();
  int* in2 = Block::GetInput("input2")->Get();
  for(int i = 0; i<MAX_ARRAY_SIZE; i++) out[i] = in1[i]+in2[i];
  Block::GetOutput("output1")->Send(out);
}

