


Section "OpenImu Installer"
  SetOutPath "$PROGRAMFILES64"
  File /r "OpenIMU"
  ExpandEnvStrings $0 %COMSPEC%
  ExecWait '"$0" /C "$PROGRAMFILES64\OpenIMU\bin\installScript.bat"'
SectionEnd
