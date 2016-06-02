#include "activitytrackerblock.h"
#include "../../newAcquisition/wimuacquisition.h"
#include <math.h>

ActivityTrackerBlock::ActivityTrackerBlock()
{
    inputStatus = 0;

}

ActivityTrackerBlock::~ActivityTrackerBlock()
{
}


void ActivityTrackerBlock::Notify(std::string strId)
{
    if(strId == "accelData"){
        inputStatus |= static_cast<unsigned char>(INPUTS::ACCELDATA);
    }
    else if(strId == "normalG"){
        inputStatus |= static_cast<unsigned char>(INPUTS::NORMALG);
    }
    else if(strId == "threshold"){
        inputStatus |= static_cast<unsigned char>(INPUTS::THREASHOLD);
    }
    else if(strId == "bufferSize"){
        inputStatus |= static_cast<unsigned char>(INPUTS::BUFFERSIZE);
    }

    if(inputStatus == static_cast<unsigned char>(INPUTS::READY)){
        work();
    }
}

void ActivityTrackerBlock::work()
{
    //clean the signal
    std::vector<int> normalDelta;
    int normalBuf = 0;

    int gravity = GetInput<int>("normalG")->Get()[0];
    int i_gravity_2 = -gravity*gravity;

    std::vector<frame> accData = GetInput<frame>("accelData")->Get();

    int dataCount = accData.size();
    for(int i = 0; i<dataCount ; i++){
        normalBuf = accData[i].x*accData[i].x + accData[i].y*accData[i].y+accData[i].z*accData[i].z + i_gravity_2;
        normalDelta.push_back(abs(sqrt(normalBuf)));
    }

    //Moving average
    int bufferSize = GetInput<int>("bufferSize")->Get()[0];
    int average = 0;

    //first load
    for(int i = 0; i<bufferSize; i++){
        average += normalDelta[i];
    }

    //Calculate active time
    int threshold = GetInput<int>("threshold")->Get()[0];
    threshold *= bufferSize;
    int activeTimeStart = 0;
    int totalActiveTime = 0;
    bool lastIsActive = false;
    bool isActive = false;

    for(int i = bufferSize, j = 0; i<dataCount; i++, j++){
        average += normalDelta[i];
        average -= normalDelta[j];
        isActive = average>=threshold;
        if(isActive != lastIsActive){
            if(isActive){
                activeTimeStart = accData[i].timestamp;
            }else{
                totalActiveTime += accData[i].timestamp - activeTimeStart;
            }
            lastIsActive = isActive;
        }
    }

    //add the rest if data ended while in activity
    if(isActive)
        totalActiveTime += (accData[dataCount-1].timestamp - activeTimeStart);

    //Calculate complement
    int totalPassiveTime = accData[dataCount-1].timestamp - accData[0].timestamp - totalActiveTime;

    //output the result
    std::vector<int> out1 = std::vector<int>{(int)totalActiveTime/1000};
    std::vector<int> out2 = std::vector<int>{(int)totalPassiveTime/1000};

    GetOutput<int>("activeTime")->Send(out1);
    GetOutput<int>("passiveTime")->Send(out2);

}
