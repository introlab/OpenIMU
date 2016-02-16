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
    models/connectors/connector.cpp \
    controllers/maincontroller.cpp \
    models/viewloader.cpp \
    models/json/jsoncpp.cpp \
    models/layoutreader.cpp

HEADERS  += views/mainwindow.h \
    models/connectors/connector.h \
    controllers/maincontroller.h \
    models/viewloader.h \
    models/json/json/json-forwards.h \
    models/json/json/json.h \
    models/layoutreader.h

FORMS    += views/mainwindow.ui
