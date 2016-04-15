TEMPLATE = subdirs

SUBDIRS += \
    vbLabel/vblabel.pro \
    app/application_openimu.pro \
    qml/jbQuick/Charts/qchart.js.pro \
    tests/tests.pro

include(qtestlib-tools/benchlib.pri)
