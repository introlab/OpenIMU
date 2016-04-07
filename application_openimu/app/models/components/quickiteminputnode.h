#ifndef QUICKITEMINPUTNODE_H
#define QUICKITEMINPUTNODE_H

#include "inputnode.h"
#include <QQuickItem>
#include <QList>

class QuickItemInputNode: public QQuickItem, public InputNode
{
    Q_OBJECT
    Q_PROPERTY(QList<int> value READ getValue WRITE setValue NOTIFY valueChanged)
    Q_PROPERTY(QString id READ getId WRITE setId)
public:
    QuickItemInputNode();
    void Put(std::vector<int> value);

    QString getId(){return id;}
    void setId(QString i){id = i; stringID = i.toUtf8().constData();}

    QList<int> getValue() const {return value;}

    void setValue(QList<int> v){value = v;}

//private:
    QString id;
    QList<int> value;

signals:
    valueChanged(QList<int>);
};

#endif // QUICKITEMINPUTNODE_H
