#-------------------------------------------------
#
# Project created by QtCreator 2016-04-15T17:47:36
#
#-------------------------------------------------

QT       += core quick

Debug:TARGET = madgwickblockd
Release:TARGET = madgwickblock
TEMPLATE = lib
CONFIG += plugin
CONFIG += c++11

DESTDIR = lib

INCLUDEPATH += ../application_openimu/app/models/json
INCLUDEPATH += ../application_openimu/app/models/components

SOURCES += \
    ../application_openimu/app/models/components/abstractinputnode.cpp \
    ../application_openimu/app/models/components/abstractoutputnode.cpp \
    ../application_openimu/app/models/components/block.cpp \
    madgwickBlock.cpp \
    MadgwickAHRS.cpp \
    ../application_openimu/app/newAcquisition/wimuacquisition.cpp

HEADERS += \
DISTFILES += \
    ../application_openimu/app/models/components/abstractinputnode.h \
    ../application_openimu/app/models/components/abstractoutputnode.h \
    ../application_openimu/app/models/components/block.h \
    ../application_openimu/app/models/components/inputnode.h \
    ../application_openimu/app/models/components/observer.h \
    ../application_openimu/app/models/components/outputnode.h \
    ../application_openimu/app/models/components/quickiteminputnodes.h \
    ../application_openimu/app/models/components/quickiteminputnodeshandles.h \
    ../application_openimu/app/models/components/quickitemoutputnodes.h \
    ../application_openimu/app/models/components/workerthreads.h \
    ../application_openimu/app/models/components/blockgenerator.h \
    ../application_openimu/app/models/components/blockplugin.h \
    madgwickBlock.h \
    madgwickblockgenerator.h \
    madgwickblockplugin.h \
    MadgwickAHRS.h \
    ../application_openimu/app/newAcquisition/wimuacquisition.h

unix {
    target.path = /usr/lib
    INSTALLS += target
}

DISTFILES += \
    madgwickblockplugin.json
