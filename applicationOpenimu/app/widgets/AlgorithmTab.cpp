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
#include "GenericAlgoResults.h"

AlgorithmTab::AlgorithmTab(QWidget *parent, RecordInfo selectedRecord) : QWidget(parent)
{
    m_parent = parent;
    m_selectedRecord = selectedRecord;

    //By default
    m_selectedIndexRow = 0;

    getAlgorithmsFromDB();

    // -- Layout
    m_algorithmListGroupBox = new QGroupBox(this);
    m_algorithmListGroupBox->setFixedHeight(300);
    m_algorithmListLayout = new QVBoxLayout(this);
    m_algorithmTabLayout = new QVBoxLayout(this);

    // -- Algorithm List Section
    m_algorithmLabel = new QLabel(tr("Tableau des algorithmes disponibles"));
    m_algorithmTableWidget = new QTableWidget(this);
    m_algorithmTableWidget->setRowCount(10);
    m_algorithmTableWidget->setColumnCount(3);

    m_algorithmTableHeaders<<"Nom"<<"Description"<<"Auteur";

    m_algorithmTableWidget->setHorizontalHeaderLabels(m_algorithmTableHeaders);

    QHeaderView * headerHoriz = m_algorithmTableWidget->horizontalHeader();
    QHeaderView * headerVerti = m_algorithmTableWidget->verticalHeader();

    headerHoriz->setHighlightSections(false);
    headerVerti->setHighlightSections(false);

    headerHoriz->setSectionResizeMode(QHeaderView::Stretch);
    headerVerti->setSectionResizeMode(QHeaderView::Stretch);

    m_algorithmTableWidget->setEditTriggers(QAbstractItemView::NoEditTriggers);
    m_algorithmTableWidget->setSelectionMode(QAbstractItemView::SingleSelection);
    m_algorithmTableWidget->setSelectionBehavior(QAbstractItemView::SelectRows);

    m_algorithmTableWidget->setShowGrid(false);
    m_algorithmTableWidget->setGeometry(QApplication::desktop()->screenGeometry());

    QString selectionStyle = "QTableWidget::item:selected{background-color: palette(highlight); color: palette(highlightedText);};";

    m_algorithmTableWidget->setStyleSheet(selectionStyle);

    for(int i =0; i<m_algorithmSerializer.m_algorithmList.size();i++)
    {
        QString name = QString::fromStdString(m_algorithmSerializer.m_algorithmList.at(i).m_name);
        m_algorithmTableWidget->setItem(i, 0, new QTableWidgetItem(name));

        QString description =QString::fromStdString(m_algorithmSerializer.m_algorithmList.at(i).m_description);
        m_algorithmTableWidget->setItem(i, 1, new QTableWidgetItem(description));

        QString author = QString::fromStdString(m_algorithmSerializer.m_algorithmList.at(i).m_author);
        m_algorithmTableWidget->setItem(i, 2, new QTableWidgetItem(author));
    }

    m_algorithmTableWidget->setRowCount(m_algorithmSerializer.m_algorithmList.size());

    connect(m_algorithmTableWidget, SIGNAL(clicked(const QModelIndex& )), this, SLOT(onClickOpenParametersWindow(const QModelIndex &)));

    // -- Parameter Section
    m_algorithmParameters = new AlgorithmDetailedView();

    m_applyAlgorithm = new QPushButton(tr(""));
    QIcon img(":/icons/applyAlgo.png");
    m_applyAlgorithm->setIcon(img);
    m_applyAlgorithm->setIconSize(QSize(175,35));
    m_applyAlgorithm->setCursor(Qt::PointingHandCursor);
    connect(m_applyAlgorithm, SIGNAL(clicked()),this, SLOT(openResultTab()));

    // -- Setting the layout
    m_algorithmListLayout->addWidget(m_algorithmLabel);
    m_algorithmListLayout->addWidget(m_algorithmTableWidget);
    m_algorithmListGroupBox->setLayout(m_algorithmListLayout);

    m_algorithmTabLayout->addWidget(m_algorithmListGroupBox);
    m_algorithmTabLayout->addWidget(m_algorithmParameters);
    m_algorithmTabLayout->addSpacing(50);
    m_algorithmTabLayout->addWidget(m_applyAlgorithm);

    this->setLayout(m_algorithmTabLayout);
}

QWidget* AlgorithmTab::getMainWindow()
{
    return m_parent;
}

void AlgorithmTab::setAlgorithm(AlgorithmInfo algorithmInfo)
{
    m_algorithmParameters->Clear();

    m_selectedAlgorithm = m_algorithmSerializer.m_algorithmList.at(m_selectedIndexRow);
    m_selectedAlgorithm.m_parameters.swap(algorithmInfo.m_parameters);
    m_algorithmParameters->setAlgorithm(algorithmInfo,m_selectedAlgorithm);
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
        m_selectedIndexRow = index.row();

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
    MainWindow* mainWindow = (MainWindow*)m_parent;
    mainWindow->startSpinner();
    mainWindow->setStatusBarText("Application de l'algorithme...");

    std::string url = "http://127.0.0.1:5000/algo?filename=" + m_selectedAlgorithm.m_filename +
            "&uuid=" + m_selectedRecord.m_recordId;
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

    if(!result)
    {
        mainWindow->setStatusBarText("Erreur de connexion lors de l'application de l'algorithme", MessageStatus::error);
    }

    loop.exec();
    reponseAlgoRecue(reply);

    mainWindow->stopSpinner();

    return result;
}

bool AlgorithmTab::getAlgorithmsFromDB()
{
    MainWindow* mainWindow = (MainWindow*)m_parent;
    mainWindow->startSpinner();
    mainWindow->setStatusBarText("Récupération des algorithmes...");

    QNetworkRequest request(QUrl("http://127.0.0.1:5000/algolist"));
    request.setRawHeader("User-Agent", "ApplicationNameV01");
    request.setRawHeader("Content-Type", "application/json");

    QNetworkAccessManager *manager = new QNetworkAccessManager();
    QNetworkReply *reply = manager->get(request);

    QEventLoop loop;
    bool result = connect(manager, SIGNAL(finished(QNetworkReply*)), &loop,SLOT(quit()));

    if(!result)
    {
        mainWindow->setStatusBarText("Erreur de connexion lors de la récupération des algorithmes", MessageStatus::error);
    }

    loop.exec();
    algoListResponse(reply);

    mainWindow->stopSpinner();

    return result;
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
    MainWindow* mainWindow = (MainWindow*)m_parent;
    AlgorithmOutputInfoSerializer algorithmOutputInfoSerializer;

    if (reply->error() == QNetworkReply::NoError)
    {
        std::string reponse = reply->readAll().toStdString();

        if(reponse != "")
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

            if(algorithmOutputInfoSerializer.m_algorithmOutput.m_dispType.compare("2d_graph")==0)
            {
                FilteredData fData;
                CJsonSerializer::Deserialize(&fData, reponse);
                WimuAcquisition wimuData;
                wimuData.setDataAccelerometer(fData.m_dataAccelerometer);
                ResultsTabWidget* res = new ResultsTabWidget(this,wimuData, m_selectedRecord);
                mainWindow->addTab(res,"Filtre: " + m_selectedRecord.m_recordName);
            }
            else if (algorithmOutputInfoSerializer.m_algorithmOutput.m_dispType.compare("Numeric value")==0)
            {
                ResultsTabWidget* res = new ResultsTabWidget(this, algorithmOutputInfoSerializer.m_algorithmOutput);
                mainWindow->addTab(res,algoInfo.m_name + ": " + m_selectedRecord.m_recordName);
            }
            else
            {
                GenericAlgoResults* res = new GenericAlgoResults(this, algorithmOutputInfoSerializer.m_algorithmOutput, reponse);
                mainWindow->addTab(res,algoInfo.m_name + ": " + m_selectedRecord.m_recordName);
            }

            mainWindow->setStatusBarText("Algorithme appliqué avec succès", MessageStatus::success);
        }
        else
        {
            mainWindow->setStatusBarText("La requête reçue n'a pas retournée des résultats", MessageStatus::warning);
        }
    }
    else
    {
        mainWindow->setStatusBarText("Erreur lors de l'application de l'algorithme", MessageStatus::error);
    }
    delete reply;
}
