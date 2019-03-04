#TODO MAKE THIS GENERIC
set (PYTHON_VERSION 3.6)
add_subdirectory(env)

set(PYTHON_ENV_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/env/python-${PYTHON_VERSION})
# file(MAKE_DIRECTORY ${PYTHON_ENV_DIRECTORY})

if(WIN32)
    set(PYTHON_EXECUTABLE ${PYTHON_ENV_DIRECTORY}/bin/python.exe)
    set(PYTHON_PIP_EXECUTABLE ${PYTHON_ENV_DIRECTORY}/bin/pip.exe)
    set(PYTHON_INSTALLER_EXECUTABLE ${PYTHON_ENV_DIRECTORY}/Scripts/pyinstaller.exe)

    #PyQt5 Ui wrapper
    set(PYQT5_UIC_EXECUTABLE ${PYTHON_ENV_DIRECTORY}/Scripts/pyuic5.exe)
    #PyQt5 Ressources compiler
    set(PYQT5_RCC_EXECUTABLE ${PYTHON_ENV_DIRECTORY}/Scripts/pyrcc5.exe)
    set(APP_ICON ${CMAKE_CURRENT_SOURCE_DIR}/resources/icons/OpenIMU.ico)

else(WIN32)
    set(PYTHON_EXECUTABLE ${PYTHON_ENV_DIRECTORY}/bin/python${PYTHON_VERSION})
    set(PYTHON_PIP_EXECUTABLE ${PYTHON_ENV_DIRECTORY}/bin/pip)
    set(PYTHON_INSTALLER_EXECUTABLE ${PYTHON_ENV_DIRECTORY}/bin/pyinstaller)
    #PyQt5 Ui wrapper
    set(PYQT5_UIC_EXECUTABLE ${PYTHON_ENV_DIRECTORY}/bin/pyuic5)
    #PyQt5 Ressources compiler
    set(PYQT5_RCC_EXECUTABLE ${PYTHON_ENV_DIRECTORY}/bin/pyrcc5)
    set(APP_ICON ${CMAKE_CURRENT_SOURCE_DIR}/resources/icons/OpenIMU.icns)
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
    resources/ui/ImportBrowser.ui
    resources/ui/ExportCSV.ui
    resources/ui/ProcessSelectDialog.ui
    resources/ui/GraphWidget.ui
    resources/ui/DataInfosWidget.ui
    resources/ui/ProgressDialog.ui
    resources/ui/StreamWindow.ui
    resources/ui/ImportMatchDialog.ui
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
        DEPENDS ${uifile} python-env)
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
        DEPENDS ${rcfile} python-env)
endforeach(rcfile)


add_custom_target(qml_target SOURCES ${qml})

# Find all python files
file(GLOB_RECURSE libopenimu_python_files libopenimu/*.py)
file(GLOB openimuapp_python_files *.py)

add_custom_target(python_target SOURCES ${libopenimu_python_files} ${openimuapp_python_files})

message(STATUS ${python_files})

#Dummy library
#Can we do better?
add_library(dummy STATIC ${moc_uis} ${uis} ${qrcs} ${srcs_qrcs})
add_dependencies(dummy ${python_uis} ${python_qrcs} python-env)

#PyInstaller (Beta, Still have problems with QtWebEngine not found.)
set (installer_args
    # --paths ${PYTHON_ENV_DIRECTORY}/lib/python${PYTHON_VERSION}/site-packages/PyQt5
    --hidden-import scipy._lib.messagestream
    --hidden-import sqlalchemy.ext.baked
    --hidden-import PyQt5.sip
    --hidden-import logging.config
    --clean
    -y
    #--windowed
    #--debug
    --icon ${APP_ICON}
)

add_custom_target(python_package
    COMMAND ${PYTHON_INSTALLER_EXECUTABLE} ${installer_args} ${CMAKE_CURRENT_SOURCE_DIR}/OpenIMUApp.py
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    DEPENDS python_target ${python_uis} ${python_qrcs} python-env
)


