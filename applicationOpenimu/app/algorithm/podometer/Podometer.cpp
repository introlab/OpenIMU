#include "Podometer.h"

Podometer::Podometer(void)
{
	accelerationVariance = 0.0;
	minimumAcceleration = std::numeric_limits<double>::max();
	maximumAcceleration = std::numeric_limits<double>::min();
	threshold = std::numeric_limits<double>::min();
	detectionSensitivity = 1.0/30.0;
	stepCount = 0;
}

Podometer::~Podometer(void)
{
}

void Podometer::setDetectionSensitivity(double myDetectionSensitivity)
{
	detectionSensitivity = myDetectionSensitivity;
}

double Podometer::computeNorm(double x, double y, double z){
	double norm = sqrt(pow(x,2)+ pow(y,2)+ pow(z,2));
	return norm;
}

void Podometer::setThreshold(double maxValue, double minValue){
	threshold = (minValue + maxValue)/2;
}

void Podometer::seekVariance(std::vector<double> myValues)
{
	if(!myValues.empty())
	{
		double mean = 0.0;
		double meanSquare = 0.0;

		for(int k = 0; k <= myValues.size() - 1; k++)
		{
			mean += myValues[k];
			meanSquare += pow(myValues[k], 2);
		}

		accelerationVariance = (pow(mean, 2) - meanSquare)/myValues.size();

		if(accelerationVariance - 0.5 > 0)
		{
			accelerationVariance -= 0.5;
		}
	
		if(accelerationVariance >= 0)
		{
			kalmanFilter.setEstimatedNoisePower(accelerationVariance);
			setDetectionSensitivity((2.0 * sqrt(accelerationVariance))/(pow(GRAVITY_FACTOR, 2)));
		}
		else
		{
			setDetectionSensitivity(1.0/30.0);
		}
	}
	else
	{
		setDetectionSensitivity(1.0/30.0);
	}
}

double Podometer::seekMinimumValue(std::vector<double> myValues)
{
	double min = std::numeric_limits<double>::max();
	for(int k = 0; k < myValues.size(); k++)
	{
		if (myValues[k] < min)
		{
			min = myValues[k];
		}
	}
	return min;
}

double Podometer::seekMaximumValue(std::vector<double> myValues)
{
	double max = std::numeric_limits<double>::min();
	for(int k = 0; k < myValues.size(); k++)
	{
		if (myValues[k] > max)
		{
			max = myValues[k];
		}
	}
	return max;
}

void Podometer::detectSteps(std::vector<double> myValues)
{
	seekVariance(myValues);
	minimumAcceleration = seekMinimumValue(myValues);
	maximumAcceleration = seekMaximumValue(myValues);
	setThreshold(minimumAcceleration, maximumAcceleration);

	double difference = maximumAcceleration - minimumAcceleration;

	// the acceleration has to go over the sensibility
	bool isOverSensibility = (abs(difference) >= detectionSensitivity);

	// if the acceleration goes over the threshold and the previous was below this threshold
	bool isOverThreshold = ((myValues[myValues.size()-1] >= threshold) && (myValues[myValues.size()-2] < threshold));

	bool isValidStep = (stepsDetected.size() >= 1) && (stepsDetected[stepsDetected.size()-1] == 0);

	if(isOverSensibility && isOverThreshold & isValidStep)
	{
		stepCount++;
		stepsDetected.push_back(1);
		stepsDetected.erase(stepsDetected.begin());
	}
	else
	{
		stepsDetected.push_back(0);
		stepsDetected.erase(stepsDetected.begin());
	}
}

//Initialization of arrays
void Podometer::createTable(int myValues){
	accelerationAmplitude.clear();
	stepsDetected.clear();
	for(int i=0; i < 50; i++)
	{
		accelerationAmplitude.push_back(myValues);
		stepsDetected.push_back(myValues);
	}
	
}

//Removes the oldest value
void Podometer::update()
{
	accelerationAmplitude.erase(accelerationAmplitude.begin());
}

void Podometer::execute(vector<SensorDataPerDay> accelerometerData)
{
	std::vector<double> xValues;
	std::vector<double> yValues;
	std::vector<double> zValues;
	double max = 0;
	//On veut juste sur un echantillon, pas sur toutes les donnees
	for(int i = 0; i< accelerometerData.size();i++){
		for(int j = 0; j< accelerometerData.at(i).getDataPerDay().size() ;j++){
			for(int k = 0; k<accelerometerData.at(i).getDataPerDay().at(j).getAccelerometerDataPerHour().size();k++){

				
				//Calculer la norme pour chaque donnee (X, Y, Z)
				for(int m = 0; m < accelerometerData.at(i).getDataPerDay().at(j).getAccelerometerDataPerHour().at(k).getXAxisValues().size(); m++)
				{
					if(accelerationAmplitude.size() < 2 || stepsDetected.size() < 2)
					{
						int tableInitValues = floor(2/(INTERVAL/1000)+0.5);
						createTable(tableInitValues);
					}
					else
					{
                                                double xValue = accelerometerData.at(i).getDataPerDay().at(j).getAccelerometerDataPerHour().at(k).getXAxisValues().at(m);
						double yValue = accelerometerData.at(i).getDataPerDay().at(j).getAccelerometerDataPerHour().at(k).getYAxisValues().at(m);
						double zValue = accelerometerData.at(i).getDataPerDay().at(j).getAccelerometerDataPerHour().at(k).getZAxisValues().at(m);

						xValues.push_back(xValue);
						yValues.push_back(yValue);
                                                zValues.push_back(zValue);

						double accelerationNorm = computeNorm(xValue, yValue, zValue);
						double filteredNormalizedAcceleration = kalmanFilter.filter(accelerationNorm)/GRAVITY_FACTOR;
						if(filteredNormalizedAcceleration > max)
							max = filteredNormalizedAcceleration;
						accelerationAmplitude.push_back(filteredNormalizedAcceleration);
						//cout << " \nDerniere valeur: " << accelerationAmplitude.at(accelerationAmplitude.size()-1);
						update();
						detectSteps(accelerationAmplitude);
					}
                }
            }
		}
	}

    cout << "Vous avez fait " << getStepCount() << " pas au total.\n";
}
	
