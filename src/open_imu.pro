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
    models/components/observer.cpp \
    models/components/abstractinputnode.cpp \
    models/components/abstractoutputnode.cpp \
    models/components/inputnode.cpp \
    models/components/outputnode.cpp \
    models/components/abstractalgorithm.cpp

HEADERS  += views/mainwindow.h \
    controllers/maincontroller.h \
    models/viewloader.h \
    models/json/json/json-forwards.h \
    models/json/json/json.h \
    models/layoutreader.h \
    models/components/observer.h \
    models/components/abstractinputnode.h \
    models/components/abstractoutputnode.h \
    models/components/inputnode.h \
    models/components/outputnode.h \
    models/components/abstractalgorithm.h

FORMS    += views/mainwindow.ui
