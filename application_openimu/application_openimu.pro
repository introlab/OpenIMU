#-------------------------------------------------
#
# Project created by QtCreator 2016-03-07T15:01:18
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = application_openimu
TEMPLATE = app

INCLUDEPATH += $$PWD/../../qwt-6.1.2/src

win32:CONFIG(release, debug|release): LIBS += -L$$PWD/../../qwt-6.1.2/lib/ -lqwt
else:win32:CONFIG(debug, debug|release): LIBS += -L$$PWD/../../qwt-6.1.2/lib/ -lqwtd
else:unix: LIBS += -L$$PWD/../../qwt-6.1.2/lib/ -lqwt

CONFIG += c++11

SOURCES += main.cpp\
     widget.cpp \
    SensorDataPerDay.cpp \
    SensorDataPerHour.cpp \
    SensorDataPerSecond.cpp \
    SensorReader.cpp \
    AccelerometerReader.cpp \
    applicationmenubar.cpp \
    mainwindow.cpp

HEADERS += widget.h \
    SensorDataPerDay.h \
    SensorDataPerHour.h \
    SensorDataPerSecond.h \
    SensorReader.h \
    AccelerometerReader.h \
    applicationmenubar.h \
    mainwindow.h

FORMS += widget.ui
