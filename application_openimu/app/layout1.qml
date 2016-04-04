import QtQuick 2.5
import QtQuick.Window 2.2
import blocks.visual.label 1.0

//import "."
import jbQuick.Charts 1.0

Chart{
    id: chart_pie;

    width:300;
    height:300;

    chartAnimated: true;
    chartAnimationEasing: Easing.Linear;
    chartAnimationDuration: 1000;
    chartType: Charts.ChartType.PIE;
    chartOptions: {"segmentStrokeColor": "#ECECEC"};
    chartData: [
        {value: 15, color: "#6AA84F"},
        {value:  3, color: "#DC3912"},
        {value:  5, color: "#FF9900"}];
}







