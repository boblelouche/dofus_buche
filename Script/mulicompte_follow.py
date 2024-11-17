import pyautogui
import time
from .Player import Player


def lastClick():
    # while not keyboard.is_pressed('left'):
    #     time.sleep(0.1)
    # pos = pyautogui.position()
    # return pos
    while True:
        if pyautogui.mouseDown(button="left"):
            while pyautogui.mouseDown(button="left"):
                time.sleep(0.1)  # Wait until the button is released
            pos = pyautogui.position()
            return pos
        time.sleep(0.1)


def follow(leader: Player, follower: list[Player]):
    dofus_window_leader = leader.foreground()
    if dofus_window_leader is not None:
        while True:
            pos = lastClick()
            print(f"Clicked at position: {pos}")


# follow(enu,iop)

print(lastClick())
