#include "explorerdisplay.h"

ExplorerDisplay::ExplorerDisplay(QWidget *parent)
{
    this->parent = parent;
    this->addTab(new QWidget() ,"Tab 2");

}
