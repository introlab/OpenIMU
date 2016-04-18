#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "applicationmenubar.h"
#include <QVBoxLayout>
#include "string.h"
#include "customqmlscene.h"
#include "models/caneva.h"
#include <QSplitter>
#include "mytreewidget.h"
#include <QWidget>
#include "dialogs/aboutdialog.h"
#include "dialogs/helpdialog.h"
#include <QStatusBar>

class MainWindow : public QMainWindow
    {
        Q_OBJECT
    public:
       MainWindow(QWidget *parent = 0);
       ~MainWindow();
       std::string getFileName(std::string s);

    signals:

    public slots:
    void openFile();
    void displayRawAccData();
    void computeSteps();
    void closeWindow();
    void onTreeItemClicked(QTreeWidgetItem* item, int /*column*/);
    void computeActivityTime();
    void closeTab(int);
    void replaceTab(QWidget * replacement, std::string label);
    void openAbout();
    void openHelp();

    private:
       QString folderName;
       QSplitter * splitter;
       Caneva *caneva;
       QWidget *mainWidget;
       ApplicationMenuBar* menu ;
       CustomQmlScene* scene;
       myTreeWidget  * tree;
       QTabWidget *tabWidget;
       QString fileSelectedName;
       QWidget *dataView;
       AboutDialog *aboutDialog;
       HelpDialog *helpDialog;
       QStatusBar * statusBar;
    };

#endif // MAINWINDOW_H
