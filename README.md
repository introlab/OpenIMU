# OpenIMU

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


### Step 1 : Create a PyCharm project
1. Using PyCharm, create a project by opening the file "{PROJECT_ROOT}/python/app/OpenIMUTest/OpenIMUTest.py"
    1. Create a Python 3.5 environment using conda in "{PROJECT_ROOT}/python/env/python-3.5"
    1. Use the conda package manager and install the following packages :
        1. PyQt5, PyQtChart, PyInstaller, scipy, numpy, jupyter

### Step 2 : Open the root CMakeLists.txt in QtCreator
1. Opening the root CMakeLists.txt will allow to create and build the project
    1. Build the project, it will automatically generate the PyQt UI and RCC files.
    1. TODO : We hope to automate the creation of the Python environment in the future and automatically install the dependencies
    1. Once the project is built, you will not need QtCreator until you change or add a resource file or a QtDesigner ui file.
    
### Step 3: Back to PyCharm for good.
1. Run the OpenIMUTest.py application from PyCharm
2. Edit the code as you would normally do in a python program.


### Notes
1. In a near future, we hope to have everything in the QtCreator IDE. Stay tuned!

Enjoy!    