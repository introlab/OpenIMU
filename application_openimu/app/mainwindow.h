#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "widget.h"
#include "applicationmenubar.h"
#include <QVBoxLayout>
#include "string.h"
#include "customqmlscene.h"
#include "models/caneva.h"
#include <QSplitter>
#include "mytreewidget.h"

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
    void onDateSelectedClicked(std::string t);
    void computeSteps();
    void closeWindow();
    void onTreeItemClicked(QTreeWidgetItem* item, int /*column*/);

    private:
       QSplitter * splitter;
       Caneva *caneva;
       QVBoxLayout *mainLayout;
       QHBoxLayout *hLayout;
       QWidget *mainWidget;
       QWidget *filesWidget;
       Widget *plotWidget ;
       ApplicationMenuBar* menu ;
       CustomQmlScene* scene;
       myTreeWidget  * tree;
    };

#endif // MAINWINDOW_H
