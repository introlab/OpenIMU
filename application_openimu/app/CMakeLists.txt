find_package(Qt5Core    REQUIRED)
find_package(Qt5Gui     REQUIRED)
find_package(Qt5Widgets REQUIRED)
find_package(Qt5Quick   REQUIRED)
find_package(Qt5Charts	REQUIRED)


add_subdirectory(acquisition)
add_subdirectory(algorithm)
add_subdirectory(dialogs)
add_subdirectory(models)
add_subdirectory(newAcquisition)
add_subdirectory(views)

SET(srcs
    ${srcs}
    accdatadisplay.cpp
    applicationmenubar.cpp
    customqmlscene.cpp
    dateselectorlabel.cpp
    mainwindow.cpp
    mytreewidget.cpp
    rangeslider.cpp
)

SET(headers
    ${headers}
    accdatadisplay.h
    applicationmenubar.h
    customqmlscene.h
    dateselectorlabel.h
    mainwindow.h
    mytreewidget.h
    rangeslider.h
)

SET(uis
    widget.ui
    help.ui
    about.ui
)

SET(qrc
    qml.qrc
    images.qrc
)

SET(qml

)

#TODO Fix the QML_IMPORT_PATH
set (QML_IMPORT_PATH
    ${CMAKE_CURRENT_SOURCE_DIR}/..
	 ${EXECUTABLE_OUTPUT_PATH}
)
set (QML2_IMPORT_PATH ${QML_IMPORT_PATH})
add_definitions(-DQML_IMPORT_PATH=${QML_IMPORT_PATH})
add_definitions(-DQML2_IMPORT_PATH=${QML2_IMPORT_PATH})



#Binary dir Required for ui_ files includes
include_directories(
    ${CMAKE_CURRENT_BINARY_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/models/json
    ${CMAKE_CURRENT_SOURCE_DIR}/views
    )

# generate rules for building source files from the resources
QT5_ADD_RESOURCES(srcs_qrc ${qrc})

#Generate .h files from the .ui files
QT5_WRAP_UI(moc_uis ${uis})

#This will generate moc_* for Qt
QT5_WRAP_CPP(moc_srcs ${headers})


#Application
add_executable(application_openimu main.cpp ${srcs} ${headers} ${moc_srcs} ${moc_uis} ${srcs_qrc} ${qml})
qt5_use_modules(application_openimu Sql Core Network Xml XmlPatterns Gui Widgets Quick Charts)
TARGET_LINK_LIBRARIES(application_openimu)






