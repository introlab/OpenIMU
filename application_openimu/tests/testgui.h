#ifndef TESTGUI_H
#define TESTGUI_H

#include <QObject>
#include <QtTest>

class TestGui : public QObject
{
    Q_OBJECT
public:
    TestGui(QObject *parent = 0);

private slots:
    void testGui();
    void testGui_data();
};

#endif // TESTGUI_H
