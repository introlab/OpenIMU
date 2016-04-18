QT += testlib widgets
QT -= gui

CONFIG += c++11

TARGET = tests
CONFIG += console
CONFIG -= app_bundle

TEMPLATE = app

SOURCES += main.cpp \
    testqstring.cpp \
    testgui.cpp \
    testbenchmark.cpp

HEADERS += \
    testqstring.h \
    testgui.h \
    testbenchmark.h
