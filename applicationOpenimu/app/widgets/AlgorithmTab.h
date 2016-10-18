#ifndef ALGORITHMTAB_H
#define ALGORITHMTAB_H

#include "MainWidget.h"
#include "QLabel"
#include "QStandardItemModel"
#include "QTableWidget"
#include <QWidget>

class AlgorithmTab : public QWidget
{
    Q_OBJECT
public:
    explicit AlgorithmTab(QWidget *parent = 0);

private:
    QVBoxLayout * algorithmLayout;

    // -- Algorithm List Section
    QLabel * algorithmLabel;
    QTableWidget * algorithmTableWidget;
    QStringList algorithmTableHeaders;

    // -- Parameter Section
    QLabel * parameterLabel;

signals:

public slots:
    void openParametersWindow(const QModelIndex &index);
};

#endif // ALGORITHMTAB_H
