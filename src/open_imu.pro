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
INCLUDEPATH += $$PWD/../qwt-6.1.2/src

SOURCES += main.cpp\
        views/mainwindow.cpp \
    models/connectors/connector.cpp \
    controllers/maincontroller.cpp \
    models/json/jsoncpp.cpp \
    models/layoutreader.cpp \
    views/explorerfile.cpp \
    views/explorerdisplay.cpp \
    models/displayloader.cpp

HEADERS  += views/mainwindow.h \
    models/connectors/connector.h \
    controllers/maincontroller.h \
    models/json/json/json-forwards.h \
    models/json/json/json.h \
    models/layoutreader.h \
    views/explorerfile.h \
    views/explorerdisplay.h \
    models/displayloader.h

FORMS    += views/mainwindow.ui


win32:CONFIG(release, debug|release): LIBS += -L$$PWD/../qwt-6.1.2/lib/ -lqwt
else:win32:CONFIG(debug, debug|release): LIBS += -L$$PWD/../qwt-6.1.2/lib/ -lqwtd
else:unix: LIBS += -L$$PWD/../qwt-6.1.2/lib/ -lqwt

INCLUDEPATH += $$PWD/../qwt-6.1.2
DEPENDPATH += $$PWD/../qwt-6.1.2
