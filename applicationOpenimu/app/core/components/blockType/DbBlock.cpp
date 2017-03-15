#include "DbBlock.h"
#include <iostream>

DbBlock::DbBlock()
    :m_manager(new QNetworkAccessManager(this))
{
    connect(m_manager, SIGNAL(finished(QNetworkReply *)), this, SLOT(reponseRecue(QNetworkReply*)));
    m_addRecordTime = new QTime();
}

DbBlock::~DbBlock()
{
}

std::vector<QString> DbBlock::getDaysInDB()
{
    std::vector<QString> listSavedDays; // Insert call to Db returning days available
    listSavedDays.push_back("24 Septembre 2016");
    listSavedDays.push_back("25 Septembre 2016");

    return listSavedDays;
}

bool DbBlock::addRecordInDB(const QString &json)
{
    QNetworkAccessManager *manager = new QNetworkAccessManager();
    QByteArray dataByteArray (json.toStdString().c_str(),json.toStdString().length());                                                                                                                  //Your webservice URL

    QNetworkRequest request(QUrl("http://127.0.0.1:5000/insertrecord"));
    QByteArray postDataSize = QByteArray::number(dataByteArray.size());

    request.setRawHeader("User-Agent", "ApplicationNameV01");
    request.setRawHeader("Content-Type", "application/json");
    request.setRawHeader("Content-Length", postDataSize);

    if (manager) {
        bool result;

        QNetworkReply *reply = manager->post(request, dataByteArray);

        result = connect(manager, SIGNAL(finished(QNetworkReply*)), this,SLOT(reponseRecue(QNetworkReply*)));

        qDebug() <<"Connection is success : ? :" << result;
        if (reply) {
            qDebug() <<"Reply from server is"<< reply;
        }
    }
    m_addRecordTime->setHMS(0,0,0,0);
    m_addRecordTime->start();
    return true;
}

bool DbBlock::addResultsInDB(const QString& json)
{
    QNetworkAccessManager *manager = new QNetworkAccessManager();
    QByteArray dataByteArray (json.toStdString().c_str(),json.toStdString().length());                                                                                                                  //Your webservice URL

    QNetworkRequest request(QUrl("http://127.0.0.1:5000/insertalgorithmresults"));
    QByteArray postDataSize = QByteArray::number(dataByteArray.size());

    request.setRawHeader("User-Agent", "ApplicationNameV01");
    request.setRawHeader("Content-Type", "application/json");
    request.setRawHeader("Content-Length", postDataSize);

    if (manager)
    {
        bool result;

        QNetworkReply *reply = manager->post(request, dataByteArray);

        result = connect(manager, SIGNAL(finished(QNetworkReply*)), this,SLOT(resultInsertionResponse(QNetworkReply*)));

        qDebug() <<"Connection is success : ? :" << result;
        if (reply)
        {
            qDebug() <<"Reply from server is"<< reply;
        }
    }
    return true;
}

void DbBlock::reponseRecue(QNetworkReply* reply)
{
    if (reply->error() == QNetworkReply::NoError)
    {
        qDebug() << reply->readAll();
    }
    else
    {
        qDebug() << "Une erreur s'est produite.";
        qWarning() <<"ErrorNo: "<< reply->error() << "for url: " << reply->url().toString();
        qDebug() << "Request failed, " << reply->errorString();
        qDebug() << "Headers:"<<  reply->rawHeaderList()<< "content:" << reply->readAll();
        qDebug() << reply->readAll();
    }
    delete reply;
}

void DbBlock::resultInsertionResponse(QNetworkReply* reply)
{
    if (reply->error() == QNetworkReply::NoError)
    {
        std::string response(reply->readAll());
    }
    else
    {
        qDebug() << "DbBlock::resultInsertionResponse(): Une erreur s'est produite.";
        qWarning() <<"ErrorNo: "<< reply->error() << "for url: " << reply->url().toString();
        qDebug() << "Request failed, " << reply->errorString();
        qDebug() << "Headers:"<<  reply->rawHeaderList()<< "content:" << reply->readAll();
        qDebug() << reply->readAll();
    }
    delete reply;
}
