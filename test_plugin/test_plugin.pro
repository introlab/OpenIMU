#-------------------------------------------------
#
# Project created by QtCreator 2016-04-15T17:47:36
#
#-------------------------------------------------

QT       += core gui widgets quick charts

Debug:TARGET = mulblockd
Release:TARGET = mulblock
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
    mulBlock.cpp

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
    mulblockplugin.h \
    mulblockgenerator.h \
    mulBlock.h

unix {
    target.path = /usr/lib
    INSTALLS += target
}

DISTFILES += \
    mulblockplugin.json
