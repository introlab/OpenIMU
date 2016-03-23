QT += core
QT -= gui

CONFIG += c++11

TARGET = OpenImuCore
CONFIG += console
CONFIG -= app_bundle

TEMPLATE = app

INCLUDEPATH += $$PWD/models/json

SOURCES += main.cpp \
    models/components/inputnode.cpp \
    models/components/observer.cpp \
    models/components/outputnode.cpp \
    models/json/jsoncpp.cpp \
    models/components/block.cpp \
    models/caneva.cpp

HEADERS += \
    models/components/inputnode.h \
    models/components/observer.h \
    models/components/outputnode.h \
    models/json/json/json-forwards.h \
    models/json/json/json.h \
    models/components/block.h \
    models/caneva.h
