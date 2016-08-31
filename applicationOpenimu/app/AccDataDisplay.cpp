#include "AccDataDisplay.h"
#include "newAcquisition/WimuAcquisition.h"
#include <math.h>
#include <QPropertyAnimation>

QT_CHARTS_USE_NAMESPACE

AccDataDisplay::AccDataDisplay()
{

}
AccDataDisplay::AccDataDisplay(std::string filePath){

    acceleroData = new WimuAcquisition(filePath,50);
    availableData = acceleroData->getData();
    sliceData = availableData;

    if(availableData.size()>0)
    {

        chart = new QChart();
        chart->legend()->show();
        chart->legend()->setAlignment(Qt::AlignBottom);
        chart->setTheme(QChart::ChartThemeDark);


        chart->createDefaultAxes();
        chart->setTitle("Données accéléromètre (en ms)");

        chartView = new QChartView(chart);
        chartView->setRenderHint(QPainter::Antialiasing);

        layout = new QVBoxLayout(this);
        //Initialize Recording Date
        QHBoxLayout *hboxDate = new QHBoxLayout();
        QLabel* dateRecorded = new QLabel();
        dateRecorded->setText(QString::fromStdString("Journée d'enregistrement: ")+ QString::fromStdString(acceleroData->getDates().back().date));
        hboxDate->addStretch();
        hboxDate->addWidget(dateRecorded);
        hboxDate->addStretch();
        layout->addLayout(hboxDate);
        //Initialize Checkbox and Label
        checkboxX = new QCheckBox("Axe X");
        checkboxY = new QCheckBox("Axe Y");
        checkboxZ = new QCheckBox("Axe Z");
        checkboxAccNorm = new QCheckBox("Norme");
        checkboxMovingAverage = new QCheckBox("Moyenne mobile");

        checkboxX->setChecked(true);
        checkboxY->setChecked(true);
        checkboxZ->setChecked(true);
        checkboxAccNorm->setChecked(false);
        checkboxMovingAverage->setChecked(false);

        QHBoxLayout *hbox = new QHBoxLayout();
        hbox->addStretch();
        hbox->addWidget(checkboxX);
        hbox->addWidget(checkboxY);
        hbox->addWidget(checkboxZ);
        hbox->addWidget(checkboxAccNorm);
        hbox->addWidget(checkboxMovingAverage);
        hbox->addStretch();

        //Initialize Slider
        slider = new QSlider();
        int tempDiff = WimuAcquisition::maxTime(availableData).timestamp- WimuAcquisition::minTime(availableData).timestamp ;
        slider->setMinimum(0);
        slider->setMaximum(tempDiff);
        slider->setOrientation(Qt::Horizontal);
        layout->addWidget(chartView);
        layout->addLayout(hbox);

        rSlider = new RangeSlider(this);
        long long min = WimuAcquisition::minTime(availableData).timestamp;
        long long max = WimuAcquisition::maxTime(availableData).timestamp;
        rSlider->setStartHour(min/1000);
        rSlider->setEndHour(max/1000);
        rSlider->setRangeValues(0,(long long)(max-min)/1000);
        layout->addWidget(rSlider);

        connect(slider,SIGNAL(valueChanged(int)),this,SLOT(sliderValueChanged(int)));
        connect(checkboxX, SIGNAL(stateChanged(int)), this, SLOT(slotDisplayXAxis(int)));
        connect(checkboxY, SIGNAL(stateChanged(int)), this, SLOT(slotDisplayYAxis(int)));
        connect(checkboxZ, SIGNAL(stateChanged(int)), this, SLOT(slotDisplayZAxis(int)));
        connect(checkboxAccNorm, SIGNAL(stateChanged(int)), this, SLOT(slotDisplayNorme(int)));
        connect(checkboxMovingAverage, SIGNAL(stateChanged(int)), this, SLOT(slotDisplayMovingAverage(int)));

        fillChartSeries();
    }
}
void AccDataDisplay::sliderValueChanged(int value)
{
    sliceData = acceleroData->getData(WimuAcquisition::minTime(availableData).timestamp + value, WimuAcquisition::maxTime(availableData).timestamp);
    chart->removeAllSeries();
    fillChartSeries();
    chartView->setChart(chart);
}
void AccDataDisplay::slotDisplayNorme(int value){
    if(value){
        chart->addSeries(lineseriesAccNorm);
        chartView->setChart(chart);
    }else{
        chart->removeSeries(lineseriesAccNorm);
        chartView->setChart(chart);
    }
}
void AccDataDisplay::slotDisplayMovingAverage(int value){
    if(value){
        chart->addSeries(lineseriesMovingAverage);
        chartView->setChart(chart);
    }else{
        chart->removeSeries(lineseriesMovingAverage);
        chartView->setChart(chart);
    }

}
void AccDataDisplay::leftSliderValueChanged(int value)
{
    rSlider->setStartHour(WimuAcquisition::minTime(availableData).timestamp+value);
}
void AccDataDisplay::rightSliderValueChanged(int value)
{
    rSlider->setEndHour(WimuAcquisition::maxTime(availableData).timestamp-value);

}
void AccDataDisplay::slotDisplayXAxis(int value){
    if(value){
        chart->addSeries(lineseriesX);
        chartView->setChart(chart);
    }else{
        chart->removeSeries(lineseriesX);
        chartView->setChart(chart);
    }
}
void AccDataDisplay::slotDisplayYAxis(int value){
    if(value){
        chart->addSeries(lineseriesY);
        chartView->setChart(chart);
    }else{
        chart->removeSeries(lineseriesY);
        chartView->setChart(chart);
    }
}
void AccDataDisplay::slotDisplayZAxis(int value){
    if(value){
        chart->addSeries(lineseriesZ);
        chartView->setChart(chart);
    }else{
        chart->removeSeries(lineseriesZ);
        chartView->setChart(chart);
    }
}
std::vector<signed short> AccDataDisplay::movingAverage(int windowSize)
{
    double sum=0;
     std::vector<signed short> filteredData;
    for(int j=0;j<windowSize;j++)
    {
        sum+=sqrt(pow(sliceData.at(j).x,2.0)+ pow(sliceData.at(j).y,2.0) + pow(sliceData.at(j).z,2.0));
    }
    filteredData.push_back(sum/windowSize);
    for (int i=1;i<sliceData.size()-windowSize;i++)
    {
        sum-=sqrt(pow(sliceData.at(i-1).x,2.0)+pow(sliceData.at(i-1).y,2.0)+ pow(sliceData.at(i-1).z,2.0));
        sum+=sqrt(pow(sliceData.at(i+windowSize-1).x,2.0)+pow(sliceData.at(i+windowSize-1).y,2.0)+ pow(sliceData.at(i+windowSize-1).z,2.0));
        filteredData.push_back(sum/windowSize);
    }
    return filteredData;
}
void AccDataDisplay::fillChartSeries(){

    std::vector<signed short> x;
    std::vector<signed short> y;
    std::vector<signed short> z;
    std::vector<signed short> norm_acc;
    std::vector<signed short> filtered_data;
    filtered_data = movingAverage(10);
    std::vector<float> t;

    for(int k = 0; k <sliceData.size(); k++){

        x.push_back(sliceData.at(k).x);
        y.push_back(sliceData.at(k).y);
        z.push_back(sliceData.at(k).z);
        norm_acc.push_back(sqrt(pow(sliceData.at(k).x,2.0) + pow(sliceData.at(k).y,2.0) + pow(sliceData.at(k).z,2.0)));
        t.push_back(k*20); // TO DO Replace w/ real value
    }

    lineseriesX = new QtCharts::QLineSeries();
    QPen penX(QRgb(0xCF000F));
    lineseriesX->setPen(penX);
    lineseriesX->setName("Axe X");
    lineseriesX->setUseOpenGL(true);


    lineseriesY = new QtCharts::QLineSeries();
    QPen penY(QRgb(0x00b16A));
    lineseriesY->setPen(penY);
    lineseriesY->setName("Axe Y");
    lineseriesY->setUseOpenGL(true);

    lineseriesZ = new QtCharts::QLineSeries();
    QPen penZ(QRgb(0x4183D7));
    lineseriesZ->setPen(penZ);
    lineseriesZ->setName("Axe Z");
    lineseriesZ->setUseOpenGL(true);

    lineseriesAccNorm = new QtCharts::QLineSeries();
    lineseriesAccNorm->setName("Norme");

    QPen pen(QRgb(0xdadfe1));
    lineseriesAccNorm->setPen(pen);
    lineseriesAccNorm->setUseOpenGL(true);

    lineseriesMovingAverage = new QtCharts::QLineSeries();
    QPen penM(QRgb(0xf89406));
    lineseriesMovingAverage->setPen(penM);
    lineseriesMovingAverage->setName("Moyenne mobile");
    lineseriesMovingAverage->setUseOpenGL(true);

    for(unsigned int i = 0; i <x.size(); i++)
    {
        lineseriesX->append(t.at(i),x.at(i));
        lineseriesY->append(t.at(i),y.at(i));
        lineseriesZ->append(t.at(i),z.at(i));
        lineseriesAccNorm->append(t.at(i),norm_acc.at(i));
    }
    for(unsigned int i = 0; i <filtered_data.size(); i++)
    {
        lineseriesMovingAverage->append(t.at(i),filtered_data.at(i));
    }
    if(checkboxX->isChecked())
        chart->addSeries(lineseriesX);

    if(checkboxY->isChecked())
        chart->addSeries(lineseriesY);

    if(checkboxZ->isChecked())
        chart->addSeries(lineseriesZ);

    if(checkboxAccNorm->isChecked())
        chart->addSeries(lineseriesAccNorm);

    if(checkboxMovingAverage->isChecked())
        chart->addSeries(lineseriesMovingAverage);

    chart->createDefaultAxes();
}
