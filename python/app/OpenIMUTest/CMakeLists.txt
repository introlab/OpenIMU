find_package(Qt5Core REQUIRED)
#find_package(Qt5Widgets REQUIRED)

#This will generate ui_ files (not needed by python)
SET(uis
    MainWindow.ui
)

SET(qrcs
    core.qrc
)

# generate rules for building source files from the resources
QT5_ADD_RESOURCES(srcs_qrcs ${qrcs})

#Generate .h files from the .ui files
#QT5_WRAP_UI(moc_uis ${uis})


# Generate PyQt5 ui files
set(python_uis)
foreach(uifile ${uis})
    message(STATUS "Processing ${uifile}")

    #Add py extension to file
    set(output_file ${uifile}.py)
    list(APPEND python_uis ${output_file})
    add_custom_command(OUTPUT ${output_file}
                   COMMAND ${PYQT5_UIC_EXECUTABLE} ${uifile} -o ${output_file}
                   DEPENDS ${uifile}
                   WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                   VERBATIM)

endforeach(uifile)

# Generate PyQt5 resources file
set (python_qrcs)
foreach(rcfile ${qrcs})
    message(STATUS "Processing ${rcfile}")

    #Add py extension to file
    set(output_file ${rcfile}.py)
    list(APPEND python_qrcs ${output_file})
    add_custom_command(OUTPUT ${output_file}
                   COMMAND ${PYQT5_RCC_EXECUTABLE} ${rcfile} -o ${output_file}
                   DEPENDS ${rcfile}
                   WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                   VERBATIM)

endforeach(rcfile)


#Dummy library
#Can we do better?
add_library(dummy STATIC ${moc_uis} ${uis} ${qrcs} ${srcs_qrcs} ${python_uis} ${python_qrcs})

