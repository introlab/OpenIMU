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
#include "core/components/blockType/DbBlock.h"
#include "../acquisition/RecordInfo.h"

class RecordsDialog : public QDialog
{
    Q_OBJECT

public:

    RecordsDialog(QWidget *parent);
    ~RecordsDialog();
    void reject();
private slots:

    void selectRecordSlot();
    void addRecordSlot();

  private:

    QPushButton *selectRecord;
    QString folderToAdd;
    QLabel* folderSelected;
    bool isFolderSelected=false;
    QPushButton *addRecord;
    QGridLayout *mainLayout;
    QLabel* recordNaming;
    QLineEdit *recordName;
    QComboBox* imuSelectComboBox;
    DbBlock * databaseAccess;
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
};
#endif // RECORDSDIALOG_H
