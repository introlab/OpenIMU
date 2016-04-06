import QtQuick 2.5
import QtQuick.Window 2.2
import blocks.visual.label 1.0
import quickItemInputNode 1.0
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4

import jbQuick.Charts 1.0

Rectangle{

    width:parent.width;
    height:parent.height;
    anchors.centerIn: parent;

    Label {
       y:0
       x: 40
       text: "Données acquises par l'accéléromètre"
       font.pixelSize: 22
       color: "steelblue"
     }

    Label {
       id: test
       y:40
       x:parent.width/2-80
       font.pixelSize: 18
       color: "steelblue"
     }

    Chart{
        y:80
        //identity and internal maping
        id: chart_line;
        property string id: "chart_line";

        QuickItemInputNode{
            id: input1;
        }
        QuickItemInputNode{
            id: input2;
        }
        QuickItemInputNode{
            id: input3;
        }

        //ui properties
        width:parent.width;
        height:parent.height-100;

        chartAnimated: true;
        chartAnimationEasing: Easing.InOutElastic;
        chartAnimationDuration: 1000;
        chartType: Charts.ChartType.LINE;
        chartOptions: {"segmentStrokeColor": "#ECECEC"};        
        Component.onCompleted: {

                var data = {

                    labels: [10,20,30,40,50,60,70],

                    datasets: [
                                {
                                label: "Données X",
                                fillColor : "rgba(0,128,128,0)",
                                strokeColor : "rgba(0,128,128,1)",
                                pointColor : "rgba(0,128,128,1)",
                                data : [65, 59, 80, 81, 56, 55, 40]
                                },
                                {
                                label: "My Second dataset",
                                fillColor : "rgba(0,255,255,0)",
                                strokeColor : "rgba(0,255,255,1)",
                                pointColor : "rgba(0,255,255,1)",
                                data : [55, 49, 70, 71, 46, 55, 30]
                                },
                                {
                                label: "My Second dataset",
                                fillColor : "rgba(0,234,234,0)",
                                strokeColor : "rgba(0,234,234,1)",
                                pointColor : "rgba(0,234,234,1)",
                                data : [25, 39, 40, 81, 16, 25, 20]
                                }
                            ]

                }
                chart_line.chartData = data
                }
    }
    Label {
        y : parent.height -20
        x : 0
       text: "Tranche horaire: "
       font.pixelSize: 14
       color: "steelblue"
     }

    Slider {
        id: slider
        property string id: "slider";
        QuickItemInputNode{
            id: inputSliderMinimumValue;
        }
        QuickItemInputNode{
            id: inputSliderMaximumValue;
        }
        width: parent.width -225
        y : parent.height -20
        x : 125
        minimumValue: inputSliderMinimumValue.valueBuf
        maximumValue: inputSliderMaximumValue.valueBuf
        stepSize: 1
        onValueChanged: test.text = "De " + value.toPrecision(3) +" h à "+ maximumValue + " h"
    }

}





