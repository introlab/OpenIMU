#include "algorithmtab.h"
#include "AlgorithmParametersWindow.h"
#include "QApplication"
#include "QGuiApplication"

AlgorithmTab::AlgorithmTab(QWidget * parent) : QWidget(parent)
{
        // -- Layout
        algorithmLayout = new QVBoxLayout(this);

        // -- Algorithm Section
        algorithmLabel = new QLabel(tr("Algorithmes"));
        algorithmTableWidget = new QTableWidget(this);

        algorithmTableWidget->setRowCount(10);
        algorithmTableWidget->setColumnCount(4);

        algorithmTableHeaders<<"Id"<<"Nom"<<"Description"<<"Auteur";
        algorithmTableWidget->setHorizontalHeaderLabels(algorithmTableHeaders);
        algorithmTableWidget->setEditTriggers(QAbstractItemView::NoEditTriggers);
        algorithmTableWidget->setSelectionBehavior(QAbstractItemView::SelectRows);
        algorithmTableWidget->setSelectionMode(QAbstractItemView::SingleSelection);
        //algorithmTableWidget->setStyleSheet("QTableView {alternate-background-color:#ecf0f1;selection-background-color: white;}");
        //algorithmTableWidget->verticalHeader()->setVisible(false);


        algorithmTableWidget->setItem(0, 1, new QTableWidgetItem("Hello"));

        connect(algorithmTableWidget, SIGNAL(doubleClicked(const QModelIndex& )), this, SLOT(openParametersWindow(const QModelIndex &)));

        // -- Parameter Section
        parameterLabel = new QLabel(tr("Paramètre(s)"));

        algorithmLayout->addWidget(algorithmLabel);
        algorithmLayout->addWidget(algorithmTableWidget);
        algorithmLayout->addWidget(parameterLabel);
        this->setLayout(algorithmLayout);
}

void AlgorithmTab::openParametersWindow(const QModelIndex &index)
{
    if (index.isValid())
    {
        algorithmTableWidget->setItem(index.row(), 2, new QTableWidgetItem("Goodbye"));

        AlgorithmParametersWindow algorithmParametersWindow;

        algorithmParametersWindow.show();

    }
}
