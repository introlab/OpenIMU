#ifndef DBBLOCK_H
#define DBBLOCK_H

#include<QString>
#include<QNetworkReply>
#include<QNetworkAccessManager>
#include"../../acquisition/CJsonSerializer.h"
#include"../../acquisition/WimuRecord.h"

class DbBlock : public QObject
{
    Q_OBJECT

    public:
        DbBlock();
        ~DbBlock();
        std::vector<QString> getDaysInDB();
        bool addRecordInDB(QString& json);

public slots:
        void reponseRecue(QNetworkReply* reply);

     private:
        QNetworkAccessManager* manager;
        QTime* addRecordTime;
};

#endif // DBWRITEBLOCK_H
