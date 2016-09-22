#ifndef TESTALL_H
#define TESTALL_H

#include <QObject>
#include <QtTest/QtTest>

#include "testmultiply.h"
#include "testpipeline.h"

class TestAll : public QObject
{
    Q_OBJECT

public:
    TestAll(QObject *parent = 0);
    ~TestAll();

private slots:
    void testMultiply();
    void testPipeline();

private:
    TestMultiply* multiply;
    TestPipeline* pipeline;
};

#endif // TESTALL_H
