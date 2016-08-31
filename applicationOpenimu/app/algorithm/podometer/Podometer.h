#pragma once
#include "KalmanFilter.h"
#include "Math.h"
#include "../../acquisition/SensorDataPerDay.h"
#include <cmath>
#include <vector>
#include <limits>

using namespace std;

static const double GRAVITY = 9.80665;
static const double GRAVITY_FACTOR = 9.80665;
static const double INTERVAL = 0.02;

class Podometer
{
public:
	Podometer(void);
	~Podometer(void);
    int getStepCount(){return stepCount;}
	void execute(vector<SensorDataPerDay> accelerometerData);
private:
	//Class member variables
	std::vector<double> accelerationAmplitude; // amplitude of the acceleration 
	double accelerationVariance; // variance of the acceleration on the window L
	double minimumAcceleration; // minimum of the acceleration on the window L
	double maximumAcceleration; // maximum of the acceleration on the window L
	double threshold; // threshold to detect a step
	double detectionSensitivity; // sensibility to detect a step
	int stepCount; // number of steps
	std::vector<double> stepsDetected; //0 = no step, 1 = one step
	KalmanFilter kalmanFilter;

	//Class methods
	void createTable(int values);
	void setDetectionSensitivity(double myDetectionSensitivity);
	void setAccelerometerValues();
	double computeNorm(double x, double y, double z);
	void setThreshold(double maxValue, double minValue);
	void seekVariance(vector<double> myValues);
	double seekMinimumValue(vector<double> myValues);
	double seekMaximumValue(vector<double> myValues);
	void detectSteps(vector<double> myValues);
	void update();
    void setKalmanFilter(KalmanFilter myKalmanFilter){kalmanFilter = myKalmanFilter;}
    KalmanFilter getKalmanFilter(){return kalmanFilter;}
};

