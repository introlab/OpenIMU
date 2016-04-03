import QtQuick 2.5
import "Algo"

Rectangle {
    property alias mouseArea: mouseArea

    width: 360
    height: 360


    MouseArea {
        id: mouseArea
        anchors.fill: parent
    }

    Button {
        id: button
        text:"Bonjour"
        onClicked: testAlgo.work(text.text)

    }

    AlgoBlock{
        id : testAlgo
        onOutput: text.work(inputValue)
    }

    Text {
        id:text
        anchors.centerIn: parent
        //onOutput: console.log("Algo output in Text")
        function work(x){
            text.text = x
        }


        text:"1"
    }
}
