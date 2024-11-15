import pyautogui
import time
from os import path
from config import (
    zap_picture_folder,
    ressource_picture_folder,
    zap_pictures,
    zap_selector_picture,
    temp_folder,
)
from utility import click_and_confirm, get_window
# import Personage


def click_on_zaap(destination, personage):
    dofus_window = get_window(personage.name)
    if dofus_window is not None:
        for picture in zap_pictures:
            # print(picture)
            try:
                image_positions = list(
                    pyautogui.locateAllOnScreen(picture, confidence=0.8)
                )
                print(image_positions)
                if not len(image_positions) == 0:
                    for box in image_positions:
                        click_and_confirm(box)
                        time.sleep(2)
                        if detect_zap_selector is not None:
                            dest_picture = path.join(zap_picture_folder, destination)
                            print(dest_picture)
                            image_positions = list(
                                pyautogui.locateAllOnScreen(
                                    dest_picture, confidence=0.92
                                )
                            )
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


def detect_zap_selector(Perso):
    dofus_window = get_window(Perso.name)
    if dofus_window is not None:
        try:
            image_positions = list(
                pyautogui.locateOnScreen(zap_selector_picture, confidence=0.8)
            )
            if not len(image_positions) == 0:
                for box in image_positions:
                    click_and_confirm(box)
                return "selector opened"
        except Exception as e:
            print(e)
            return None


def craft_plank(personage):
    # print(listdir(ressource_picture_folder))
    dofus_window = get_window(personage)
    if dofus_window is not None:
        try:
            scierie_pict = path.join(ressource_picture_folder, "bois", "scierie.png")
            image_positions = list(
                pyautogui.locateAllOnScreen(scierie_pict, confidence=0.8)
            )
            print(image_positions)
            if not len(image_positions) == 0:
                return "scierie"
        except Exception as e:
            return e


def get_screenshot_region(personage, region):
    dofus_window = get_window(personage.name)
    if dofus_window is not None:
        time.sleep(1)
        print(pyautogui.size())
        i = 0
        screenshot = path.join(temp_folder, f"screenshot_{i}.png")
        pyautogui.screenshot(imageFilename=screenshot, region=region, allScreens=False)


# get_screenshot_region(enu ,region_inventory )

# go_brak_bank(Personage.Lea)
# print(Personage.Lea.position)
# change_map('u')
# deplacement("l")
# print(craft_plank())
# click_on_zaap("Plaine des Scarafeuilles zap.png")
# inventory_full = detect_full_inventory(Personage.Iro.name)
# detect_full_inventory(Personage.Iro)
# get_screenshot_region(Personage.Iro, ((700,50,220,55)))
# detect_inventory_open(Personage.Iro)
# print(Personage.Iro.inventory_open)
# time.sleep(2)
# detect_inventory_open(Personage.Lea)
# print(Personage.Lea.inventory_open)
