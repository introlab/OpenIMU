#ifndef RESULTSTABWIDGET_H
#define RESULTSTABWIDGET_H

#include <QWidget>
#include <QGridLayout>
#include <string>
#include <QLabel>


class ResultsTabWidget: public QWidget
{
    Q_OBJECT

    public:
    ResultsTabWidget();
    ResultsTabWidget(QWidget *parent);

    ~ResultsTabWidget();

    public slots:

    private:
    QGridLayout* layout;

    QLabel* recordTitle;
    QLabel* recordDate;
    QLabel* imuType;

};

#endif
