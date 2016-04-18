#include "activitytrackerblock.h"
#include "newAcquisition/wimuacquisition.h"
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
    std::vector<unsigned short> normalDelta;
    signed int normalBuf = 0;

    signed short gravity = GetInput<signed short>("normalG")->Get()[0];
    signed short i_gravity_2 = -gravity*gravity;

    std::vector<frame> accData = GetInput<frame>("accelData")->Get();

    int dataCount = accData.size();
    for(int i = 0; i<dataCount ; i++){
        normalBuf = accData[i].x*accData[i].x + accData[i].y*accData[i].y+accData[i].z*accData[i].z + i_gravity_2;
        normalDelta.push_back(abs(sqrt(normalBuf)));
    }

    //Moving average
    unsigned short bufferSize = GetInput<unsigned short>("bufferSize")->Get()[0];
    unsigned int average = 0;

    //first load
    for(int i = 0; i<bufferSize; i++){
        average += normalDelta[i];
    }

    //Calculate active time
    unsigned int threshold = GetInput<unsigned short>("threshold")->Get()[0];
    threshold *= bufferSize;
    long long activeTimeStart = 0;
    long long totalActiveTime = 0;
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
    long long totalPassiveTime = accData[dataCount-1].timestamp - accData[0].timestamp - totalActiveTime;

    //output the result
    GetOutput("activeTime")->Send({totalActiveTime});
    GetOutput("passiveTime")->Send({totalPassiveTime});

}
