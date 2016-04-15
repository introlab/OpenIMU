#include "customqmlscene.h"
#include <QQuickView>
#include <QQuickItem>
#include <iostream>
#include <QQmlApplicationEngine>
#include <qboxlayout.h>
#include <models/components/quickiteminputnodeshandles.h>
#include <QApplication>

CustomQmlScene::CustomQmlScene(std::string filename, QWidget* parent = 0): QWidget(parent)
{
    qmlRegisterType<QuickItemInputNodeIntHandle>("InputNodeInt", 1, 0, "InputNodeInt");
    qmlRegisterType<QuickItemOutputNodeInt>("OutputNodeInt", 1, 0, "OutputNodeInt");

    qmlRegisterType<QuickItemInputNodeDoubleHandle>("InputNodeDouble", 1, 0, "InputNodeDouble");
    qmlRegisterType<QuickItemOutputNodeDouble>("OutputNodeDouble", 1, 0, "OutputNodeDouble");

    qmlRegisterType<QuickItemInputNodeStringHandle>("InputNodeString", 1, 0, "InputNodeString");
    qmlRegisterType<QuickItemOutputNodeString>("OutputNodeString", 1, 0, "OutputNodeString");

    filename = "qrc:/" + filename;
    QQuickView* view = new QQuickView();

    //view->engine()->addImportPath("../jbQuick/.");
    //view->engine()->addImportPath(QApplication::applicationDirPath() + "/jbQuick/.");
    view->engine()->addImportPath(QApplication::applicationDirPath() + "/qml");

    //DL test import paths
    qDebug() << "Current Import paths : " << view->engine()->importPathList();


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

QQuickItem *CustomQmlScene::getInputNode(QString blockId, QString inputId, QQuickItem * container)
{
    if(!container)
        container = this->container;

    QStringList path = blockId.split(".");
    if(path.length() <= 1){
        foreach (QQuickItem *child, container->childItems()) {
            if(child->property("id").toString()==blockId)
                foreach (QQuickItem *input, child->childItems()){
                    if(input->property("id").toString()==inputId)
                        return (QQuickItem*)input;
                }
        }
    }
    else {
        foreach (QQuickItem *child, container->childItems()) {
            if(child->property("id").toString()==path[0])
            {
              path.removeFirst();
              return getInputNode(path.join("."),inputId,child);
            }
        }
    }
    return 0;
}

QQuickItem *CustomQmlScene::getOutputNode(QString blockId, QString outputId, QQuickItem *container)
{
    if(!container)
        container = this->container;

    QStringList path = blockId.split(".");
    if(path.length() <= 1){
        foreach (QQuickItem *child, container->childItems()) {
            if(child->property("id").toString()==blockId)
                foreach (QQuickItem *output, child->childItems()){
                    if(output->property("id").toString()==outputId)
                        return (QQuickItem*)output;
                }
        }
    }
    else {
        foreach (QQuickItem *child, container->childItems()) {
            if(child->property("id").toString()==path[0])
            {
              path.removeFirst();
              return getOutputNode(path.join("."),outputId,child);
            }
        }
    }
    return 0;
}


