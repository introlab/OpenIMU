#include "algorithmtab.h"
#include "../../MainWindow.h"
#include "../dialogs/AlgorithmParametersDialog.h"
#include "ResultsTabWidget.h"
#include "QHeaderView"
#include <QEventLoop>
#include <QDebug>

AlgorithmTab::AlgorithmTab(QWidget * parent, std::string uuid) : QWidget(parent)
{
        m_parent = parent;
        m_uuid = uuid;

        getAlgorithmsFromDB();

        // -- Layout
        algorithmLayout = new QVBoxLayout(this);

        // -- Algorithm Section
        algorithmLabel = new QLabel(tr("Algorithmes"));
        algorithmTableWidget = new QTableWidget(this);

        algorithmTableWidget->setRowCount(10);
        algorithmTableWidget->setColumnCount(3);

        algorithmTableHeaders<<"Nom"<<"Description"<<"Auteur";

        algorithmTableWidget->setHorizontalHeaderLabels(algorithmTableHeaders);

        QHeaderView * headerHoriz = algorithmTableWidget->horizontalHeader();
        QHeaderView * headerVerti = algorithmTableWidget->verticalHeader();
        headerHoriz->setSectionResizeMode(QHeaderView::Stretch);
        headerVerti->setSectionResizeMode(QHeaderView::Stretch);

        algorithmTableWidget->setEditTriggers(QAbstractItemView::NoEditTriggers);
        algorithmTableWidget->setSelectionBehavior(QAbstractItemView::SelectRows);
        algorithmTableWidget->setSelectionMode(QAbstractItemView::SingleSelection);
        //algorithmTableWidget->setStyleSheet("QTableView {alternate-background-color:#ecf0f1;selection-background-color: white;}");
        //algorithmTableWidget->verticalHeader()->setVisible(false);
        //algorithmTableWidget->verticalHeader()->setSectionResizeMode(QHeaderView::Stretch);

        for(int i =0; i<algoList.m_algorithmList.size();i++)
        {
            QString name = QString::fromStdString(algoList.m_algorithmList.at(i).name);
            algorithmTableWidget->setItem(i, 0, new QTableWidgetItem(name));
        }

        connect(algorithmTableWidget, SIGNAL(doubleClicked(const QModelIndex& )), this, SLOT(openParametersWindow(const QModelIndex &)));

        // -- Parameter Section
        parameterLabel = new QLabel(tr("Paramètre(s)"));
        parameterValues = new QLabel();
        // -- Result Section
        applyAlgorithm = new QPushButton(tr("Appliquer algorithme"));
        connect(applyAlgorithm, SIGNAL(clicked()),this, SLOT(openResultTab()));

        algorithmLayout->addWidget(algorithmLabel);
        algorithmLayout->addWidget(algorithmTableWidget);
        algorithmLayout->addWidget(parameterLabel);
        algorithmLayout->addWidget(parameterValues);
        algorithmLayout->addWidget(applyAlgorithm);

        this->setLayout(algorithmLayout);

        this->setStyleSheet( "QPushButton{"
                             "background-color: rgba(239, 73, 73,0.7);"
                             "border-style: inset;"
                             "border-width: 2px;"
                             "border-radius: 10px;"
                             "border-color: white;"
                             "font: 12px;"
                             "min-width: 10em;"
                             "padding: 6px; }"
                             "QPushButton:pressed { background-color: rgba(164, 49, 49, 0.7);}"
         );
}

void AlgorithmTab::setAlgoParameters(std::vector<ParametersInfo> parametersListUpdated)
{
    algoList.m_algorithmList.at(selectedIndexRow).parameters.swap(parametersListUpdated);
    createAlgoRequest();
    qDebug() << "hereee";
    QString temp;
    for(int i=0; i<parametersListUpdated.size();i++)
    {
        qDebug() << "hereee 2";
        temp = temp + QString::fromStdString(parametersListUpdated.at(i).name) + QString::fromStdString(parametersListUpdated.at(i).value);
        qDebug() << temp;
    }

    parameterValues->setText(temp);

}

bool AlgorithmTab::createAlgoRequest()
{
    std::string algoName = algoList.m_algorithmList.at(selectedIndexRow).name;
    std::string url = "http://127.0.0.1:5000/algo?filename="+algoName+"&uuid="+m_uuid;

    for(int i=0; i< algoList.m_algorithmList.at(selectedIndexRow).parameters.size();i++)
    {
        if(algoList.m_algorithmList.at(selectedIndexRow).parameters.at(i).name != "uuid")
        {
            url = url + "&"+algoList.m_algorithmList.at(selectedIndexRow).parameters.at(i).name +"="+algoList.m_algorithmList.at(selectedIndexRow).parameters.at(i).value;
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

void AlgorithmTab::openResultTab()
{

    MainWindow * test = (MainWindow*)m_parent;
    ResultsTabWidget* res = new ResultsTabWidget();
    test->replaceTab(res,"Résultats");
}

void AlgorithmTab::openParametersWindow(const QModelIndex &index)
{
    if (index.isValid() && algoList.m_algorithmList.size() != 0)
    {
        //Retrieve the selected Algorithm and it's parameters
        AlgorithmInfo clickedAlgorithm = algoList.m_algorithmList.at(index.row());
        selectedIndexRow = index.row();
        if(clickedAlgorithm.parameters.size()>0)
        {
            AlgorithmParametersDialog * algorithmParametersWindow = new AlgorithmParametersDialog(this, clickedAlgorithm);
            algorithmParametersWindow->exec();
            delete algorithmParametersWindow;
        }
        else
        {
            //TODO: Find a way to tell the user the algorithm doesn't have parameters.
        }
    }
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
    if (reply->error() == QNetworkReply::NoError)
   {
       std::string testReponse = reply->readAll();
       CJsonSerializer::Deserialize(&algoList, testReponse);
   }
   else
   {
       qDebug() << "error connect";
       qWarning() <<"ErrorNo: "<< reply->error() << "for url: " << reply->url().toString();
       qDebug() << "Request failed, " << reply->errorString();
       qDebug() << "Headers:"<<  reply->rawHeaderList()<< "content:" << reply->readAll();
       qDebug() << reply->readAll();
   }
   delete reply;
}

void AlgorithmTab::reponseAlgoRecue(QNetworkReply* reply)
{
    if (reply->error() == QNetworkReply::NoError)
   {
       std::string testReponse = reply->readAll();
       qDebug() << QString::fromStdString(testReponse);
   }
   else
   {
       qDebug() << "Error connect";
       qWarning() <<"ErrorNo: "<< reply->error() << "for url: " << reply->url().toString();
       qDebug() << "Request failed, " << reply->errorString();
       qDebug() << "Headers:"<<  reply->rawHeaderList()<< "content:" << reply->readAll();
       qDebug() << reply->readAll();
   }
   delete reply;
}
