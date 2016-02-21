#include "explorerdisplay.h"

//QWidget *temp = new QWidget();
//gridLayout = new QGridLayout();
//temp->setLayout(gridLayout);

ExplorerDisplay::ExplorerDisplay(QWidget *parent)
{
    this->parent = parent;
    this->initialize();

}

void ExplorerDisplay::initialize()
{
    this->addTab(new QWidget(),"Dummy");
}
