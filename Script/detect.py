import pyautogui
import pygetwindow as gw
import time
from os import path, listdir, remove, rename
from ocr import read_img
from config import files
import json
from json_utility import write_json

recolte_time = 10
dofus_window_name = "Ironamo - Dofus Retro v1.44.2"
temp_folder = r"C:\Users\apeir\Documents\code\dofus\temp"
pict_folder = r"C:\Users\apeir\Documents\code\dofus\photo"
screenshot = path.join(temp_folder, f"temp_pict_{0}.png")
map_info_json = r"C:\Users\apeir\Documents\code\dofus\map_info\name.json"


def clean_temp():
    for file in listdir(temp_folder):
        remove(path.join(temp_folder, file))


clean_temp()


def going_to_map():
    print("dep")


def check_actual_map():
    # Load the screenshot and the template image
    dofus_window = gw.getWindowsWithTitle(dofus_window_name)[0]
    dofus_window.activate()
    time.sleep(1)
    # Check if the window was found
    if dofus_window:
        left = 250
        top = 10
        width = 750
        height = 120
        # dofus_window.activate()
        i = 0
        screenshot_path = path.join(temp_folder, f"temp_actual_map_{i}.png")
        while path.isfile(screenshot_path):
            i += 1
            screenshot_path = path.join(temp_folder, f"temp_actual_map_{i}.png")
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        screenshot.save(screenshot_path)
        read_img(screenshot_path)
        output_file = screenshot_path.replace(path.splitext(screenshot_path)[1], ".txt")
        name = ""
        with open(output_file) as txt_file:
            for line in txt_file.readlines():
                name += line
        if ":" in name:
            name = name.replace(":", "_")
        if "\\" in name:
            name = name.replace("\\", "N")
        if "/" in name:
            name = name.replace("/", "N")
        name = f"{name.replace("\n","")}.txt"
        rename(output_file, output_file.replace(path.basename(output_file), name))
        map_info = check_map_info(name)
        if map_info is not None:
            return map_info
        else:
            new_map_info = {name: {"coord": "", "ressource": []}}
            write_json(
                new_map_info,
                files["name.json"],
                "maps",
            )
            return "the map have been added to db"

        # print(dofus_window.left, dofus_window.top, dofus_window.width, dofus_window.height)


def check_map_info(ocr_find):
    # def check_map_info():
    with open(map_info_json, "r") as map_object:
        map_info = json.load(map_object)
        for map in map_info["maps"]:
            if ocr_find in map.keys():
                return map
        return None


# print(check_map_info("AstrubFortdlAstrub-2Neutre_Coordonnes_1-25re"))
# print(check_map_info("Astrubre_Coordonnes_1-25re"))
# print(check_actual_map())
