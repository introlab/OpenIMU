import QtQuick 2.5
import QtQuick.Window 2.2
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

    Column{
         property string id: "col1";
        spacing: 5

        Label {
            InputNodeString{
                id: inputTitle;
            }
            property string id: "label_title_value";
            text: "test"//inputTitle.value[0]
            font.pixelSize: 14
            color: "steelblue"
        }

        Row{
            property string id: "row1";
            Chart{
                property string id: "chart_bar"

                InputNodeString{
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
                    'labels': y.value,
                            'datasets':[
                                {'fillColor': "rgba(0,128,128,0)",'strokeColor': "rgba(255,0,0,1)",'data':  y.value},
                            ]};
            }

            Column{
                spacing: 10
                property string id: "col2";
                Label {
                    property string id: "vtotalLabel"
                    InputNodeInt{
                        id: inputvtotal;
                    }
                    text: "Totale de la journée :" + inputvtotal.value[0]
                }
                Label{
                    property string id:"vmoyLabel"
                    InputNodeInt{
                        id: inputvmoy;
                    }
                    text:"Valeur moyenne : " + inputvmoy.value[0]
                }
                Label{
                    property string id:"vmaxLabel"
                    InputNodeInt{
                        id: inputvmax;
                    }
                    text:"Valeur maximum : " + inputvmax.value[0]
                }
                Label{
                    property string id:"vminLabel"
                    InputNodeInt{
                        id: inputvmin;
                    }
                    text:"Valeur minimum : " + inputvmin.value[0]
                }
            }
        }
    }
}
