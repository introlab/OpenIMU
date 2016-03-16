#ifndef APPLICATIONMENU_H
#define APPLICATIONMENU_H

#include <QWidget>

class QMenu;

class ApplicationMenu : public QWidget
{
    Q_OBJECT
public:
    explicit ApplicationMenu(QWidget *parent = 0);

signals:

public slots:
private:

    QMenu *fileMenu;
    QMenu *editMenu;
    QMenu *formatMenu;
    QMenu *helpMenu;

};

#endif // APPLICATIONMENU_H
