TEMPLATE = subdirs

SUBDIRS += \
    app/application_openimu.pro \
    qml/jbQuick/Charts/qchart.js.pro
##   tests/tests.pro

include(qtestlib-tools/benchlib.pri)
