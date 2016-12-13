#ifndef GENERICALGORESULTS_H
#define GENERICALGORESULTS_H

#include <QWidget>
#include <QtCharts/QChartView>

#include "../algorithm/AlgorithmOutputInfo.h"

namespace Ui {
class GenericAlgoResults;
}

class GenericAlgoResults : public QWidget
{
    Q_OBJECT

public:
    explicit GenericAlgoResults(QWidget *parent = 0);
    GenericAlgoResults(QWidget *parent, AlgorithmOutputInfo algoOutput, std::string json);
    ~GenericAlgoResults();

private:
    Ui::GenericAlgoResults *ui;
};

#endif // GENERICALGORESULTS_H
