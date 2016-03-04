#ifndef INCREMENTOR_H
#define INCREMENTOR_H

#include <QQuickItem>

class Incrementor : public QQuickItem
{
    Q_OBJECT
    Q_DISABLE_COPY(Incrementor)

public:
    Incrementor(QQuickItem *parent = 0);
    ~Incrementor();
};

#endif // INCREMENTOR_H
