#include "KalmanFilter.h"


KalmanFilter::KalmanFilter(void)
{
	filterGain = 1;
	desirableNoisePower = 1;
	estimatedNoisePower = 10;
	
	A = 1;
	C = 1;
	B = 0;
	u = 0;
	P = -1;

	estimatedSignal = -1; //estimated signal without noise
	measuredSignal = -1;  //measured
}


KalmanFilter::~KalmanFilter(void)
{
}

void KalmanFilter::setEstimatedNoisePower(double myEstimatedNoisePower)//signal: signal measured
{
	this->estimatedNoisePower = myEstimatedNoisePower;
}

double KalmanFilter::filter(double myMeasuredSignal){
	
	this->measuredSignal = myMeasuredSignal;

	if(this->estimatedSignal == -1)
	{
		estimatedSignal = (1/C) * measuredSignal;
		P = (1/C) * estimatedNoisePower * (1/C);
	}
	else
	{
		//Kalman filter: prediction and covariance P
		estimatedSignal = A * estimatedSignal + B*u;
		P = A * P * A + desirableNoisePower;

		//Gain
		int rv = 10;//estimatedNoisePower;
		filterGain = P * C * (1 / (C * P * C + rv));//replace rv estimatedNoisePower
		double temp = estimatedSignal;
		//Correction
		estimatedSignal = estimatedSignal + filterGain * (measuredSignal - C * estimatedSignal);
		//cout << "\nCorrected value = estimatedSignal + filterGain * measuredSignal - C * estimatedSignal)";
		//cout << "\n          " << estimatedSignal << " = " << temp << " + " << filterGain << " * ( " << measuredSignal << " - " << C << " * " << temp << " )\n"; 
		P = P - filterGain * C * P;
	}

	return estimatedSignal;
}
