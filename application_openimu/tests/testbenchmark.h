#ifndef TESTBENCHMARK_H
#define TESTBENCHMARK_H

#include <QObject>
#include <QTest>

class TestBenchmark : public QObject
{
    Q_OBJECT
public:
    explicit TestBenchmark(QObject *parent = 0);

signals:

public slots:
private slots:
    void simple();
    void multiple();
    void multiple_data();
};

#endif // TESTBENCHMARK_H
