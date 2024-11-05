import pyautogui
import time
import win32api
from config import *
from os import rename
import keyboard
# from imagehash import average_hash
from PIL import Image
from imagehash import phash
from imagehash import hex_to_hash
from math import sqrt
from json_utility import read_pkl, update_pkl
import json
import logging

pictures = read_pkl(files["pictures_db"])

def make_image_hash(image_path):
    image = Image.open(image_path)
    hash = phash(image)
    image.close()
    return hash

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


def fget_screenshot_region(Perso, region):
        Perso.get_window()
        if Perso.window is not None:
            time.sleep(1)
            width, height = region[2], region[3]
            for left in range(0, width, 50):
                for top in range(0, height, 50):
                    quad_region = (region[0] + left, region[1] + top, 50, 50)
                    quad_screenshot = path.join(directories["map_quad"], f'{left}_{top}.png')
                    pyautogui.screenshot(imageFilename=quad_screenshot, region=quad_region, allScreens=False)


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
        with open(files["saved_road"], 'r+') as file:
            if path.getsize(files["saved_road"]) > 0:
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
                with open(files["saved_road"], 'w') as file:
                    json.dump(file_data, file, indent=4)
                return True
        time.sleep(0.1)
        road.append(detect_click_left())
        print(road)


def get_map_name_picture(Perso):
    # time.sleep(2)
    # screenshot_path = path.join(directories["temp"], f'actual_map.png')
    Perso.get_window()
    if Perso.window is not None:
        screenshot_path = path.join(directories["temp"], f'actual_map_{Perso.name}.png')
        screenshot = pyautogui.screenshot(region=regions["map_name"])
        screenshot.save(screenshot_path)
        return screenshot_path


def find_map_changer(window):
    # Perso.get_window()
    # if Perso.window is not None:
        left = window.left+300
        top = window.top + 35
        width = window.width - 600
        height = window.height -45
        # window.left, screen_height = pyautogui.size()
        # window.left, screen_height = window.width, window.height
        region = {
            "l":(0, 0, width //10, height),
            "r":(width-width//10, 0, width//10,  height),
            "d":(0,height - height//10-210,width, height//10)
        }

        u=(left, top,width, height//10)
        print(region)

        map_changer={"l":(),"r":(),"d":(),"u":()}
        # print(pyautogui.size())
        keyboard.press("a")
        time.sleep(2)
        screenshot_path = path.join(directories['temp'],f'window screenshot.png')
        screenshot = pyautogui.screenshot(screenshot_path, region=(left,top,width, height))
        pyautogui.screenshot(path.join(directories['temp'],f'window_up screenshot.png'), region=(left,top,width, height//10))
        pyautogui.screenshot(path.join(directories['temp'],f'window_down screenshot.png'), region=(left,top+height - height//10-210,width, height//10))
        pyautogui.screenshot(path.join(directories['temp'],f'window_left screenshot.png'), region=(left,top, width//10, height))
        pyautogui.screenshot(path.join(directories['temp'],f'window_right screenshot.png'), region=(left+width-width//10,top, width//10, height))
        keyboard.release("a")
        for direction in region:
            for name, picture in pictures["on_map"]["move"].items():
                if name.startswith("arrow"):
                    try:
                        # image_positions = list(pyautogui.locateAllOnScreen(picture, confidence=0.8))
                        # (image_left, image_top) = pyautogui.locate(picture.path, screenshot_path,region=region[direction], confidence=0.1)       
                        
                        print(f"", picture.path)
                        # (image_left, image_top) = pyautogui.locate(picture.path, screenshot_path, confidence=0.1)       
                        image = pyautogui.locate(picture.path, screenshot_path, region=region[direction], confidence=0.8)       
                        
                        (image_left, image_top) = (image.left ,image.top) 

                        print(f"pos ",image_left, image_top)
                        # image_positions = list(pyautogui.locateOnWindow(picture.path, windows_title, region=region[direction], confidence=0.8))       
                        # image_positions = list(pyautogui.locate(picture.path, region=region[direction], confidence=0.8))       
                        # print(image_positions)
                        map_changer[direction]=(int(image_left+left), int(image_top+75+top))
                        screenshot = pyautogui.screenshot(path.join(directories['temp'],f'{image_left}_{image_top}_screenshot.png'), region=(int(image_left)-50,int(image_top)-50,150,150))
                        break

                            # for box in image_positions:
                                
                                # break
                    except Exception as e :
                        logging.info(f"{name} not found")
                        keyboard.release("a")
                        # print(e)   
        for name, picture in pictures["on_map"]["move"].items():
                if name.startswith("star"):
                    try:
                        # image_positions = list(pyautogui.locateAllOnScreen(picture, confidence=0.8))
                        # (image_left,image_top) = pyautogui.locateOnScreen(picture.path, region=u, confidence=0.8)
                        image = pyautogui.locate(picture.path, screenshot_path,region=u, confidence=0.7)       
                        (image_left, image_top) = (image.left ,image.top) 

                        # print(image_positions)
                        map_changer["u"]=(int(image_left+left), int(image_top+top))
                        screenshot = pyautogui.screenshot(path.join(directories['temp'],f'{image_left}_{image_top}_screenshot.png'), region=(int(image_left)-50,int(image_top)-50,150,150))
                        break
                    except Exception as e :
                        logging.info(f"{name} not found")
                        continue
        return map_changer


def find_actual_map(Perso):
    Perso.get_window()
    if Perso.window is not None:
        file_data=read_pkl(files["map_position_db"])
        map_name_picture =  get_map_name_picture(Perso)
        # time.sleep(1)
        # print(map_name_picture)
        actual_hash = make_image_hash(map_name_picture)
        # print(actual_hash)
        for key, value in file_data.items():
            if 'image_hash' in value:
                if hex_to_hash(value['image_hash']) - actual_hash <= 5:
                    print(f"Image hash found in key: {key}")
                return key
        new_key = str(len(file_data.keys())+1)
        map_changer = find_map_changer(Perso.window)
        # print(map_changer)
        t = { new_key: {
            # "position" :["x","y"],
            "position" :f'{Perso.position}',
            "name":"",
            "picture_path": path.join(directories["map_name"],f'{new_key}.png'),
            "image_hash":f'{actual_hash}',
            "map_changer": map_changer,
            "ressource": {}}}    
        file_data.update(t)
        update_pkl(files["map_position_db"],file_data)

        # rename(map_name_picture, path.join(,f'{key}.png'))
        try:
            rename(map_name_picture, path.join(directories["map_name"],f'{new_key}.png'))
        except:
            rename(map_name_picture, path.join(directories["map_name"],f'{new_key}bis.png'))
        return new_key
    
def confirme_changement_map(timeout=15):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(files["map_loading_picture"], confidence=0.8)
            if location:
                return True
        except Exception as e:
            continue
        time.sleep(0.1)
    return False


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
    return(pos.x,pos.y)
    
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
    screenshot_path = path.join(directories["temp"], f'{key}.png')
    screenshot = pyautogui.screenshot(region=regions["map_name"])
    screenshot.save(screenshot_path)
    return screenshot_path
    
      tuple: The color of the pixel at the given coordinates.
    """
    screenshot = pyautogui.screenshot()
    pixel = screenshot.getpixel(pos)
    return pixel

def detect_pixel_change_color_on_x(Perso,region):
    Perso.get_window()
    if Perso.window is not None:
        time.sleep(1)
        x_change_pos=[]
        screenshot = pyautogui.screenshot(imageFilename=path.join(directories["temp"],'1.png'), region=regions["fight_zone"])
        init_color=get_pixel_color_on_pos((region[0],region[1]))
        print(init_color)
        print(region[0],region[0]+region[2])
        for i in [region[0],region[0]+region[2]]:
            color = screenshot.getpixel((i,region[1]))
            print(color)
            if color!=init_color:
                x_change_pos.append((i,region[1]))
                init_color=color
            i+=1
        return x_change_pos


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
    try:
        image_positions = list(pyautogui.locateAllOnScreen(picture, confidence=0.8))
        # image_positions = list(pyautogui.locateAllOnScreen(picture, region=zone, confidence=0.85))       
        # print(image_positions)
        if not len(image_positions) == 0:
            for box in image_positions:
                print(box.left, box.top)
                pyautogui.doubleClick(box.left+5,box.top+5)
                return 'done'
    except:
        return None


def calcule_distance(A,B):
    return int(sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2))


def remove_closest_point():
# # Handle JSON file reading and writing
    file_data=read_pkl(files["map_position_db"])
    keys = list(file_data.keys())
    for key in keys:
        ressource_types = list(file_data[key]["ressource"].keys())
        if len(ressource_types)!=0:
            for ressource_type in ressource_types:
                checked = []
                temp=file_data[key]["ressource"][ressource_type]
                # print(file_data[key]["ressource"][ressource_type])
                for Point in temp:
                    checked.append(Point)
                    temp.remove(Point)                
                    for Second_point in temp:
                        if calcule_distance(Point, Second_point)<2000:
                            file_data[key]["ressource"][ressource_type].remove(Second_point)
    file_data.update()
    update_pkl(files["map_position_db"],file_data)
          

def calculate_path(actual_position, destination):
    distance_x =  sqrt((destination[0]-actual_position[0])**2)
    distance_y =  sqrt((destination[1]-actual_position[1])**2)
    if destination[0]<actual_position[0]:
        distance_x*=-1
    if destination[1]>actual_position[1]:
        distance_y*=-1
    return (distance_x,distance_y)
# def deplacement(chemin):
#     for e in chemin:
#         change_map(e)
#         time.sleep(6)
#         # start_time = actual_time = time.time()

        # while actual_time-start_time<5:
            # image_positions = list(pyautogui.locateAllOnScreen(files["map_loading_picture"], confidence=0.8))
            # if len(image_positions)!=0:
                # print("map have changed")
                # break
            # actual_time=time.time()
                        # time.sleep(1)
        # return "le deplacement n'as pas eu lieu"
        # print("cooldown over")
#