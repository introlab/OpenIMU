#include "MyTreeWidget.h"

void myTreeWidget::addChildren(QTreeWidgetItem* item,QString filePath)
{
    QDir* rootDir = new QDir(filePath);
    QFileInfoList filesList = rootDir->entryInfoList();

    foreach(QFileInfo fileInfo, filesList)
    {
        QTreeWidgetItem* child = new QTreeWidgetItem();
        child->setText(0,fileInfo.fileName());
        if(fileInfo.isFile() && fileInfo.fileName().contains("ACC"))
        {
          child->setText(1,QString::number(fileInfo.size()));
        }
        if(fileInfo.isDir())
        {
          child->setText(2,fileInfo.filePath());
        }
    if(fileInfo.fileName().contains("ACC"))
        item->addChild(child);
    }
}
