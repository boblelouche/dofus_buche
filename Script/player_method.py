import time
import pyautogui
from config import positions, files, colors, directories
import pandas as pd
from .utility import (
    click_and_confirme_absolute,
    click_on_picture_once,
    click_on_picture,
    get_pixel_color_on_pos,
    get_map_name_picture,
    make_image_hash,
    read_pkl,
    update_pkl,
    confirm_map_change,
)
from imagehash import hex_to_hash
import cv2 as cv
import numpy as np
from pynput.keyboard import Controller
from os import path, rename
import logging
from config import regions
from .window import Window
import Script.ocr as viewer
import sys

keyboard = Controller()
pictures = read_pkl(files["pictures_db"])


def fdetect_pos_on_mini_map(self):
    if self.is_window_inactive():
        self.get_window()
    time.sleep(1)
    # mini_map_screenshot = path.join(directories["temp"], f"{self.name}_mini_map.png")
    mini_map_ocr = path.join(directories["temp"], f"{self.name}_mini_map_ocr.png")
    actual_map_ocr_path_txt = mini_map_ocr.replace(
        path.splitext(mini_map_ocr)[1], ".txt"
    )
    # arrow_pos = pyautogui.locateOnWindow(files["actual_tour"], title=self.Leader.window.title, grayscale=True, region=regions["combat_mini"])
    time.sleep(1)
    pyautogui.moveTo(regions["center_mini_map"])
    time.sleep(1)
    pyautogui.screenshot(
        imageFilename=mini_map_ocr, region=regions["ocr_mini_map"], allScreens=False
    )
    viewer.read_img(mini_map_ocr)
    read_actual_map_ocr_path(self, actual_map_ocr_path_txt)


def read_actual_map_ocr_path(self, actual_map_ocr_path_txt):
    if path.isfile(actual_map_ocr_path_txt):
        try:
            info = open(actual_map_ocr_path_txt, "r")
            # print([info.readline().split(",")[0],info.readline().split(",")[-1]])

            pos = info.readline().split(",")
            # = pos
            # print(info.readline().split(","))
            info.close()
            self.position = [int(pos[0]), int(pos[1])]

        except Exception as e:
            logging.debug(msg=f"la position de {self.name} a cause {e}")

        # info = open(actual_map_ocr_path_txt, "r")
        # # print([info.readline().split(",")[0],info.readline().split(",")[-1]])
        # pos = info.readline().split(",")
        # # = pos
        # # print(info.readline().split(","))
        # info.close()
        # self.Leader.position = [int(pos[0]),int(pos[1])]


def fgo_and_vide_on_brak_bank(Perso):
    Perso.go_brak_bank()
    time.sleep(2)
    Perso.vider_ressource_on_bank()
    time.sleep(1.15)
    if Perso.monture is not None:
        Perso.monture.prendre_ressource_on_dd()
        pyautogui.click(positions["brak_bankier"])
        # cursor.click_on(positions["brak_bankier"])
        time.sleep(1)
        pyautogui.click(
            (positions["brak_bankier"][0] + 10, positions["brak_bankier"][1] + 11)
        )
        # cursor.click_on((positions["brak_bankier"][0]+10,positions["brak_bankier"][1]+11))
        time.sleep(1)
        pyautogui.click(positions["open_chest"])
        # cursor.click_on(positions["open_chest"])
        time.sleep(0.5)
        Perso.vider_ressource_on_bank()


def fgo_brak_bank(Perso):
    if Perso.is_window_inactive():
        Perso.foreground()
    Perso.use_brak_popo()
    time.sleep(3)
    # print(positions_brak_zapi_milice)
    click_and_confirme_absolute(positions["brak_zapi_milice"])
    time.sleep(3)
    pyautogui.click(positions["active_zapy_divers"])
    try:
        click_on_picture(files["zapy_divers_desactivate_picture"])
        time.sleep(1)
    except Exception as e:
        print(e)
        print("already activate")
    click_on_picture(files["zapy_bank"])
    time.sleep(1)
    pyautogui.click(positions["enter_brak_bank"])
    time.sleep(3)
    pyautogui.click(positions["brak_bankier"])
    time.sleep(1)
    pyautogui.click(
        (positions["brak_bankier"][0] + 10, positions["brak_bankier"][1] + 11)
    )
    time.sleep(1)
    pyautogui.click(positions["open_chest"])
    time.sleep(0.5)


def fvider_ressource_on_bank(Perso):
    if Perso.is_window_inactive():
        Perso.foreground()
    # click_on_picture(path.join(pict_folder,"inventaire_ressource_desactivate.png"),region=region_inventory)
    try:
        click_on_picture(files["inventaire_ressource_desactivate.png"])
        time.sleep(2)
    except Exception as e:
        print(e)
        print("divers already activate")
    first_ressource_empty = (
        get_pixel_color_on_pos(positions["first_ressource"])
        == colors["couleur_inventory_no_ressource"]
    )
    second_ressource_empty = (
        get_pixel_color_on_pos(positions["second_ressource"])
        == colors["couleur_inventory_no_ressource"]
    )
    print(first_ressource_empty, second_ressource_empty)
    keyboard.press("ctrl")
    time.sleep(2)
    start_time = time.time()
    while not first_ressource_empty and not second_ressource_empty:
        pyautogui.doubleClick(positions["first_ressource"])
        time.sleep(0.5)
        first_ressource_empty = (
            get_pixel_color_on_pos(positions["first_ressource"])
            == colors["couleur_inventory_no_ressource"]
        )
        second_ressource_empty = (
            get_pixel_color_on_pos(positions["second_ressource"])
            == colors["couleur_inventory_no_ressource"]
        )
        if start_time - time.time() > 300:
            keyboard.release("ctrl")
            return "trop long"
    keyboard.release("ctrl")
    keyboard.press_and_release("escape")
    print(first_ressource_empty, second_ressource_empty)

    Perso.inventory_full = 0
    Perso.update_player()
    return "all done"


def fcheck_map_changer(Perso):
    print("todo")


def fuse_brak_popo(Perso):
    if Perso.is_window_inactive():
        Perso.foreground()
    Perso.detect_inventory_open()
    if Perso.inventory_open != 1:
        keyboard.press_and_release("i")
        time.sleep(2)
    try:
        # click_on_picture(path.join(pict_folder,"inventaire_divers_desactivate.png"),region=region_inventory)
        click_on_picture_once(files["inv_div_des"])
        time.sleep(2)
    except Exception as e:
        print(e)
        print("divers already activate")
    # use_ressource(path.join(ressource_picture_folder, "potion", "brakmar.png"))
    click_on_picture_once(path.join(directories["ressource"], "potion", "brakmar.png"))
    keyboard.press_and_release("escape")
    time.sleep(2)
    Perso.positions = ["-23", "38"]
    Perso.update_player()


def ffind_actual_map(Perso):
    if Perso.is_window_inactive():
        Perso.foreground()
    map_name_picture = get_map_name_picture(Perso)
    # time.sleep(1)
    # print(map_name_picture)
    actual_hash = make_image_hash(map_name_picture)
    # print(actual_hash)
    file_data = read_pkl(files["map_position_db"])
    for key, value in file_data.items():
        if "image_hash" in value:
            if hex_to_hash(value["image_hash"]) - actual_hash <= 5:
                print(f"Image hash found in key: {key}")

                return key
    new_key = str(len(file_data.keys()) + 1)
    # map_changer = find_map_changer(Perso.window)
    # print(map_changer)
    t = {}
    t[new_key] = {
        # "position" :["x","y"],
        "position": f"{Perso.position}",
        "name": "",
        "picture_path": path.join(directories["map_name"], f"{new_key}.png"),
        "image_hash": f"{actual_hash}",
        "map_changer": find_map_changer(Perso.window),
        "ressource": {},
    }
    # file_data.update(t)
    update_pkl(files["map_position_db"], t)

    # rename(map_name_picture, path.join(,f'{key}.png'))
    try:
        rename(map_name_picture, path.join(directories["map_name"], f"{new_key}.png"))
    except Exception as e:
        print(e)
        print("picture already in db")
    return new_key


def find_map_changer(window: Window):
    # Perso.foreground()
    # if Perso.window is not None:
    (left, top, width, height) = window.get_game_bounds()
    if sys.platform != "darwin":
        top = top + 35
        height = height - 35

    region = {
        "l": (0, 0, width // 10, height),
        "r": (width - width // 10, 0, width // 10, height),
        "d": (0, height - height // 10 - window.chat_bar_height, width, height // 10),
    }
    region_u = (left, top, width, height // 10)
    print(region)

    # u = (left, top, width, height // 10)
    map_changer = {"l": (), "r": (), "d": (), "u": ()}
    keyboard.press("a")
    keyboard.release("a")
    time.sleep(2)
    screenshot_path = path.join(directories["temp"], "window_screenshot.png")
    print(screenshot_path)
    print(
        top,
        left,
        width,
        height,
        window.chat_bar_height,
        window.margin_width,
        window.play_box_height,
        window.play_box_width,
    )

    map_width = window.chat_bar_height - 130
    screenshot = pyautogui.screenshot(
        path.join(directories["temp"], "minimap.png"),
        region=(
            left + width // 2 + window.margin_width - map_width // 2 - 130,
            top + height - window.chat_bar_height + 65,
            map_width,
            map_width,
        ),
    )
    screenshot.save(path.join(directories["temp"], "minimap.png"))

    screenshot = pyautogui.screenshot(
        screenshot_path, region=(left, top, width, height)
    )
    screenshot.save(screenshot_path)
    # screenshot = mss().grab(
    #     {"left": left, "top": top, "width": width, "height": height}
    # )
    print(screenshot)
    # screenshot_image = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
    # screenshot_image.save(screenshot_path)
    haystack = cv.imread(screenshot_path)
    screenshotl = haystack[0 : 0 + height - window.chat_bar_height, 0 : 0 + width // 10]
    screenshotd = haystack[
        0 + height - height // 10 - window.chat_bar_height : 0
        + height
        - window.chat_bar_height,
        0 : 0 + width,
    ]
    screenshotr = haystack[
        0 : 0 + height - window.chat_bar_height, 0 + width - width // 10 : 0 + width
    ]
    screenshot_region = {"l": screenshotl, "r": screenshotr, "d": screenshotd}
    cv.imwrite(path.join(directories["temp"], "screenshotl.png"), screenshotl)
    cv.imwrite(path.join(directories["temp"], "screenshotd.png"), screenshotd)
    cv.imwrite(path.join(directories["temp"], "screenshotr.png"), screenshotr)
    for direction in region:
        for name, picture in pictures["on_map"]["move"].items():
            if name.startswith("arrow"):
                try:
                    res = locate_in_picture(screenshot_region[direction], picture.path)
                    i = 0
                    for minVal, maxVal, (min_x, min_y), maxLoc in res:
                        (image_left, image_top) = (
                            region[direction][0] + min_x + left + 15,
                            region[direction][1] + min_y + top + 60,
                        )
                        logging.debug(f"arrow {direction} {image_left} {image_top}")
                        map_changer[direction] = (int(image_left), int(image_top))
                        s = pyautogui.screenshot(
                            path.join(
                                directories["temp"],
                                f"{direction}_{i}_{image_left}_{image_top}_screenshot.png",
                            ),
                            region=(
                                int(image_left) - 50,
                                int(image_top) - 50,
                                150,
                                150,
                            ),
                        )
                        s.save(
                            path.join(
                                directories["temp"],
                                f"{direction}_{i}_{image_left}_{image_top}_screenshot.png",
                            )
                        )
                        i += 1
                    break
                except Exception as e:
                    logging.info(f"{name} not found {e}")
                    keyboard.release("a")
                    # print(e)

    for name, picture in pictures["on_map"]["move"].items():
        if name.startswith("star"):
            try:
                screenshotu = haystack[0 : 0 + height // 10, 0:width]
                cv.imwrite(
                    path.join(directories["temp"], "screenshotu.png"), screenshotu
                )

                # (minVal, maxVal, minLoc, (min_x, min_y)) = locate_in_picture(
                #     screenshotu, picture.path
                # )
                # print("up", map_changer)
                # (image_left, image_top) = (
                #     region["u"][0] + min_x + left + 15,
                #     region["u"][1] + min_y + top + 10,
                # )
                # logging.debug(f"star up {image_left} {image_top}")
                # map_changer["u"] = (int(image_left), int(image_top))

                # s = pyautogui.screenshot(
                #     path.join(
                #         directories["temp"],
                #         f"{image_left}_{image_top}_screenshot.png",
                #     ),
                #     region=(int(image_left) - 50, int(image_top) - 50, 150, 150),
                # )
                # s.save(
                #     path.join(
                #         directories["temp"],
                #         f"{image_left}_{image_top}_screenshot.png",
                #     )
                # )

                res = locate_in_picture(screenshotu, picture.path)
                i = 0
                for minVal, maxVal, minLoc, (min_x, min_y) in res:
                    print(f"Up method {i}")
                    (image_left, image_top) = (
                        region_u[0] + min_x + left + 15,
                        region_u[1] + min_y + top + 10,
                    )
                    logging.debug(f"star up {image_left} {image_top}")
                    map_changer["u"] = (int(image_left), int(image_top))

                    s = pyautogui.screenshot(
                        path.join(
                            directories["temp"],
                            f"u_{i}_{image_left}_{image_top}_screenshot.png",
                        ),
                        region=(int(image_left) - 50, int(image_top) - 50, 150, 150),
                    )
                    s.save(
                        path.join(
                            directories["temp"],
                            f"u_{i}_{image_left}_{image_top}_screenshot.png",
                        )
                    )
                    i += 1
                break
            except Exception as e:
                print(e)
                logging.info(f"{name} not found")
                continue
    return map_changer


def locate_in_picture(haystack, needle_path):
    locate_method = [
        cv.TM_SQDIFF,
        cv.TM_SQDIFF_NORMED,
        cv.TM_CCORR,
        cv.TM_CCORR_NORMED,
        cv.TM_CCOEFF,
        cv.TM_CCOEFF_NORMED,
    ]
    res = []
    minLoc = (None, None)
    for method in locate_method:
        needle = cv.imread(needle_path)
        scGray = cv.cvtColor(np.array(haystack.astype(np.float32)), cv.COLOR_RGB2GRAY)
        needleGray = cv.cvtColor(np.array(needle.astype(np.float32)), cv.COLOR_RGB2GRAY)
        result = cv.matchTemplate(scGray, needleGray, method)
        minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(result)
        print("method",needle_path, method, minVal, maxVal, minLoc, maxLoc)
        # pyautogui.screenshot()
        res.append((minVal, maxVal, minLoc, maxLoc))
    return res


def fmove_map(Perso, direction):
    # check=None
    if Perso.is_window_inactive():
        Perso.foreground()
    direction_dict = {"u": (1, -1), "d": (1, 1), "r": (0, 1), "l": (0, -1)}
    file_data = {}
    file_data = read_pkl(files["map_position_db"])
    # df = pd.read_csv(files["db_map"], sep=';',  encoding='utf-8', index_col=0)
    for key in file_data:
        if file_data[key]["position"] == Perso.position:
            logging.info("actual position knowed")
            Perso.position = [int(Perso.position[0]), int(Perso.position[1])]
            Perso.actual_map_key = key
            if file_data[Perso.actual_map_key]["map_changer"][direction] == ():
                # print(key, Perso.actual_map_key, Perso.position)
                find_map_changer(Perso.window)
                return "direction move not know"
            else:
                pos = file_data[Perso.actual_map_key]["map_changer"][direction]
                pyautogui.click((pos[0], pos[1]))

                if confirm_map_change(Perso.window):
                    logging.info(f"{Perso.name} move to direction : {direction}")
                    time.sleep(0.5)
                    if direction in direction_dict:
                        index, value = direction_dict[direction]
                        Perso.position[index] = Perso.position[index] + value
                    Perso.update_player()
                    return
                else:
                    logging.warning(
                        f"bad map_changer[{direction}] for map {Perso.actual_map_key}"
                    )
                    return

    logging.info(f"{Perso.position} not in db")
    Perso.actual_map_key = ffind_actual_map(Perso)
    file_data = read_pkl(files["map_position_db"])
    pos = file_data[Perso.actual_map_key]["map_changer"][direction]
    logging.info(f"{pos} will be clicked")
    pyautogui.click((pos[0], pos[1]))

    if confirm_map_change(Perso.window):
        logging.info(f"db_updated {Perso.name} move to direction : {direction}")
        time.sleep(0.5)
        if direction in direction_dict:
            index, value = direction_dict[direction]
            Perso.position[index] = Perso.position[index] + value
        Perso.position = [int(Perso.position[0]), int(Perso.position[1])]
        Perso.update_player()
    else:
        logging.warning(f"bad map_changer[{direction}] for map {Perso.actual_map_key}")
        return
