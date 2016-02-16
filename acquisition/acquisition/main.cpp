#include <stdio.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <windows.h>

using namespace std;
typedef unsigned char BYTE;
const int freq=50;

void LoadAccelerometerdata();
void showX(BYTE* ,int);

int main( int argc, const char* argv[] )
{
	LoadAccelerometerdata();
	return 0;
}

long getFileSize(FILE *file)
{
	long lCurPos, lEndPos;
	lCurPos = ftell(file);
	fseek(file, 0, 2);
	lEndPos = ftell(file);
	fseek(file, lCurPos, 0);
	return lEndPos;
}
void LoadAccelerometerdata()
{
	const char *filePath = "C:\\ACC_4.DAT";	
	BYTE *fileBuf;			// Pointer to our buffered data
	FILE *file = NULL;		// File pointer

	// Open the file in binary mode using the "rb" format string
	// This also checks if the file exists and/or can be opened for reading correctly
	if ((file = fopen(filePath, "rb")) == NULL)
		cout << "Could not open specified file" << endl;
	else
		cout << "File opened successfully" << endl;

	// Get the size of the file in bytes
	long fileSize = getFileSize(file);

	// Allocate space in the buffer for the whole file
	fileBuf = new BYTE[fileSize];

	// Read the file in to the buffer
	fread(fileBuf, fileSize, 1, file);

	showX(fileBuf,0);
	cin.get();
	delete[]fileBuf;
    fclose(file);   // Almost forgot this 
}

void showX(BYTE* fileBuf, int start)
{
	int time=0;
	for (int i = start; i < start+4; i++)
	{
		time+=fileBuf[i];
		int shift = ((i==start+3)? 1:0x100);
		time*=shift;
	}
	printf("TIMESTAMP: %X \n", time);
	signed short int accx[freq];
	signed short int accy[freq];
	signed short int accz[freq];
	for (int i = 0; i < freq; i++)
	{
		accx[i]= fileBuf[start+4+2*i]*0x100+fileBuf[start+4+2*i+1];
		printf("Acceleration X: %d \n", accx[i]);
	}
	cout<<endl;
	for (int i = 0; i < freq; i++)
	{
		accy[i]= fileBuf[start+4+2*freq+2*i]*0x100+fileBuf[start+4+2*freq+2*i+1];
		printf("Acceleration Y: %d \n", accy[i]);
	}
	cout<<endl;
	for (int i = 0; i < freq; i++)
	{
		accz[i]= fileBuf[start+4+4*freq+2*i]*0x100+fileBuf[start+4+4*freq+2*i+1];
		printf("Acceleration Z: %d \n", accz[i]);
	}
	cout<<endl;

}