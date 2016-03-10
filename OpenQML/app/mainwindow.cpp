#include <QQuickView>
#include <QQmlApplicationEngine>
#include <QVBoxLayout>
#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    QQmlApplicationEngine engine;
    engine.addImportPath("C:/Users/dror2202/Documents/OpenQML");
    engine.load(QUrl(QStringLiteral("qrc:/main.qml")));

    QQuickView *view = new QQuickView(&engine,0);
    QWidget *container = QWidget::createWindowContainer(view, this);
    container->setMinimumSize(200, 200);
    container->setMaximumSize(200, 200);
    container->setFocusPolicy(Qt::TabFocus);


    QVBoxLayout* verticalLayout = new QVBoxLayout();
    ui->centralWidget->setLayout(verticalLayout);
    verticalLayout->addWidget(container);
}

MainWindow::~MainWindow()
{
    delete ui;
}
