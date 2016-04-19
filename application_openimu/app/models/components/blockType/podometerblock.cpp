#include "podometerBlock.h"
#include "../../algorithm/podometer2/stepCounter.h"
#include <iostream>
#include <vector>
#include "../abstractinputnode.h"
#include "../abstractoutputnode.h"
#include "../../newAcquisition/wimuacquisition.h"

 PodometerBlock::PodometerBlock() : Block()
 {
 }

 PodometerBlock::~PodometerBlock()
 {
 }

void PodometerBlock::work()
{
    std::vector<frame> accData = GetInput<frame>("accelData")->Get();
    int stepNumber = 0;
    stepCounter* sc = new stepCounter(&accData,10);
    stepNumber = sc->detect_peak(1100);
    GetOutput<int>("stepNumber")->Send({stepNumber});
}

