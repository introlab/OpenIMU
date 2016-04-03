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
  std::cout<<"WORKING ON ADD!\n";

  int sum = Block::GetInput("input1")->Get() + Block::GetInput("input2")->Get();

  std::cout<<"add result: "<<sum<<std::endl<<std::endl;

  Block::GetOutput("output1")->Send(sum);
}

