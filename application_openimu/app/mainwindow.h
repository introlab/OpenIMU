#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "widget.h"
#include "applicationmenubar.h"
#include <QVBoxLayout>
#include "string.h"
#include "customqmlscene.h"
#include "models/caneva.h"

class MainWindow : public QMainWindow
    {
        Q_OBJECT
    public:
       MainWindow(QWidget *parent = 0);
       std::string getFileName(std::string s);

    signals:

    public slots:
    void openFile();
    void onDateSelectedClicked(std::string t);
    void computeSteps();

    private:
       Caneva *caneva;
       QVBoxLayout *mainLayout;
       QHBoxLayout *hLayout;
       QWidget *mainWidget;
       QWidget *filesWidget;
       Widget *plotWidget ;
       ApplicationMenuBar* menu ;
       CustomQmlScene* scene;
    };

#endif // MAINWINDOW_H
