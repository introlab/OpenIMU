#include "podometerBlock.h"
#include "../../../algorithm/podometer/StepCounter.h"
#include <iostream>
#include <vector>
#include "../AbstractInputNode.h"
#include "../AbstractOutputNode.h"
#include "../../../acquisition/WimuAcquisition.h"

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
    StepCounter* sc = new StepCounter(&accData,10);
    stepNumber = sc->detect_peak(1100);
    int moy = ((stepNumber/2)+stepNumber)/2;
    GetOutput<int>("stepNumber")->Send({stepNumber});
    GetOutput<int>("stepNumberChart")->Send({stepNumber/2,stepNumber});
    GetOutput<int>("stepNumberMoyenne")->Send({moy});
    GetOutput<int>("stepNumberMin")->Send({stepNumber/2});
}

