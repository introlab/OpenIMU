import QtQuick 2.6
import QtQuick.Controls 2.0

RangeSlider {
    id: control
    first.value: 0
    second.value: 1
	signal qmlSignal(var anObject)
    background: Rectangle {
        x: control.leftPadding
        y: control.topPadding + control.availableHeight / 2 - height / 2
        implicitWidth: 320
        implicitHeight: 2
        width: control.availableWidth
        height: implicitHeight
        radius: 2
        color: "#bdbebf"

        Rectangle {
            x: control.first.visualPosition * parent.width
            width: control.second.visualPosition * parent.width - x
            height: parent.height
            color: "#c0392b"
            radius: 2
        }
    }
	 
    first.handle: Rectangle {
		id: rect1
		x: control.leftPadding + first.visualPosition * (control.availableWidth - width)
        y: control.topPadding + control.availableHeight / 2 - height / 2
        implicitWidth: 26
        implicitHeight: 26
        radius: 13
        color: first.pressed ? "#f0f0f0" : "#f6f6f6"
		border.color: "#bdbebf"
    	
}
    second.handle: Rectangle {
		id:rect2
        x: control.leftPadding + second.visualPosition * (control.availableWidth - width)
        y: control.topPadding + control.availableHeight / 2 - height / 2
        implicitWidth: 26
        implicitHeight: 26
        radius: 13
        color: second.pressed ? "#f0f0f0" : "#f6f6f6"
        border.color: "#bdbebf"
    }
}