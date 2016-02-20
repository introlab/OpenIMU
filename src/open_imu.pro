#-------------------------------------------------
#
# Project created by QtCreator 2016-02-03T12:02:44
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = open_imu
TEMPLATE = app

INCLUDEPATH += $$PWD/models/json

SOURCES += main.cpp\
        views/mainwindow.cpp \
    controllers/maincontroller.cpp \
    models/viewloader.cpp \
    models/json/jsoncpp.cpp \
    models/layoutreader.cpp \
    models/connectors/input.cpp \
    models/connectors/output.cpp \
    models/ialgo.cpp \
    models/connectors/iconnector.cpp \
    models/observer.cpp

HEADERS  += views/mainwindow.h \
    controllers/maincontroller.h \
    models/viewloader.h \
    models/json/json/json-forwards.h \
    models/json/json/json.h \
    models/layoutreader.h \
    models/connectors/input.h \
    models/connectors/output.h \
    models/ialgo.h \
    models/connectors/iconnector.h \
    models/observer.h

FORMS    += views/mainwindow.ui
