#ifndef TESTQSTRING_H
#define TESTQSTRING_H

#include <QObject>
#include <QtTest/QtTest>

class TestQString : public QObject
{
    Q_OBJECT
public:
    TestQString(QObject *parent = 0);

private slots:
    void toUpper_data();
    void toUpper();
};

#endif // TESTQSTRING_H
