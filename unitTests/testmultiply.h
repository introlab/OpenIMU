#ifndef TESTMULTIPLY_H
#define TESTMULTIPLY_H

#include <QObject>
#include <QtTest/QtTest>
#include "../applicationOpenimu/app/core/Caneva.h"

class TestMultiply : public QObject
{
    Q_OBJECT
public:
    explicit TestMultiply(QObject *parent = 0);

private slots:
    void testsJSON();
    void testsJSON_data();

private:
    Caneva* caneva;
};

#endif // TESTMULTIPLY_H
