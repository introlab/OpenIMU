#ifndef QUICKITEMINPUTNODE_H
#define QUICKITEMINPUTNODE_H

#include "inputnode.h"
#include <QQuickItem>

class QuickItemInputNode: public QQuickItem, public InputNode
{
    Q_OBJECT
    Q_PROPERTY(int valueBuf READ getValueBuf WRITE setValueBuf NOTIFY valueBufChanged)
    Q_PROPERTY(QString id READ getId WRITE setId)
public:
    QuickItemInputNode();
    void Put(int value);

    QString getId(){return id;}
    void setId(QString i){id = i; stringID = i.toUtf8().constData();}

    int getValueBuf(){return valueBuf;}
    void setValueBuf(int v){valueBuf = v;}

//private:
    QString id;

signals:
    valueBufChanged(int);


};

#endif // QUICKITEMINPUTNODE_H
