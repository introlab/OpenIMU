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
        width:parent.width;
        height:parent.height;
        anchors.centerIn: parent;


        Label {
            InputNodeString{
                id: inputTitle;
            }
            property string id: "label_title_value";
            x: parent.x + parent.width/2 - this.width/2
            text: inputTitle.value[0]
            font.pixelSize: 20
            color: "steelblue"
            anchors.margins: 10
        }

        //Top Row - Information for the current day.
        Row{
            property string id: "row1";
            width:parent.width;
            height:0.15*parent.height;
            Column
            {
                property string id: "col2";
                width:0.5*parent.width;
                height:parent.height;

                Label {
                     text: "Analyse de pas journaliere"
                     font.pixelSize: 14
                     font.underline:true
                     color: "steelblue"
                     y: parent.y +300
                }

                Label {
                    InputNodeInt{
                        id: inputStepNumber;
                    }
                    property string id: "label_step";
                     text: "Nombre de pas: " + inputStepNumber.value[0]
                     font.pixelSize: 14
                }

            }
        }

        //Bottom Row - Information for the sample data.
        Row{
            property string id: "row2";
            width:parent.width;
            height:0.85*parent.height;

            Column{
                spacing: 10
                property string id: "col3";
                width:0.5*parent.width;
                height:parent.height;

                Label {
                     text: "Analyse de pas tendancielle"
                     font.pixelSize: 14
                     font.underline:true
                     color:"steelblue"
                }

                Chart{
                    InputNodeString{
                        id: x;
                    }
                    InputNodeInt{
                        id: y;
                    }
                    property string id: "chart_step";
                    width:parent.width;
                    height:0.75*parent.height;
                    chartAnimated: true;
                    chartAnimationEasing: Easing.Linear;
                    chartAnimationDuration: 1000;
                    chartType: Charts.ChartType.BAR;
                    chartData: {
                        'labels': x.value,
                        'datasets':[
                            {'fillColor': "rgba(255,0,0,1)",'strokeColor': "rgba(255,0,0,1)",'data':  y.value},
                        ]};
                }
            }

            Column{
                spacing: this.height/(this.children.length+3)

                property string id: "col4";
                width:0.5*parent.width;
                height:parent.height;
                x : parent.x + 300;


                Label {
                    InputNodeInt{
                        id: inputStartDate;
                    }
                    property string id: "label_start_date";

                     text: "Date de debut: " + inputStartDate.value[0]
                     font.pixelSize: 14
                }

                Label {
                    InputNodeInt{
                        id: inputEndDate;
                    }
                    property string id: "label_end_date";
                     text: "Date de fin: " + inputEndDate.value[0];
                     font.pixelSize: 14
                }

                Label {
                    InputNodeInt{
                        id: inputDaysAvailable;
                    }
                    property string id: "label_days";
                     text: "Nombre de jours etudies: " + inputDaysAvailable.value[0];
                     font.pixelSize: 14
                }

                Label {
                    property string id: "vtotalLabel"
                    InputNodeInt{
                        id: inputvtotal;
                    }
                    text: "Totale de pas dans l'échantillon: " + inputvtotal.value[0]
                    font.pixelSize: 14
                }
                Label{
                    property string id:"vmoyLabel"
                    InputNodeInt{
                        id: inputvmoy;
                    }
                    text:"Valeur moyenne: " + inputvmoy.value[0]
                    font.pixelSize: 14
                }
                Label{
                    property string id:"vmaxLabel"
                    InputNodeInt{
                        id: inputvmax;
                    }
                    text:"Valeur maximum: " + inputvmax.value[0]
                    font.pixelSize: 14
                }
                Label{
                    property string id:"vminLabel"
                    InputNodeInt{
                        id: inputvmin;
                    }
                    text:"Valeur minimum: " + inputvmin.value[0]
                    font.pixelSize: 14
                }
            }
        }
    }
}


