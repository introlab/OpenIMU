#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QLabel>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    hBox = new QHBoxLayout();
    explorerFile = new ExplorerFile(this);
    explorerTab = new ExplorerTab(this);


    hBox->addWidget(explorerFile);
    hBox->addWidget(new QLabel("Hello"));

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
