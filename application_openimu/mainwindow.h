#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "widget.h"
#include "applicationmenubar.h"
#include <QVBoxLayout>
#include "string.h"

class MainWindow : public QMainWindow
    {
        Q_OBJECT
    public:
       MainWindow(QWidget *parent = 0);
       std::string getFileName(std::string s);

    signals:

    public slots:
    void openFile();
    void computeSteps();

    private:
       QVBoxLayout *mainLayout;
       QHBoxLayout *filesSelected;
       QWidget *mainWidget;
       QWidget *filesWidget;
       Widget *plotWidget ;
       ApplicationMenuBar* menu ;
       bool plotDisplay;
    };

#endif // MAINWINDOW_H
