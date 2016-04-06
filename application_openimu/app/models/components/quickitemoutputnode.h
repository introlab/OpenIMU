#ifndef QUICKITEMOUTPUTNODE_H
#define QUICKITEMOUTPUTNODE_H

#include "outputnode.h"
#include <QThread>

class QuickItemOutputNode: public QObject, public OutputNode
{
    Q_OBJECT
    Q_PROPERTY(QString id READ getId WRITE setId)
    Q_PROPERTY(int* value READ getValue WRITE setValue)
public:
    QuickItemOutputNode();

    QString getId(){return id;}
    void setId(QString i){id = i;}

    int* getValue(){return value;}
    void setValue(int v[]);

    int value[MAX_ARRAY_SIZE];
    QString id;

signals:
    void resultReady(const QString &s);

};


class WorkerThread : public QThread
{
    Q_OBJECT
public:
    WorkerThread(QuickItemOutputNode* outputNode, int value[])
        {this->outputNode = outputNode; for(int i=0; i<MAX_ARRAY_SIZE;i++) this->value[i] = value[i];}
    void run() Q_DECL_OVERRIDE
        {outputNode->Send(value);}
private:
    QuickItemOutputNode* outputNode;
    int value[MAX_ARRAY_SIZE];
};


#endif // QUICKITEMOUTPUTNODE_H
