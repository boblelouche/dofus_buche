$Ret = Ma_Fonction("Cliquez sur Oui ou sur Non")
If $Ret = 6 Then
	MsgBox(0, "", "Vous avez cliqu� sur Oui")
Else
	MsgBox(0, "", "Vous avez cliqu� sur Non")
EndIf

Func Ma_Fonction($Param)
	$Retour = MsgBox(4, "", $Param)
	Return $Retour
EndFunc