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
#include <QProcess>

#include "widgets/ApplicationMenubar.h"
#include "string.h"
#include "widgets/MainWidget.h"
#include "widgets/MyTreeWidget.h"
#include "dialogs/AboutDialog.h"
#include "dialogs/HelpDialog.h"
#include "core/components/blockType/DbBlock.h"
#include "dialogs/RecordsDialog.h"
#include "../../acquisition/CJsonSerializer.h"
#include "../../acquisition/WimuRecord.h"
#include "widgets/RecordsWidget.h"
#include "widgets/AlgorithmTab.h"
#include "widgets/HomeWidget.h"
#include "../acquisition/RecordInfo.h"
#include "utilities/Utilities.h"

class MainWindow : public QMainWindow
    {
        Q_OBJECT
    public:
       MainWindow(QWidget *parent = 0);
       ~MainWindow();
       std::string getFileName(std::string s);
       void retranslateUi();
       void setStatusBarText(QString txt, MessageStatus status = none);
    signals:

    public slots:

        void openFile();
        void openRecordDialog();
        void closeTab(int);
        void onTabChanged(int);
        void addTab(QWidget * tab, std::string label);
        void openAbout();
        void openHelp();
        void setApplicationInEnglish();
        void setApplicationInFrench();

        void onListItemClicked(QTreeWidgetItem* item,int column);
        void onListItemDoubleClicked(QTreeWidgetItem* item,int column);
        void closeWindow();

        //Visual feedback
        void startSpinner();
        void stopSpinner(bool playAudio = false);

        //Getting records from DB
        bool getRecordsFromDB();
        void reponseRecue(QNetworkReply* reply);

        //Getting results from DB
        bool getSavedResultsFromDB();
        void savedResultsReponse(QNetworkReply* reply);


        //Getting data from specific record
        bool getDataFromUUIDFromDB(std::string uuid);
        void reponseRecueAcc(QNetworkReply* reply);

        //Delete specific record
        bool deleteRecordFromUUID(std::string uuid);
        bool deleteRecordFromList();
        void reponseRecueDelete(QNetworkReply* reply);

        //Rename specific record
        bool renameRecordFromUUID(std::string uuid, std::string newname);
        void reponseRecueRename(QNetworkReply* reply);

        void deleteRecord();
        void openAlgorithmTab();
        void openHomeTab();

        //Launch the python api
        static void launchApi(){
            QProcess* p = new QProcess();
            p->start("cmd.exe", QStringList() << "/c" << "..\\PythonAPI\\src\\runapi.bat");
            p->waitForFinished(500);
            p->deleteLater();
        }

    private:

        QTabWidget *tabWidget;
        QString folderName;
        QStatusBar * statusBar;
        RecordInfo selectedRecord;
        MainWidget * mainWidget;
        ApplicationMenuBar* menu;
        myTreeWidget  * listWidget;
        AboutDialog *aboutDialog;
        HelpDialog *helpDialog;
        DbBlock * databaseAccess = new DbBlock;
        RecordsDialog * rDialog;
        WimuRecord record;
        AlgorithmOutputInfoSerializer savedResults;
        WimuAcquisition wimuAcquisition;
        RecordsWidget* recordsTab;
        AlgorithmTab* algorithmTab;
        QLabel* spinnerStatusBar;
        QMovie* movieSpinnerBar;
        HomeWidget * homeWidget;
};

#endif // MAINWINDOW_H
