#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "widget.h"
#include "applicationmenubar.h"
#include <QVBoxLayout>
#include "string.h"
#include "controllers/toolbarcontroller.h"
#include "customqmlscene.h"


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
       ToolbarController *toolbarController;
       QVBoxLayout *mainLayout;
       QHBoxLayout *hLayout;
       QWidget *mainWidget;
       QWidget *filesWidget;
       Widget *plotWidget ;
       ApplicationMenuBar* menu ;
       CustomQmlScene* scene;
    };

#endif // MAINWINDOW_H
