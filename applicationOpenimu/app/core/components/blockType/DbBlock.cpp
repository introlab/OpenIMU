#include "DbBlock.h"
#include <iostream>

DbBlock::DbBlock()
    :manager(new QNetworkAccessManager(this))
{
    connect(manager, SIGNAL(finished(QNetworkReply *)), this, SLOT(reponseRecue(QNetworkReply*)));
}

DbBlock::~DbBlock()
{
}

std::vector<QString> DbBlock::getDaysInDB()
{
    std::cout<<"Request available days in database"<<std::endl;
    std::vector<QString> listSavedDays; // Insert call to Db returning days available
    listSavedDays.push_back("24 Septembre 2016");
    listSavedDays.push_back("25 Septembre 2016");

    return listSavedDays;
}

 bool DbBlock::addRecordInDB(QString recordName, QString imuType, QString folderPath)
 {
    return true;
 }

 void DbBlock::requete(const QString & pseudo, const QString & password)
 {
     QNetworkRequest request(QUrl("http://127.0.0.1:5000/hello"));
     request.setRawHeader("User-Agent", "User Agent");
     request.setHeader(QNetworkRequest::ContentTypeHeader, "application/x-www-form-urlencoded");

     QNetworkReply *reply = manager->get(request);
      Q_UNUSED(reply);
 }

 void DbBlock::reponseRecue(QNetworkReply* reply)
 {
     if (reply->error() == QNetworkReply::NoError)
    {
        qDebug() << "connection";
        qDebug() << reply->readAll();

    }
    else
    {
        qDebug() << "error connect";
    }
    delete reply;
 }
