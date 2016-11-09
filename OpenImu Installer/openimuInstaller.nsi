Section "OpenImu Installer"
  SetOutPath "$PROGRAMFILES64"
  File /r "OpenIMU"
  ExpandEnvStrings $0 %COMSPEC%
  ExecWait '"$0" /C "$PROGRAMFILES64\OpenIMU\bin\installScript.bat"'
  SetOutPath "$PROGRAMFILES64\OpenIMU\bin\"
  CreateShortCut "$DESKTOP\Openimu.exe.lnk" "$PROGRAMFILES64\OpenIMU\bin\applicationOpenimu.exe" "" "$PROGRAMFILES64\OpenIMU\applicationOpenimu\app\icons\logo.ico"
  CreateDirectory "$SMPROGRAMS\OpenImu\"
  CreateShortCut "$SMPROGRAMS\OpenImu\OpenImu.lnk" "$PROGRAMFILES64\OpenIMU\bin\applicationOpenimu.exe" "" "$PROGRAMFILES64\OpenIMU\applicationOpenimu\app\icons\logo.ico"
SectionEnd
