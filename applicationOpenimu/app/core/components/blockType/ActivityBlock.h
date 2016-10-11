#ifndef ACTIVITYBLOCK_H
#define ACTIVITYBLOCK_H

#include "../Block.h"
#include<QString>
#include<QNetworkReply>
#include<QNetworkAccessManager>

class ActivityBlock : public QObject
{
    Q_OBJECT

    public:
        ActivityBlock();
        ~ActivityBlock();

        std::vector<QString> getDaysInDB();
        void requete(const QString &, const QString &);

        bool getRecordsFromDB();
        bool run(QString &json);
public slots:
           void reponseRecue(QNetworkReply*);

     private:
        QNetworkAccessManager* manager;
};

#endif // DBWRITEBLOCK_H
