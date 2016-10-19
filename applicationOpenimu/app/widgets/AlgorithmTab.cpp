#include "algorithmtab.h"
#include "../../MainWindow.h"
#include "AlgorithmParametersWindow.h"
#include "ResultsTabWidget.h"

AlgorithmTab::AlgorithmTab(QWidget * parent, std::string uuid) : QWidget(parent)
{
        m_parent = parent;
        m_uuid = uuid;

        // -- Layout
        algorithmLayout = new QVBoxLayout(this);

        // -- Algorithm Section
        algorithmLabel = new QLabel(tr("Algorithmes"));
        algorithmTableWidget = new QTableWidget(this);

        algorithmTableWidget->setRowCount(10);
        algorithmTableWidget->setColumnCount(3);

        algorithmTableHeaders<<"Nom"<<"Description"<<"Auteur";
        algorithmTableWidget->setHorizontalHeaderLabels(algorithmTableHeaders);
        algorithmTableWidget->setEditTriggers(QAbstractItemView::NoEditTriggers);
        algorithmTableWidget->setSelectionBehavior(QAbstractItemView::SelectRows);
        algorithmTableWidget->setSelectionMode(QAbstractItemView::SingleSelection);
        //algorithmTableWidget->setStyleSheet("QTableView {alternate-background-color:#ecf0f1;selection-background-color: white;}");
        //algorithmTableWidget->verticalHeader()->setVisible(false);


        algorithmTableWidget->setItem(0, 1, new QTableWidgetItem("Hello"));

        connect(algorithmTableWidget, SIGNAL(doubleClicked(const QModelIndex& )), this, SLOT(openParametersWindow(const QModelIndex &)));

        // -- Parameter Section
        parameterLabel = new QLabel(tr("Paramètre(s)"));

        // -- Result Section
        applyAlgorithm = new QPushButton(tr("Appliquer algorithme"));
        connect(applyAlgorithm, SIGNAL(clicked()),this, SLOT(openResultTab()));

        algorithmLayout->addWidget(algorithmLabel);
        algorithmLayout->addWidget(algorithmTableWidget);
        algorithmLayout->addWidget(parameterLabel);
        algorithmLayout->addWidget(applyAlgorithm);

        this->setLayout(algorithmLayout);

        this->setStyleSheet( "QPushButton{"
                             "background-color: rgba(230, 233, 239,1);"
                             "border-style: inset;"
                             "border-width: 2px;"
                             "border-radius: 10px;"
                             "border-color: white;"
                             "font: 12px;"
                             "min-width: 10em;"
                             "padding: 6px; }"
         );
}

void AlgorithmTab::openResultTab()
{
    MainWindow * test = (MainWindow*)m_parent;
    ResultsTabWidget* res = new ResultsTabWidget();
    test->replaceTab(res,"Résultats");
}

void AlgorithmTab::openParametersWindow(const QModelIndex &index)
{
    if (index.isValid())
    {
        algorithmTableWidget->setItem(index.row(), 2, new QTableWidgetItem("Goodbye"));

        AlgorithmParametersWindow algorithmParametersWindow;

        algorithmParametersWindow.show();

    }
}

bool AlgorithmTab::getAlgorithmsFromDB()
{
    QNetworkRequest request(QUrl("http://127.0.0.1:5000/algolist"));
    request.setRawHeader("User-Agent", "ApplicationNameV01");
    request.setRawHeader("Content-Type", "application/json");

    QNetworkAccessManager *manager = new QNetworkAccessManager();
    QNetworkReply *reply = manager->get(request);
    bool result = connect(manager, SIGNAL(finished(QNetworkReply*)), this ,SLOT(reponseRecue(QNetworkReply*)));

    return true;
}

void AlgorithmTab::reponseRecue(QNetworkReply* reply)
{
    if (reply->error() == QNetworkReply::NoError)
   {
       qDebug() << "connection";
       std::string testReponse(reply->readAll());
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
