Pour que le plugin soit trouvé au runtime, il faut copier manuellement les trois fichier du plugin au bon endroit.

Par exemple, pour le plugin vbPlugin, il faut copier:
vbPlugind.dll
vblabel.qml
qmldir

dans un répertoir AU MÊME NIVEAU que l'application (app.exe)
donc à ->
C:\Users\Mic\Documents\OpenIMU\build-OpenQML-Desktop_Qt_5_5_1_MinGW_32bit-Debug\app\debug\blocks\visual\label