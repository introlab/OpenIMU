#include "stepCounter.h"
#include <math.h>

stepCounter::stepCounter(std::vector<frame> *_data,int windowSize)
{
	data=_data;
    movingAverage(windowSize);
}


stepCounter::~stepCounter(void)
{
}
void stepCounter::movingAverage(int windowSize)
{
	double sum=0;
	for(int j=0;j<windowSize;j++)
	{
		sum+=sqrt(pow(data->at(j).x,2.0)
			+pow(data->at(j).y,2.0)
			+pow(data->at(j).z,2.0));
	}
	filteredData.push_back(sum/windowSize);
	for (int i=1;i<data->size()-windowSize;i++)
	{
		sum-=sqrt(pow(data->at(i-1).x,2.0)
			+pow(data->at(i-1).y,2.0)+
			pow(data->at(i-1).z,2.0));
		sum+=sqrt(pow(data->at(i+windowSize-1).x,2.0)
			+pow(data->at(i+windowSize-1).y,2.0)+
			pow(data->at(i+windowSize-1).z,2.0));
		filteredData.push_back(sum/windowSize);
	}
}
int stepCounter::detect_peak(double delta /* delta used for distinguishing peaks */)
{
	//int*            emi_peaks = new int(); /* emission peaks will be put here */ 
	int            num_emi_peaks; /* number of emission peaks found */
	//int*            absop_peaks = new int(); /* absorption peaks will be put here */ 
	int            num_absop_peaks; /* number of absorption peaks found */
	int     i;
	double  mx;
	double  mn;
	int     mx_pos = 0;
	int     mn_pos = 0;
	int     is_detecting_emi = 1;


	mx = filteredData.at(0);
	mn = filteredData.at(0);

	num_emi_peaks = 0;
	num_absop_peaks = 0;

	for(i = 1; i < filteredData.size(); ++i)
	{
		if(filteredData.at(i) > mx)
		{
			mx_pos = i;
			mx = filteredData.at(i);
		}
		if(filteredData.at(i) < mn)
		{
			mn_pos = i;
			mn = filteredData.at(i);
		}

		if(is_detecting_emi &&
			filteredData.at(i) < mx - delta)
		{
			//emi_peaks[num_emi_peaks] = mx_pos;
			++ (num_emi_peaks);

			is_detecting_emi = 0;

			i = mx_pos - 1;

			mn = filteredData.at(mx_pos);
			mn_pos = mx_pos;
		}
		else if((!is_detecting_emi) &&
			filteredData.at(i) > mn + delta)
		{
			//absop_peaks[num_absop_peaks] = mn_pos;
			++ (num_absop_peaks);
			is_detecting_emi = 1;
			i = mn_pos - 1;
			mx = filteredData.at(mn_pos);
			mx_pos = mn_pos;
		}
	}

	return num_emi_peaks;
}
