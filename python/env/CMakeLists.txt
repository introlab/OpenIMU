# Will try to install env if not present.
# Conda needs to be installed first

if(WIN32)
    message(STATUS "env $ENV{HOMEPATH}")
    set(CONDA_PATH "$ENV{SYSTEMDRIVE}$ENV{HOMEPATH}/Miniconda3/Scripts/conda.exe")
else(WIN32)
    set(CONDA_PATH "$ENV{HOME}/miniconda3/bin/conda")
endif(WIN32)



set (ENV_PATH ${CMAKE_CURRENT_SOURCE_DIR}/python-${PYTHON_VERSION})

file(MAKE_DIRECTORY ${ENV_PATH})

# Default packages.
set (pip_packages
    PyQt5
    PyQtChart
    PyQt3D
)

set (conda_packages
    cython
    numpy
    scipy
    # Not used for now
    # jupyter
    sqlalchemy
    alembic
)


# Define custom packages to install
if(WIN32)
    set (pip_packages
        ${pip_packages}
        pypiwin32
        PyInstaller
    )

    set (conda_packages
        ${conda_packages}
        PyInstaller
    )
else(WIN32)
    set (pip_packages
        ${pip_packages}
        PyInstaller
        # Warning, development version for now to fix OSX package
        # https://github.com/pyinstaller/pyinstaller/tarball/develop
    )
endif(WIN32)



if(WIN32)
    # Create environment, will produce python executable
    add_custom_command(
        OUTPUT ${ENV_PATH}/python.exe
        COMMAND ${CONDA_PATH} install -m -c defaults -c conda-forge -y -p ${ENV_PATH} python=${PYTHON_VERSION} ${conda_packages}
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
        OUTPUT ${ENV_PATH}/bin/python${PYTHON_VERSION}
        COMMAND ${CONDA_PATH} install -m -c defaults -c conda-forge -y -p ${ENV_PATH} python=${PYTHON_VERSION} ${conda_packages}
        COMMAND ${CMAKE_COMMAND} -E create_symlink ${ENV_PATH}/bin/python${PYTHON_VERSION} ${ENV_PATH}/bin/python
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    )

    add_custom_target(python_symlink
        COMMAND ${CMAKE_COMMAND} -E create_symlink ${ENV_PATH}/bin/python${PYTHON_VERSION} ${ENV_PATH}/bin/python
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        DEPENDS ${ENV_PATH}/bin/python${PYTHON_VERSION}
    )

    # Will always be considered out of date...
    # Always proceed...
    # TODO - INSTALL WITH CONDA ?
    add_custom_target(
        python-env
        COMMAND ${ENV_PATH}/bin/python${PYTHON_VERSION} -m pip install ${pip_packages}
        WORKING_DIRECTORY ${ENV_PATH}/bin
        DEPENDS python_symlink
    )
endif(WIN32)
