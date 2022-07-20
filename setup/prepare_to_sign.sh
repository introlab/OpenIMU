#!/bin/sh
SCRIPT_PATH="`pwd`";

cd ${SCRIPT_PATH}/../python/dist/OpenIMU.app/Contents/MacOS
mv PySide6/ ../Frameworks/
ln -s ../Frameworks/PySide6 .
cd ../Frameworks
ln -s ../MacOS/Qt* .
ln -s ../MacOS/lib*.dylib .
mkdir ${SCRIPT_PATH}/../python/dist/OpenIMU.app/Contents/Plugins

