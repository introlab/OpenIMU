#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QLabel>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    QWidget *temp = new QWidget();
    gridLayout = new QGridLayout();
    temp->setLayout(gridLayout);

    hBox = new QHBoxLayout();
    explorerFile = new ExplorerFile(this);
    explorerTab = new ExplorerTab(this);
    explorerTab->addTab(temp ,"Tab 1");



    hBox->addWidget(explorerFile);
    hBox->addWidget(explorerTab);



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
