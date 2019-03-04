# OpenIMU - Data Analyser for Inertial Measurement Units and Actimetry Data

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/e2aa64a094a3435b9e76b63f5b0f0491)](https://www.codacy.com/app/SBriere/OpenIMU?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=introlab/OpenIMU&amp;utm_campaign=Badge_Grade)

## Authors
*   Dominic Létourneau (@doumdi) 
*   Simon Brière (@sbriere)

## Description
OpenIMU aims to provide an open source and free generic data importer, viewer, manager, processor and exporter for Inertial Measurement Units (IMU) and actimetry data. By using a common sensor data format and structure, data from different sources can be imported and managed in the software.
This software was developped with support from [INTER](http://regroupementinter.com).

## Features

### Current features
*   Common file format (SQLite) managed by OpenIMU, but that can also be opened from other software

*   Import recorded data from sensors:
  *   [Actigraph GTX3 series](https://www.actigraphcorp.com/actigraph-wgt3x-bt)
  
  *   [OpenIMU-MiniLogger](https://github.com/introlab/OpenIMU-MiniLogger)
  
  *   AppleWatch SensorLogger (Open-source project available soon)

*   Transfer data directly from sensors:

  *   AppleWatch SensorLogger (Open-source project available soon)

*   Data organization

  *   By participants groups
  
  *   By participants
  
  *   By recordsets
  
  *   By results
  
*   Data viewing

  *   Temporal display of recordsets to quickly see when data was recorded

  *   Sensor graph view plotting with zoom functions

  *   GPS viewer for GPS data

*   Data processing

  *   Processing module, currently supporting:
  
    *   Freedson Activity Algorithm (Freedson PS1, Melanson E, Sirard J., Calibration of the Computer Science and Applications, Inc. accelerometer., Med Sci Sports Exerc. 1998 May;30(5):777-81)

  *   Processed results viewer

*   Data exporter

  *   CSV format

### Planned features
*   English translation (currently only available in French)

*   Data splitting into sub-recordsets (by time, by day, manually)

*   Versatile data exporter (currently exporting all data, not possible to filter or change format)

*   Matlab API to access the OpenIMU file format (database)

*   More data processing modules

## Screenshots
![Screenshot_1](./docs/images/Start_Screen.png)
![Screenshot_2](./docs/images/SensorView_Screen.png)
![Screenshot_3](./docs/images/GPSView_Screen.png)
![Screenshot_4](./docs/images/Analyze_Screen.png)
![Screenshot_5](./docs/images/Results_Screen.png)

## Getting Started for Developers
Please follow those steps to setup your development environment.

### Requirements
1.  Make sure you have a valid compiler installed
  a. Linux : gcc/g++
  b. Mac : LLVM through XCode
  c. Windows: Visual Studio C++ 2017

2.  Install [CMake](https://cmake.org/download/)

3.  Install [Qt + QtCreator](https://www.qt.io/)
  a. Install the latest Desktop distribution fitting your compiling environment (will not be needed in the future)
   
4.  Install [MiniConda3](https://conda.io/miniconda.html)
  b. Install Python 3.6 version for current user (in user directory)
   
5.  Install [PyCharm Community Edition](https://www.jetbrains.com/pycharm/)

### Step 1 : Open the root CMakeLists.txt in QtCreator
1.  Opening the root CMakeLists.txt will allow to create and build the project
  a. Build the project, it will automatically generate the Python environment in env/python-3.6, PyQt UI and RCC files.
  b. All python dependencies will be automatically downloaded
  c. Once the project is built, you will not need QtCreator until you change or add a resource file or a QtDesigner ui file.
  d. If you change or add ui or resources files, you need to rebuild the project from QtCreator.

### Step 2 : Create a PyCharm project
1.  Using PyCharm, opening the directory "{PROJECT_ROOT}/python"
  a. Select the existing Python 3.6 environment in "{PROJECT_ROOT}/python/env/python-3.6" in the app menu :
    I. PyCharm->Preferences->Project:python->Project Interpreter
        
### Step 3 : Run the application
1.  Run the OpenIMUApp.py application from PyCharm
 
2.  Edit the code as you would normally do in a python program.
 
3.  Run tests in the tests directory

### Notes
1.  In a near future, we hope to have everything in the QtCreator IDE. Stay tuned!

Enjoy!    
