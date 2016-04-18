#include "madgwickBlock.h"
#include "../application_openimu/app/newAcquisition/wimuacquisition.h"

#include <math.h>

MadgwickBlock::MadgwickBlock(): Block()
{
    madgwick = new Madgwick();
}

MadgwickBlock::~MadgwickBlock()
{
}

void MadgwickBlock::Notify(std::string inputID)
{
    if(inputID == "accelData"){
        inputStatus |= static_cast<unsigned char>(INPUTS::ACCELDATA);
    }
    else if(inputID == "gyroData"){
        inputStatus |= static_cast<unsigned char>(INPUTS::GYRODATA);
    }
    else if(inputID == "magnetoData"){
        inputStatus |= static_cast<unsigned char>(INPUTS::MAGNETODATA);
    }
    else if(inputID == "sampleRate"){
        inputStatus |= static_cast<unsigned char>(INPUTS::SAMPLERATE);
        madgwick->begin(GetInput("sampleRate")->Get()[0]);
    }

    if(inputStatus == static_cast<unsigned char>(INPUTS::READY)){
        work();
    }
}

void MadgwickBlock::work()
{
    //Load inputs
    std::vector<frame> a = GetInput<frame>("accelData")->Get();
    std::vector<frame> g = GetInput<frame>("gyroData")->Get();
    std::vector<frame> m = GetInput<frame>("magnetoData")->Get();

    //get smallest array size just in case
    unsigned int numberOfSamples = std::min( std::min(a.size(),g.size()) , m.size());

    //Iterate for Madgwick
    for(unsigned int i = 0; i<numberOfSamples; i++){
        madgwick->update(g[i].x, g[i].y, g[i].z,
                         a[i].x, a[i].y, a[i].z,
                         m[i].x, m[i].y, m[i].z
                         );
    }

    //Set outputs
    GetOutput<float>("roll")->Send({madgwick->getRoll()});
    GetOutput<float>("pitch")->Send({madgwick->getPitch()});
    GetOutput<float>("yaw")->Send({madgwick->getYaw()});
}
