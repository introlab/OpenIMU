#ifndef MYTREEWIDGET_H
#define MYTREEWIDGET_H
#include <QtGui>
#include <QTreeWidget>

class myTreeWidget:public QTreeWidget
{
    Q_OBJECT
public:
    myTreeWidget(QWidget* parent):QTreeWidget(parent)
    {
      connect(this , SIGNAL(itemClicked(QTreeWidgetItem*,int)),parent,SLOT(onListItemClicked(QTreeWidgetItem*,int)));
      connect(this, SIGNAL(itemDoubleClicked(QTreeWidgetItem*,int)),parent, SLOT(onListItemDoubleClicked(QTreeWidgetItem*,int)));
    }
    ~myTreeWidget(){}

    void addChildren(QTreeWidgetItem* item,QString filePath);
};
#endif
