import pyautogui
import pygetwindow as gw
import time

window_name = "Ironamo - Dofus Retro v1.44.2"
divers = [1462, 184]


def gotobank():
    dofus_window = gw.getWindowsWithTitle(window_name)[0]
    # Load the screenshot and the template image
    dofus_window.activate()
    time.sleep(1)
    # Check if the window was found
    if dofus_window:
        # keyboard.press_and_release('i')
        # time.sleep(1)
        # pyautogui.leftClick(x=divers[0],y=divers[1])
        # pos_potion=pyautogui.locateOnScreen(r"C:\Users\apeir\Documents\code\dofus\photo\ressource\potion\potion_de_rapel.png", confidence=0.98)
        # pyautogui.doubleClick(x=pos_potion.left,y=pos_potion.top)
        # pos_zap = pyautogui.locateOnScreen(r"C:\Users\apeir\Documents\code\dofus\photo\map\zap\zap-20.png", confidence=0.80)
        # pyautogui.click(x=pos_zap.left,y=pos_zap.top)
        # pyautogui.click(x=pos_zap.left+35,y=pos_zap.top+40)
        # pos_destination = pyautogui.locateOnScreen(r"C:\Users\apeir\Documents\code\dofus\photo\map\zap\Cité d'asturb zap.png", confidence=0.9)
        # pyautogui.doubleClick(x=pos_destination.left, y=pos_destination.top)
        # pyautogui.click(x=910,y=820)
        # time.sleep(5)
        # pyautogui.click(x=811,y=824)
        # time.sleep(5)
        # pyautogui.click(x=910,y=820)
        # time.sleep(5)
        # pyautogui.click(x=1413,y=263)
        # time.sleep(5)
        # pyautogui.click(x=1342,y=448)
        pos_bankier = pyautogui.locateOnScreen(
            r"C:\Users\apeir\Documents\code\dofus\photo\bankier2.png", confidence=0.7
        )
        pyautogui.doubleClick(x=pos_bankier.left, y=pos_bankier.top)


#
# pyautogui.doubleClick(x=po

gotobank()
