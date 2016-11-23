#include "algorithmtab.h"
#include "../dialogs/AlgorithmParametersDialog.h"
#include "../../MainWindow.h"
#include "ResultsTabWidget.h"
#include "../utils/Utils.h"
#include "QHeaderView"
#include <QEventLoop>
#include <QDebug>

AlgorithmTab::AlgorithmTab(QWidget *parent, RecordInfo selectedRecord) : QWidget(parent)
{
        m_parent = parent;
        m_selectedRecord = selectedRecord;
        m_algorithmSerializer = new AlgorithmInfoSerializer();
        m_algorithmOutputSerializer = new AlgorithmOutputInfoSerializer();

        MainWindow * mainWindow = (MainWindow*)m_parent;

        //By default
        selectedIndexRow = 0;

        getAlgorithmsFromDB();

        // -- Layout
        algorithmListGroupBox = new QGroupBox();
        algorithmListGroupBox->setFixedHeight(300);
        //algorithmListGroupBox->setFlat(true);
        algorithmListLayout = new QVBoxLayout();

        algorithmTabLayout = new QVBoxLayout();


        // -- Algorithm List Section
        algorithmLabel = new QLabel(tr("Tableau des algorithmes disponibles"));
        algorithmTableWidget = new QTableWidget(this);

        algorithmTableWidget->setRowCount(10);
        algorithmTableWidget->setColumnCount(3);
        //algorithmTableWidget->setSizePolicy(QSizePolicy::Ignored,QSizePolicy::Ignored);

        algorithmTableHeaders<<"Nom"<<"Description"<<"Auteur";

        algorithmTableWidget->setHorizontalHeaderLabels(algorithmTableHeaders);

        QHeaderView * headerHoriz = algorithmTableWidget->horizontalHeader();
        QHeaderView * headerVerti = algorithmTableWidget->verticalHeader();

        headerHoriz->setSectionResizeMode(QHeaderView::Stretch);
        headerVerti->setSectionResizeMode(QHeaderView::Stretch);

        algorithmTableWidget->setEditTriggers(QAbstractItemView::NoEditTriggers);
        algorithmTableWidget->setSelectionBehavior(QAbstractItemView::SelectRows);
        algorithmTableWidget->setSelectionMode(QAbstractItemView::SingleSelection);
        //algorithmTableWidget->setShowGrid(false);

        QString headerStyle = "QHeaderView::section { border: none; }";
        QString gridStyle = "QTableView::item { border: none; }";

        algorithmTableWidget->setStyleSheet(headerStyle + gridStyle);

        for(int i =0; i<m_algorithmSerializer->m_algorithmList.size();i++)
        {
            QString name = Utils::capitalizeFirstCharacter(m_algorithmSerializer->m_algorithmList.at(i).name);
            algorithmTableWidget->setItem(i, 0, new QTableWidgetItem(name));

            QString description = Utils::capitalizeFirstCharacter(m_algorithmSerializer->m_algorithmList.at(i).description);
            algorithmTableWidget->setItem(i, 1, new QTableWidgetItem(description));

            QString author = Utils::capitalizeFirstCharacter(m_algorithmSerializer->m_algorithmList.at(i).author);
            algorithmTableWidget->setItem(i, 2, new QTableWidgetItem(author));
        }

        algorithmTableWidget->setRowCount(m_algorithmSerializer->m_algorithmList.size());

/*      //TO DELETE: (Just to see the scroll behavior)
        for(int i =0; i<10;i++)
        {
            QString name = QString::fromStdString("NAME: " + i);
            algorithmTableWidget->setItem(i, 0, new QTableWidgetItem(name));

            QString description = QString::fromStdString("DESCRIPTION: " + i);
            algorithmTableWidget->setItem(i, 1, new QTableWidgetItem(description));

            QString author = QString::fromStdString("AUTHOR: " + i);
            algorithmTableWidget->setItem(i, 2, new QTableWidgetItem(author));
        }

        algorithmTableWidget->setRowCount(algoList.m_algorithmList.size() + 10);
*/

        connect(algorithmTableWidget, SIGNAL(clicked(const QModelIndex& )), this, SLOT(openParametersWindow(const QModelIndex &)));

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

void AlgorithmTab::setAlgorithm(AlgorithmInfo algorithmInfo)
{
    algorithmParameters->Clear();

    //TODO:MADO selectedDataValues->setText(Utils::capitalizeFirstCharacter(QString::fromStdString(m_selectedRecord.m_recordName)));
    m_selectedAlgorithm = m_algorithmSerializer->m_algorithmList.at(selectedIndexRow);
    m_selectedAlgorithm.parameters.swap(algorithmInfo.parameters);
    algorithmParameters->setAlgorithm(algorithmInfo,m_selectedAlgorithm);
    }


void AlgorithmTab::openResultTab()
{
    bool showMessage = false;
    if(m_selectedAlgorithm.parameters.size() != 0)
    {
        for(int i=0; i< m_selectedAlgorithm.parameters.size();i++)
        {
            if(m_selectedAlgorithm.parameters.at(i).name != "uuid" && m_selectedAlgorithm.parameters.at(i).value.empty())
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

void AlgorithmTab::openParametersWindow(const QModelIndex &index)
{
    if (index.isValid() && m_algorithmSerializer->m_algorithmList.size() != 0)
    {
        //Retrieve the selected Algorithm and it's parameters
        AlgorithmInfo clickedAlgorithm = m_algorithmSerializer->m_algorithmList.at(index.row());
        selectedIndexRow = index.row();

        if((clickedAlgorithm.parameters.size() <= 0)||
                ((clickedAlgorithm.parameters.size() == 1) && (clickedAlgorithm.parameters.at(0).name == "uuid")))
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
    std::string url = "http://127.0.0.1:5000/algo?filename=" + m_selectedAlgorithm.name +
            "&uuid=" + m_selectedRecord.m_recordId;

    for(int i=0; i< m_selectedAlgorithm.parameters.size();i++)
    {
        if(m_selectedAlgorithm.parameters.at(i).name != "uuid")
        {
            url = url + "&"+m_selectedAlgorithm.parameters.at(i).name +"="+m_selectedAlgorithm.parameters.at(i).value;
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
    reponseRecue(reply);

    return true;
}

void AlgorithmTab::reponseRecue(QNetworkReply* reply)
{
    MainWindow * mainWindow = (MainWindow*)m_parent;
    if (reply->error() == QNetworkReply::NoError)
   {
       mainWindow->setStatusBarText(tr("Application de l'agorithme complété"));
       std::string testReponse = reply->readAll().toStdString();
       CJsonSerializer::Deserialize(m_algorithmSerializer, testReponse);
   }
   else
   {
       mainWindow->setStatusBarText(tr("Application de l'agorithme non réussi"));
   }
   delete reply;
}

void AlgorithmTab::reponseAlgoRecue(QNetworkReply* reply)
{
    if (reply->error() == QNetworkReply::NoError)
   {
       std::string reponse = reply->readAll().toStdString();
       AlgorithmOutputInfoSerializer algorithmOutputInfoSerializer;
       if(reponse != "")
       {
           CJsonSerializer::Deserialize(&algorithmOutputInfoSerializer, reponse);
           MainWindow * test = (MainWindow*)m_parent;
           AlgorithmInfo &algoInfo = m_algorithmSerializer->m_algorithmList.at(selectedIndexRow);
           ResultsTabWidget* res = new ResultsTabWidget(this, m_selectedRecord, algoInfo, algorithmOutputInfoSerializer.m_algorithmOutput);
           test->replaceTab(res,algoInfo.name + ": " + m_selectedRecord.m_recordName);
       }
   }
   else
   {
       //qDebug() << "Error connect";
       //qWarning() <<"ErrorNo: "<< reply->error() << "for url: " << reply->url().toString();
       //qDebug() << "Request failed, " << reply->errorString();
       //qDebug() << "Headers:"<<  reply->rawHeaderList()<< "content:" << reply->readAll();
       //qDebug() << reply->readAll();
   }
   delete reply;
}
