#include "ResultsTabWidget.h"
#include <QtWidgets>
#include <QPdfWriter>
#include <QPainter>

ResultsTabWidget::ResultsTabWidget(QWidget *parent,RecordInfo& recordInfo, AlgorithmOutputInfo output):QWidget(parent)
{
    m_parent = parent;
    m_recordInfo= recordInfo;
    init(output);
}


void ResultsTabWidget::init(AlgorithmOutputInfo output)
{
    m_databaseAccess = new DbBlock();

    m_algorithmOutputInfo = output;

    layout = new QGridLayout;
    this->setLayout(layout);

    QString algoName = "Algorithme appliqué: " + QString::fromStdString(m_algorithmOutputInfo.m_algorithmName);
    QString recordName = QString::fromStdString(m_recordInfo.m_recordName);

    algoLabel = new QLabel(algoName);
    algoLabel->setFont(QFont( "Arial", 12, QFont::Bold));

    recordLabel = new QLabel("Enregistrement utilisé: "+ recordName);
    dateLabel = new QLabel("Date de l'enregistrement: " + QString::fromStdString(m_algorithmOutputInfo.m_date));
    startHourLabel = new QLabel("Heure de début séléctionné: " + QString::fromStdString(m_algorithmOutputInfo.m_startTime));
    endHourLabel = new QLabel("Heure de fin séléctionné: " + QString::fromStdString(m_algorithmOutputInfo.m_endTime));
    positionLabel = new QLabel("Position du Wimu: " + QString::fromStdString(m_recordInfo.m_imuPosition));
    measureUnitLabel = new QLabel("Unité de mesure: " + QString::fromStdString(m_algorithmOutputInfo.m_measureUnit)) ;
    computeTimeLabel = new QLabel("Temps de calculs: " +QString::fromStdString(std::to_string(m_algorithmOutputInfo.m_executionTime) + "ms"));

    layout->addWidget(algoLabel,0,0);
    layout->addWidget(recordLabel,1,0);
    layout->addWidget(dateLabel,2,0);
    layout->addWidget(startHourLabel,3,0);
    layout->addWidget(endHourLabel,4,0);
    layout->addWidget(positionLabel,5,0);
    layout->addWidget(measureUnitLabel,6,0);
    layout->addWidget(computeTimeLabel,7,0);

    layout->setMargin(10);
    chartView = new QChartView();

    if(m_algorithmOutputInfo.m_algorithmName == "activityTracker")
    {
        QPieSeries *series = new QPieSeries();
        series->setHoleSize(0.35);
        QPieSlice *slice = series->append("Temps actif: " + QString::fromStdString(std::to_string(m_algorithmOutputInfo.m_value)) + " %" , m_algorithmOutputInfo.m_value);
        slice->setExploded();
        slice->setLabelVisible();
        series->append("Temps passif: " +  QString::fromStdString(std::to_string(100-m_algorithmOutputInfo.m_value)) + " %", m_algorithmOutputInfo.m_value-100);
        chartView->setRenderHint(QPainter::Antialiasing);
        chartView->chart()->setTitle("Temps d'activité");
        chartView->chart()->setTitleFont(QFont("Arial", 14));
        chartView->chart()->addSeries(series);
        chartView->chart()->legend()->setAlignment(Qt::AlignBottom);
        chartView->chart()->setTheme(QChart::ChartThemeLight);
        chartView->chart()->setAnimationOptions(QChart::SeriesAnimations);
        chartView->chart()->legend()->setFont(QFont("Arial", 12));

         exportToPdf = new QPushButton("Exporter en PDF");

        connect(exportToPdf, SIGNAL(clicked()), this, SLOT(exportToPdfSlot()));
        layout->addWidget(chartView,8,0);
        layout->addWidget(exportToPdf,9,0);

    }
    else
    {
       QLabel* labelResult = new QLabel("Résultat de l'algorithme : " + QString::fromStdString(std::to_string(m_algorithmOutputInfo.m_value)) +" pas" );

       algoLabel->setFont(QFont( "Arial", 12, QFont::Light));
       layout->addWidget(labelResult,9,0,Qt::AlignCenter);
    }

    connect(exportToPdf, SIGNAL(clicked()), this, SLOT(exportToPdfSlot()));

    saveResultsToDB = new QPushButton("Sauvegarder en base de données");
    connect(saveResultsToDB, SIGNAL(clicked()), this, SLOT(exportToDBSlot()));

    layout->addWidget(saveResultsToDB,9,1);

    this->setStyleSheet( "QPushButton{"
                   "background-color: rgba(119, 160, 175,0.7);"
                   "border-style: inset;"
                   "border-width: 0.2px;"
                   "border-radius: 10px;"
                   "border-color: white;"
                   "font: 12px;"
                   "min-width: 10em;"
                   "padding: 6px; }"
                   "QPushButton:pressed { background-color: rgba(70, 95, 104, 0.7);}"
                   );
}

ResultsTabWidget::ResultsTabWidget()
{

}

ResultsTabWidget::~ResultsTabWidget()
{

}
void ResultsTabWidget::exportToDBSlot()
{
    // MainWindow -> AlgorithmTab -> ResultsTab
    AlgorithmTab * algorithmTab = (AlgorithmTab*)m_parent;
    MainWindow * mainWindow = (MainWindow*)algorithmTab->getMainWindow();

    QString status = "Prêt";
    mainWindow->setStatusBarText(tr("Insertion des résultats dans la base de données en cours..."));
    mainWindow->startSpinner();

    QInputDialog* resultsNameInputDialog = new QInputDialog();
    resultsNameInputDialog->setWindowFlags(this->windowFlags() & ~Qt::WindowContextHelpButtonHint);
    resultsNameInputDialog->setOptions(QInputDialog::NoButtons);
    resultsNameInputDialog->setWindowIcon(QIcon(QString::fromUtf8("../icons/logo.ico")));

    // Also sets the text for the InputDialog
    QString suggestedName = QDir::home().dirName() + "_";
    QString message = "Veuillez entrer un nom permettant d'identifier ces résultats.";
    bool dialogResponse;
    QString dialogText =  resultsNameInputDialog->getText(NULL ,"Identification des résultats",
                                                          message, QLineEdit::Normal,
                                                          suggestedName, &dialogResponse);
    if (dialogResponse && !dialogText.isEmpty())
    {
        std::string serializedData;
        AlgorithmOutputInfoSerializer serializer;

        m_algorithmOutputInfo.m_resultName = dialogText.toStdString();
        serializer.Serialize(m_algorithmOutputInfo, serializedData);

        bool resultsAddedSuccessfully = m_databaseAccess->addResultsInDB(QString::fromStdString(serializedData));

        if(resultsAddedSuccessfully)
        {
            status = "Enregistrement en base de données réussi";
        }
        else
        {
            status = "Échec de l'enregistrement en base de données";
        }
    }
    else
    {
        status = "Enregistrement en base de données annulé";
    }

    delete resultsNameInputDialog;
    mainWindow->stopSpinner();
    mainWindow->setStatusBarText(status);
}

void ResultsTabWidget::exportToPdfSlot()
{
    // MainWindow -> AlgorithmTab -> ResultsTab
    AlgorithmTab * algorithmTab = (AlgorithmTab*)m_parent;
    MainWindow * mainWindow = (MainWindow*)algorithmTab->getMainWindow();
    mainWindow->setStatusBarText(tr("Enregistrement des résultats sous forme de fichier PDF en cours..."));
    mainWindow->startSpinner();

    QString status = "Prêt";

    QString filename = QFileDialog::getSaveFileName(this,tr("Save Document"), QDir::currentPath(),tr("PDF (*.pdf)"));
    if( !filename.isNull() )
    {
        QPdfWriter writer(filename);
        QPainter painter(&writer);

        painter.setPen(Qt::black);
        painter.drawText(4000,0,"Rapport d'algorithme: ");

        painter.setPen(Qt::black);
        painter.drawText(250,500,algoLabel->text());

        painter.setPen(Qt::black);
        painter.drawText(250,750,recordLabel->text());

        painter.setPen(Qt::black);
        painter.drawText(250,1000,dateLabel->text());

        painter.setPen(Qt::black);
        painter.drawText(250,1500,startHourLabel->text());

        painter.setPen(Qt::black);
        painter.drawText(250,1750,endHourLabel->text());

        painter.setPen(Qt::black);
        painter.drawText(250,2000,positionLabel->text());

        painter.setPen(Qt::black);
        painter.drawText(250,2250,measureUnitLabel->text());

        painter.setPen(Qt::black);
        painter.drawText(250,2500,computeTimeLabel->text());

        QPixmap pix = chartView->grab();
        int h = painter.window().height()*0.4;
        int w = h * 1.1;
        int x = (painter.window().width() / 2) - (w/2);
        int y = (painter.window().height() / 2) - (h/2);
        painter.drawPixmap(x, y, w, h, pix);

        painter.end();

        status = "Enregistrement du PDF réussi";
    }
    else
    {
        status = "Échec de l'enregistrement du PDF";
    }

    mainWindow->stopSpinner();
    mainWindow->setStatusBarText(status);
}
