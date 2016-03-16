#include "widget.h"
#include "ui_widget.h"
#include <qwt_legend.h>
#include <qwt_plot_curve.h>
#include "AccelerometerReader.h"
#include <vector>

Widget::Widget(QWidget *parent) : QwtPlot(parent),
     ui(new Ui::Widget)
{
     ui->setupUi(this);
     this->setupPlot();
}

Widget::~Widget()
{
     delete ui;
}

void Widget::changeEvent(QEvent *e)
{
    QWidget::changeEvent(e);
    switch (e->type()) {
    case QEvent::LanguageChange:
        ui->retranslateUi(this);
        break;
    default:
        break;
    }
}
void Widget::setupPlot() {

    this->setTitle("Accelerometer Data");
    this->setCanvasBackground(QColor(Qt::white));

    this->setAutoReplot(false);
    this->setMinimumWidth(400);

    // legend
    QwtLegend *legend = new QwtLegend;
    legend->setFrameStyle(QFrame::Box|QFrame::Sunken);
    this->insertLegend(legend, QwtPlot::BottomLegend);

    // axis
    this->setAxisTitle(QwtPlot::xBottom, "Axe temporelle");
    this->setAxisTitle(QwtPlot::yLeft, "x,y,z Axis");

    //data
    // add curves
    QwtPlotCurve *curve1 = new QwtPlotCurve("X Axis");
    QwtPlotCurve *curve2 = new QwtPlotCurve("Y Axis");
    QwtPlotCurve *curve3 = new QwtPlotCurve("Z Axis");

    vector<signed short> x;
    vector<signed short> y;
    vector<signed short> z;
    vector<float> t;
    int size =0;
    AccelerometerReader accReader("C:\\Users\\stef\\Desktop\\Projet S7-S8\\data_step");

    accReader.LoadSensorData();
    vector<SensorDataPerDay> availableData = accReader.GetAccelerometerData();

    for(int i = 0; i< availableData.size();i++){

        for(int j = 0; j< availableData.at(i).getDataPerDay().size() ;j++){

            for(int k = 0; k <availableData.at(i).getDataPerDay().at(j).getAccelerometerDataPerHour().size();k++){
                for(float i=0.0;i<0.98;i+=0.02)
                {
                    t.push_back(i+k);
                }

                vector<signed short> tmpx = availableData.at(i).getDataPerDay().at(j).getAccelerometerDataPerHour().at(k).getXAxisValues();
                vector<signed short> tmpy = availableData.at(i).getDataPerDay().at(j).getAccelerometerDataPerHour().at(k).getYAxisValues();
                vector<signed short> tmpz = availableData.at(i).getDataPerDay().at(j).getAccelerometerDataPerHour().at(k).getZAxisValues();

                x.insert(x.end(),tmpx.begin(),tmpx.end());
                y.insert(y.end(),tmpy.begin(),tmpy.end());
                z.insert(z.end(),tmpz.begin(),tmpz.end());
           }

        }
    }

     QPolygonF points, points1, points2;

     for(unsigned int i = 0; i <x.size(); i++)
     {
       points << QPointF(t.at(i),x.at(i));
       points1 << QPointF(t.at(i),y.at(i));
       points2 << QPointF(t.at(i),z.at(i));
     }


    curve1->setPen(* new QPen(Qt::blue));
    curve1->setSamples(points);
    curve1->attach(this);

    curve2->setPen(* new QPen(Qt::red));
    curve2->setSamples(points1);
    curve2->attach(this);

    curve3->setPen(* new QPen(Qt::green));
    curve3->setSamples(points2);
    curve3->attach(this);

    this->replot();
}
