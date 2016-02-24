#include <stdio.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <windows.h>
#include "AccelerometerReader.h"
#include "GyroscopeReader.h"
#include "MagnetometerReader.h"

using namespace std;

int main( int argc, const char* argv[] )
{
	AccelerometerReader accReader("C:\\Users\\stef\\Desktop\\Projet S7-S8\\data_WIMU\\data_WIMU");
	accReader.LoadSensorData();

	GyroscopeReader gyrReader("C:\\Users\\stef\\Desktop\\Projet S7-S8\\data_WIMU\\data_WIMU");
	gyrReader.LoadSensorData();

	MagnetometerReader magReader("C:\\Users\\stef\\Desktop\\Projet S7-S8\\data_WIMU\\data_WIMU");
	magReader.LoadSensorData();
	
	return 0;
}