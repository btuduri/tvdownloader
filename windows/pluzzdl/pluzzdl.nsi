; Fichier NSIS pour pluzzdl

; Theme
;--------------------------------

	; Theme Modern UI
	!include "MUI2.nsh"

; General
;--------------------------------

	; Nom du programme
	Name "pluzzdl"

	; Nom de l'executable
	OutFile "pluzzdl_0.8.5.exe"

	; Dossier d'installation par defaut
	InstallDir "$PROGRAMFILES\pluzzdl"

	; Recupere si possible le repertoire d'installation dans le registre (pour les mises a jour)
	InstallDirRegKey HKLM "Software\pluzzdl" "Install_Dir"

	; Demande les privileges necessaires pour Windows Vista
	RequestExecutionLevel admin

; Parametres de l'interface
;--------------------------------

	; Ajoute une fenetre de confirmation si on annule l'installation
	!define MUI_ABORTWARNING

; Pages a afficher
;--------------------------------

	; Licence
	!insertmacro MUI_PAGE_LICENSE "COPYING"
	
	; Composants
	!insertmacro MUI_PAGE_COMPONENTS
	
	; Repertoire
	!insertmacro MUI_PAGE_DIRECTORY
	
	; Fenetre recapitulatif de fin
	!insertmacro MUI_PAGE_INSTFILES

	!insertmacro MUI_UNPAGE_CONFIRM
	!insertmacro MUI_UNPAGE_INSTFILES

; Langue
;--------------------------------

	; Francais 
	!insertmacro MUI_LANGUAGE "French"

; Section instalation
;--------------------------------

	; Section qui comprend le coeur du programme

		Section "pluzzdl" TVD
	
			; Section obligatoire
			SectionIn RO
	
			; Repertoire d'installation
			SetOutPath "$INSTDIR"
	
			; Fichiers a ajouter
			File /r dist\*.*		
	
			; On ajoute le repertoire d'installation au registre
			WriteRegStr HKLM "Software\pluzzdl" "Install_Dir" "$INSTDIR"
			
			; On creer un desinstalleur
			WriteUninstaller "$INSTDIR\Uninstall.exe"
			
			;
			; Raccourcis dans le menu démarrer
			;
			
			; On cree le repertoire
			CreateDirectory "$SMPROGRAMS\pluzzdl"
			; On cree le raccourci du programme
			CreateShortCut "$SMPROGRAMS\pluzzdl\pluzzdl.lnk" "$INSTDIR\mainGui.exe" "" "$INSTDIR\ico\tvdownloader.ico" 0
			; On cree le raccourci du desinstalleur
			CreateShortCut "$SMPROGRAMS\pluzzdl\Uninstall.lnk" "$INSTDIR\Uninstall.exe" "" "$INSTDIR\Uninstall.exe" 0
			
			; Raccourci sur le bureau
			CreateShortCut "$DESKTOP\pluzzdl.lnk" "$INSTDIR\mainGui.exe" "" "$INSTDIR\ico\tvdownloader.ico" 0
	
		SectionEnd

; Descriptions
;--------------------------------

	; Textes affiches pour les differentes sections que l'on vient de faire
	LangString DESC_TVD ${LANG_FRENCH} "Coeur du programme."

	; On assigne ces textes aux sections
	!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
		!insertmacro MUI_DESCRIPTION_TEXT ${TVD} $(DESC_TVD)
	!insertmacro MUI_FUNCTION_DESCRIPTION_END

; Desinstallation
;--------------------------------

	Section "Uninstall"
		
		; On supprime les raccourcis
		Delete "$DESKTOP\pluzzdl.lnk"
		Delete "$SMPROGRAMS\pluzzdl\Uninstall.lnk"
		Delete "$SMPROGRAMS\pluzzdl\pluzzdl.lnk"
		RMDir "$SMPROGRAMS\pluzzdl"

		; On supprime la clef registre
		DeleteRegKey /ifempty HKLM "Software\pluzzdl"

		; On supprime le repertoire d'installation
		RMDir /r "$INSTDIR"

	SectionEnd
