import pyautogui
import time
import win32api
from config import *
from os import rename,listdir
# from json_utility import write_json
import json
import keyboard
# from imagehash import average_hash
from PIL import Image
from imagehash import phash
from imagehash import hex_to_hash

def make_image_hash(image_path):
    image = Image.open(image_path)
    hash = phash(image)
    image.close()
    return hash
# print(str(make_image_hash(r"C:\Users\apeir\Documents\code\dofus\temp\actual_map.png")))

# def image_hash2(image_path):
#     image = Image.open(image_path)
#     return average_hash(image)




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

def get_map_name_picture():
    # time.sleep(2)
    screenshot_path = path.join(temp_folder, 'actual_map.png')
    # screenshot_path = path.join(temp_folder, f'actual_map{Perso.name}.png')
    screenshot = pyautogui.screenshot(region=region_map_name)
    screenshot.save(screenshot_path)
    return screenshot_path

def find_map_changer():
    screen_width, screen_height = pyautogui.size()
    region = {
        "l":(screen_width // 10, 0, screen_width // 7, screen_height-250),
        "r":(screen_width-500, 0, screen_width-250, screen_height-250),
        "d":(0, screen_height-400, screen_width, screen_height-250)
    }
    u=(0, 0, screen_width, 150)
    map_changer={"l":(),"r":(),"d":(),"u":()}
    print(pyautogui.size())
    for direction in region:
        for picture in move_arrows:
            try:
                keyboard.press("a")
                time.sleep(2)
                # image_positions = list(pyautogui.locateAllOnScreen(picture, confidence=0.8))
                image_positions = list(pyautogui.locateAllOnScreen(picture, region=region[direction], confidence=0.8))       
                # print(image_positions)
                if not len(image_positions) == 0:
                    for box in image_positions:
                        keyboard.release("a")
                        map_changer[direction]=(int(box.left), int(box.top+75))
                        break
                    break
            except Exception as e :
                keyboard.release("a")
                # print(e)   
    for picture in move_stars:
        try:
            keyboard.press("a")
            time.sleep(2)
            # image_positions = list(pyautogui.locateAllOnScreen(picture, confidence=0.8))
            image_positions = list(pyautogui.locateAllOnScreen(picture, region=u, confidence=0.7))       
            # print(image_positions)
            if not len(image_positions) == 0:
                for box in image_positions:
                    keyboard.release("a")
                    map_changer["u"]=(int(box.left), int(box.top))
                    break
                break
        except Exception as e :
            keyboard.release("a")
            continue
    return map_changer

def find_actual_map(name, actual_position):
    dofus_window = get_window(name)
    if dofus_window is not None:    
        try:
        # Handle JSON file reading and writing
            with open(map_position, 'r+') as file:
                if path.getsize(map_position) > 0:
                    file_data = json.load(file)
                else:
                    file_data = {}
        except json.JSONDecodeError:
            file_data = {}
        map_name_picture =  get_map_name_picture()
        # time.sleep(1)
        # print(map_name_picture)
        actual_hash = make_image_hash(map_name_picture)
        # print(actual_hash)
        keys = list(file_data.keys())
        # for key in keys:
        for key in keys:
            if 'image_hash' in file_data[key]:
                stored_hash = hex_to_hash(file_data[key]['image_hash'])  # Convert the string back to an imagehash object
                if stored_hash == actual_hash:  # Now this comparison should work
                    print(f"Image hash found in key: {key}")
                    return key
        new_key = str(len(keys)+1)
        map_changer = find_map_changer()
        # print(map_changer)
        t = { new_key: {
            # "position" :["x","y"],
            "position" :actual_position,
            "name":"",
            "picture_path": path.join(map_name_picture_folder,f'{new_key}.png'),
            "image_hash":f'{actual_hash}',
            "map_changer": map_changer,
            "ressource": {}}}    
        file_data.update(t)
        with open(map_position, 'w+') as file:
            json.dump(file_data, file, indent=4)
        # rename(map_name_picture, path.join(,f'{key}.png'))
        try:
            rename(map_name_picture, path.join(map_name_picture_folder,f'{new_key}.png'))
        except:
            rename(map_name_picture, path.join(map_name_picture_folder,f'{new_key}bis.png'))

        return new_key


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


def get_pixel_color_on_pos(pos):
    """
    This function returns the color of the pixel at the given coordinates.

    Args:
      x (int): The x-coordinate of the pixel.
      y (int): The y-coordinate of the pixel.

    Returns:
def get_map_info(key):
    screenshot_path = path.join(temp_folder, f'{key}.png')
    screenshot = pyautogui.screenshot(region=region_map_name)
    screenshot.save(screenshot_path)
    return screenshot_path
    
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



# def deplacement(chemin):
#     for e in chemin:
#         change_map(e)
#         time.sleep(6)
#         # start_time = actual_time = time.time()

        # while actual_time-start_time<5:
            # image_positions = list(pyautogui.locateAllOnScreen(map_loading_picture, confidence=0.8))
            # if len(image_positions)!=0:
                # print("map have changed")
                # break
            # actual_time=time.time()
                        # time.sleep(1)
        # return "le deplacement n'as pas eu lieu"
        # print("cooldown over")
# dofus_window = get_window('Laestra')
# time.sleep(1)
# click_on_picture(r'C:\Users\apeir\Documents\code\dofus\photo\inventaire_divers_desactivate.png')
