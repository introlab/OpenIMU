TEMPLATE = lib
TARGET = vbLabel
QT += qml quick
CONFIG += qt plugin c++11

TARGET = $$qtLibraryTarget($$TARGET)
uri = blocks.visual.label

# Input
SOURCES += \
    vblabel_plugin.cpp \
    vblabel.cpp

HEADERS += \
    vblabel_plugin.h \
    vblabel.h

DISTFILES = qmldir \
    vbLabel.qml

!equals(_PRO_FILE_PWD_, $$OUT_PWD) {
    copy_qmldir.target = $$OUT_PWD/qmldir
    copy_qmldir.depends = $$_PRO_FILE_PWD_/qmldir
    copy_qmldir.commands = $(COPY_FILE) \"$$replace(copy_qmldir.depends, /, $$QMAKE_DIR_SEP)\" \"$$replace(copy_qmldir.target, /, $$QMAKE_DIR_SEP)\"
    QMAKE_EXTRA_TARGETS += copy_qmldir
    PRE_TARGETDEPS += $$copy_qmldir.target

    copy_qmldir2.target = $$PWD/../qmldir
    copy_qmldir2.depends = $$_PRO_FILE_PWD_/qmldir
    copy_qmldir2.commands = $(COPY_FILE) \"$$replace(copy_qmldir2.depends, /, $$QMAKE_DIR_SEP)\" \"$$replace(copy_qmldir2.target, /, $$QMAKE_DIR_SEP)\"
    QMAKE_EXTRA_TARGETS += copy_qmldir2
    PRE_TARGETDEPS += $$copy_qmldir2.target

    copy_lib.target = $$PWD/../$$TARGET
    copy_lib.depends = $$_PRO_FILE_PWD_/$$TARGET
    copy_lib.commands = $(COPY_FILE) \"$$replace(copy_lib.depends, /, $$QMAKE_DIR_SEP)\" \"$$replace(copy_qmllib.target, /, $$QMAKE_DIR_SEP)\"
    QMAKE_EXTRA_TARGETS += copy_qmllib
    PRE_TARGETDEPS += $$copy_qmllib.target
}

qmldir.files = qmldir
unix {
    installPath = $$[QT_INSTALL_QML]/$$replace(uri, \\., /)
    qmldir.path = $$installPath
    target.path = $$installPath
    INSTALLS += target qmldir
}
