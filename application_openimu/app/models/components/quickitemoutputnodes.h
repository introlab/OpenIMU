#ifndef QUICKITEMOUTPUTNODE_H
#define QUICKITEMOUTPUTNODE_H

#include "workerthreads.h"
#include "outputnode.h"
#include <QThread>
#include <QList>
#include <QQuickItem>

//Integer
class QuickItemOutputNodeInt: public QQuickItem
{
    Q_OBJECT
    Q_PROPERTY(QString id READ getId WRITE setId)
    Q_PROPERTY(QList<int> value READ getValue WRITE setValue)
public:
    QuickItemOutputNodeInt(): QQuickItem() {}

    QString getId(){return id;}
    void setId(QString i){id = i;}

    QList<int> getValue(){return value;}
    void setValue(QList<int> v){
        value = v;

        WorkerThreadInt *workerThread = new WorkerThreadInt(outputNode, value.toVector().toStdVector());
        QObject::connect(workerThread, &WorkerThreadInt::finished, workerThread, &QObject::deleteLater);
        workerThread->start();
    }

    void setOutputNode(OutputNode<int> *node){outputNode = node;}

    OutputNode<int> *outputNode;
    QList<int> value;
    QString id;

signals:
    void resultReady(const QString &s);

};

//Double
class QuickItemOutputNodeDouble: public QQuickItem
{
    Q_OBJECT
    Q_PROPERTY(QString id READ getId WRITE setId)
    Q_PROPERTY(QList<double> value READ getValue WRITE setValue)
public:
    QuickItemOutputNodeDouble(): QQuickItem() {}

    QString getId(){return id;}
    void setId(QString i){id = i;}

    QList<double> getValue(){return value;}
    void setValue(QList<double> v){
        value = v;

        WorkerThreadDouble *workerThread = new WorkerThreadDouble(outputNode, value.toVector().toStdVector());
        QObject::connect(workerThread, &WorkerThreadDouble::finished, workerThread, &QObject::deleteLater);
        workerThread->start();
    }

    void setOutputNode(OutputNode<double> *node){outputNode = node;}

    OutputNode<double> *outputNode;

    QList<double> value;
    QString id;

signals:
    void resultReady(const QString &s);

};

//String
class QuickItemOutputNodeString: public QQuickItem
{
    Q_OBJECT
    Q_PROPERTY(QString id READ getId WRITE setId)
    Q_PROPERTY(QList<QString> value READ getValue WRITE setValue)
public:
    QuickItemOutputNodeString(): QQuickItem() {}

    QString getId(){return id;}
    void setId(QString i){id = i;}

    QList<QString> getValue(){return value;}
    void setValue(QList<QString> v){
        value = v;

        WorkerThreadString *workerThread = new WorkerThreadString(outputNode, value);
        QObject::connect(workerThread, &WorkerThreadString::finished, workerThread, &QObject::deleteLater);
        workerThread->start();
    }

    void setOutputNode(OutputNode<std::string> *node){outputNode = node;}

    OutputNode<std::string> *outputNode;

    QList<QString> value;
    QString id;

signals:
    void resultReady(const QString &s);

};


#endif // QUICKITEMOUTPUTNODE_H
