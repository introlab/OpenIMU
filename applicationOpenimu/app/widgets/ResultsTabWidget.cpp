#include "ResultsTabWidget.h"
#include <QtWidgets>
#include <QPdfWriter>
#include <QPainter>

ResultsTabWidget::ResultsTabWidget(QWidget *parent,RecordInfo& recordInfo, AlgorithmInfo algoInfo, AlgorithmOutputInfo output):QWidget(parent)
{
    m_recordInfo= recordInfo;
    init(algoInfo, output);
}


void ResultsTabWidget::init(AlgorithmInfo algoInfo, AlgorithmOutputInfo output)
{
    qDebug() << "ResultsTabWidget::init()";

    qDebug() << "calling ResultsTabWidget(): init() : AlgorithmOutput : AlgorithmInfo : name: " << QString::fromStdString(output.m_algorithmInfo.name);
    qDebug() << "calling ResultsTabWidget(): init() AlgorithmOutput : AlgorithmInfo : author: " << QString::fromStdString(output.m_algorithmInfo.author);
    qDebug() << "calling ResultsTabWidget(): init() AlgorithmOutput : AlgorithmInfo : description: " << QString::fromStdString(output.m_algorithmInfo.description);
    qDebug() << "calling ResultsTabWidget(): init() AlgorithmOutput : AlgorithmInfo : details: " << QString::fromStdString(output.m_algorithmInfo.details);

    for(int i = 0; i < output.m_algorithmInfo.parameters.size(); i++)
    {
        ParametersInfo p = output.m_algorithmInfo.parameters.at(i);
        qDebug() << "calling ResultsTabWidget(): init() AlgorithmOutput : AlgorithmInfo : parameter(s) " << i  << " " + QString::fromStdString(p.name);
        qDebug() << "calling ResultsTabWidget(): init() AlgorithmOutput : AlgorithmInfo : parameter(s) " << i << " " + QString::fromStdString(p.description);
        qDebug() << "calling ResultsTabWidget(): init() AlgorithmOutput : AlgorithmInfo : parameter(s) " << i << " " + QString::fromStdString(p.value);
    }

    qDebug() << "calling ResultsTabWidget(): init() AlgorithmOutput : Date: " << QString::fromStdString(output.m_date);
    qDebug() << "calling ResultsTabWidget(): init() AlgorithmOutput : Start time: " << QString::fromStdString(output.m_startTime);
    qDebug() << "calling ResultsTabWidget(): init() AlgorithmOutput : End time: " << QString::fromStdString(output.m_endTime);
    qDebug() << "calling ResultsTabWidget(): init() AlgorithmOutput : Execution time: " << output.m_executionTime;
    qDebug() << "calling ResultsTabWidget(): init() AlgorithmOutput : Measurement unit: " << QString::fromStdString(output.m_measureUnit);
    qDebug() << "calling ResultsTabWidget(): init() AlgorithmOutput : Value " << output.m_value;

    m_databaseAccess = new DbBlock();

    m_algorithmOutputInfo = output;
    m_algorithmOutputInfo.m_algorithmInfo = algoInfo;

    layout = new QGridLayout;
    this->setLayout(layout);

    qDebug() << "ResultsTabWidget::init(): UI Stuff";

    QString algoName = "Algorithme appliqué: " + QString::fromStdString(m_algorithmOutputInfo.m_algorithmInfo.name);
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

    if(algoInfo.name == "activityTracker")
    {
        qDebug() << "ResultsTabWidget::init(): if(activityTracker)";
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
        qDebug() << "ResultsTabWidget::init(): Not activity tracker";
       QLabel* labelResult = new QLabel("Résultat de l'algorithme : " + QString::fromStdString(std::to_string(m_algorithmOutputInfo.m_value)) +" pas" );

       algoLabel->setFont(QFont( "Arial", 12, QFont::Light));
       layout->addWidget(labelResult,9,0,Qt::AlignCenter);
    }

    qDebug() << "ResultsTabWidget::init(): Buttons...";

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
    qDebug() << "calling exportToDB()";


    qDebug() << "calling exportToDB(): AlgorithmOutput : AlgorithmInfo : name: " << QString::fromStdString(m_algorithmOutputInfo.m_algorithmInfo.name);
    qDebug() << "calling exportToDB(): AlgorithmOutput : AlgorithmInfo : author: " << QString::fromStdString(m_algorithmOutputInfo.m_algorithmInfo.author);
    qDebug() << "calling exportToDB(): AlgorithmOutput : AlgorithmInfo : description: " << QString::fromStdString(m_algorithmOutputInfo.m_algorithmInfo.description);
    qDebug() << "calling exportToDB(): AlgorithmOutput : AlgorithmInfo : details: " << QString::fromStdString(m_algorithmOutputInfo.m_algorithmInfo.details);

    for(int i = 0; i < m_algorithmOutputInfo.m_algorithmInfo.parameters.size(); i++)
    {
        ParametersInfo p = m_algorithmOutputInfo.m_algorithmInfo.parameters.at(i);
        qDebug() << "calling exportToDB(): AlgorithmOutput : AlgorithmInfo : parameter(s) " << i  << " " + QString::fromStdString(p.name);
        qDebug() << "calling exportToDB(): AlgorithmOutput : AlgorithmInfo : parameter(s) " << i << " " + QString::fromStdString(p.description);
        qDebug() << "calling exportToDB(): AlgorithmOutput : AlgorithmInfo : parameter(s) " << i << " " + QString::fromStdString(p.value);
    }

    qDebug() << "calling exportToDB(): AlgorithmOutput : Date: " << QString::fromStdString(m_algorithmOutputInfo.m_date);
    qDebug() << "calling exportToDB(): AlgorithmOutput : Start time: " << QString::fromStdString(m_algorithmOutputInfo.m_startTime);
    qDebug() << "calling exportToDB(): AlgorithmOutput : End time: " << QString::fromStdString(m_algorithmOutputInfo.m_endTime);
    qDebug() << "calling exportToDB(): AlgorithmOutput : Execution time: " << m_algorithmOutputInfo.m_executionTime;
    qDebug() << "calling exportToDB(): AlgorithmOutput : Measurement unit: " << QString::fromStdString(m_algorithmOutputInfo.m_measureUnit);
    qDebug() << "calling exportToDB(): AlgorithmOutput : Value " << m_algorithmOutputInfo.m_value;


    std::string serializedData;
    AlgorithmOutputInfoSerializer serializer;
    qDebug() << "calling exportToDB() : Serialiazer created";

    serializer.Serialize(m_algorithmOutputInfo, serializedData);

    m_databaseAccess->addResultsInDB(QString::fromStdString(serializedData));

    qDebug() << "calling exportToDB() : addResultsInDB()";
}

void ResultsTabWidget::exportToPdfSlot()
{
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
    }
}
