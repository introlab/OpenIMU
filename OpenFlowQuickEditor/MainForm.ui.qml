import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.2

Item {
    width: 800
    height: 600

    RowLayout {
        id: layout
        anchors.fill: parent
        spacing: 6

        BlockListView{

        }

        Editor {
            Layout.preferredHeight: 480
            Layout.preferredWidth: 325
            Layout.maximumWidth: 1000
            Layout.minimumHeight: 200
            Layout.maximumHeight: 1000
        }

        ColumnLayout {
            id: columnLayout2
            width: 100
            height: 100
            spacing: 6

            Rectangle {
                color: 'teal'
                Layout.minimumWidth: 50
                Layout.preferredWidth: 100
                Layout.maximumWidth: 300
                Layout.minimumHeight: 150
                Text {
                    anchors.centerIn: parent
                    text: parent.width + 'x' + parent.height
                }
            }
            Rectangle {
                color: 'plum'
                Layout.fillWidth: true
                Layout.minimumWidth: 100
                Layout.preferredWidth: 200
                Layout.preferredHeight: 100
                Layout.maximumWidth: 300
                Text {
                    anchors.centerIn: parent
                    text: parent.width + 'x' + parent.height
                }
            }
        }
    }
}
