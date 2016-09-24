import QtQuick 2.0

import QtQuick.Controls 1.4
import QtQuick.Layouts 1.2


ColumnLayout {
    id: availableListView
    spacing: 6

    ListView {
        id: blockList
        Layout.fillHeight: true
        highlight: Rectangle { color: "lightsteelblue"; radius: 5 }
        focus: true
        model: BlockListModel {
            id: blockListModel
        }
        delegate: BlockListDelegate {
            id: blockListDelegate
        }
    }

    TextArea {
        id: availableListViewBlockDescription
        text: "Description of the selected block in the list."
        Layout.maximumWidth: 300
        font.pointSize: 10
        verticalAlignment: Text.AlignBottom
        wrapMode: Text.WordWrap
    }
}
