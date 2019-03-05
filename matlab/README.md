# OpenIMU - Data Analyser for Inertial Measurement Units and Actimetry Data
# MATLAB scripts

## Authors
*   Antoine Guillerand

## Description
Matlab scripts contained in this folder are used to access the OpenIMU file format (database) from Matlab, allowing easy manipulation and prototyping of analysis scripts.

## Usage
Each of the scripts starting with "get" are used to access data from the file format. 
Currently, only Apple Watch data has been tested, but the scripts should be working with other sensors as well.

Example of use to load multiple datas is provided in the "MainOIReader.m" script.

## Installation
1.  Install JDBC driver for SQLite in Matlab (see [SQLite JDBC for Windows](https://www.mathworks.com/help/database/ug/sqlite-jdbc-windows.html) )

2.  Copy the scripts and run them, making sure to change the parameters in the files for your setup (database name, driver location, date, participant id)

## Notes

Enjoy!    
