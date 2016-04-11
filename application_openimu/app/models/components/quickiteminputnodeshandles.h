#ifndef QUICKITEMINPUTNODESHANDLES_H
#define QUICKITEMINPUTNODESHANDLES_H

#include <QQuickItem>
#include <QObject>
#include <QList>

class QuickItemInputNodeIntHandle: public QQuickItem
{
    Q_OBJECT
    Q_PROPERTY(QList<int> value READ getValue WRITE setValue NOTIFY valueChanged)
    Q_PROPERTY(QString id READ getId WRITE setId)
public:
    QuickItemInputNodeIntHandle(): QQuickItem() {id = "";}

    void Put(std::vector<int> value){
        this->value = QList<int>::fromVector(QVector<int>::fromStdVector(value));
        emit valueChanged(this->value);
    }

    QString getId(){return id;}
    void setId(QString i){id = i;}

    QList<int> getValue() const {return value;}

    void setValue(QList<int> v){value = v;}

//private:
    QString id;
    QList<int> value;

signals:
    valueChanged(QList<int>);
};


class QuickItemInputNodeDoubleHandle: public QQuickItem
{
    Q_OBJECT
    Q_PROPERTY(QList<double> value READ getValue WRITE setValue NOTIFY valueChanged)
    Q_PROPERTY(QString id READ getId WRITE setId)
public:
    QuickItemInputNodeDoubleHandle(): QQuickItem() {id = "";}

    void Put(std::vector<double> value) {
        this->value = QList<double>::fromVector(QVector<double>::fromStdVector(value));
        emit valueChanged(this->value);
    }

    QString getId(){return id;}
    void setId(QString i){id = i;}

    QList<double> getValue() const {return value;}

    void setValue(QList<double> v){value = v;}

//private:
    QString id;
    QList<double> value;

signals:
    valueChanged(QList<double>);
};


class QuickItemInputNodeStringHandle: public QQuickItem
{
    Q_OBJECT
    Q_PROPERTY(QList<QString> value READ getValue WRITE setValue NOTIFY valueChanged)
    Q_PROPERTY(QString id READ getId WRITE setId)
public:
    QuickItemInputNodeStringHandle(): QQuickItem() {id = "";}

    void Put(std::vector<std::string> v) {
        value.clear();
        foreach(std::string str, v){
            value.push_back(QString::fromStdString(str));
        }
        emit valueChanged(value);
    }

    QString getId(){return id;}
    void setId(QString i){id = i;}

    QList<QString> getValue() const {return value;}

    void setValue(QList<QString> v){value = v;}

//private:
    QString id;
    QList<QString> value;

signals:
    valueChanged(QList<QString>);
};


#endif // QUICKITEMINPUTNODESHANDLES_H
