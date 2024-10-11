import pyautogui
import pygetwindow as gw
import time 
import keyboard
import opencv



# Get a window by its title, for example "Untitled - Notepad"
dofus_window = gw.getWindowsWithTitle('Ironamo - Dofus Retro v1.44.2')[0]

# Check if the window was found
if dofus_window:
    # Activate the window to bring it to the front
    keyboard.wait('esc')
    dofus_window.activate()
    while 1 :
        time.sleep(1)
        pyautogui.press('f1')
