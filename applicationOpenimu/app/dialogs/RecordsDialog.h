#ifndef RECORDSDIALOG_H
#define RECORDSDIALOG_H

#include<QDialog>
#include<QPushButton>
#include<QLabel>
#include<QGridLayout>
#include<QLineEdit>
#include<QComboBox>
#include<QTextEdit>
#include<QMovie>
#include<QNetworkReply>
#include<QNetworkAccessManager>

class RecordsDialog : public QDialog
{
    Q_OBJECT

public:

    RecordsDialog(QWidget *parent);
    ~RecordsDialog();
    void reject();
    bool addRecordInDB(QString& json, bool isSingleRecord);
    bool addRecordFileListToBD(QStringList & fileList, std::string folderPath);

public slots:
    void reponseRecue(QNetworkReply* reply);
    void selectRecordSlot();
    void addRecordSlot();

  private:

    QPushButton *selectRecord;
    QString folderToAdd;
    QLabel* folderSelected;
    QPushButton *addRecord;
    QGridLayout *mainLayout;
    QLabel* recordNaming;
    QLineEdit *recordName;
    QComboBox* imuSelectComboBox;
    QLabel* selectedImu;
    QLabel* selectedImuLabel;
    QLabel* successLabel;
    QComboBox* imuPositionComboBox;
    QLabel* imuPosition;
    QLabel* recordDetails;
    QTextEdit* userDetails;
    QLabel* spinner;
    QMovie* movie;
    QWidget* m_parent;

    QString current_uuid;
    bool isFolderSelected=false;
};
#endif // RECORDSDIALOG_H
