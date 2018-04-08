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

add_subdirectory(env)

set(PYTHON_ENV_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/env/python-3.6)
# file(MAKE_DIRECTORY ${PYTHON_ENV_DIRECTORY})

if(WIN32)
    set(PYTHON_EXECUTABLE ${PYTHON_ENV_DIRECTORY}/bin/python.exe)
    set(PYTHON_PIP_EXECUTABLE ${PYTHON_ENV_DIRECTORY}/bin/pip.exe)

    #PyQt5 Ui wrapper
    set(PYQT5_UIC_EXECUTABLE ${PYTHON_ENV_DIRECTORY}/Scripts/pyuic5.exe)
    #PyQt5 Ressources compiler
    set(PYQT5_RCC_EXECUTABLE ${PYTHON_ENV_DIRECTORY}/Scripts/pyrcc5.exe)

else(WIN32)
    set(PYTHON_EXECUTABLE ${PYTHON_ENV_DIRECTORY}/bin/python)
    set(PYTHON_PIP_EXECUTABLE ${PYTHON_ENV_DIRECTORY}/bin/pip)
    #PyQt5 Ui wrapper
    set(PYQT5_UIC_EXECUTABLE ${PYTHON_ENV_DIRECTORY}/bin/pyuic5)
    #PyQt5 Ressources compiler
    set(PYQT5_RCC_EXECUTABLE ${PYTHON_ENV_DIRECTORY}/bin/pyrcc5)
endif(WIN32)

find_package(Qt5Core REQUIRED)
#find_package(Qt5Widgets REQUIRED)

#This will generate ui_ files (not needed by python)
SET(uis
    resources/ui/MainWindow.ui
    resources/ui/StartDialog.ui
    resources/ui/ImportDialog.ui
    resources/ui/ImportManager.ui
    resources/ui/GroupWidget.ui
    resources/ui/ParticipantWidget.ui
    resources/ui/RecordsetWidget.ui
    resources/ui/ResultWidget.ui
)

SET(qrcs
    resources/core.qrc
)

SET(qml
    resources/test.qml
)

# generate rules for building source files from the resources
QT5_ADD_RESOURCES(srcs_qrcs ${qrcs})

#Generate .h files from the .ui files
#QT5_WRAP_UI(moc_uis ${uis})

file(MAKE_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/resources/ui/python)

# Generate PyQt5 ui files
set(python_uis)
foreach(uifile ${uis})
    message(STATUS "Processing ${uifile}")
    get_filename_component (name_without_extension ${uifile} NAME_WE)
    #Add py extension to file
    set(output_file ${name_without_extension}_ui.py)
    list(APPEND python_uis ${output_file})
    add_custom_target(${output_file}
        COMMAND ${PYQT5_UIC_EXECUTABLE} ${uifile} -o resources/ui/python/${output_file}
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        DEPENDS ${uifile})
endforeach(uifile)

# Generate PyQt5 resources file
set (python_qrcs)
foreach(rcfile ${qrcs})
    message(STATUS "Processing ${rcfile}")
    get_filename_component (name_without_extension ${rcfile} NAME_WE)
    #Add py extension to file
    set(output_file ${name_without_extension}_rc.py)
    list(APPEND python_qrcs ${output_file})
    add_custom_target(${output_file}
        COMMAND ${PYQT5_RCC_EXECUTABLE} ${rcfile} -o ${output_file}
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        DEPENDS ${rcfile})
endforeach(rcfile)


#Dummy library
#Can we do better?
add_library(dummy STATIC ${moc_uis} ${uis} ${qrcs} ${srcs_qrcs})
add_dependencies(dummy ${python_uis} ${python_qrcs} python-env)

add_custom_target(qml_files SOURCES ${qml})



