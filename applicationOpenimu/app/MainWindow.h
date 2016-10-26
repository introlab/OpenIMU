#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QWidget>
#include <QVBoxLayout>
#include <QStatusBar>
#include <QListWidget>
#include <QNetworkReply>
#include <QNetworkAccessManager>
#include <QMovie>

#include "widgets/ApplicationMenubar.h"
#include "string.h"
#include "widgets/MainWidget.h"
#include "widgets/MyListWidget.h"
#include "dialogs/AboutDialog.h"
#include "dialogs/HelpDialog.h"
#include "core/components/blockType/DbBlock.h"
#include "dialogs/RecordsDialog.h"
#include "../../acquisition/CJsonSerializer.h"
#include "../../acquisition/WimuRecord.h"
#include "widgets/RecordsWidget.h"
#include "widgets/AlgorithmTab.h"
#include "widgets/HomeWidget.h"

class MainWindow : public QMainWindow
    {
        Q_OBJECT
    public:
       MainWindow(QWidget *parent = 0);
       ~MainWindow();
       std::string getFileName(std::string s);
       void retranslateUi();

    signals:

    public slots:


    void openFile();
    void openRecordDialog();
    void closeTab(int);
    void replaceTab(QWidget * replacement, std::string label);
    void openAbout();
    void openHelp();
    void setApplicationInEnglish();
    void setApplicationInFrench();

    void onListItemClicked(QListWidgetItem* item);
    void closeWindow();

    //Getting records from DB
    bool getRecordsFromDB();
    void reponseRecue(QNetworkReply* reply);

    //Getting data from specific record
    bool getDataFromUUIDFromDB(std::string uuid);
    void reponseRecueAcc(QNetworkReply* reply);

    //Delete specific record
    bool deleteRecordFromUUID(std::string uuid);
    void reponseRecueDelete(QNetworkReply* reply);

    void deleteRecord();
    void openAlgorithmTab();
    void openHomeTab();
    private:

   QTabWidget *tabWidget;
   QString folderName;
   QStatusBar * statusBar;
   std::string selectedUUID;
   MainWidget * mainWidget;
   ApplicationMenuBar* menu ;
   MyListWidget  * listWidget;
   AboutDialog *aboutDialog;
   HelpDialog *helpDialog;
   DbBlock * databaseAccess = new DbBlock;
   RecordsDialog * rDialog;
   WimuRecord record;
   WimuAcquisition acceleroData;
   RecordsWidget* recordsTab;
   AlgorithmTab* algorithmTab;
   QLabel* spinnerStatusBar;
   QMovie* movieSpinnerBar;
   HomeWidget * homeWidget;

};

#endif // MAINWINDOW_H
