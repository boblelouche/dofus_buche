import pyautogui
import time 
import keyboard
import cv2 as cv
from os import path, listdir, remove, rename
import numpy as np
import random
from config import * 
from utility import *
import Personage


def clic_on_zap(destination, personage):
    dofus_window = get_window(personage.name)
    if dofus_window is not None:
        for picture in zap_pictures:
            # print(picture)
            try:
                image_positions = list(pyautogui.locateAllOnScreen(picture,confidence=0.8))
                print(image_positions)
                if not len(image_positions) == 0:
                    for box in image_positions:              
                        click_and_confirme(box)
                        time.sleep(2)
                        if detect_zap_selector is not None:
                            dest_picture = path.join(zap_picture_folder, destination)
                            print(dest_picture)
                            image_positions = list(pyautogui.locateAllOnScreen(dest_picture,confidence=0.92))  
                            for box in image_positions:              
                                pyautogui.doubleClick(box)
                            return "zap selector is opened"
                                    # print("open")
            except Exception as e:
                print(e)
                continue
    else:
        raise "window not found"
            # print(image_positions)
                

def detect_zap_selector(personage):
    dofus_window = get_window(personage)
    if dofus_window is not None:
        try:
            image_positions = list(pyautogui.locateOnScreen(zap_selector_picture,confidence=0.8))
            if not len(image_positions) == 0:
                for box in image_positions:
                    click_and_confirme(box)
                return "selector opened"
        except Exception as e:
            return None


def make_planche(personage):
    # print(listdir(ressource_picture_folder))
    dofus_window = get_window(personage)
    if dofus_window is not None:
        try:
            scierie_pict = path.join(ressource_picture_folder,'bois','scierie.png')
            image_positions = list(pyautogui.locateAllOnScreen(scierie_pict,confidence=0.8))
            print(image_positions)
            if not len(image_positions) == 0:
                return "scierie"
        except Exception as e:
            return e

def deplacement(chemin):
    for e in chemin:
        change_map(e)
        time.sleep(6)
        # start_time = actual_time = time.time()

        # while actual_time-start_time<5:
            # image_positions = list(pyautogui.locateAllOnScreen(map_loading_picture, confidence=0.8))
            # if len(image_positions)!=0:
                # print("map have changed")
                # break
            # actual_time=time.time()
                        # time.sleep(1)
        # return "le deplacement n'as pas eu lieu"
        # print("cooldown over")
        


def change_map(direction,personage):
    dofus_window = get_window(personage)
    if dofus_window is not None:
        screen_width, screen_height = pyautogui.size()
        region = {
            "l":(screen_width // 10, 0, screen_width // 7, screen_height-250),
            "r":(screen_width-500, 0, screen_width-250, screen_height-250),
            "u":(0, 0, screen_width, 150),
            "d":(0, screen_height-400, screen_width, screen_height-250)
        }
        print(pyautogui.size())
        i=0
        screenshot = path.join(temp_folder,f'screenshot_{i}.png')
        pyautogui.screenshot(imageFilename=screenshot,region=region[direction])
        print(region[direction])
        if direction =="u":        
            for picture in move_stars:
                keyboard.press("a")
                time.sleep(2)
                try:
                    # image_positions = list(pyautogui.locateAllOnScreen(picture, confidence=0.8))
                    image_positions = list(pyautogui.locateAllOnScreen(picture, region=region[direction], confidence=0.7))       
                    # print(image_positions)
                    if not len(image_positions) == 0:
                        for box in image_positions:
                            keyboard.release("a")
                            pyautogui.click(x = box.left+10, y = box.top+10)
                            return "found on windows"
                except Exception as e :
                    keyboard.release("a")
                    print(e)
                    continue
        else:       
            for picture in move_arrows:
                keyboard.press("a")
                time.sleep(2)
                try:
                    # image_positions = list(pyautogui.locateAllOnScreen(picture, confidence=0.8))
                    image_positions = list(pyautogui.locateAllOnScreen(picture, region=region[direction], confidence=0.7))       
                    # print(image_positions)
                    if not len(image_positions) == 0:
                        for box in image_positions:
                            keyboard.release("a")
                            pyautogui.click(x = box.left, y = box.top+75)
                            return "found on windows"
                except Exception as e :
                    keyboard.release("a")
                    print(e)
                    continue
    else:
        raise "window not found"


def get_screenshot_region(personage, region):
    dofus_window = get_window(personage.name)
    if dofus_window is not None:
        time.sleep(1)
        print(pyautogui.size())
        i=0
        screenshot = path.join(temp_folder,f'screenshot_{i}.png')
        pyautogui.screenshot(imageFilename=screenshot, region=region, allScreens=False)


# get_screenshot_region(enu ,region_inventory )

# go_brak_bank(Personage.Lea)     
# print(Personage.Lea.position)
# change_map('u')
# deplacement("l")
# print(make_planche())
# clic_on_zap("Plaine des Scarafeuilles zap.png")
# inventory_full = detect_full_inventory(Personage.Iro.name)
# detect_full_inventory(Personage.Iro)
# get_screenshot_region(Personage.Iro, ((700,50,220,55)))
# detect_inventory_open(Personage.Iro)
# print(Personage.Iro.inventory_open)
# time.sleep(2)
# detect_inventory_open(Personage.Lea)
# print(Personage.Lea.inventory_open)
