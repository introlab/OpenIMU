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

    ChartView {
        id: chart_line
        title: "Chart"
        property string id: "chart_line";
        InputNodeInt{
            id: inputTimeAxis;
        }
        InputNodeInt{
            id: inputXAxis;
        }
        InputNodeInt{
            id: inputYAxis;
        }
        InputNodeInt{
            id: inputZAxis;
        }

        y:80
        anchors.fill: parent
        legend.alignment: Qt.AlignBottom
        antialiasing: false
        animationOptions: ChartView.NoAnimation
        //    theme: ChartView.ChartThemeLight
        property bool openGL: true
        onOpenGLChanged: {
            series("series1").useOpenGL = openGL;
            series("series2").useOpenGL = openGL;
        }
        ValueAxis {
            id: axisX
            min: 0
            max: 10

        }
        ValueAxis {
            id: axisY
            min: 0
            max: 10
        }
        LineSeries {
            id: series1
            axisX: axisX
            axisY: axisY
            useOpenGL: chart_line.openGL
            XYPoint{ x: 1.1; y: 2.1 }
            XYPoint{ x: 4; y: 2.1 }

        }
        LineSeries {
            id: series2
            axisX: axisX
            axisY: axisY
            useOpenGL: chart_line.openGL
           // values : [{ x: 1.1, y: 2.1 }]
        }
        LineSeries {
            id: series3
            axisX: axisX
            axisY: axisY
            useOpenGL: chart_line.openGL
        }
    }
    // Add data dynamically to the series
    Component.onCompleted: {
        for (var i = 0; i <= 10; i++) {
           // series1.append(i,i);//inputXAxis.value[i], inputTimeAxis.value[i]);
          //  series2.append(i+1,i);//inputYAxis.value[i], inputTimeAxis.value.at(i));
          //  series3.append(i+2,i);//inputZAxis.value[i], inputTimeAxis.value.at(i));
        }
    }

    Label {
        y:0
        x: parent.width/2-150
        text: "Donnees acquises par l'accelerometre"
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
        InputNodeInt{
            id: inputSliderMinimumValue;
        }
        InputNodeInt{
            id: inputSliderMaximumValue;
        }
        width: parent.width -225
        y : parent.height -20
        x : 125
        minimumValue: inputSliderMinimumValue.value[0]
        maximumValue: inputSliderMaximumValue.value[0]
        stepSize: 1
        onValueChanged: test.text = "De " + value.toPrecision(3) +" h a  "+ maximumValue + " h"
    }

}


