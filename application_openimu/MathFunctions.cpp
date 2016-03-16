#include "MathFunctions.h"
#include <math.h>

MathFunctions::MathFunctions(void)
{
}


MathFunctions::~MathFunctions(void)
{
}

double MathFunctions::computeNorm(double x, double y, double z){
	double norm = sqrt(pow(x,2)+ pow(y,2)+ pow(z,2));
	return norm/9.80665;
}

