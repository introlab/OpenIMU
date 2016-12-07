#include "ResultsTabWidget.h"
#include <QtWidgets>
#include "StepCounterResults.h"
#include "ActivityTrackerResults.h"
#include "utilities/PdfGenerator.h"

ResultsTabWidget::ResultsTabWidget()
{

}

ResultsTabWidget::ResultsTabWidget(QWidget *parent, AlgorithmOutputInfo output, bool isSaved):QWidget(parent)
{
    m_parent = parent;
    init(output, isSaved);
}

ResultsTabWidget::ResultsTabWidget(QWidget *parent, WimuAcquisition& accData, RecordInfo& rInfo):QWidget(parent)
{
    m_parent = parent;
    m_accData = new WimuAcquisition();
    m_accData->setDataAccelerometer(accData.getDataAccelerometer());
    m_recordInfo = rInfo;

    AccDataDisplay* accDataDisplay = new AccDataDisplay(accData);
    initFilterView(accDataDisplay);
}

ResultsTabWidget::~ResultsTabWidget()
{

}

void ResultsTabWidget::init(AlgorithmOutputInfo output, bool isSaved)
{
    m_databaseAccess = new DbBlock();

    m_algorithmOutputInfo = output;

    if(m_algorithmOutputInfo.m_algorithmName == "Temps d'activité")
    {
        ActivityTrackerResults * res = new ActivityTrackerResults(this, m_algorithmOutputInfo);
        if(isSaved)
        {
            res->hideButtons();
        }
        QVBoxLayout* layoutV = new QVBoxLayout();
        layoutV->addWidget(res);
        this->setLayout(layoutV);


    }
    else
    {
       StepCounterResults * res = new StepCounterResults(this, m_algorithmOutputInfo);
       if(isSaved)
       {
           res->hideButtons();
       }
       QVBoxLayout* layoutV = new QVBoxLayout();
       layoutV->addWidget(res);
       this->setLayout(layoutV);

    }
}


void ResultsTabWidget::initFilterView(AccDataDisplay* accDataDisplay)
{
    layout = new QGridLayout;
    this->setLayout(layout);
    accDataDisplay->showSimplfiedDataDisplay();
    saveResultsToDB = new QPushButton("");
    QIcon img(":/icons/save as record.png");
    saveResultsToDB->setIcon(img);
    saveResultsToDB->setIconSize(QSize(375,35));
    saveResultsToDB->setFlat(true);
    saveResultsToDB->setCursor(Qt::PointingHandCursor);
    saveResultsToDB->setMaximumWidth(375);
    saveResultsToDB->setStyleSheet("border:none");
    connect(saveResultsToDB, SIGNAL(clicked()), this, SLOT(exportDataToDBSlot()));

    layout->addWidget(accDataDisplay);
    layout->addWidget(saveResultsToDB,1,0, Qt::AlignCenter);
}

void ResultsTabWidget::exportToDBSlot()
{
    // MainWindow -> AlgorithmTab -> ResultsTab
    AlgorithmTab * algorithmTab = (AlgorithmTab*)m_parent;
    MainWindow * mainWindow = (MainWindow*)algorithmTab->getMainWindow();

    QString statusMessage = "Prêt";
    MessageStatus status = MessageStatus::none;

    mainWindow->setStatusBarText(tr("Insertion des résultats dans la base de données en cours..."));
    mainWindow->startSpinner();

    QInputDialog* resultsNameInputDialog = new QInputDialog();
    resultsNameInputDialog->setWindowFlags(this->windowFlags() & ~Qt::WindowContextHelpButtonHint);
    resultsNameInputDialog->setOptions(QInputDialog::NoButtons);
    resultsNameInputDialog->setWindowIcon(QIcon(QString::fromUtf8("../icons/logo.ico")));

    // Also sets the text for the InputDialog
    QString message = "Veuillez entrer un nom permettant d'identifier ces résultats.";
    bool dialogResponse;
    QString dialogText =  resultsNameInputDialog->getText(NULL ,"Identification des résultats",
                                                          message, QLineEdit::Normal,
                                                          "", &dialogResponse);
    if (dialogResponse && !dialogText.isEmpty())
    {
        std::string serializedData;
        AlgorithmOutputInfoSerializer serializer;

        m_algorithmOutputInfo.m_resultName = dialogText.toStdString();
        serializer.Serialize(m_algorithmOutputInfo, serializedData);

        bool resultsAddedSuccessfully = m_databaseAccess->addResultsInDB(QString::fromStdString(serializedData));

        if(resultsAddedSuccessfully)
        {
            statusMessage = "Enregistrement en base de données réussi";
            status = MessageStatus::success;
        }
        else
        {
            statusMessage = "Échec de l'enregistrement en base de données";
            status = MessageStatus::error;
        }
    }
    else
    {
        statusMessage = "Enregistrement en base de données annulé";
        status = MessageStatus::error;
    }

    delete resultsNameInputDialog;
    mainWindow->stopSpinner(true);
    mainWindow->setStatusBarText(statusMessage, status);
}

void ResultsTabWidget::exportDataToDBSlot()
{  
    RecordInfo newInfo;
    newInfo.m_imuPosition = m_recordInfo.m_imuPosition;
    newInfo.m_imuType = m_recordInfo.m_imuType;
    newInfo.m_parentId = m_recordInfo.m_recordId;
    newInfo.m_recordName = "filtered" + m_recordInfo.m_recordName;
    newInfo.m_recordDetails = m_recordInfo.m_recordDetails;

    std::string output;
    CJsonSerializer::Serialize(m_accData, newInfo, output);
    m_databaseAccess = new DbBlock();
    QString temp = QString::fromStdString(output);//TODO remove
    m_databaseAccess->addRecordInDB(temp);
}

void ResultsTabWidget::exportToPdfSlot()
{
    // MainWindow -> AlgorithmTab -> ResultsTab
    AlgorithmTab * algorithmTab = (AlgorithmTab*)m_parent;
    MainWindow * mainWindow = (MainWindow*)algorithmTab->getMainWindow();
    mainWindow->setStatusBarText(tr("Enregistrement des résultats sous forme de fichier PDF en cours..."));
    mainWindow->startSpinner();

    QString statusMessage = "Prêt";
    MessageStatus status = MessageStatus::none;

    QString filename = QFileDialog::getSaveFileName(this,tr("Save Document"), QDir::currentPath(),tr("PDF (*.pdf)"));
    if( !filename.isNull() )
    {

        PDFGenerator pdfGen(filename);
        int offset = 800;
        int lineHeight = 400;
        pdfGen.DrawHeader("Résultat des algorithmes");
        pdfGen.drawText(0,5*lineHeight + offset,Qt::AlignVCenter,"Description détaillée",20);
        pdfGen.drawText(200,6.2*lineHeight + offset,Qt::AlignVCenter,"Nom de l'enregistrement: " +QString::fromStdString(m_algorithmOutputInfo.m_recordName));
        pdfGen.drawText(200,7.2*lineHeight + offset,Qt::AlignVCenter,"Date de l'enregistrement: " + QString::fromStdString(m_algorithmOutputInfo.m_date));
        pdfGen.drawText(200,8.2*lineHeight + offset,Qt::AlignVCenter,"Date de l'enregistrement: " + QString::fromStdString(m_algorithmOutputInfo.m_date));
        pdfGen.drawText(200,9.2*lineHeight + offset,Qt::AlignVCenter,"Type de IMU: " + QString::fromStdString(m_algorithmOutputInfo.m_recordImuPosition));
        pdfGen.drawText(200,10.2*lineHeight + offset,Qt::AlignVCenter,"Position de la centralle inertielle:" + QString::fromStdString(m_algorithmOutputInfo.m_recordType));

        pdfGen.drawText(0,12.2*lineHeight + offset,Qt::AlignVCenter,"Algorithmes",20);
        pdfGen.drawText(200,13.4*lineHeight + offset,Qt::AlignVCenter,"Algorithme appliqué: " + QString::fromStdString(m_algorithmOutputInfo.m_algorithmName));
        pdfGen.drawText(200,14.4*lineHeight + offset,Qt::AlignVCenter,"Valeur obtenue: " +QString::fromStdString(std::to_string(m_algorithmOutputInfo.m_value)));
        pdfGen.drawText(200,15.4*lineHeight + offset,Qt::AlignVCenter,"Temps de calculs: " +QString::fromStdString(std::to_string(m_algorithmOutputInfo.m_executionTime)));

       /* QPixmap pix = chartView->grab();
        int h = painter.window().height()*0.4;
        int w = h * 1.1;
        int x = (painter.window().width() / 2) - (w/2);
        int y = (painter.window().height() / 2) - (h/2);
        painter.drawPixmap(x, y, w, h, pix);

        painter.end();*/

        statusMessage = "Enregistrement du PDF réussi";
        status = MessageStatus::success;
    }
    else
    {
        statusMessage = "Échec de l'enregistrement du PDF";
        status = MessageStatus::error;
    }

    mainWindow->stopSpinner(true);
    mainWindow->setStatusBarText(statusMessage, status);
}
