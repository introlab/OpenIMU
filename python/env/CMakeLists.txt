# Will try to install env if not present.
# Conda needs to be installed first

if(WIN32)
    message(STATUS "env $ENV{HOMEPATH}")
    set(CONDA_PATH "$ENV{HOMEPATH}/Miniconda3/Scripts/conda.exe")
else(WIN32)
    set(CONDA_PATH "$ENV{HOME}/miniconda3/bin/conda")
endif(WIN32)



set (ENV_PATH ${CMAKE_CURRENT_SOURCE_DIR}/python-${PYTHON_VERSION})

file(MAKE_DIRECTORY ${ENV_PATH})

# Define packages to install
set (pip_packages
    PyQt5
    PyQtChart
)

set (conda_packages
    numpy
    scipy
    PyInstaller
    jupyter
    sqlalchemy
)

if(WIN32)
    # Create environment, will produce python executable
    add_custom_command(
        OUTPUT ${ENV_PATH}/python.exe
        COMMAND ${CONDA_PATH} create -c anaconda -c conda-forge -y -p ${ENV_PATH} python=${PYTHON_VERSION} ${conda_packages}
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    )

    # Will always be considered out of date...
    # Always proceed...
    # TODO - INSTALL WITH CONDA ?
    add_custom_target(
        python-env
        COMMAND ${ENV_PATH}/Scripts/pip.exe install ${pip_packages}
        WORKING_DIRECTORY ${ENV_PATH}
        DEPENDS ${ENV_PATH}/python.exe
    )
else(WIN32)

    # Create environment, will produce python executable
    add_custom_command(
        OUTPUT ${ENV_PATH}/bin/python
        COMMAND ${CONDA_PATH} create -y -p ${ENV_PATH} python=${PYTHON_VERSION}
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    )

    # Will always be considered out of date...
    # Always proceed...
    # TODO - INSTALL WITH CONDA ?
    add_custom_target(
        python-env
        COMMAND ${ENV_PATH}/bin/pip install ${python_packages}
        WORKING_DIRECTORY ${ENV_PATH}
        DEPENDS ${ENV_PATH}/bin/python
    )
endif(WIN32)
