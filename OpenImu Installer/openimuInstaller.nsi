


Section "OpenImu Installer"
  SetOutPath "$PROGRAMFILES64"
  File /r "OpenIMU"
  CreateShortCut "$DESKTOP\OpenIMU.lnk" "$PROGRAMFILES64\OpenIMU\bin\applicationOpenimu.exe" "" "$PROGRAMFILES64\OpenIMU\applicationOpenimu\app\icons\logo.ico"
  CreateShortCut "$STARTMENU\OpenIMU.lnk" "$PROGRAMFILES64\OpenIMU\bin\applicationOpenimu.exe" "" "$PROGRAMFILES64\OpenIMU\applicationOpenimu\app\icons\logo.ico"
  ExpandEnvStrings $0 %COMSPEC%
  ExecWait '"$0" /C "$PROGRAMFILES64\OpenIMU\bin\installScript.bat"'
SectionEnd
