#ifndef TESTBENCHMARK_H
#define TESTBENCHMARK_H

#include <QObject>
#include <QTest>
#include "../../application_openimu/app/models/caneva.h"

class TestBenchmark : public QObject
{
    Q_OBJECT
public:
    explicit TestBenchmark(QObject *parent = 0);

signals:

private slots:
    void multiple_delay();
    void multiple_delay_data();

private:
    Caneva* caneva;
};

#endif // TESTBENCHMARK_H
