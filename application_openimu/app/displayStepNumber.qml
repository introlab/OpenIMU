import QtQuick 2.5
import QtQuick.Window 2.2
//import blocks.visual.label 1.0
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

    Item{
        id:test
        property var valueString: ""
        property var valueInt : ""
        property var valuearray :""
        property var valueLabel:""
        property var valueData:""
    }



    Column{

        spacing: 5

        Label {
            InputNodeString{
                id: inputtitle;
            }
            text: inputtitle.value + test.valueString
            font.pixelSize: 14
            color: "steelblue"
        }


        Row{

            Chart{
                id: chart_bar

                InputNodeInt{
                    id:x
                }
                InputNodeInt{
                    id:y
                }

                width:350;
                height:350;
                chartAnimated: true;
                chartAnimationEasing: Easing.Linear
                chartAnimationDuration: 1000;
                chartType: Charts.ChartType.BAR;
                chartData: {
                    'labels': x.value,
                    'datasets':[
                        {'fillColor': "rgba(0,128,128,0)",'strokeColor': "rgba(255,0,0,1)",'data':  y.value},
                    ]};
                }


            Column{
                spacing: 10

                Label {
                    id: vtotal
                    InputNodeInt{
                        id: inputvtotal;
                    }
                    text: "Totale de la journée :" + inputvtotal.value + test.valueInt
                }
                Label{
                    id:vmoy
                    InputNodeInt{
                        id: inputvmoy;
                    }
                    text:"Valeur moyenne : " + inputvmoy.value +  test.valueInt
                }
                Label{
                    id:vmax
                    InputNodeInt{
                        id: inputvmax;
                    }
                    text:"Valeur maximum : " + inputvmax.value + test.valueInt
                }
                Label{
                    id:vmin
                    InputNodeInt{
                        id: inputvmin;
                    }
                    text:"Valeur minimum : " + inputvmin.value + test.valueInt
                }
            }
        }
    }



}


