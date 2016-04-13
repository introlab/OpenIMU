#include "accdatadisplay.h"
#include <QtCharts/QChartView>
#include <QtCharts/QLineSeries>
#include <QtCharts/QLegend>
#include <QtCharts/QValueAxis>

#include "newAcquisition/wimuacquisition.h"
#include "acquisition/AccelerometerReader.h"
AccDataDisplay::AccDataDisplay()
{

}
AccDataDisplay::AccDataDisplay(std::string filePath){

    WimuAcquisition acceleroData = WimuAcquisition(filePath,50);

    AccelerometerReader accReader(filePath);

    accReader.LoadSensorData(false);
    vector<SensorDataPerDay> availableData = accReader.GetAccelerometerData();

    if(availableData.size()>0)
    {
        vector<signed short> x;
        vector<signed short> y;
        vector<signed short> z;
        vector<float> t;

        for(int k = 0; k <availableData.at(0).getDataPerDay().at(0).getAccelerometerDataPerHour().size();k++){
            for(float i=0.0;i<0.98;i+=0.02)
            {
                t.push_back(i+k);
            }

            vector<signed short> tmpx = availableData.at(0).getDataPerDay().at(0).getAccelerometerDataPerHour().at(k).getXAxisValues();
            vector<signed short> tmpy = availableData.at(0).getDataPerDay().at(0).getAccelerometerDataPerHour().at(k).getYAxisValues();
            vector<signed short> tmpz = availableData.at(0).getDataPerDay().at(0).getAccelerometerDataPerHour().at(k).getZAxisValues();

            x.insert(x.end(),tmpx.begin(),tmpx.end());
            y.insert(y.end(),tmpy.begin(),tmpy.end());
            z.insert(z.end(),tmpz.begin(),tmpz.end());
        }

        QtCharts::QLineSeries *lineseriesX = new QtCharts::QLineSeries();
        lineseriesX->setName("Axe X");
        lineseriesX->setUseOpenGL(true);

        QtCharts::QLineSeries *lineseriesY = new QtCharts::QLineSeries();
        lineseriesY->setName("Axe Y");
        lineseriesY->setUseOpenGL(true);

        QtCharts::QLineSeries *lineseriesZ = new QtCharts::QLineSeries();
        lineseriesZ->setName("Axe Z");
        lineseriesZ->setUseOpenGL(true);

        for(unsigned int i = 0; i <x.size(); i++)
        {
            lineseriesX->append(QPoint(t.at(i),x.at(i)));
            lineseriesY->append(QPoint(t.at(i),y.at(i)));
            lineseriesZ->append(QPoint(t.at(i),z.at(i)));
        }

        QChart *chart = new QChart();
        chart->legend()->show();
        chart->legend()->setAlignment(Qt::AlignBottom);
        chart->addSeries(lineseriesX);
        chart->addSeries(lineseriesY);
        chart->addSeries(lineseriesZ);

        chart->createDefaultAxes();
        chart->setTitle("Données accéléromètre");

        chartView = new QChartView(chart);
        chartView->setRenderHint(QPainter::Antialiasing);
    }
}
QChartView * AccDataDisplay::getChartView(){
    return chartView;
}
