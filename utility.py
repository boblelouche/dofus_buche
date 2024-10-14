import pyautogui
import time
import win32api
import time
from config import *
from os import path, listdir
from json_utility import write_json
import json



def click_and_confirme(pos):
    pyautogui.click(x=pos.left,y=pos.top)
    time.sleep(1)
    pyautogui.click(x=pos.left+40, y=pos.top+40)


def click_and_confirme_absolute(pos):
    x, y = pos
    pyautogui.click((x,y))
    time.sleep(1)
    pyautogui.click(x+40, y+40)


# time.sleep(collecte_time[ressource_type])

def detect_click_left():
    state_left = win32api.GetKeyState(0x01)  # Left button up = 0 or 1. Button down = -127 or -128
    while True:
        a = win32api.GetKeyState(0x01)
        if a != state_left:  # Button state changed
            state_left = a
            if a < 0:
                return pyautogui.position()
        time.sleep(0.001)

def detect_escape():
    state_escape = win32api.GetKeyState(0x1B)  # Escape button up = 0 or 1. Button down = -127 or -128
    while True:
        a = win32api.GetKeyState(0x1B)
        if a != state_escape:  # Button state changed
            state_escape = a
            if a < 0:
                return True
        time.sleep(1)


def save_road(name):
    road = []
    state_escape = win32api.GetKeyState(0x1B)  # Escape button up = 0 or 1. Button down = -127 or -128
    try:
    # Handle JSON file reading and writing
        with open(saved_road, 'r+') as file:
            if path.getsize(saved_road) > 0:
                file_data = json.load(file)
            else:
                file_data = {}
    except json.JSONDecodeError:
        file_data = {}
    while True:
        a = win32api.GetKeyState(0x1B)
        if a != state_escape:  # Button state changed
            state_escape = a
            if a < 0:

                new_road = {name: road}
                file_data.update(new_road)

                with open(saved_road, 'w') as file:
                    json.dump(file_data, file, indent=4)

                return True
        time.sleep(0.1)
        road.append(detect_click_left())
        print(road)



def get_pixel_color_on_click():
    """
    This function returns the color of the pixel at the given coordinates.

    Args:
      x (int): The x-coordinate of the pixel.
      y (int): The y-coordinate of the pixel.

    Returns:
      tuple: The color of the pixel at the given coordinates.
    """
    pos = detect_click_left()
    screenshot = pyautogui.screenshot()
    # print(pos.x,pos.y)
    pixel = screenshot.getpixel((pos.x,pos.y))
    return pixel


def get_pixel_color_on_pos(pos):
    """
    This function returns the color of the pixel at the given coordinates.

    Args:
      x (int): The x-coordinate of the pixel.
      y (int): The y-coordinate of the pixel.

    Returns:
      tuple: The color of the pixel at the given coordinates.
    """
    screenshot = pyautogui.screenshot()
    pixel = screenshot.getpixel(pos)
    return pixel




def use_ressource(picture_ressource_path):
    try:
        # image_positions = list(pyautogui.locateAllOnScreen(picture, confidence=0.8))
        # image_positions = list(pyautogui.locateAllOnScreen(picture_ressource_path, region=region_inventory, confidence=0.7))       
        image_positions = list(pyautogui.locateAllOnScreen(picture_ressource_path, confidence=0.85))       
        print(image_positions)
        if not len(image_positions) == 0:
            for box in image_positions[0]:
                print(box)
                pyautogui.doubleClick(box.left,box.top)
    except:
        return None


# def click_on_picture(picture,zone=(0,0,1920,1080)):
def click_on_picture(picture):
    # try:
        image_positions = list(pyautogui.locateAllOnScreen(picture, confidence=0.8))
        # image_positions = list(pyautogui.locateAllOnScreen(picture, region=zone, confidence=0.85))       
        # print(image_positions)
        if not len(image_positions) == 0:
            for box in image_positions:
                print(box.left, box.top)
                pyautogui.click(box.left+5,box.top+5)

def click_on_picture_once(picture):
    # try:
        image_positions = list(pyautogui.locateAllOnScreen(picture, confidence=0.8))
        # image_positions = list(pyautogui.locateAllOnScreen(picture, region=zone, confidence=0.85))       
        # print(image_positions)
        if not len(image_positions) == 0:
            for box in image_positions:
                print(box.left, box.top)
                pyautogui.doubleClick(box.left+5,box.top+5)
                return 'done'
    # except:
    #     return None



# dofus_window = get_window('Laestra')
# time.sleep(1)
# click_on_picture(r'C:\Users\apeir\Documents\code\dofus\photo\inventaire_divers_desactivate.png')

# get_screenshot_region()
# print(detect_click_left())
# print(get_pixel_color())
# save_road('open_dd')
# follow_saved_road(Personage.Taz,'key_masters')
# print(get_pixel_color_on_click())