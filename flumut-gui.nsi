; Install parameters
Name "FluMutGUI"
Outfile "FluMutGUI_Installer.exe"
Icon "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
RequestExecutionLevel user
InstallDir $LOCALAPPDATA\FluMutGUI

; Uninstall parameters
UninstallCaption "Uninstall FluMutGUI"
UninstallIcon "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Include modern layout
!include "MUI2.nsh"
!include "FileFunc.nsh"

; Customize license and finish pages
!define MUI_LICENSEPAGE_RADIOBUTTONS
!define MUI_FINISHPAGE_SHOWREADME ""
!define MUI_FINISHPAGE_SHOWREADME_TEXT "Create Desktop Shortcut"
!define MUI_FINISHPAGE_SHOWREADME_FUNCTION AddDesktopShortcut
!define MUI_FINISHPAGE_LINK "Visit FluMut documentation"
!define MUI_FINISHPAGE_LINK_LOCATION "https://izsvenezie-virology.github.io/FluMut/"

; Insert install pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Insert uninstall pages
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Insert language
!insertmacro MUI_LANGUAGE "English"

; Create desktop shortcut 
Function AddDesktopShortcut
    CreateShortCut "$DESKTOP\FluMutGUI.lnk" "$INSTDIR\FluMutGUI.exe" "" "$INSTDIR\FluMutGUI.exe"
FunctionEnd


Section "Install FluMutGUI"

    SetOutPath "$INSTDIR"

    File /r "dist\FluMutGUI\*"

    ; Create Desktop and Start menu folder shortcut
    CreateShortCut "$SMPROGRAMS\FluMutGUI.lnk" "$INSTDIR\FluMutGUI.exe" "" "$INSTDIR\FluMutGUI.exe"

    WriteUninstaller "$INSTDIR\Uninstall.exe"

    ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
    IntFmt $0 "0x%08X" $0

    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\FluMutGUI" \
                 "DisplayName" "FluMutGUI"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\FluMutGUI" \
                 "UninstallString" "$\"$INSTDIR\Uninstall.exe$\""
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\FluMutGUI" \
                 "Publisher" "IZSVe-virology"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\FluMutGUI" \
                 "DisplayVersion" "${VERSION}"
    WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\FluMutGUI" \
                 "EstimatedSize" "$0"
    WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\FluMutGUI" \
                 "NoModify" "1"
    WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\FluMutGUI" \
                 "NoRepair" "1"

SectionEnd


Section "Uninstall"
    Delete "$INSTDIR\*"

    Delete "$INSTDIR\Uninstall.exe"
    Delete "$DESKTOP\FluMutGUI.lnk"
    Delete "$SMPROGRAMS\FluMutGUI.lnk"

    RMDir "$INSTDIR"

    DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\FluMutGUI"
    DeleteRegKey HKCU "Software\IZSVenezie-virology\FluMutGUI"
SectionEnd
