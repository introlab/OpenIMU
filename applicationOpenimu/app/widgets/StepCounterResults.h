#ifndef STEPCOUNTERRESULTS_H
#define STEPCOUNTERRESULTS_H

#include <QWidget>
#include "../algorithm/AlgorithmOutputInfo.h"

namespace Ui {
class StepCounterResults;
}

class StepCounterResults : public QWidget
{
    Q_OBJECT

public:
    explicit StepCounterResults(QWidget *parent = 0);
    StepCounterResults(QWidget *parent, AlgorithmOutputInfo algoOutput);
    ~StepCounterResults();

private:
    Ui::StepCounterResults *ui;
};

#endif // STEPCOUNTERRESULTS_H
