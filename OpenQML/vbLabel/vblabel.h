#ifndef VBLABEL_H
#define VBLABEL_H

#include <QQuickItem>

class VBLabel : public QQuickItem
{
    Q_OBJECT
    Q_DISABLE_COPY(VBLabel)

public:
    VBLabel(QQuickItem *parent = 0);
    ~VBLabel();
};

#endif // VBLABEL_H
