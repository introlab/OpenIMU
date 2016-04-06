#include "customqmlscene.h"
#include <QQuickView>
#include <QQuickItem>
#include <iostream>
#include <QQmlApplicationEngine>
#include <qboxlayout.h>
#include <models/components/quickiteminputnode.h>

CustomQmlScene::CustomQmlScene(std::string filename, QWidget* parent = 0): QWidget(parent)
{
    qmlRegisterType<QuickItemInputNode>("quickItemInputNode", 1, 0, "QuickItemInputNode");
    qmlRegisterType<QuickItemInputNode>("quickItemOutputNode", 1, 0, "QuickItemOutputNode");

    filename = "qrc:/" + filename;
    QQuickView* view = new QQuickView();

    view->engine()->addImportPath("../jbQuick/.");


    QWidget* widget = QWidget::createWindowContainer(view, this);
    view->setSource(QUrl((QString)filename.c_str()));

    if(view->status()!=QQuickView::Ready)
        qDebug("can't initialise view");
    widget->setMinimumSize(500,100);

    container = view->rootObject();

    QVBoxLayout* mainLayout = new QVBoxLayout();
    mainLayout->addWidget(widget);
    this->setLayout(mainLayout);
}

QuickItemInputNode *CustomQmlScene::getInputNode(QString blockId, QString inputId)
{
    foreach (QQuickItem *child, container->childItems()) {
      if(child->property("id").toString()==blockId)
          foreach (QQuickItem *input, child->childItems()){
              if(input->property("id").toString()==inputId)
                  return (QuickItemInputNode*)input;
          }
    }
    return 0;
}

QuickItemOutputNode *CustomQmlScene::getOutputNode(QString blockId, QString inputId)
{
    foreach (QQuickItem *child, container->childItems()) {
      if(child->property("id").toString()==blockId)
          foreach (QQuickItem *input, child->childItems()){
              if(input->property("id").toString()==inputId)
                  return (QuickItemOutputNode*)input;
          }
    }
    return 0;
}


