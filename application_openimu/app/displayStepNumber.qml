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
        text: "Compteur de pas"
        font.pixelSize: 14
        color: "steelblue"
    }

    ChartView {
        y : 50
        width: 400
        height: 300
        theme: ChartView.ChartThemeBlueIcy
        antialiasing: true

        PieSeries {
            id: pieSeries
            PieSlice { label: "Jour 1"; value: 2220 }
            PieSlice { label: "Jour 2"; value: 8800 }
        }
}
}


