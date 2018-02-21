#Generate the python environment
#Will need Anaconda
#Python 3.5 required

# Example:
# conda create python=3.5 -p /Users/dominic/WA/OpenIMU.git/python/env

# Dans le répertoire env, installer les packages: PyQt5, PyInstaller, numpy, scipy
# pip install PyQt5, PyQtChart, PyInstaller, scipy, numpy

#find_package( PythonInterp 3.5 REQUIRED )
#find_package( PythonLibs 3.5 REQUIRED )

#PYTHONINTERP_FOUND         - Was the Python executable found
#PYTHON_EXECUTABLE          - path to the Python interpreter

#TODO MAKE THIS GENERIC
set(PYTHON_EXECUTABLE ${CMAKE_CURRENT_SOURCE_DIR}/env/python-3.5/bin/python)
set(PYTHON_PIP_EXECUTABLE ${CMAKE_CURRENT_SOURCE_DIR}/env/python-3.5/bin/pip)

#PyQt5 Ui wrapper
set(PYQT5_UIC_EXECUTABLE ${CMAKE_CURRENT_SOURCE_DIR}/env/python-3.5/bin/pyuic5)
#PyQt5 Ressources compiler
set(PYQT5_RCC_EXECUTABLE ${CMAKE_CURRENT_SOURCE_DIR}/env/python-3.5/bin/pyrcc5)

add_subdirectory(app)
