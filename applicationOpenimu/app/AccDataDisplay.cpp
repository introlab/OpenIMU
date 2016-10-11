#include "AccDataDisplay.h"
#include "acquisition/WimuAcquisition.h"
#include <math.h>
#include <QPropertyAnimation>
#include "graph/ChartView.h"
#include <QQuickView>
#include <QPushButton>
#include <QEventLoop>

QT_CHARTS_USE_NAMESPACE

AccDataDisplay::AccDataDisplay()
{

}

bool AccDataDisplay::getDataFromUUIDFromDB(std::string uuid)
{
    std::string url = "http://127.0.0.1:5000/data?uuid="+uuid;
    QNetworkRequest request(QUrl(QString::fromStdString(url)));
    request.setRawHeader("User-Agent", "ApplicationNameV01");
    request.setRawHeader("Content-Type", "application/json");

    QNetworkAccessManager *manager = new QNetworkAccessManager();
    QNetworkReply *reply = manager->get(request);
    QEventLoop loop;
    bool result = connect(manager, SIGNAL(finished(QNetworkReply*)), &loop,SLOT(quit()));
    loop.exec();
    reponseRecue(reply);
    return true;
}

void AccDataDisplay::reponseRecue(QNetworkReply* reply)
{
    if (reply->error() == QNetworkReply::NoError)
   {
       qDebug() << "connection UUID";
       std::string testReponse =  reply->readAll();//"{\"record\":{\"name\" : \"zebi\",\"date\" : \"10/09/2016\",\"format\":\"lol\"}, \"accelerometres\" : [{\"x\":1,\"y\":2,\"z\":3,\"t\":4},{\"x\":1,\"y\":2,\"z\":3,\"t\":4}],\"magnetometres\" : [{\"x\":1,\"y\":2,\"z\":3,\"t\":4},{\"x\":1,\"y\":2,\"z\":3,\"t\":4}],\"gyrometres\" : [{\"x\":1,\"y\":2,\"z\":3,\"t\":4}, {\"x\":1,\"y\":2,\"z\":3,\"t\":4}]}";
       qDebug() << QString::fromStdString(testReponse);

       CJsonSerializer::Deserialize(&acceleroData, testReponse);

   }
   else
   {
       qDebug() << "error connect";
       qWarning() <<"ErrorNo: "<< reply->error() << "for url: " << reply->url().toString();
       qDebug() << "Request failed, " << reply->errorString();
       qDebug() << "Headers:"<<  reply->rawHeaderList()<< "content:" << reply->readAll();
       qDebug() << reply->readAll();
   }
   delete reply;
}

AccDataDisplay::AccDataDisplay(std::string uuid){

    this->grabGesture(Qt::PanGesture);
    this->grabGesture(Qt::PinchGesture);

  //  acceleroData = new WimuAcquisition(uuid,"","",50);
  //  acceleroData->initialize();

    //** Retrieving data from BD
    getDataFromUUIDFromDB(uuid);
    //**

    availableData = acceleroData.getData();
    sliceData = availableData;


    qDebug() << "available data " << availableData.size();

    if(availableData.size()>0)
    {

        chart = new DataChart();
        chart->legend()->show();
        chart->legend()->setAlignment(Qt::AlignBottom);
        chart->setTheme(QChart::ChartThemeDark);


        chart->createDefaultAxes();
        chart->setTitle(tr("Données accéléromètre (en ms)"));
        chart->setAnimationOptions(QChart::SeriesAnimations);

        chartView = new ChartView(chart);
        chartView->setRenderHint(QPainter::Antialiasing);

        layout = new QVBoxLayout(this);

        //Initialize Recording Date
        QHBoxLayout *hboxDate = new QHBoxLayout();

        QPushButton* pbtn = new QPushButton("Reset Zoom");
        connect(pbtn, SIGNAL (released()), this, SLOT (handleResetZoomBtn()));

        pbtn->setStyleSheet(
             "border-style: outset;"
             "border-width: 2px;"
             "border-radius: 10px;"
             "border-color: beige;"
             "font: bold 10px;"
             "min-width: 6em;"
             "padding: 4px");

        pbtn->setStyleSheet("QPushButton{background-color: #ecf0f1;  border-width: 2px; border-radius: 10px;font: bold 10px; min-width: 6em; padding: 4px;}"
            "QPushButton:focus:hover{ QPushButton{background-color: red;  border-width: 2px; border-radius: 10px; font: bold 10px; min-width: 6em; padding: 4px;}"
            "QPushButton:focus:pressed{{QPushButton{background-color: green;  border-width: 2px; border-radius: 10px; font: bold 10px; min-width: 6em; padding: 4px;}");

        QLabel* dateRecorded = new QLabel();
        dateRecorded->setText(QString::fromStdString("Journée d'enregistrement: ")+ QString::fromStdString(acceleroData.getDates().back().date));
        hboxDate->addStretch();
        hboxDate->addWidget(dateRecorded);
        hboxDate->addStretch();
        hboxDate->addWidget(pbtn);

        //Initialize Checkbox and Label
        checkboxX = new QCheckBox(tr("Axe X"));
        checkboxY = new QCheckBox(tr("Axe Y"));
        checkboxZ = new QCheckBox(tr("Axe Z"));
        checkboxAccNorm = new QCheckBox(tr("Norme"));
        checkboxMovingAverage = new QCheckBox(tr("Moyenne mobile"));

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


        long long min = WimuAcquisition::minTime(availableData).timestamp;
        long long max = WimuAcquisition::maxTime(availableData).timestamp;

        rSlider = new RangeSlider(this);
        rSlider->setStartHour(min/1000);
        rSlider->setEndHour(max/1000);
        rSlider->setLeftSliderRange(min,max);
        rSlider->setRightSliderRange((long long)(max/2),max);

        layout->addLayout(hboxDate);
        layout->addWidget(chartView);
        layout->addLayout(hbox);
        layout->addWidget(rSlider);

        connect(checkboxX, SIGNAL(stateChanged(int)), this, SLOT(slotDisplayXAxis(int)));
        connect(checkboxY, SIGNAL(stateChanged(int)), this, SLOT(slotDisplayYAxis(int)));
        connect(checkboxZ, SIGNAL(stateChanged(int)), this, SLOT(slotDisplayZAxis(int)));
        connect(checkboxAccNorm, SIGNAL(stateChanged(int)), this, SLOT(slotDisplayNorme(int)));
        connect(checkboxMovingAverage, SIGNAL(stateChanged(int)), this, SLOT(slotDisplayMovingAverage(int)));

        fillChartSeries();
    }
}
void AccDataDisplay::handleResetZoomBtn()
{
    chart->zoomReset();
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
    rSlider->setStartHour(WimuAcquisition::minTime(availableData).timestamp + value);
    sliceData = acceleroData.getData(WimuAcquisition::minTime(availableData).timestamp + value, WimuAcquisition::maxTime(availableData).timestamp);
    chart->removeAllSeries();
    fillChartSeries();
    chartView->setChart(chart);
}
void AccDataDisplay::rightSliderValueChanged(int value)
{
    rSlider->setEndHour(WimuAcquisition::maxTime(availableData).timestamp-value);
    sliceData = acceleroData.getData(WimuAcquisition::minTime(availableData).timestamp + value, WimuAcquisition::maxTime(availableData).timestamp);
    chart->removeAllSeries();
    fillChartSeries();
    chartView->setChart(chart);

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
    lineseriesX->setName(tr("Axe X"));
    lineseriesX->setUseOpenGL(true);


    lineseriesY = new QtCharts::QLineSeries();
    QPen penY(QRgb(0x00b16A));
    lineseriesY->setPen(penY);
    lineseriesY->setName(tr("Axe Y"));
    lineseriesY->setUseOpenGL(true);

    lineseriesZ = new QtCharts::QLineSeries();
    QPen penZ(QRgb(0x4183D7));
    lineseriesZ->setPen(penZ);
    lineseriesZ->setName(tr("Axe Z"));
    lineseriesZ->setUseOpenGL(true);

    lineseriesAccNorm = new QtCharts::QLineSeries();
    lineseriesAccNorm->setName(tr("Norme"));

    QPen pen(QRgb(0xdadfe1));
    lineseriesAccNorm->setPen(pen);
    lineseriesAccNorm->setUseOpenGL(true);

    lineseriesMovingAverage = new QtCharts::QLineSeries();
    QPen penM(QRgb(0xf89406));
    lineseriesMovingAverage->setPen(penM);
    lineseriesMovingAverage->setName(tr("Moyenne mobile"));
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
