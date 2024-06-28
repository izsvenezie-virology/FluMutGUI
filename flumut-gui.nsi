Name "FluMutGUI"

InstallDir $LOCALAPPDATA\FluMutGUI

!include "MUI2.nsh"

!define MUI_LICENSEPAGE_RADIOBUTTONS


!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"


Section "Install FluMut"

    SetOutPath "$INSTDIR"

    File /r "dist\flumut-gui\*"

    WriteUninstaller "$INSTDIR\Uninstall.exe"

    CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
    CreateShortCut "$SMPROGRAMS\$StartMenuFolder\MyPythonApp.lnk" "$INSTDIR\flumut-gui.exe" "" "$INSTDIR\flumut-gui.exe"

    ; Create Desktop shortcut
    CreateShortCut "$DESKTOP\FluMutGUI.lnk" "$INSTDIR\flumut-gui.exe" "" "$INSTDIR\flumut-gui.exe"
    CreateShortCut "$SMPROGRAMS\FluMutGUI.lnk" "$INSTDIR\flumut-gui.exe" "" "$INSTDIR\flumut-gui.exe"


SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\*"

    RMDir "$INSTDIR"

    Delete "$INSTDIR\Uninstall.exe"
    Delete "$DESKTOP\FluMutGUI.lnk"
    Delete "$SMPROGRAMS\FluMutGUI.lnk"
SectionEnd

UninstallCaption "Uninstall FluMut"
UninstallIcon "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

Icon "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
Outfile "FluMutGUIInstaller.exe"
RequestExecutionLevel user
