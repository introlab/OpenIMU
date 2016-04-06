#pragma once
#include <iostream>

using namespace std;

class KalmanFilter
{
public:
	KalmanFilter(void);
	~KalmanFilter(void);

	double filter(double measuredSignal);//signal: signal measured
	void setEstimatedNoisePower(double myEstimatedNoisePower);
private:
	double filterGain;
	double desirableNoisePower;
	double estimatedNoisePower;
	double A;
	double C;
	double B;
	double u;
	double P;
	double estimatedSignal; // estimated signal without noise
	double measuredSignal;
};

