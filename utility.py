import pyautogui
import time
import win32api
import time
from config import *
import keyboard
import Personage
from os import path, listdir





def detect_full_inventory(personage):
    # global inventory_full
    dofus_window = get_window(personage.name)
    if dofus_window is not None:
        keyboard.press_and_release("i")
        time.sleep(0.5)
        screenshot = pyautogui.screenshot()
        if screenshot.getpixel(position['inventory_max']) == couleur_inventory_full:
            personage.inventory_full = 1
            print("inventaire plein")
        else:
            personage.inventory_full = 0
                     
            print("on peut continuer")
        keyboard.press_and_release("i")
        # return inventory_full
    

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

def get_screenshot_region(personage, region):
    dofus_window = get_window(personage.name)
    if dofus_window is not None:
        time.sleep(1)
        i=0
        # pyautogui.click(position['first_ressource'])
        # time.sleep(2)
        screenshot = path.join(temp_folder,f'screenshot_{i}.png')
        pyautogui.screenshot(imageFilename=screenshot, region=region, allScreens=False)
        

def get_screenshot_first_ressouce(perso):
    get_screenshot_region(perso,(1284,318,43,40))


def detect_click_left():
    state_left = win32api.GetKeyState(0x01)  # Left button up = 0 or 1. Button down = -127 or -128
    while True:
        a = win32api.GetKeyState(0x01)
        if a != state_left:  # Button state changed
            state_left = a
            if a < 0:
                return pyautogui.position()
        time.sleep(0.001)

def save_road(name):
    global saved_road
    road=[]
    while not keyboard.is_pressed('esc'):
        road.append(detect_click_left())
    saved_road[name]=road

save_road('key_masters')


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
    print(pos.x,pos.y)
    pixel = screenshot.getpixel((pos.x,pos.y))
    return pixel

# print(get_pixel_color_on_click())

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

def go_brak_bank(personage):
    dofus_window = get_window(personage.name)
    if dofus_window is not None:
    # use_brak_popo(personage)
    # time.sleep(1)
    # print(position_brak_zapi_milice)
        click_and_confirme_absolute(position["brak_zapi_milice"])
        time.sleep(3)
        pyautogui.click(position["active_zapy_divers"])
        try:
            click_on_picture(zapy_divers_desactivate_picture)
            time.sleep(1)
        except:
            print("already activate")
        click_on_picture(zapy_bank)
        time.sleep(1)
        pyautogui.click(position["enter_brak_bank"])
        time.sleep(3)
        click_and_confirme_absolute(position["brak_bankier"])
        time.sleep(1)
        pyautogui.click(position["open_chest"])
        time.sleep(0.5)


def vider_ressource_on_bank(personage):
    dofus_window = get_window(personage.name)
    if dofus_window is not None:
        keyboard.press('ctrl')

        while not get_pixel_color_on_pos(position['first_ressource']) == couleur_inventory_no_ressource:
            pyautogui.doubleClick(position['first_ressource'])
            time.sleep(0.5)
        keyboard.release("ctrl")
        personage.inventory_full=0
        return "all done"

# vider_ressource_on_bank(Personage.Lea)
    # while not 

    # print(personage.position)

    # print("to do")

def detect_inventory_open(personage):
    dofus_window = get_window(personage.name)
    if dofus_window is not None:
        time.sleep(1)
        try:
            # image_positions = list(pyautogui.locateAllOnScreen(picture, confidence=0.8))
            image_positions = list(pyautogui.locateAllOnScreen(r"./photo/ton inventaire.png", region=region_teste_inventory, confidence=0.7))       
            # print(image_positions)
            if not len(image_positions) == 0:
                personage.inventory_open = 1
            else:
                personage.inventory_open = 0

        except:
            personage.inventory_open = 0
    else:
        return None


def use_brak_popo(personage):
    dofus_window = get_window(personage.name)
    if dofus_window is not None:
        detect_inventory_open(personage)
        if personage.inventory_open !=1:
            keyboard.press_and_release("i")
            time.sleep(1)
        try:    
            click_on_picture(path.join(pict_folder,"inventaire_divers_desactivate.png"))
            time.sleep(0.5)
        except:
            print("divers already activate")    
        # use_ressource(path.join(ressource_picture_folder, "potion", "brakmar.png"))
        click_on_picture(path.join(ressource_picture_folder, "potion", "brakmar.png"))
        personage.position = [-23,38]



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
    # except:
    #     return None
# dofus_window = get_window('Laestra')
# time.sleep(1)
# click_on_picture(r'C:\Users\apeir\Documents\code\dofus\photo\inventaire_divers_desactivate.png')

# get_screenshot_region()
# print(detect_click_left())
# print(get_pixel_color())