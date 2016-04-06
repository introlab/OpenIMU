import QtQuick 2.5
import QtQuick.Window 2.2
import blocks.visual.label 1.0
import quickItemInputNode 1.0

//import "."
import jbQuick.Charts 1.0
Rectangle{

    width:parent.width;
    height:parent.height;
    anchors.centerIn: parent;
    Chart{
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
        chartAnimationEasing: Easing.Linear;
        chartAnimationDuration: 1000;
        //chartOptions: {"segmentStrokeColor": "#ECECEC"};

/*
        var data = {
        labels: [10,20,30,40,50,60,70] // for x-axis lables
        datasets: [
        {
        fillColor : "rgba(0,128,128,1)",
        strokeColor : "rgba(0,128,128,1)",
        pointColor : "rgba(0,128,128,1)",
        data : arr1 // just keep appending values to this array
        },
        {
        fillColor : "rgba(0,255,255,1)",
        strokeColor : "rgba(0,255,255,1)",
        pointColor : "rgba(0,255,255,1)",
        data : arr1
        } ]
        */


        //chartType: Charts.ChartType.LINE;
        Component.onCompleted: {
            /*var data = {

                labels: [10,20,30,40,50,60,70],

                datasets: [
                            {
                            fillColor : "rgba(0,128,128,0)",
                            strokeColor : "rgba(255,0,0,1)",
                            pointColor : "rgba(255,0,0,1)",
                            data: [1,2,3,4,5,6]
                            },
                            {
                            fillColor : "rgba(0,255,255,0)",
                            strokeColor : "rgba(0,255,0,1)",
                            pointColor : "rgba(0,255,0,1)",
                            data: [1,2,3,4,5,6]
                            },
                            {
                            fillColor : "rgba(0,255,255,0)",
                            strokeColor : "rgba(0,0,255,1)",
                            pointColor : "rgba(0,0,255,1)",
                            data: [1,2,3,4,5,6]
                            }
                        ]

            }
            chart_pie.chartData = data*/



            console.log("!!!!data is ", data.toString());
        }

    }
}





