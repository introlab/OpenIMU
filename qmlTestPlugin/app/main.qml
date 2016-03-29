import QtQuick 2.5
import QtQuick.Window 2.2
import blocks.incrementor 1.0 as Hello

Window {
    visible: true

    Hello.Incrementor{

    }

    MainForm {
        anchors.fill: parent
        mouseArea.onClicked: {
            Qt.quit();
        }
    }
}
