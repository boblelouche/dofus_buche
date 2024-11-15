#include <MsgBoxConstants.au3>

Local $sString = "" ; A string for displaying purposes

Local $aArray[4]
$aArray[0] = "A" ; We fill an array
$aArray[1] = 0 ; with several
$aArray[2] = 1.3434 ; different
$aArray[3] = "Example Text" ; example values.

For $iElement In $aArray ; Here it starts...
    $sString &= $iElement & @CRLF
Next

; Display the results
MsgBox($MB_OK, "For..In Array Example", "Result: " & @CRLF & $sString) 