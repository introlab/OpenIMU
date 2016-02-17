#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "packageexplorer.h"



MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    hBox = new QHBoxLayout();
    //packageExplorer = new PackageExplorer();

    //hBox->addWidget(packageExplorer);


    gridLayout = new QGridLayout();
    this->centralWidget()->setLayout(hBox);

}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::AddCustomWidget(QWidget* widget, int x, int y)
{
    this->gridLayout->addWidget(widget,x,y);
}
