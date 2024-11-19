from imagehash import phash
from os import rename, remove
from PIL import Image
import pyautogui
import time
from os import path, listdir
import json
from config import directories, regions
from utility import detect_click_left
from Player import Player


def make_image_hash(image_path):
    image = Image.open(image_path)
    hash = phash(image)
    image.close()
    return hash


# windows=(300,800,1000,50)


def fget_screenshot_region_quad(Perso: Player, region, long):
    Perso.foreground()
    if Perso.window is not None:
        width, height = region[2], region[3]
        for left in range(0, width, long):
            for top in range(0, height, long):
                quad_region = (region[0] + left, region[1] + top, long, long)
                quad_screenshot = path.join(
                    directories["map"], "quad", f"{left}_{top}.png"
                )
                pyautogui.screenshot(
                    quad_screenshot,
                    region=quad_region,
                    allScreens=False,
                )
                # pyautogui.screenshot()


# fget_screenshot_region_quad(Iro,regions["window_dofus"],100)


def fget_screenshot_region(Perso, region):
    # Perso.foreground()
    # time.sleep(1)
    # if Perso.window is not None:
    # screenshot_path = path.join(directories["temp"], f'{region[0]}_{region[1]}_{region[2]}_{region[3]}.png')
    screenshot_path = path.join(directories["temp"], f"{region}.png")
    pyautogui.screenshot(
        screenshot_path,
        region=region,
        allScreens=False,
    )
    return screenshot_path


def test_screenshot_region(Perso):
    Perso.foreground()
    time.sleep(1)
    if Perso.window is not None:
        for file in listdir(directories["temp"]):
            remove(path.join(directories["temp"], file))
        for region in regions.keys():
            screenshot_path = fget_screenshot_region(Perso, regions[region])
            nscreenshot_path = screenshot_path.replace(
                f"{regions[region]}.png", f"{region}_{regions[region]}.png"
            )
            rename(screenshot_path, nscreenshot_path)


# test_screenshot_region(Iro)


def compare_picture():
    liste_pict = ["1.png", "1bis.png", "1ter.png", "2.png", "3.png"]
    liste_pict = ["1.png", "1bis.png", "1ter.png", "2.png", "3.png"]
    transformed_list = [path.join(directories["map_name"], file) for file in liste_pict]
    print(transformed_list)
    hasc = {}
    with open("test.json", "r+") as file:
        try:
            if path.getsize("test.json") > 0:
                file_data = json.load(file)
            else:
                file_data = {}
        except json.JSONDecodeError:
            file_data = {}

    temp = transformed_list
    checked = []
    for pict in transformed_list:
        # hasc[path.basename(pict)]={"hash":make_image_hash(pict)}
        hasc[path.basename(pict)] = {"hash": str(make_image_hash(pict))}

    distance = {}
    for Point in temp:
        h = make_image_hash(Point)
        hasc[path.basename(Point)] = {"hash": h}

    for Point in temp:
        temp.remove(Point)
        # for Second_point in temp:
        #     d = hasc[path.basename(Point)]["hash"]-hasc[path.basename(Point)]["hash"]
        #     # print(d)
    #         hasc[path.basename(Point)][path.basename(Second_point)] =int(d)
    # for key, values in hasc.items():
    #     if not key in file_data.keys():
    #         file_data[key]={}
    #     for value in values:
    #         # print(value)
    #         if value in hasc.keys():
    #             file_data[key][value] = hasc[value]
    # for point in transformed_list:
    #     for key, value in file_data[path.basename(Point)].items():
    #         if key == 'hash':
    #             value = str(value)

    # print(hasc)
    # print(file_data)
    # file_data.update()
    # with open("test.json","w+") as file:
    #     json.dump(file_data, file, indent=4)
    # print(type(value), value)
    # print(key, value)
map_cell ={
    (0,0):(910,440),
    (0,1):(972,411),
    (0,3):(1056,361),
    (0,4):(1102,300),
    (0,-2):(870,480),
    (1,0):(960,462),
    (-1,0):(867,410),
    (-1,1):(909,391)
}
xoffset=28
yoffset=28
def get_pos_from_cell(x,y):
    pixel_x = 910 + (x*xoffset + y*yoffset) 
    pixel_y = 440 + (x*xoffset - y*yoffset)
    print(pixel_x,pixel_y)   # grid_positions[(x, y)] = (sqrt(pixel_x**2), sqrt(pixel_y**2))
    return (pixel_x,pixel_y)   # grid_positions[(x, y)] = (sqrt(pixel_x**2), sqrt(pixel_y**2))
# print(detect_click_left())
pyautogui.moveTo(get_pos_from_cell(0,4))