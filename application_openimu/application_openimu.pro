#-------------------------------------------------
#
# Project created by QtCreator 2016-03-07T15:01:18
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = application_openimu
TEMPLATE = app

INCLUDEPATH += $$PWD/../../qwt-6.1.2/src $$PWD/models/json

win32:CONFIG(release, debug|release): LIBS += -L$$PWD/../../qwt-6.1.2/lib/ -lqwt
else:win32:CONFIG(debug, debug|release): LIBS += -L$$PWD/../../qwt-6.1.2/lib/ -lqwtd
else:unix: LIBS += -L$$PWD/../../qwt-6.1.2/lib/ -lqwt

CONFIG += c++11 console

SOURCES += main.cpp\
    widget.cpp \
    acquisition/SensorDataPerDay.cpp \
    acquisition/SensorDataPerHour.cpp \
    acquisition/SensorDataPerSecond.cpp \
    acquisition/SensorReader.cpp \
    acquisition/AccelerometerReader.cpp \
    applicationmenubar.cpp \
    mainwindow.cpp \
    models/components/inputnode.cpp \
    models/components/observer.cpp \
    models/components/outputnode.cpp \
    models/json/jsoncpp.cpp \
    models/components/block.cpp \
    models/caneva.cpp

HEADERS += widget.h \
    acquisition/SensorDataPerDay.h \
    acquisition/SensorDataPerHour.h \
    acquisition/SensorDataPerSecond.h \
    acquisition/SensorReader.h \
    acquisition/AccelerometerReader.h \
    applicationmenubar.h \
    mainwindow.h \
    models/components/inputnode.h \
    models/components/observer.h \
    models/components/outputnode.h \
    models/json/json/json-forwards.h \
    models/json/json/json.h \
    models/components/block.h \
    models/caneva.h

FORMS += widget.ui
