#pragma once
#include "wimuacquisition.h"
class stepCounter
{
public:
	stepCounter(std::vector<frame> *_data, int windowSize);
	~stepCounter(void);
	void movingAverage(int windowSize);
	int detect_peak(double delta);
	//void slope(std::vector<int> );
private:
	std::vector<frame> *data;
	std::vector<double> filteredData;
};

