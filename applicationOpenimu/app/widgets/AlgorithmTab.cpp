#include "QHeaderView"
#include <QEventLoop>
#include <QDebug>

#include "algorithmtab.h"
#include "ResultsTabWidget.h"

#include "../dialogs/AlgorithmParametersDialog.h"
#include "../../MainWindow.h"
#include "../utilities/Utilities.h"
#include "../algorithm/FilteredData.h"
#include "acquisition/CJsonSerializer.h"

AlgorithmTab::AlgorithmTab(QWidget *parent, RecordInfo selectedRecord) : QWidget(parent)
{
        m_parent = parent;
        m_selectedRecord = selectedRecord;

        MainWindow * mainWindow = (MainWindow*)m_parent;

        //By default
        selectedIndexRow = 0;

        getAlgorithmsFromDB();

        // -- Layout
        algorithmListGroupBox = new QGroupBox(this);
        algorithmListGroupBox->setFixedHeight(300);
        algorithmListLayout = new QVBoxLayout(this);
        algorithmTabLayout = new QVBoxLayout(this);

        // -- Algorithm List Section
        algorithmLabel = new QLabel(tr("Tableau des algorithmes disponibles"));
        algorithmTableWidget = new QTableWidget(this);
        algorithmTableWidget->setRowCount(10);
        algorithmTableWidget->setColumnCount(3);

        algorithmTableHeaders<<"Nom"<<"Description"<<"Auteur";

        algorithmTableWidget->setHorizontalHeaderLabels(algorithmTableHeaders);

        QHeaderView * headerHoriz = algorithmTableWidget->horizontalHeader();
        QHeaderView * headerVerti = algorithmTableWidget->verticalHeader();

        headerHoriz->setHighlightSections(false);
        headerVerti->setHighlightSections(false);

        headerHoriz->setSectionResizeMode(QHeaderView::Stretch);
        headerVerti->setSectionResizeMode(QHeaderView::Stretch);

        algorithmTableWidget->setEditTriggers(QAbstractItemView::NoEditTriggers);
        algorithmTableWidget->setSelectionMode(QAbstractItemView::SingleSelection);
        algorithmTableWidget->setSelectionBehavior(QAbstractItemView::SelectRows);

        algorithmTableWidget->setShowGrid(false);
        algorithmTableWidget->setGeometry(QApplication::desktop()->screenGeometry());

        QString selectionStyle = "QTableWidget::item:selected{background-color: palette(highlight); color: palette(highlightedText);};";

        algorithmTableWidget->setStyleSheet(selectionStyle);

        for(int i =0; i<m_algorithmSerializer.m_algorithmList.size();i++)
        {
            QString name = QString::fromStdString(m_algorithmSerializer.m_algorithmList.at(i).m_name);
            algorithmTableWidget->setItem(i, 0, new QTableWidgetItem(name));

            QString description =QString::fromStdString(m_algorithmSerializer.m_algorithmList.at(i).m_description);
            algorithmTableWidget->setItem(i, 1, new QTableWidgetItem(description));

            QString author = QString::fromStdString(m_algorithmSerializer.m_algorithmList.at(i).m_author);
            algorithmTableWidget->setItem(i, 2, new QTableWidgetItem(author));
        }

        algorithmTableWidget->setRowCount(m_algorithmSerializer.m_algorithmList.size());

        connect(algorithmTableWidget, SIGNAL(clicked(const QModelIndex& )), this, SLOT(onClickOpenParametersWindow(const QModelIndex &)));

        // -- Parameter Section
        algorithmParameters = new AlgorithmDetailedView();

        applyAlgorithm = new QPushButton(tr("Appliquer algorithme"));
        connect(applyAlgorithm, SIGNAL(clicked()),this, SLOT(openResultTab()));

        // -- Setting the layout
        algorithmListLayout->addWidget(algorithmLabel);
        algorithmListLayout->addWidget(algorithmTableWidget);
        algorithmListGroupBox->setLayout(algorithmListLayout);

        algorithmTabLayout->addWidget(algorithmListGroupBox);
        algorithmTabLayout->addWidget(algorithmParameters);
        algorithmTabLayout->addSpacing(50);
        algorithmTabLayout->addWidget(applyAlgorithm);

        this->setLayout(algorithmTabLayout);
        this->setStyleSheet( "QPushButton{"
                             "background-color: rgba(119, 160, 175,0.7);"
                             "border-style: inset;"
                             "border-width: 0px;"
                             "border-radius: 10px;"
                             "border-color: white;"
                             "font: 12px;"
                             "min-width: 10em;"
                             "padding: 6px; }"
                             "QPushButton:pressed { background-color: rgba(70, 95, 104, 0.7);}"
                             );
}

QWidget* AlgorithmTab::getMainWindow()
{
    return m_parent;
}

void AlgorithmTab::setAlgorithm(AlgorithmInfo algorithmInfo)
{
    algorithmParameters->Clear();

    m_selectedAlgorithm = m_algorithmSerializer.m_algorithmList.at(selectedIndexRow);
    m_selectedAlgorithm.m_parameters.swap(algorithmInfo.m_parameters);
    algorithmParameters->setAlgorithm(algorithmInfo,m_selectedAlgorithm);
}

void AlgorithmTab::openResultTab()
{
    bool showMessage = false;
    if(m_selectedAlgorithm.m_parameters.size() != 0)
    {
        for(int i=0; i< m_selectedAlgorithm.m_parameters.size();i++)
        {
            if(m_selectedAlgorithm.m_parameters.at(i).m_name != "uuid" && m_selectedAlgorithm.m_parameters.at(i).m_value.empty())
            {
                showMessage = true;
            }
        }

        if(showMessage)
        {
            QMessageBox messageBox;
            messageBox.warning(0,tr("Avertissement"),"Veuillez entrer des valeur pour le(s) paramètre(s)");
            messageBox.setFixedSize(500,200);
        }
        else
        {
            createAlgoRequest();
        }
    }
}

void AlgorithmTab::onClickOpenParametersWindow(const QModelIndex &index)
{
    if (index.isValid() && m_algorithmSerializer.m_algorithmList.size() != 0)
    {
        //Retrieve the selected Algorithm and it's parameters
        AlgorithmInfo clickedAlgorithm = m_algorithmSerializer.m_algorithmList.at(index.row());
        selectedIndexRow = index.row();

        if((clickedAlgorithm.m_parameters.size() <= 0)||
                ((clickedAlgorithm.m_parameters.size() == 1) && (clickedAlgorithm.m_parameters.at(0).m_name == "uuid")))
        {
            setAlgorithm(clickedAlgorithm);
        }
        else
        {
            setAlgorithm(clickedAlgorithm);
            AlgorithmParametersDialog * algorithmParametersWindow = new AlgorithmParametersDialog(this, clickedAlgorithm);
            algorithmParametersWindow->exec();
            delete algorithmParametersWindow;
        }
    }
}

bool AlgorithmTab::createAlgoRequest()
{
    std::string url = "http://127.0.0.1:5000/algo?filename=" + m_selectedAlgorithm.m_filename +
            "&uuid=" + m_selectedRecord.m_recordId;
    qDebug()<< QString::fromStdString(url);
    for(int i=0; i< m_selectedAlgorithm.m_parameters.size();i++)
    {
        if(m_selectedAlgorithm.m_parameters.at(i).m_name != "uuid")
        {
            url = url + "&"+m_selectedAlgorithm.m_parameters.at(i).m_name +"="+m_selectedAlgorithm.m_parameters.at(i).m_value;
        }
    }

    QNetworkRequest request(QUrl(QString::fromStdString(url)));
    request.setRawHeader("User-Agent", "ApplicationNameV01");
    request.setRawHeader("Content-Type", "application/json");

    QNetworkAccessManager *manager = new QNetworkAccessManager();
    QNetworkReply *reply = manager->get(request);

    QEventLoop loop;

    bool result = connect(manager, SIGNAL(finished(QNetworkReply*)), &loop,SLOT(quit()));
    loop.exec();
    reponseAlgoRecue(reply);

    return true;
}

bool AlgorithmTab::getAlgorithmsFromDB()
{
    QNetworkRequest request(QUrl("http://127.0.0.1:5000/algolist"));
    request.setRawHeader("User-Agent", "ApplicationNameV01");
    request.setRawHeader("Content-Type", "application/json");

    QNetworkAccessManager *manager = new QNetworkAccessManager();
    QNetworkReply *reply = manager->get(request);

    QEventLoop loop;
    bool result = connect(manager, SIGNAL(finished(QNetworkReply*)), &loop,SLOT(quit()));
    loop.exec();
    algoListResponse(reply);

    return true;
}

void AlgorithmTab::algoListResponse(QNetworkReply* reply)
{
    MainWindow * mainWindow = (MainWindow*)m_parent;
    if (reply->error() == QNetworkReply::NoError)
   {
       mainWindow->setStatusBarText(tr("L'algorithme a été appliqué avec succès"), MessageStatus::success);
       std::string testReponse = reply->readAll().toStdString();
       m_algorithmSerializer.Deserialize(testReponse);
   }
   else
   {
       mainWindow->setStatusBarText(tr("Échec de l'application de l'algorithme"), MessageStatus::error);
   }
   delete reply;
}

void AlgorithmTab::reponseAlgoRecue(QNetworkReply* reply)
{
    if (reply->error() == QNetworkReply::NoError)
   {
       std::string reponse = reply->readAll().toStdString();
       AlgorithmOutputInfoSerializer algorithmOutputInfoSerializer;
       MainWindow * window = (MainWindow*)m_parent;

       if(reponse != "" && m_selectedAlgorithm.m_id.compare("3") != 0)
       {
           algorithmOutputInfoSerializer.Deserialize(reponse);


           AlgorithmInfo &algoInfo = m_selectedAlgorithm;

           algorithmOutputInfoSerializer.m_algorithmOutput.m_algorithmId = algoInfo.m_id;
           algorithmOutputInfoSerializer.m_algorithmOutput.m_algorithmName = algoInfo.m_name;
           algorithmOutputInfoSerializer.m_algorithmOutput.m_algorithmParameters = algoInfo.m_parameters;
           algorithmOutputInfoSerializer.m_algorithmOutput.m_recordType = m_selectedRecord.m_imuType;
           algorithmOutputInfoSerializer.m_algorithmOutput.m_recordId = m_selectedRecord.m_recordId;
           algorithmOutputInfoSerializer.m_algorithmOutput.m_recordName = m_selectedRecord.m_recordName;
           algorithmOutputInfoSerializer.m_algorithmOutput.m_recordImuPosition = m_selectedRecord.m_imuPosition;

           ResultsTabWidget* res = new ResultsTabWidget(this, algorithmOutputInfoSerializer.m_algorithmOutput);
           window->addTab(res,algoInfo.m_name + ": " + m_selectedRecord.m_recordName);
       }
       else
       {
            FilteredData fData;
            CJsonSerializer::Deserialize(&fData, reponse);
            WimuAcquisition wimuData;
            wimuData.setDataAccelerometer(fData.m_dataAccelerometer);
            ResultsTabWidget* res = new ResultsTabWidget(this,wimuData, m_selectedRecord);
            window->addTab(res,"Filtre: " + m_selectedRecord.m_recordName);
       }
   }
   else
   {
       qDebug() << reply->readAll();
   }
   delete reply;
}
