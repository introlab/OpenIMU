#ifndef TESTQSTRING_H
#define TESTQSTRING_H

#include <QObject>
#include <QtTest/QtTest>
#include "../applicationOpenimu/app/core/Caneva.h"
class TestPipeline : public QObject
{
    Q_OBJECT

public:
    TestPipeline(QObject *parent = 0);

private slots:
    void testsJSON();
    void testsJSON_data();

private:
    Caneva* caneva;
};

#endif // TESTQSTRING_H
