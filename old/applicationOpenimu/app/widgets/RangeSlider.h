#ifndef RANGESLIDER_H
#define RANGESLIDER_H

#include <QObject>
#include <QWidget>
#include <QLabel>
#include <QSlider>
#include <QHBoxLayout>

class RangeSlider : public QWidget
{
    Q_OBJECT
public:
    explicit RangeSlider(QWidget *parent = 0);
    void setStartHour(long long min);
    void setEndHour(long long max);
signals:

public slots:

private:
    QLabel * m_rightLabel;
    QLabel * m_leftLabel;
    QHBoxLayout* m_mainLayout;
    QWidget* m_refParent;

};

#endif // RANGESLIDER_H
