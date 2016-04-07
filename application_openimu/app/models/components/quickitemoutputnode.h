#ifndef QUICKITEMOUTPUTNODE_H
#define QUICKITEMOUTPUTNODE_H

#include "outputnode.h"
#include <QThread>
#include <QVector>

class QuickItemOutputNode: public QObject, public OutputNode
{
    Q_OBJECT
    Q_PROPERTY(QString id READ getId WRITE setId)
    Q_PROPERTY(QVector<int> value READ getValue WRITE setValue)
public:
    QuickItemOutputNode();

    QString getId(){return id;}
    void setId(QString i){id = i;}

    QVector<int> getValue(){return value;}
    void setValue(QVector<int> value);

    QVector<int> value;
    QString id;

signals:
    void resultReady(const QString &s);

};


class WorkerThread : public QThread
{
    Q_OBJECT
public:
    WorkerThread(QuickItemOutputNode* outputNode, std::vector<int> value)
        {this->outputNode = outputNode; this->value = value;}
    void run() Q_DECL_OVERRIDE
        {outputNode->Send(value);}
private:
    QuickItemOutputNode* outputNode;
    std::vector<int> value;
};


#endif // QUICKITEMOUTPUTNODE_H
