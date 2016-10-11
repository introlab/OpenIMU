#include "ActivityBlock.h"
#include <iostream>

ActivityBlock::ActivityBlock()
    :manager(new QNetworkAccessManager(this))
{
    connect(manager, SIGNAL(finished(QNetworkReply *)), this, SLOT(reponseRecue(QNetworkReply*)));
}

ActivityBlock::~ActivityBlock()
{
}

bool ActivityBlock::run(QString& json)
 {

     QNetworkAccessManager *manager = new QNetworkAccessManager();

     //json = "{\"record\":{\"name\" : \"zebi\",\"date\" : \"10/09/2016\",\"format\":\"lol\"}, \"accelerometres\" : [{\"x\":1,\"y\":2,\"z\":3,\"t\":4},{\"x\":1,\"y\":2,\"z\":3,\"t\":4}],\"magnetometres\" : [{\"x\":1,\"y\":2,\"z\":3,\"t\":4},{\"x\":1,\"y\":2,\"z\":3,\"t\":4}],\"gyrometres\" : [{\"x\":1,\"y\":2,\"z\":3,\"t\":4}, {\"x\":1,\"y\":2,\"z\":3,\"t\":4}]}";

     QByteArray dataByteArray (json.toStdString().c_str(),json.toStdString().length());                                                                                                                  //Your webservice URL

     QNetworkRequest request(QUrl("http://127.0.0.1:5000/algo?filename=activityTracker&uuid=57fbe940e003461b702b0eda"));
     QByteArray postDataSize = QByteArray::number(dataByteArray.size());

     request.setRawHeader("User-Agent", "ApplicationNameV01");
     request.setRawHeader("Content-Type", "application/json");
     request.setRawHeader("Content-Length", postDataSize);

     if (manager) {
     bool result;

     result = connect(manager, SIGNAL(finished(QNetworkReply*)), this,SLOT(reponseRecue(QNetworkReply*)));
     QNetworkReply *reply = manager->get(request);

     qDebug() <<"Connection is success : ? :" << result;
     if (reply) {
        qDebug() <<"Reply from server is"<< reply;
     }
    }
     return true;
 }


/*
 void ActivityBlock::reponseRecue(QNetworkReply* reply)
 {
     if (reply->error() == QNetworkReply::NoError)
    {
        qDebug() << "connection";
        QByteArray testReponse = reply->readAll();// "[{ \"_id\" : \"foo\", \"name\" : \"test\"},{ \"_id\" : \"foo2\", \"name\" : \"test2\"}]\n";
        qDebug()<<testReponse;

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
 */

 void ActivityBlock::requete(const QString & pseudo, const QString & password)
 {
     QNetworkRequest request(QUrl("http://127.0.0.1:5000/hello"));
     request.setRawHeader("User-Agent", "User Agent");
     request.setHeader(QNetworkRequest::ContentTypeHeader, "application/x-www-form-urlencoded");

     QNetworkReply *reply = manager->get(request);
      Q_UNUSED(reply);
 }

 void ActivityBlock::reponseRecue(QNetworkReply* reply)
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
