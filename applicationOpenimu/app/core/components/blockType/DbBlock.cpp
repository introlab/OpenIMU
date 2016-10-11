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

 bool DbBlock::addRecordInDB(QString json)
 {

     QNetworkAccessManager *manager = new QNetworkAccessManager();

     //json = "{\"record\":{\"name\" : \"zebi\",\"date\" : \"10/09/2016\",\"format\":\"lol\"}, \"accelerometres\" : [{\"x\":1,\"y\":2,\"z\":3,\"t\":4},{\"x\":1,\"y\":2,\"z\":3,\"t\":4}],\"magnetometres\" : [{\"x\":1,\"y\":2,\"z\":3,\"t\":4},{\"x\":1,\"y\":2,\"z\":3,\"t\":4}],\"gyrometres\" : [{\"x\":1,\"y\":2,\"z\":3,\"t\":4}, {\"x\":1,\"y\":2,\"z\":3,\"t\":4}]}";

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
        qDebug() << reply->readAll();
        qDebug() << "error connect";
    }
    delete reply;
 }
