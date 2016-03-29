#include <QQuickView>
#include <QVBoxLayout>
#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <iostream>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    //QQmlApplicationEngine* engine = new QQmlApplicationEngine();
    //engine->load(QUrl(QStringLiteral("qrc:/main.qml")));

    QQuickView* view = new QQuickView();
    QWidget* widget = QWidget::createWindowContainer(view, ui->centralWidget);
    view->setSource(QUrl((QStringLiteral("qrc:/main.qml"))));
    //std::cout << "view status: " << view->status() << std::endl;
    //while(view->status()!=QQuickView::Ready){}
    if(view->status()!=QQuickView::Ready)
        qDebug("can't initialise view");
    widget->setMinimumSize(500,100);
    QQuickItem* container = view->rootObject();

    //container->setProperty("text", "Hello alternate universe");

    //QQuickView *view = new QQuickView(engine,0);
    //QWidget *container = QWidget::createWindowContainer(view, this);
    //container->setMinimumSize(200, 200);
    //container->setMaximumSize(200, 200);
    //container->setFocusPolicy(Qt::TabFocus);


    QVBoxLayout* verticalLayout = new QVBoxLayout();
    ui->centralWidget->setLayout(verticalLayout);
    verticalLayout->addWidget(widget);
}

MainWindow::~MainWindow()
{
    delete ui;
}
