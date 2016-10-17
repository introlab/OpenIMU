#include "QTableView"
#include "MainWidget.h"
#include "QLabel"
#include "QStandardItemModel"
#include "algorithmtab.h"

AlgorithmTab::AlgorithmTab(QWidget *parent) : QWidget(parent)
{
    // -- Algorithm Section
    QLabel *algorithmLabel = new QLabel(tr("Algorithms"));

    QTableView *algorithmTableView = new QTableView(this);
   // connect(algorithmTableView, SIGNAL(itemClicked(QTableViewItem*)),this, SLOT(onListItemClicked(QTableViewItem*)));

    //algorithmTableView->setAlternatingRowColors(true);
    //algorithmTableView->setStyleSheet("alternate-background-color:#ecf0f1;background-color:white;");

    QStandardItemModel *algorithmModel = new QStandardItemModel(this);
    algorithmModel->setHeaderData(0, Qt::Horizontal, QObject::tr("ID"));
    algorithmModel->setHeaderData(1, Qt::Horizontal, QObject::tr("Name"));
    algorithmModel->setHeaderData(2, Qt::Horizontal, QObject::tr("Description"));
    algorithmModel->setHeaderData(3, Qt::Horizontal, QObject::tr("Author"));

    algorithmTableView->setModel(algorithmModel);
    algorithmTableView->show();

    // -- Parameter Section
    QLabel *parameterLabel = new QLabel(tr("Parameter(s)"));

}
