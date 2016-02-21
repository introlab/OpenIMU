#include <stdio.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <windows.h>
#include "AccelerometerReader.h"

using namespace std;

int main( int argc, const char* argv[] )
{
	AccelerometerReader accReader("C:\\Users\\stef\\Desktop\\Projet S7-S8\\data_WIMU\\data_WIMU");
	accReader.LoadAccelerometerData();
	return 0;
}