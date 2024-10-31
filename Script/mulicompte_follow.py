import pyautogui
import time 
import keyboard
import cv2 as cv
from os import path, listdir, remove, rename
import numpy as np
import random
from config import * 

def lastClick():
    # while not keyboard.is_pressed('left'):
    #     time.sleep(0.1)
    # pos = pyautogui.position()
    # return pos
  while True:
        if pyautogui.mouseDown(button='left'):
            while pyautogui.mouseDown(button='left'):
                time.sleep(0.1)  # Wait until the button is released
            pos = pyautogui.position()
            return pos
        time.sleep(0.1)


def follow(leader,follower):
    dofus_window_leader = get_window(leader)
    if dofus_window_leader is not None:
        while True:
            pos = lastClick()
            print(f"Clicked at position: {pos}")

# follow(enu,iop)

print(lastClick())