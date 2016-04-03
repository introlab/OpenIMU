import QtQuick 2.0

Item {
    signal output()
    property int inputValue: 0

    function work(input) {
        console.log("Algo new input " + input.toString() + ";")
        inputValue = input +1
        output.call()
    }

}
