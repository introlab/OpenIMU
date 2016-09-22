#include "testall.h"

TestAll::TestAll(QObject *parent) : QObject(parent)
{
    multiply = new TestMultiply();
    pipeline = new TestPipeline();
}

TestAll::~TestAll()
{
    delete multiply;
    delete pipeline;
}

void TestAll::testMultiply()
{
    QTest::qExec(multiply);
}

void TestAll::testPipeline()
{
    QTest::qExec(pipeline);
}
