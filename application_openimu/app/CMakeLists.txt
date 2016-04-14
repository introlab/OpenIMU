find_package(Qt5Core    REQUIRED)
find_package(Qt5Gui     REQUIRED)
find_package(Qt5Widgets REQUIRED)
find_package(Qt5Quick   REQUIRED)
find_package(Qt5Charts	REQUIRED)

#TODO
#Add subdirectories here
SET(srcs
    acquisition/SensorDataPerDay.cpp
    acquisition/SensorDataPerHour.cpp
    acquisition/SensorDataPerSecond.cpp
    acquisition/SensorReader.cpp
    acquisition/AccelerometerReader.cpp
    applicationmenubar.cpp
    mainwindow.cpp
    models/json/jsoncpp.cpp
    models/components/block.cpp
    models/caneva.cpp
    models/components/blockType/addBlock.cpp
    models/components/blockType/subBlock.cpp
    models/components/blockType/mulBlock.cpp
    models/components/blockType/divBlock.cpp
    models/components/blockType/blockFactory.cpp
    customqmlscene.cpp
    acquisition/GyroscopeReader.cpp
    acquisition/MagnetometerReader.cpp
    views/toolbarview.cpp
    dateselectorlabel.cpp
    models/components/blockType/podometerBlock.cpp
    algorithm/podometer/KalmanFilter.cpp
    algorithm/podometer/Podometer.cpp
    models/components/abstractinputnode.cpp
    models/components/abstractoutputnode.cpp
    models/components/blockType/dbwriteblock.cpp
    newAcquisition/wimuacquisition.cpp
    mytreewidget.cpp
    accdatadisplay.cpp
)


#TODO
#Add subdirectories here
SET(headers
    acquisition/SensorDataPerDay.h
       acquisition/SensorDataPerHour.h
       acquisition/SensorDataPerSecond.h
       acquisition/SensorReader.h
       acquisition/AccelerometerReader.h
       applicationmenubar.h
       mainwindow.h
       models/components/observer.h
       models/json/json/json-forwards.h
       models/json/json/json.h
       models/components/block.h
       models/caneva.h
       models/components/blockType/addBlock.h
       models/components/blockType/subBlock.h
       models/components/blockType/mulBlock.h
       models/components/blockType/divBlock.h
       models/components/blockType/blockFactory.h
       customqmlscene.h
       acquisition/GyroscopeReader.h
       acquisition/MagnetometerReader.h
       models/components/blockType/blockType.h
       views/toolbarview.h
       dateselectorlabel.h
       models/components/blockType/podometerblock.h
       algorithm/podometer/KalmanFilter.h
       algorithm/podometer/Podometer.h
       models/components/abstractinputnode.h
       models/components/inputnode.h
       models/components/abstractoutputnode.h
       models/components/outputnode.h
       models/components/workerthreads.h
       models/components/quickitemoutputnodes.h
       models/components/quickiteminputnodeshandles.h
       models/components/quickiteminputnodes.h
       models/components/blockType/dbwriteblock.h
       newAcquisition/wimuacquisition.h
       mytreewidget.h
       accdatadisplay.h
)

SET(uis
    widget.ui
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
TARGET_LINK_LIBRARIES(application_openimu vbLabel)






