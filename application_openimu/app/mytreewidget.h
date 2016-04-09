#ifndef MYTREEWIDGET_H
#define MYTREEWIDGET_H
//myTreeWidget.h file
#include <QtGui>
#include <QTreeWidget>

class myTreeWidget:public QTreeWidget
{
  Q_OBJECT
  public:
    myTreeWidget(QWidget* parent):
    QTreeWidget(parent)
    {
      //Add Subdirectories as children 	when user clicks on a file item,
      //otherwise adding all children recursively may consume HUGE amount of memory
      connect(this , SIGNAL(itemClicked(QTreeWidgetItem*,int)),parent,SLOT(onTreeItemClicked(QTreeWidgetItem*,int)));
    }
    ~myTreeWidget(){}

  void addChildren(QTreeWidgetItem* item,QString filePath);
  public slots:

};
#endif
