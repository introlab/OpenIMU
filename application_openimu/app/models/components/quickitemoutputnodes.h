#ifndef QUICKITEMOUTPUTNODE_H
#define QUICKITEMOUTPUTNODE_H

#include "workerthreads.h"
#include "outputnode.h"
#include <QThread>
#include <QVector>

//Integer
class QuickItemOutputNodeInt: public QObject, public OutputNode<int>
{
    Q_OBJECT
    Q_PROPERTY(QString id READ getId WRITE setId)
    Q_PROPERTY(QVector<int> value READ getValue WRITE setValue)
public:
    QuickItemOutputNodeInt(): QObject(), OutputNode<int>() {}

    QString getId(){return id;}
    void setId(QString i){id = i;}

    QVector<int> getValue(){return value;}
    void setValue(QVector<int> value){
        this->value = value;
        this->setValueBuf( value.toStdVector());

        WorkerThreadInt *workerThread = new WorkerThreadInt(this, this->getValueBuf());
        QObject::connect(workerThread, &WorkerThreadInt::finished, workerThread, &QObject::deleteLater);
        workerThread->start();
    }

    QVector<int> value;
    QString id;

signals:
    void resultReady(const QString &s);

};

//Double
class QuickItemOutputNodeDouble: public QObject, public OutputNode<double>
{
    Q_OBJECT
    Q_PROPERTY(QString id READ getId WRITE setId)
    Q_PROPERTY(QVector<double> value READ getValue WRITE setValue)
public:
    QuickItemOutputNodeDouble(): QObject(), OutputNode<double>() {}

    QString getId(){return id;}
    void setId(QString i){id = i;}

    QVector<double> getValue(){return value;}
    void setValue(QVector<double> value){
        this->value = value;
        this->setValueBuf( value.toStdVector());

        WorkerThreadDouble *workerThread = new WorkerThreadDouble(this, this->getValueBuf());
        QObject::connect(workerThread, &WorkerThreadDouble::finished, workerThread, &QObject::deleteLater);
        workerThread->start();
    }

    QVector<double> value;
    QString id;

signals:
    void resultReady(const QString &s);

};


#endif // QUICKITEMOUTPUTNODE_H
