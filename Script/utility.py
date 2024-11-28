import pyautogui
import time
from config import path, directories, regions, files
from PIL import Image
from imagehash import phash
from math import sqrt
from Script.json_utility import read_pkl, update_pkl
import json
import logging
from Script.inputs import wait_for_click, wait_for_esc
from pynput import mouse
from mss import mss
import pytesseract
import cv2
import numpy as np
from models.Window import Window
import Script.ocr as viewer


def make_image_hash(image_path):
    image = Image.open(image_path)
    hash = phash(image)
    image.close()
    return hash


# def image_hash2(image_path):
#     image = Image.open(image_path)
#     return average_hash(image)


def click_and_confirm(pos):
    pyautogui.click(x=pos.left, y=pos.top)
    time.sleep(1)
    pyautogui.click(x=pos.left + 40, y=pos.top + 40)


def click_and_confirme_absolute(pos):
    x, y = pos
    pyautogui.click((x, y))
    time.sleep(1)
    pyautogui.click(x + 40, y + 40)


# time.sleep(collecte_time[ressource_type])


def detect_click_left():
    logging.info("waiting for an click is done")
    return wait_for_click()


def fget_screenshot_region(Perso, region):
    if Perso.is_window_inactive():
        Perso.foreground()
    # time.sleep(1)
    width, height = region[2], region[3]
    for left in range(0, width, 50):
        for top in range(0, height, 50):
            quad_screenshot = path.join(directories["map_quad"], f"{left}_{top}.png")
            mss().save(
                mon=(region[0] + left, region[1] + top, 50, 50), output=quad_screenshot
            )
            # pyautogui.screenshot(
            #     imageFilename=quad_screenshot, region=quad_region, allScreens=False
            # )


def save_road(name: str):
    path = []
    print("save road")

    def on_mouse_click(x, y, button, pressed):
        logging.debug(f"{button} {"Pressed" if pressed else "Released"} at {(x, y)}")
        if pressed:
            path.append((x, y))

    mouse_listener = mouse.Listener(on_click=on_mouse_click)
    mouse_listener.start()

    wait_for_esc()

    road = {
        "name": name,
        "path": path,
    }

    print("road")
    print(road)
    with open(files["saved_road"], "w") as file:
        json.dump(road, file, indent=4)

    print(path)


def get_map_name_picture(Perso):
    # time.sleep(2)
    # screenshot_path = path.join(directories["temp"], f'actual_map.png')
    if Perso.is_window_inactive():
        Perso.foreground()
    screenshot_path = path.join(directories["temp"], f"actual_map_{Perso.name}.png")
    screenshot = pyautogui.screenshot(region=regions["map_name"])
    screenshot.save(screenshot_path)
    return screenshot_path


def confirm_map_change(window: Window, timeout: int = 6):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            viewer
            (left, top, width, height) = window.game_bounds
            screenshot_path = path.join(directories["temp"], "search_load.png")
            # mss().save(output=screenpath)
            screenshot = pyautogui.screenshot(
                screenshot_path,
                region=(left, top, 500, 150),
            )
            screenshot.save(screenshot_path)
            img = cv2.imread(screenshot_path)
            # img = np.array(img.astype(np.float32))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
            print(d)
            location = pyautogui.locate(
                files["map_loading_picture"], screenshot_path, confidence=0.8
            )
            if location:
                return True
        except Exception as e:
            print("Map change not found", e)

        time.sleep(1)
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
    return (pos.x, pos.y)

    pixel = screenshot.getpixel((pos.x, pos.y))
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


def detect_pixel_change_color_on_x(Perso, region):
    if Perso.is_window_inactive():
        Perso.foreground()
    time.sleep(1)
    x_change_pos = []
    screenshot = pyautogui.screenshot(
        imageFilename=path.join(directories["temp"], "1.png"),
        region=regions["fight_zone"],
    )
    init_color = get_pixel_color_on_pos((region[0], region[1]))
    print(init_color)
    print(region[0], region[0] + region[2])
    for i in [region[0], region[0] + region[2]]:
        color = screenshot.getpixel((i, region[1]))
        print(color)
        if color != init_color:
            x_change_pos.append((i, region[1]))
            init_color = color
        i += 1
    return x_change_pos


def use_ressource(picture_ressource_path):
    try:
        # image_positions = list(pyautogui.locateAllOnScreen(picture, confidence=0.8))
        # image_positions = list(pyautogui.locateAllOnScreen(picture_ressource_path, region=region_inventory, confidence=0.7))
        image_positions = list(
            pyautogui.locateAllOnScreen(picture_ressource_path, confidence=0.85)
        )
        print(image_positions)
        if not len(image_positions) == 0:
            for box in image_positions[0]:
                print(box)
                pyautogui.doubleClick(box.left, box.top)
    except Exception as e:
        print(e)
        return None


def click_on_picture(picture):
    # try:
    image_positions = list(pyautogui.locateAllOnScreen(picture, confidence=0.8))
    # image_positions = list(pyautogui.locateAllOnScreen(picture, region=zone, confidence=0.85))
    # print(image_positions)
    if not len(image_positions) == 0:
        for box in image_positions:
            print(box.left, box.top)
            pyautogui.click(box.left + 5, box.top + 5)


def click_on_picture_once(picture):
    try:
        image_positions = list(pyautogui.locateAllOnScreen(picture, confidence=0.8))
        # image_positions = list(pyautogui.locateAllOnScreen(picture, region=zone, confidence=0.85))
        # print(image_positions)
        if not len(image_positions) == 0:
            for box in image_positions:
                print(box.left, box.top)
                pyautogui.doubleClick(box.left + 5, box.top + 5)
                return "done"
    except Exception as e:
        print(e)
        return None


def calcule_distance(A, B):
    return int(sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2))


def remove_closest_point():
    # # Handle JSON file reading and writing
    file_data = read_pkl(files["map_position_db"])
    keys = list(file_data.keys())
    for key in keys:
        ressource_types = list(file_data[key]["ressource"].keys())
        if len(ressource_types) != 0:
            for ressource_type in ressource_types:
                checked = []
                temp = file_data[key]["ressource"][ressource_type]
                # print(file_data[key]["ressource"][ressource_type])
                for Point in temp:
                    checked.append(Point)
                    temp.remove(Point)
                    for Second_point in temp:
                        if calcule_distance(Point, Second_point) < 2000:
                            file_data[key]["ressource"][ressource_type].remove(
                                Second_point
                            )
    file_data.update()
    update_pkl(files["map_position_db"], file_data)


def calculate_path(actual_position, destination):
    distance_x = sqrt((destination[0] - actual_position[0]) ** 2)
    distance_y = sqrt((destination[1] - actual_position[1]) ** 2)
    if destination[0] < actual_position[0]:
        distance_x *= -1
    if destination[1] > actual_position[1]:
        distance_y *= -1
    return (distance_x, distance_y)


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
# save_road("toto")
