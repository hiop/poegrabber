Traytip, PoE Grabber, "Скрипт запущен!",,1

IfNotExist, %A_WorkingDir%\poescrptshy.lnk
{
	IfExist %A_WorkingDir%\poescrpt.bat
	{
		FileCreateShortcut, %A_WorkingDir%\poescrpt.bat, %A_WorkingDir%\poescrptshy.lnk,,,,,,,7
	}
	IfExist %A_WorkingDir%\poescrpt.exe
	{
		FileCreateShortcut, %A_WorkingDir%\poescrpt.exe, %A_WorkingDir%\poescrptshy.lnk,,,,,,,7
	}
}

~^c::
	IfWinActive, Path of Exile 
	{
		Sleep, 100
		FileEncoding, UTF-8
		;FileDelete, ./iteminfo.txt 
		Sleep, 100
		Fileappend,%clipboard%,./iteminfo.txt
		Run, %A_WorkingDir%/poescrptshy

	}
	return

OnClipboardChange:
	IfExist, ./iteminfo.txt 
	{
		varString = %clipboard%
		If (InStr(varString, "|")){
			StringReplace, clipboard, clipboard, |, , All
			Traytip, PoE Grabber, %clipboard%,,1
		}
		If (InStr(varString, "$empty")){
			Traytip, PoE Grabber, Нет обработчика!!!,,1
			clipboard=
		}
		If (InStr(varString, "$none")){
			Traytip, PoE Grabber, Проблема с предметом!!!,,1
			clipboard=
		}
	}