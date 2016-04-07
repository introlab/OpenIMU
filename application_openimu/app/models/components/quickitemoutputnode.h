#ifndef QUICKITEMOUTPUTNODE_H
#define QUICKITEMOUTPUTNODE_H

#include "outputnode.h"
#include <QThread>
#include <QVector>

template <class T>
class WorkerThread;

template <class T>
class QuickItemOutputNode: public QObject, public OutputNode<T>
{
    Q_OBJECT
    Q_PROPERTY(QString id READ getId WRITE setId)
    Q_PROPERTY(QVector<T> value READ getValue WRITE setValue)
public:
    QuickItemOutputNode(): QObject(), OutputNode<T>() {}

    QString getId(){return id;}
    void setId(QString i){id = i;}

    QVector<T> getValue(){return value;}
    void setValue(QVector<T> value){
        this->value = value;
        this->setValueBuf( value.toStdVector());

        WorkerThread<T> *workerThread = new WorkerThread<T>(this, this->getValueBuf());
        QObject::connect(workerThread, &WorkerThread<T>::finished, workerThread, &QObject::deleteLater);
        workerThread->start();
    }


    QVector<T> value;
    QString id;

signals:
    void resultReady(const QString &s);

};

template <class T>
class WorkerThread : public QThread
{
    Q_OBJECT
public:
    WorkerThread(QuickItemOutputNode<T>* outputNode, std::vector<T> value)
        {this->outputNode = outputNode; this->value = value;}
    void run() Q_DECL_OVERRIDE
        {outputNode->Send(value);}
private:
    QuickItemOutputNode<T>* outputNode;
    std::vector<T> value;
};



class QuickItemOutputNodeInt: public QuickItemOutputNode<int>{
public:
    QuickItemOutputNodeInt() :QuickItemOutputNode<int>() {}
};

class QuickItemOutputNodeDouble: public QuickItemOutputNode<double>{
public:
    QuickItemOutputNodeDouble() :QuickItemOutputNode<double>() {}
};
#endif // QUICKITEMOUTPUTNODE_H
