# OpenIMU - Data Analyser for Inertial Measurement Units and Actimetry Data

## Authors
* Dominic Létourneau (@doumdi) 
* Simon Brière (@sbriere)

## Getting Started for Developers
Please follow those steps to setup your development environment.

### Requirements
1. Install [CMake](https://cmake.org/download/)
1. Install [Qt + QtCreator](https://www.qt.io/) 
1. Install [MiniConda3](https://conda.io/miniconda.html)
    1. Install Python 3.6 version in the default directory
    1. You can also install the full Anaconda distribution, but it is not required.
1. Install [PyCharm Community Edition](https://www.jetbrains.com/pycharm/)

### Step 1 : Open the root CMakeLists.txt in QtCreator
1. Opening the root CMakeLists.txt will allow to create and build the project
    1. Build the project, it will automatically generate the Python environment in env/python-3.6, PyQt UI and RCC files.
    1. Once the project is built, you will not need QtCreator until you change or add a resource file or a QtDesigner ui file.
    1. If you change or add ui or resources files, you need to rebuild the project from QtCreator.

### Step 2 : Create a PyCharm project
1. Using PyCharm, create a project by opening the file "{PROJECT_ROOT}/python/"
    1. Select the Python 3.6 environment using conda in "{PROJECT_ROOT}/python/env/python-3.6"
        
### Step 3 : Run the application
1. Run the OpenIMUApp.py application from PyCharm
2. Edit the code as you would normally do in a python program.

### Notes
1. In a near future, we hope to have everything in the QtCreator IDE. Stay tuned!

Enjoy!    
