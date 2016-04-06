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

        chartAnimated: true;
        chartAnimationEasing: Easing.Linear;
        chartAnimationDuration: 1000;
        chartType: Charts.ChartType.PIE;
        chartOptions: {"segmentStrokeColor": "#ECECEC"};
        chartData: [
            {value:  input1.valueBuf, color: "#6AA84F"},
            {value:  input2.valueBuf, color: "#DC3912"},
            {value:  input3.valueBuf, color: "#FF9900"}];



    }

}





