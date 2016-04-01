//Must be Singleton

#include "toolbarcontroller.h"
#include <QFileDialog>
#include <iostream>

ToolbarController::ToolbarController()
{

    this->toolbar = new ToolbarView(this);

    QAction* actionOuvrir = new QAction("Ouvrir",this->toolbar->fichier);
    this->toolbar->fichier->addAction(actionOuvrir);

    connect(actionOuvrir, &QAction::triggered,this,&ToolbarController::openFile);


}

void ToolbarController:: openFile(){    
   std::cout<<"Hello";

   //QString folderName = QFileDialog::getExistingDirectory(this, tr("Open File"),"/path/to/file/");
    /*
        QString folderName = QFileDialog::getExistingDirectory(this, tr("Open File"),"/path/to/file/");
        qDebug() << "List items = " << folderName;
        SensorReader *reader = new SensorReader();
        vector<string> x = reader->listFiles(folderName.toStdString());
        QVBoxLayout *filesLayout = new QVBoxLayout;
        foreach (string t , x){

            //qDebug() << "List items = " << getFileName(t).c_str();
            filesLayout->addWidget(new QLabel(getFileName(t).c_str(),filesWidget));
        }
        filesWidget->setLayout(filesLayout);
     */

}
void ToolbarController:: computeSteps(){
/*
    plotWidget = new Widget(this->parentWidget());
    plotWidget->setFolderPath(folderName.toStdString());
    plotWidget->setupPlot();
    mainLayout->addWidget(plotWidget);
    plotDisplay = true;
    */
}





