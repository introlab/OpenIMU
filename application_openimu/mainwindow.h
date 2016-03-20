#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "widget.h"
#include "applicationmenubar.h"
#include <QVBoxLayout>

class MainWindow : public QMainWindow
    {
        Q_OBJECT
    public:
       MainWindow(QWidget *parent = 0);

    signals:

    public slots:
    void openFile();

    private:
       QVBoxLayout *mainLayout;
       QWidget *mainWidget;
       Widget *plotWidget ;
       ApplicationMenuBar* menu ;

    };

#endif // MAINWINDOW_H
