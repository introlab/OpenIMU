import QtQuick 2.0

Component {
    Item {
        width: 180; height: 40
        MouseArea{
            id: mouseArea2
            anchors.fill: parent
            Row {
                id: row1
                anchors.verticalCenter: parent.verticalCenter
                Text {
                    width: 150
                    id:txt
                    text: blockName
                    anchors.verticalCenter: parent.verticalCenter
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                }
                MouseArea{
                    id: mouseArea1

                    width: 25
                    height: 25
                    anchors.verticalCenter: parent.verticalCenter

                    Text{
                        text: '+'
                        anchors.verticalCenter: parent.verticalCenter
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignRight
                        width: 25
                        height: 25
                    }
                    onClicked: {
                        txt.text="Adding block!!!"
                        blockListModel.append(
                                    {blockName: blockName + "!",
                                     description: "This block was added dynamically."
                                          })
                    }
                }
            }
            onClicked: {
                txt.text="Clicked!!!"
                availableListViewBlockDescription.text=description
            }
        }
    }
}
