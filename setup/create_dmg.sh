#!/bin/sh
SCRIPT_PATH="`pwd`";

# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p ${SCRIPT_PATH}/../python/dist/dmg
# Empty the dmg folder.
rm -r ${SCRIPT_PATH}/../python/dist/dmg/*
# Copy the app bundle to the dmg folder.
cp -R "${SCRIPT_PATH}/../python/dist/OpenIMU.app" "${SCRIPT_PATH}/../python/dist/dmg"
# If the DMG already exists, delete it.
test -f "${SCRIPT_PATH}/../python/dist/OpenIMU.dmg" && rm "${SCRIPT_PATH}/../python/dist/OpenIMU.dmg"
/usr/local/bin/create-dmg \
  --volname "OpenIMU" \
  --volicon "${SCRIPT_PATH}/../python/resources/icons/OpenIMU.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "OpenIMU.app" 175 120 \
  --hide-extension "OpenIMU.app" \
  --app-drop-link 425 120 \
  "${SCRIPT_PATH}/../python/dist/OpenIMU.dmg" \
  "${SCRIPT_PATH}/../python/dist/dmg/"
  
# Empty the dmg folder.
rm -r ${SCRIPT_PATH}/../python/dist/dmg/*
