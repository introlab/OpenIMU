; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "OpenIMU"
#define MyAppVersion "1.1.3"
#define MyAppPublisher "INTER - CdRV - 3IT - USherbrooke"
#define MyAppURL "https://github.com/introlab/OpenIMU"
#define MyAppExeName "OpenIMU.exe"

#define MyAppVersionString StringChange(MyAppVersion, ".", "_")
#define AppGUID "{09CAE440-5766-4518-8D40-DFF3B434591A}"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{#AppGUID}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
UninstallDisplayName={#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={commonpf64}\OpenIMU
DisableProgramGroupPage=yes
OutputDir=.
OutputBaseFilename=Setup_OpenIMU_{#MyAppVersionString}
SetupIconFile=..\python\resources\icons\OpenIMU.ico
Compression=lzma2/Ultra
SolidCompression=true
InternalCompressLevel=Ultra
ShowLanguageDialog=yes
LicenseFile="..\LICENSE.TXT"
WizardStyle=modern

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Utility files
Source: "UninsIS.dll"; Flags: dontcopy
; Application files
Source: "..\python\dist\OpenIMU\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs
; Alembic files
Source: "..\python\alembic.ini"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\python\alembic\*"; DestDir: "{app}\alembic"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{commonprograms}\OpenIMU\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Add firewall exception
Filename: "{sys}\netsh.exe"; Parameters: "advfirewall firewall add rule name=""OpenIMU"" protocol=TCP dir=in action=allow program=""{app}\{#MyAppExeName}"" "; StatusMsg: "Adding Firewall Exception"; Flags: runhidden

[UninstallRun]
Filename: "{sys}\netsh.exe"; Parameters: "advfirewall firewall delete rule name=""OpenIMU"" "; StatusMsg: "Removing Firewall Exception"; Flags: runhidden; RunOnceId: "DelFirewallException"


[Code]
// Import IsISPackageInstalled() function from UninsIS.dll at setup time
function DLLIsISPackageInstalled(AppId: string; Is64BitInstallMode,
  IsAdminInstallMode: DWORD): DWORD;
  external 'IsISPackageInstalled@files:UninsIS.dll stdcall setuponly';

// Import CompareISPackageVersion() function from UninsIS.dll at setup time
function DLLCompareISPackageVersion(AppId, InstallingVersion: string;
  Is64BitInstallMode, IsAdminInstallMode: DWORD): LongInt;
  external 'CompareISPackageVersion@files:UninsIS.dll stdcall setuponly';

// Import UninstallISPackage() function from UninsIS.dll at setup time
function DLLUninstallISPackage(AppId: string; Is64BitInstallMode,
  IsAdminInstallMode: DWORD): DWORD;
  external 'UninstallISPackage@files:UninsIS.dll stdcall setuponly';

// Wrapper for UninsIS.dll IsISPackageInstalled() function
// Returns true if package is detected as installed, or false otherwise
function IsISPackageInstalled(): Boolean;
begin
  result := DLLIsISPackageInstalled('{#AppGUID}',  // AppId
    DWORD(Is64BitInstallMode()),                   // Is64BitInstallMode
    DWORD(IsAdminInstallMode())) = 1;              // IsAdminInstallMode
  if result then
    Log('UninsIS.dll - Package detected as installed')
  else
    Log('UninsIS.dll - Package not detected as installed');
end;

// Wrapper for UninsIS.dll CompareISPackageVersion() function
// Returns:
// < 0 if version we are installing is < installed version
// 0   if version we are installing is = installed version
// > 0 if version we are installing is > installed version
function CompareISPackageVersion(): LongInt;
begin
  result := DLLCompareISPackageVersion('{#AppGUID}',  // AppId
    '{#MyAppVersion}',                                  // InstallingVersion
    DWORD(Is64BitInstallMode()),                      // Is64BitInstallMode
    DWORD(IsAdminInstallMode()));                     // IsAdminInstallMode
  if result < 0 then
    Log('UninsIS.dll - This version {#MyAppVersion} older than installed version')
  else if result = 0 then
    Log('UninsIS.dll - This version {#MyAppVersion} same as installed version')
  else
    Log('UninsIS.dll - This version {#MyAppVersion} newer than installed version');
end;

// Wrapper for UninsIS.dll UninstallISPackage() function
// Returns 0 for success, non-zero for failure
function UninstallISPackage(): DWORD;
begin
  result := DLLUninstallISPackage('{#AppGUID}',  // AppId
    DWORD(Is64BitInstallMode()),                 // Is64BitInstallMode
    DWORD(IsAdminInstallMode()));                // IsAdminInstallMode
  if result = 0 then
    Log('UninsIS.dll - Installed package uninstall completed successfully')
  else
    Log('UninsIS.dll - installed package uninstall did not complete successfully');
end;


function PrepareToInstall(var NeedsRestart: Boolean): string;
begin
  result := '';
  // If package installed, uninstall it automatically if the version we are
  // installing does not match the installed version; If you want to
  // automatically uninstall only...
  // ...when downgrading: change <> to <
  // ...when upgrading:   change <> to >
  //if IsISPackageInstalled() and (CompareISPackageVersion() <> 0) then
  if IsISPackageInstalled() then
    UninstallISPackage();
end;