[Setup]
AppName=Huginn Deepfake Guard
AppVersion=1.0
DefaultDirName={autopf}\Huginn
DefaultGroupName=Huginn
OutputDir=.
OutputBaseFilename=HuginnInstaller
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Files]
Source: "src\Huginn.App\bin\Release\net9.0-windows\win-x64\publish\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\Huginn"; Filename: "{app}\Huginn.App.exe"
Name: "{commondesktop}\Huginn"; Filename: "{app}\Huginn.App.exe"

[Run]
Filename: "{app}\Huginn.App.exe"; Description: "Запустить Huginn"; Flags: nowait postinstall skipifsilent
