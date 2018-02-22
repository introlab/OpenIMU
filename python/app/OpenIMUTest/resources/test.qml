import QtQuick 2.9
import QtQuick.Controls 1.4

Rectangle {
  id: rectangle1

  width: 100
  height: 100
  color: "#cf1a1a"

  Button {
          id: idButtonClick

          anchors.fill: rectangle1

          height: 20
          width: 50

          text: "click"

          onClicked: {
              console.log("idButtonClick");
        }
  }

}

