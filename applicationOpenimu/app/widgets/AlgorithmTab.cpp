#include "algorithmtab.h"
#include "../dialogs/AlgorithmParametersDialog.h"
#include "../../MainWindow.h"
#include "ResultsTabWidget.h"
#include "../utilities/Utilities.h"
#include "QHeaderView"
#include <QEventLoop>
#include <QDebug>

AlgorithmTab::AlgorithmTab(QWidget *parent, RecordInfo selectedRecord) : QWidget(parent)
{
        m_parent = parent;
        m_selectedRecord = selectedRecord;

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

        for(int i =0; i<m_algorithmSerializer.m_algorithmList.size();i++)
        {
            QString name = Utilities::capitalizeFirstCharacter(m_algorithmSerializer.m_algorithmList.at(i).m_name);
            algorithmTableWidget->setItem(i, 0, new QTableWidgetItem(name));

            QString description = Utilities::capitalizeFirstCharacter(m_algorithmSerializer.m_algorithmList.at(i).m_description);
            algorithmTableWidget->setItem(i, 1, new QTableWidgetItem(description));

            QString author = Utilities::capitalizeFirstCharacter(m_algorithmSerializer.m_algorithmList.at(i).m_author);
            algorithmTableWidget->setItem(i, 2, new QTableWidgetItem(author));
        }

        algorithmTableWidget->setRowCount(m_algorithmSerializer.m_algorithmList.size());

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
    qDebug() << "calling setAlgorithm()" ;
    qDebug() << "calling setAlgorithm() : Algorithm: " + QString::fromStdString(algorithmInfo.m_name) ;

    algorithmParameters->Clear();

    //TODO:MADO selectedDataValues->setText(Utils::capitalizeFirstCharacter(QString::fromStdString(m_selectedRecord.m_recordName)));
    m_selectedAlgorithm = m_algorithmSerializer.m_algorithmList.at(selectedIndexRow);
    m_selectedAlgorithm.m_parameters.swap(algorithmInfo.m_parameters);
    algorithmParameters->setAlgorithm(algorithmInfo,m_selectedAlgorithm);
}


void AlgorithmTab::openResultTab()
{
    qDebug() << "calling AlgorithmTab::openResultTab()";
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
        qDebug() << "calling AlgorithmTab::openResultTab(): checked parameters";
        if(showMessage)
        {
            QMessageBox messageBox;
            messageBox.warning(0,tr("Avertissement"),"Veuillez entrer des valeur pour le(s) paramètre(s)");
            messageBox.setFixedSize(500,200);
        }
        else
        {
            qDebug() << "calling AlgorithmTab::openResultTab(): createAlgoRequest()";
            createAlgoRequest();
        }
    }
    else
        qDebug() << "calling AlgorithmTab::openResultTab(): param size is zero";
}

void AlgorithmTab::openParametersWindow(const QModelIndex &index)
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
    qDebug() << "calling AlgorithmTab::openResultTab(): createAlgoRequest()";
    std::string url = "http://127.0.0.1:5000/algo?filename=" + m_selectedAlgorithm.m_name +
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

    qDebug() << "calling AlgorithmTab::createAlgoRequest(): about to connect..";
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
       m_algorithmSerializer.Deserialize(testReponse);
   }
   else
   {
       mainWindow->setStatusBarText(tr("Application de l'agorithme non réussi"));
   }
   delete reply;
}

void AlgorithmTab::reponseAlgoRecue(QNetworkReply* reply)
{
    qDebug() << "calling AlgorithmTab::reponseAlgoRecue()";
    if (reply->error() == QNetworkReply::NoError)
   {
       std::string reponse = reply->readAll().toStdString();
       AlgorithmOutputInfoSerializer algorithmOutputInfoSerializer;
       qDebug() << "calling AlgorithmTab::reponseAlgoRecue() Response : " + QString::fromStdString(reponse);
       if(reponse != "")
       {
           qDebug() << "calling AlgorithmTab::reponseAlgoRecue(): About to Deserialize response";
           algorithmOutputInfoSerializer.Deserialize(reponse);

           qDebug() << "calling AlgorithmTab::reponseAlgoRecue(): About to create ResultsTab";
           MainWindow * test = (MainWindow*)m_parent;
           AlgorithmInfo &algoInfo = m_algorithmSerializer.m_algorithmList.at(selectedIndexRow);

           algorithmOutputInfoSerializer.m_algorithmOutput.m_algorithmId = algoInfo.m_id;
           algorithmOutputInfoSerializer.m_algorithmOutput.m_algorithmName = algoInfo.m_name;
           algorithmOutputInfoSerializer.m_algorithmOutput.m_algorithmParameters = algoInfo.m_parameters;

           ResultsTabWidget* res = new ResultsTabWidget(this, m_selectedRecord, algorithmOutputInfoSerializer.m_algorithmOutput);
           test->addTab(res,algoInfo.m_name + ": " + m_selectedRecord.m_recordName);
       }
       else
       {
           qDebug() << "calling AlgorithmTab::reponseAlgoRecue() Reponse = empty string";
       }
   }
   else
   {
       qDebug() << "calling AlgorithmTab::reponseAlgoRecue() Error connect";
       //qWarning() <<"ErrorNo: "<< reply->error() << "for url: " << reply->url().toString();
       //qDebug() << "Request failed, " << reply->errorString();
       //qDebug() << "Headers:"<<  reply->rawHeaderList()<< "content:" << reply->readAll();
       //qDebug() << reply->readAll();
   }
   delete reply;
}
