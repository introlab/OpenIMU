#include "ResultsTabWidget.h"

ResultsTabWidget::ResultsTabWidget(QWidget *parent):QWidget(parent)
{
    layout = new QGridLayout;
    this->setLayout(layout);

    recordTitle = new QLabel("Test");
    recordDate = new QLabel("Journée d'enregistrement: ");

    layout->addWidget(recordTitle,0,0);
    layout->addWidget(recordDate,1,0);
}

ResultsTabWidget::ResultsTabWidget()
{

}

ResultsTabWidget::~ResultsTabWidget()
{

}
