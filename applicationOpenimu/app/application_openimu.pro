#-------------------------------------------------
#
# Project created by QtCreator 2016-03-07T15:01:18
#
#-------------------------------------------------

QT       += qml quick core gui



greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = application_openimu
TEMPLATE = app

INCLUDEPATH += $$PWD/core/json
INCLUDEPATH += $$PWD/../../../build-qtcharts-Kit_Qt-Debug/include


#win32:CONFIG(release, debug|release): LIBS += -L$$PWD/../../../build-qtcharts-Kit_Qt-Debug/lib/ -lQt5Charts
#else:win32:CONFIG(debug, debug|release): LIBS += -L$$PWD/../../../build-qtcharts-Kit_Qt-Debug/lib/ -lQt5Chartsd
#else:unix: LIBS += -L$$PWD/../../../build-qtcharts-Kit_Qt-Debug/lib/ -lQt5Charts

QT += charts

CONFIG += c++11

SOURCES += main.cpp\
    applicationmenubar.cpp \
    mainwindow.cpp \
    core/json/jsoncpp.cpp \
    core/components/block.cpp \
    core/caneva.cpp \
    core/components/blockType/addBlock.cpp \
    core/components/blockType/subBlock.cpp \
    core/components/blockType/divBlock.cpp \
    core/components/blockType/blockFactory.cpp \
    customqmlscene.cpp \
    dateselectorlabel.cpp \
    core/components/blockType/podometerBlock.cpp \
    core/components/abstractinputnode.cpp \
    core/components/abstractoutputnode.cpp \
    core/components/blockType/dbwriteblock.cpp \
    acquisition/wimuacquisition.cpp \
    mytreewidget.cpp \
    accdatadisplay.cpp \
    core/components/blockType/activitytrackerblock.cpp \
    core/components/blockgenerator.cpp \
    dialogs/aboutdialog.cpp \
    dialogs/helpdialog.cpp \
    rangeslider.cpp \
    algorithm/podometer/stepCounter.cpp



HEADERS += \
    applicationmenubar.h \
    mainwindow.h \
    core/components/observer.h \
    core/json/json/json-forwards.h \
    core/json/json/json.h \
    core/components/block.h \
    core/caneva.h \
    core/components/blockType/addBlock.h \
    core/components/blockType/subBlock.h \
    core/components/blockType/divBlock.h \
    core/components/blockType/blockFactory.h \
    customqmlscene.h \
    core/components/blockType/blockType.h \
    dateselectorlabel.h \
    core/components/blockType/podometerblock.h \
    core/components/abstractinputnode.h \
    core/components/inputnode.h \
    core/components/abstractoutputnode.h \
    core/components/outputnode.h \
    core/components/workerthreads.h \
    core/components/quickitemoutputnodes.h \
    core/components/quickiteminputnodeshandles.h \
    core/components/quickiteminputnodes.h \
    core/components/blockType/dbwriteblock.h \
    acquisition/wimuacquisition.h \
    mytreewidget.h \
    accdatadisplay.h \
    core/components/blockType/activitytrackerblock.h \
    dialogs/aboutdialog.h \
    dialogs/helpdialog.h \
    core/components/blockplugin.h \
    core/components/blockgenerator.h \
    rangeslider.h \
    algorithm/podometer/stepCounter.h

FORMS += widget.ui \
    help.ui \
    about.ui

RESOURCES += qml.qrc \
    images.qrc

# Additional import path used to resolve QML modules in Qt Creator's code model
QML_IMPORT_PATH = $$PWD/..

QSG_RENDERER_DEBUG=dump

# Default rules for deployment.
include(deployment.pri)

DISTFILES += \
    blockplugin.json


