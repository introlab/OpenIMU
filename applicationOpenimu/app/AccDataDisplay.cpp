#include "AccDataDisplay.h"
#include "ui_AccDataDisplay.h"

#include <math.h>
#include <QPropertyAnimation>
#include <time.h>
#include <ctime>

AccDataDisplay::AccDataDisplay(const WimuAcquisition& accData, QWidget *parent) :
    QWidget(parent),
    m_ui(new Ui::AccDataDisplay)
{
    m_ui->setupUi(this);

    this->grabGesture(Qt::PanGesture);
    this->grabGesture(Qt::PinchGesture);
    this->setStyleSheet("background-color:white;");
    m_availableData = accData.getDataAccelerometer();
    m_sliceData = m_availableData;

    if(m_availableData.size()> 0)
    {
        m_chart = new DataChart();
        m_chart->legend()->show();
        m_chart->legend()->setAlignment(Qt::AlignBottom);
        m_chart->setTheme(QChart::ChartThemeDark);

        m_rSliderValue = 1;
        m_lSliderValue = 0;

        m_chart->createDefaultAxes();
        m_chart->setTitle(tr("Données accéléromètre (en ms)"));
        m_chart->setAnimationOptions(QChart::SeriesAnimations);

        m_chartView = new ChartView(m_chart);
        m_chartView->setRenderHint(QPainter::Antialiasing);

        connect(m_ui->pbtn, SIGNAL (released()), this, SLOT (handleResetZoomBtn()));

        this->setStyleSheet( "QPushButton{"
                             "background-color: rgba(119, 160, 175,0.7);"
                             "border-style: inset;"
                             "border-width: 2px;"
                             "border-radius: 10px;"
                             "border-color: white;"
                             "font: 12px;"
                             "min-width: 10em;"
                             "padding: 6px; }"
                             "QPushButton:pressed { background-color: rgba(70, 95, 104, 0.7);}"
                             );
        m_ui->dateRecordedDate->setText(QString::fromStdString(accData.getDates().back().date));

        m_ui->checkboxX->setChecked(true);
        m_ui->checkboxY->setChecked(true);
        m_ui->checkboxZ->setChecked(true);
        m_ui->checkboxAccNorm->setChecked(false);
        m_ui->checkboxMovingAverage->setChecked(false);

        long long min = WimuAcquisition::minTime(m_availableData).timestamp;

        m_rSlider = new RangeSlider(this);
        int tmpmin = int(m_sliceData.size()*m_lSliderValue/50);
        tmpmin = min + tmpmin;

        int tmpmax = int(m_sliceData.size()*m_rSliderValue/50);
        tmpmax = min + tmpmax;

        m_rSlider->setStartHour(tmpmin);
        m_rSlider->setEndHour(tmpmax);

        m_ui->graphLayout->addWidget(m_chartView);
        m_ui->sliderLayout->addWidget(m_rSlider);




        connect(m_ui->checkboxX, SIGNAL(stateChanged(int)), this, SLOT(slotDisplayXAxis(int)));
        connect(m_ui->checkboxY, SIGNAL(stateChanged(int)), this, SLOT(slotDisplayYAxis(int)));
        connect(m_ui->checkboxZ, SIGNAL(stateChanged(int)), this, SLOT(slotDisplayZAxis(int)));
        connect(m_ui->checkboxAccNorm, SIGNAL(stateChanged(int)), this, SLOT(slotDisplayNorme(int)));
        connect(m_ui->checkboxMovingAverage, SIGNAL(stateChanged(int)), this, SLOT(slotDisplayMovingAverage(int)));
        connect(m_ui->saveDataSet, SIGNAL(clicked(bool)), this, SLOT(slotSaveNewSetRange()));

        fillChartSeries();
    }
}

AccDataDisplay::~AccDataDisplay()
{
    delete m_ui;
}

void AccDataDisplay::showSimplfiedDataDisplay()
{
    if(m_availableData.size()> 0)
    {
        m_ui->checkboxX->hide();
        m_ui->checkboxY->hide();
        m_ui->checkboxZ->hide();
        m_ui->checkboxAccNorm->hide();
        m_ui->checkboxMovingAverage->hide();
        m_rSlider->hide();
        m_ui->pbtn->hide();
        m_ui->dateRecorded->hide();
        m_ui->groupBoxAxes->hide();
        m_ui->groupBoxSlider->hide();
        m_ui->groupBoxSave->hide();
        m_ui->saveDataSet->hide();
        m_ui->dateRecordedDate->hide();
    }
}


void AccDataDisplay::setInfo(RecordInfo recInfo)
{
    m_recordInfo = recInfo;
}

void AccDataDisplay::slotSaveNewSetRange()
{
    int tmpmin = int(m_sliceData.size()*m_lSliderValue);
    int tmpmax = int(m_sliceData.size()*m_rSliderValue);

    m_availableData.clear();
    for(int k = tmpmin; k <tmpmax; k++){
        frame value;
        value.x = m_sliceData.at(k).x;
        value.y = m_sliceData.at(k).y;
        value.z = m_sliceData.at(k).z;
        value.timestamp = k*20;
        m_availableData.push_back(value);
    }

    m_sliceData.clear();
    m_sliceData = m_availableData;
    m_rSliderValue = 1;
    m_lSliderValue = 0;

    m_rSlider->setStartHour(m_sliceData.at(0).timestamp);
    m_rSlider->setEndHour(m_sliceData.at(m_sliceData.size()-1).timestamp);

    m_chart->removeAllSeries();
    fillChartSeries();
    m_chartView->setChart(m_chart);

    WimuAcquisition* wimuData = new WimuAcquisition();

    wimuData->setDataAccelerometer(m_sliceData);

    m_recordInfo.m_recordDetails =  "Cet enregistrement est un sous-ensemble de :" + m_recordInfo.m_recordName + ". " + m_ui->recordDetailsLineEdit->text().toStdString();
    m_recordInfo.m_parentId = m_recordInfo.m_recordId;
    m_recordInfo.m_recordName = m_ui->recordNameLineEdit->text().toStdString();

    std::string output;
    CJsonSerializer::Serialize(wimuData,m_recordInfo, output);
    m_databaseAccess = new DbBlock;
    QString outputString = QString::fromStdString(output);//TODO remove
    m_databaseAccess->addRecordInDB(outputString);

    //TODO: FEEDBACK and Close the Dialog
}


void AccDataDisplay::handleResetZoomBtn()
{
    m_chart->zoomReset();
}
void AccDataDisplay::slotDisplayNorme(int value){
    if(value){
        m_chart->addSeries(m_lineseriesAccNorm);
        m_chartView->setChart(m_chart);
    }else{
        m_chart->removeSeries(m_lineseriesAccNorm);
        m_chartView->setChart(m_chart);
    }
}
void AccDataDisplay::slotDisplayMovingAverage(int value){
    if(value){
        m_chart->addSeries(m_lineseriesMovingAverage);
        m_chartView->setChart(m_chart);
    }else{
        m_chart->removeSeries(m_lineseriesMovingAverage);
        m_chartView->setChart(m_chart);
    }
}


void AccDataDisplay::leftSliderValueChanged(double value)
{
    m_lSliderValue = value;
    int tmpmin = int(m_sliceData.size()*m_lSliderValue/50);
    tmpmin = WimuAcquisition::minTime(m_availableData).timestamp + tmpmin;
    m_rSlider->setStartHour(tmpmin);
    m_chart->removeAllSeries();
    fillChartSeries();
    m_chartView->setChart(m_chart);
}

void AccDataDisplay::rightSliderValueChanged(double value)
{
    m_rSliderValue = value;
    int tmpmax = int(m_sliceData.size()*m_rSliderValue/50);
    tmpmax = WimuAcquisition::minTime(m_availableData).timestamp + tmpmax;
    m_rSlider->setEndHour(tmpmax);
    m_chart->removeAllSeries();
    fillChartSeries();
    m_chartView->setChart(m_chart);

}

void AccDataDisplay::slotDisplayXAxis(int value){
    if(value){
        m_chart->addSeries(m_lineseriesX);
        m_chartView->setChart(m_chart);
    }else{
        m_chart->removeSeries(m_lineseriesX);
        m_chartView->setChart(m_chart);
    }
}
void AccDataDisplay::slotDisplayYAxis(int value){
    if(value){
        m_chart->addSeries(m_lineseriesY);
        m_chartView->setChart(m_chart);
    }else{
        m_chart->removeSeries(m_lineseriesY);
        m_chartView->setChart(m_chart);
    }
}
void AccDataDisplay::slotDisplayZAxis(int value){
    if(value){
        m_chart->addSeries(m_lineseriesZ);
        m_chartView->setChart(m_chart);
    }else{
        m_chart->removeSeries(m_lineseriesZ);
        m_chartView->setChart(m_chart);
    }
}

std::vector<signed short> AccDataDisplay::movingAverage(int windowSize)
{
    int tmpmin = int(m_sliceData.size()*m_lSliderValue);
    int tmpmax = int(m_sliceData.size()*m_rSliderValue);
    double sum=0;
    std::vector<signed short> filteredData;
    if(tmpmax-tmpmin < windowSize+1)
    {
        return filteredData;
    }
    for(int j=tmpmin;j<tmpmin+windowSize;j++)
    {
        sum+=sqrt(pow(m_sliceData.at(j).x,2.0)+ pow(m_sliceData.at(j).y,2.0) + pow(m_sliceData.at(j).z,2.0));
    }
    filteredData.push_back(sum/windowSize);
    for (int i=tmpmin+1;i<tmpmax-windowSize;i++)
    {
        sum-=sqrt(pow(m_sliceData.at(i-1).x,2.0)+pow(m_sliceData.at(i-1).y,2.0)+ pow(m_sliceData.at(i-1).z,2.0));
        sum+=sqrt(pow(m_sliceData.at(i+windowSize-1).x,2.0)+pow(m_sliceData.at(i+windowSize-1).y,2.0)+ pow(m_sliceData.at(i+windowSize-1).z,2.0));
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
    int tmpmin = int(m_sliceData.size()*m_lSliderValue);
    int tmpmax = int(m_sliceData.size()*m_rSliderValue);

    for(int k = tmpmin; k <tmpmax; k++){

        x.push_back(m_sliceData.at(k).x);
        y.push_back(m_sliceData.at(k).y);
        z.push_back(m_sliceData.at(k).z);
        norm_acc.push_back(sqrt(pow(m_sliceData.at(k).x,2.0) + pow(m_sliceData.at(k).y,2.0) + pow(m_sliceData.at(k).z,2.0)));
        t.push_back(k*20); // TO DO Replace w/ real value
    }

    m_lineseriesX = new QtCharts::QLineSeries();
    QPen penX(QRgb(0xCF000F));
    m_lineseriesX->setPen(penX);
    m_lineseriesX->setName(tr("Axe X"));
    m_lineseriesX->setUseOpenGL(true);

    m_lineseriesY = new QtCharts::QLineSeries();
    QPen penY(QRgb(0x00b16A));
    m_lineseriesY->setPen(penY);
    m_lineseriesY->setName(tr("Axe Y"));
    m_lineseriesY->setUseOpenGL(true);

    m_lineseriesZ = new QtCharts::QLineSeries();
    QPen penZ(QRgb(0x4183D7));
    m_lineseriesZ->setPen(penZ);
    m_lineseriesZ->setName(tr("Axe Z"));
    m_lineseriesZ->setUseOpenGL(true);

    m_lineseriesAccNorm = new QtCharts::QLineSeries();
    m_lineseriesAccNorm->setName(tr("Norme"));

    QPen pen(QRgb(0xdadfe1));
    m_lineseriesAccNorm->setPen(pen);
    m_lineseriesAccNorm->setUseOpenGL(true);

    m_lineseriesMovingAverage = new QtCharts::QLineSeries();
    QPen penM(QRgb(0xf89406));
    m_lineseriesMovingAverage->setPen(penM);
    m_lineseriesMovingAverage->setName(tr("Moyenne mobile"));
    m_lineseriesMovingAverage->setUseOpenGL(true);

    for(unsigned int i = 0; i <x.size(); i++)
    {
        m_lineseriesX->append(t.at(i),x.at(i));
        m_lineseriesY->append(t.at(i),y.at(i));
        m_lineseriesZ->append(t.at(i),z.at(i));
        m_lineseriesAccNorm->append(t.at(i),norm_acc.at(i));
    }
    for(unsigned int i = 0; i <filtered_data.size(); i++)
    {
        m_lineseriesMovingAverage->append(t.at(i),filtered_data.at(i));
    }
    if(m_ui->checkboxX->isChecked())
        m_chart->addSeries(m_lineseriesX);

    if(m_ui->checkboxY->isChecked())
        m_chart->addSeries(m_lineseriesY);

    if(m_ui->checkboxZ->isChecked())
        m_chart->addSeries(m_lineseriesZ);

    if(m_ui->checkboxAccNorm->isChecked())
        m_chart->addSeries(m_lineseriesAccNorm);

    if(m_ui->checkboxMovingAverage->isChecked())
        m_chart->addSeries(m_lineseriesMovingAverage);

    m_chart->createDefaultAxes();
}

void AccDataDisplay:: firstUpdated(const QVariant &v) {
      leftSliderValueChanged(v.toDouble());
}

void AccDataDisplay:: secondUpdated(const QVariant &v) {
      rightSliderValueChanged(v.toDouble());
}
