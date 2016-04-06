#ifndef QUICKITEMINPUTNODE_H
#define QUICKITEMINPUTNODE_H

#include "inputnode.h"
#include <QQuickItem>

class QuickItemInputNode: public QQuickItem, public InputNode
{
    Q_OBJECT
    Q_PROPERTY(QList<int> value READ getValue WRITE setValue NOTIFY valueChanged)
    Q_PROPERTY(QString id READ getId WRITE setId)
public:
    QuickItemInputNode();
    void Put(int value[]);

    QString getId(){return id;}
    void setId(QString i){id = i; stringID = i.toUtf8().constData();}

    QList<int> getValue() const
    {
       /*QList<int> ql;
       ql.reserve(2);
       std::copy(valueBuf + 0, valueBuf + 2, std::back_inserter(ql));
       return ql;*/
        return value;
    }

    void setValue(QList<int> v){for(int i=0; i<MAX_ARRAY_SIZE;i++) value[i] = v[i];}

//private:
    QString id;
    QList<int> value;

signals:
    valueChanged(QList<int>);
};

#endif // QUICKITEMINPUTNODE_H
