#include"HomeWidget.h"
#include "ui_homewidget.h"

HomeWidget::HomeWidget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::HomeWidget)
{
    ui->setupUi(this);
    m_parent = parent;
}

HomeWidget::~HomeWidget()
{
    delete ui;
}
