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
INCLUDEPATH += $$PWD/../../qwt-6.1.2/src

SOURCES += main.cpp\
        views/mainwindow.cpp \
    controllers/maincontroller.cpp \
    models/json/jsoncpp.cpp \
    models/components/observer.cpp \
    models/components/abstractinputnode.cpp \
    models/components/abstractoutputnode.cpp \
    models/components/inputnode.cpp \
    models/components/outputnode.cpp \
    models/components/abstractalgorithm.cpp \
    views/explorerfile.cpp \
    views/explorerdisplay.cpp \
    views/display.cpp \
    models/jsonreader.cpp \
    models/builder.cpp \
    models/components/abstractwidgetcontroller.cpp \
    models/displaybuilder.cpp \
    packages/widgets/plot/plot.cpp \
    packages/widgets/plot/plotcontroller.cpp \
    packages/widgets/plot/widgetobservable.cpp \
    packages/widgets/plot/widgetobserver.cpp \
    packages/widgets/plot/curvedata.cpp \
    packages/widgets/plot/knob.cpp \
    packages/widgets/plot/samplingthread.cpp \
    packages/widgets/plot/signaldata.cpp \
    packages/widgets/plot/wheelbox.cpp


HEADERS  += views/mainwindow.h \
    controllers/maincontroller.h \
    models/json/json/json-forwards.h \
    models/json/json/json.h \
    models/components/observer.h \
    models/components/abstractinputnode.h \
    models/components/abstractoutputnode.h \
    models/components/inputnode.h \
    models/components/outputnode.h \
    models/components/abstractalgorithm.h \
    views/explorerfile.h \
    views/explorerdisplay.h \
    views/display.h \
    models/jsonreader.h \
    models/builder.h \
    models/components/abstractwidgetcontroller.h \
    models/displaybuilder.h \
    packages/widgets/plot/plot.h \
    packages/widgets/plot/plotcontroller.h \
    packages/widgets/plot/widgetobservable.h \
    packages/widgets/plot/widgetobserver.h \
    packages/widgets/plot/curvedata.h \
    packages/widgets/plot/knob.h \
    packages/widgets/plot/samplingthread.h \
    packages/widgets/plot/signaldata.h \
    packages/widgets/plot/wheelbox.h



FORMS    += views/mainwindow.ui


win32:CONFIG(release, debug|release): LIBS += -L$$PWD/../../qwt-6.1.2/lib/ -lqwt
else:win32:CONFIG(debug, debug|release): LIBS += -L$$PWD/../../qwt-6.1.2/lib/ -lqwtd
else:unix: LIBS += -L$$PWD/../../qwt-6.1.2/lib/ -lqwt

INCLUDEPATH += $$PWD/../../qwt-6.1.2
DEPENDPATH += $$PWD/../../qwt-6.1.2
