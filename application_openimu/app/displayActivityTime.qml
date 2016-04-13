import QtQuick 2.5
import QtQuick.Window 2.2
import blocks.visual.label 1.0
import InputNodeInt 1.0
import InputNodeDouble 1.0
import InputNodeString 1.0
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick 2.0
import QtCharts 2.1

import jbQuick.Charts 1.0

Rectangle{
    width:parent.width;
    height:parent.height;
    anchors.centerIn: parent;
    Label {
        y : 0
        x : 0
        text: "Temps d'activité"
        font.pixelSize: 14
        color: "steelblue"
    }
/* Chart {
        id: chart_polar;
        width: parent.width;
        height: parent.width;
        chartAnimated: true;
        chartAnimationEasing: Easing.InBounce;
        chartAnimationDuration: 2000;
        chartType: Charts.ChartType.POLAR;
        chartData: {
            'datasets':[
                        {'color': "rgba(0,128,128,0)",'value': 10},
                        {'color': "rgba(255,128,128,0)",'value': 15}
                    ]
        };
        Component.onCompleted: {

            console.log("!!!!data is ");
        }
 }*/
}


