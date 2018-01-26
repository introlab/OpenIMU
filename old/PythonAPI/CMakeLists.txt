#PythonAPI must be installed

#Get all python files in the subdirectory
file(GLOB_RECURSE python_srcs RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "src/*.py")
file(GLOB_RECURSE python_libs RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "lib/*.py")

#Debug
#message(STATUS " SRCS ${python_srcs}")
#message(STATUS " LIBS ${python_libs}")

#This will display the files in the project
add_custom_target(python_files SOURCES ${python_srcs} ${python_libs})

if(APPLE)

    #Create directory
    set(BUNDLE_EXECUTABLE_PATH "${EXECUTABLE_OUTPUT_PATH}/applicationOpenimu.app/Contents/MacOS")

    if (EXISTS ${BUNDLE_EXECUTABLE_PATH})
        #Create directory
        file(MAKE_DIRECTORY ${BUNDLE_EXECUTABLE_PATH}/PythonAPI)

        message(STATUS "Copy Python files to : ${BUNDLE_EXECUTABLE_PATH}/PythonAPI")

        #Copy API Files
        file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/src DESTINATION ${BUNDLE_EXECUTABLE_PATH}/PythonAPI)
        file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/lib DESTINATION ${BUNDLE_EXECUTABLE_PATH}/PythonAPI)

    endif()
endif()
