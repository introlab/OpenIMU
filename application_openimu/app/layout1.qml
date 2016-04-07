import QtQuick 2.5
import QtQuick.Window 2.2
import blocks.visual.label 1.0
import quickItemInputNode 1.0
import QtQuick.Controls 1.4
//import "."
import jbQuick.Charts 1.0
Rectangle{

    width:parent.width;
    height:parent.height;
    anchors.centerIn: parent;
    Label{
        QuickItemInputNode{
            id: inputStepNumber;
        }
        id: label_steps
         property string id: "label_steps";
        text: "Steps: "+inputStepNumber.valueBuf
        y:0


    }
    Chart{
        y:50
        //identity and internal maping
        id: chart_pie;
        property string id: "chart_pie";

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
        height:parent.height;


        chartAnimated: true;
        chartAnimationEasing: Easing.Linear;
        chartAnimationDuration: 1000;
        chartType: Charts.ChartType.LINE;
        chartOptions: {"segmentStrokeColor": "#ECECEC"};

        Component.onCompleted: {

        var data = {

            labels: [10,20,30,40,50,60,70],

            datasets: [
                        {
                        fillColor : "rgba(0,128,128,0)",
                        strokeColor : "rgba(0,128,128,1)",
                        pointColor : "rgba(0,128,128,1)",
                        data : [65, 59, 80, 56, 55, 40]
                        },
                        {
                        fillColor : "rgba(0,255,255,0)",
                        strokeColor : "rgba(0,255,255,1)",
                        pointColor : "rgba(0,255,255,1)",
                        data : [55, 49, 70, 71, 46, 55, 30]
                        }
                    ]

        }
        chart_pie.chartData = data
        }







    }

}





