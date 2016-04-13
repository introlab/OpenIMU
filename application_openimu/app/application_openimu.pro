#-------------------------------------------------
#
# Project created by QtCreator 2016-03-07T15:01:18
#
#-------------------------------------------------

QT       += qml quick core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = application_openimu
TEMPLATE = app

INCLUDEPATH += $$PWD/models/json

CONFIG += c++11

SOURCES += main.cpp\
    acquisition/SensorDataPerDay.cpp \
    acquisition/SensorDataPerHour.cpp \
    acquisition/SensorDataPerSecond.cpp \
    acquisition/SensorReader.cpp \
    acquisition/AccelerometerReader.cpp \
    applicationmenubar.cpp \
    mainwindow.cpp \
    models/json/jsoncpp.cpp \
    models/components/block.cpp \
    models/caneva.cpp \
    models/components/blockType/addBlock.cpp \
    models/components/blockType/subBlock.cpp \
    models/components/blockType/mulBlock.cpp \
    models/components/blockType/divBlock.cpp \
    models/components/blockType/blockFactory.cpp \
    customqmlscene.cpp \
    acquisition/GyroscopeReader.cpp \
    acquisition/MagnetometerReader.cpp \
    applicationmenu.cpp \
    views/toolbarview.cpp\
    dateselectorlabel.cpp \
    models/components/blockType/podometerBlock.cpp \
    algorithm/podometer/KalmanFilter.cpp \
    algorithm/podometer/Podometer.cpp \
    models/components/abstractinputnode.cpp \
    models/components/abstractoutputnode.cpp \
    models/components/blockType/dbwriteblock.cpp \
    newAcquisition/wimuacquisition.cpp \
    mytreewidget.cpp



HEADERS += \
    acquisition/SensorDataPerDay.h \
    acquisition/SensorDataPerHour.h \
    acquisition/SensorDataPerSecond.h \
    acquisition/SensorReader.h \
    acquisition/AccelerometerReader.h \
    applicationmenubar.h \
    mainwindow.h \
    models/components/observer.h \
    models/json/json/json-forwards.h \
    models/json/json/json.h \
    models/components/block.h \
    models/caneva.h \
    models/components/blockType/addBlock.h \
    models/components/blockType/subBlock.h \
    models/components/blockType/mulBlock.h \
    models/components/blockType/divBlock.h \
    models/components/blockType/blockFactory.h \
    customqmlscene.h \
    acquisition/GyroscopeReader.h \
    acquisition/MagnetometerReader.h \
    models/components/blockType/blockType.h \
    applicationmenu.h \
    views/toolbarview.h\
    controllers/toolbarcontroller.h \
    dateselectorlabel.h \
    models/components/blockType/podometerblock.h \
    algorithm/podometer/KalmanFilter.h \
    algorithm/podometer/Podometer.h \
    models/components/abstractinputnode.h \
    models/components/inputnode.h \
    models/components/abstractoutputnode.h \
    models/components/outputnode.h \
    models/components/workerthreads.h \
    models/components/quickitemoutputnodes.h \
    models/components/quickiteminputnodeshandles.h \
    models/components/quickiteminputnodes.h \
    models/components/blockType/dbwriteblock.h \
    newAcquisition/wimuacquisition.h \
    mytreewidget.h

FORMS += widget.ui

RESOURCES += qml.qrc \
    images.qrc

# Additional import path used to resolve QML modules in Qt Creator's code model
QML_IMPORT_PATH = $$PWD/..

QSG_RENDERER_DEBUG=dump

# Default rules for deployment.
include(deployment.pri)


