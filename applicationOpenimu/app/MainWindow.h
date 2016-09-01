#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "ApplicationMenubar.h"
#include <QVBoxLayout>
#include "string.h"
#include "CustomQmlScene.h"
#include "core/Caneva.h"
#include <QSplitter>
#include "MyTreeWidget.h"
#include <QWidget>
#include "dialogs/AboutDialog.h"
#include "dialogs/HelpDialog.h"
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
