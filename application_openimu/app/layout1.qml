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

        chartType: Charts.ChartType.LINE;
       /*chartData: [
            {value:2},
            {value:3},
            {value:5},
            {value:7},
            {value:11},
        ];*/

        chartData: {
            'labels':input1.value,
            'datasets':[
                {'fillColor': "rgba(0,128,128,0)",'pointColor': "rgba(255,0,0,1)",'strokeColor': "rgba(255,0,0,1)",'data': input1.value},
                {'fillColor': "rgba(0,128,128,0)",'pointColor': "rgba(0,255,0,1)",'strokeColor': "rgba(0,255,0,1)",'data': input2.value},
                {'fillColor': "rgba(0,128,128,0)",'pointColor': "rgba(0,0,255,1)",'strokeColor': "rgba(0,0,255,1)",'data': input3.value}
            ]
        };

        chartAnimated: true;
        chartAnimationEasing: Easing.InOutElastic;
        chartAnimationDuration: 1000;

        chartOptions: {"segmentStrokeColor": "#ECECEC"};        
        Component.onCompleted: {

            console.log("!!!!data is ", data.toString());
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
        minimumValue: inputSliderMinimumValue.value[0]
        maximumValue: inputSliderMaximumValue.value[0]
        stepSize: 1
        onValueChanged: test.text = "De " + value.toPrecision(3) +" h à "+ maximumValue + " h"
    }

}


