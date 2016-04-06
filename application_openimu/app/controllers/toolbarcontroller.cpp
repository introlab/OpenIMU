//Must be Singleton
/*
#include "toolbarcontroller.h"

ToolbarController::ToolbarController(QWidget *parent)
{
    toolbar = new ToolbarView(this);
}

void ToolbarController:: openFile(){
    if(!plotDisplay){
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

    }
}
void ToolbarController:: computeSteps(){

  /* plotWidget = new Widget(this->parentWidget());
    plotWidget->setFolderPath(folderName.toStdString());
    plotWidget->setupPlot();
    mainLayout->addWidget(plotWidget);
    plotDisplay = true;*//*
}

ToolbarView ToolbarController::getToolbar() const
{
    return toolbar;
}

void ToolbarController::setToolbar(const ToolbarView &value)
{
    toolbar = value;
}
*/


