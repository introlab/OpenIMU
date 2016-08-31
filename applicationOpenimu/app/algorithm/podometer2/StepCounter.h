#pragma once
#include "../../newAcquisition/WimuAcquisition.h"

class StepCounter
{
public:
    StepCounter(std::vector<frame> *_data, int windowSize);
    ~StepCounter(void);
	void movingAverage(int windowSize);
	int detect_peak(double delta);

private:
	std::vector<frame> *data;
	std::vector<double> filteredData;
};

