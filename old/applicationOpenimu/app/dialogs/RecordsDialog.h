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
#include "../acquisition/RecordInfo.h"

class RecordsDialog : public QDialog
{
    Q_OBJECT

public:

    RecordsDialog(QWidget *parent);
    ~RecordsDialog();
    bool addRecordInDB(QString& json, bool isSingleRecord);
    bool addRecordFileListToBD(QStringList & fileList, std::string folderPath);

public slots:
    void reponseRecue(QNetworkReply* reply);
    void selectRecordSlot();
    void addRecordSlot();

  private:

    QPushButton *m_selectRecord;
    QString m_folderToAdd;
    QLabel* m_folderSelected;
    QPushButton *m_addRecord;
    QGridLayout *m_mainLayout;
    QLabel* m_recordNaming;
    QLineEdit *m_recordName;
    QComboBox* m_imuSelectComboBox;
    QLabel* m_selectedImu;
    QLabel* m_selectedImuLabel;
    QLabel* m_successLabel;
    QComboBox* m_imuPositionComboBox;
    QLabel* m_imuPosition;
    QLabel* m_recordDetails;
    QTextEdit* m_userDetails;
    QLabel* m_spinner;
    QMovie* m_movie;
    QWidget* m_parent;

    QString m_current_uuid;
    QString m_error_msg;
    bool m_isFolderSelected=false;
    bool m_isDuplicateName = false;
};
#endif // RECORDSDIALOG_H
