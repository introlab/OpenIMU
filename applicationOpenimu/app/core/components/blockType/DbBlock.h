#ifndef DBBLOCK_H
#define DBBLOCK_H

#include "../Block.h"
#include<QString>
#include<QNetworkReply>
#include<QNetworkAccessManager>

class DbBlock : public QObject
{
    Q_OBJECT

    public:
        DbBlock();
        ~DbBlock();

        std::vector<QString> getDaysInDB();
        bool addRecordInDB(QString& json);
        void requete(const QString &, const QString &);

       public slots:
           void reponseRecue(QNetworkReply*);

     private:
        QNetworkAccessManager* manager;
};

#endif // DBWRITEBLOCK_H
