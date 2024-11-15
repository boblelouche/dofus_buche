import time
import pyautogui
import json
from config import files, colors, positions
import keyboard
from .utility import get_pixel_color_on_pos, click_on_picture


class Mount:
    def __init__(self, pers, Pods, effect, lvl):
        self.pers = pers
        self.Pods = Pods
        self.effect = effect
        self.lvl = lvl
        self.dd_full = 0
        self.inventory_open = 0

    def open_inventory(self):
        self.pers.get_window()
        if self.pers.window is not None:
            keyboard.press_and_release("escape")
            time.sleep(0.5)
            keyboard.press_and_release("escape")
            with open(files["saved_road"], "r") as file:
                data = json.load(file)
                # print(data[road_name])
                road = data["open_dd"]
                for point in road:
                    pyautogui.click((point[0], point[1]))
                    time.sleep(0.8)
            self.inventory_open = 1
            time.sleep(0.5)

    def remplir_dd(self):
        self.pers.get_window()
        if self.pers.window is not None:
            if not self.inventory_open == 1:
                self.open_inventory()
            self.check_if_dd_is_full()
            if self.dd_full == 1:
                return "dd full"
            self.vider_ressource_on_dd()
            keyboard.press_and_release("escape")
            time.sleep(0.5)
            keyboard.press_and_release("escape")

    def vider_ressource_on_dd(self):
        # print(first_ressource_empty, second_ressource_empty )
        self.pers.get_window()
        if self.pers.window is not None:
            if not self.inventory_open == 1:
                self.open_inventory()
            try:
                click_on_picture(files["inv_res_des"])
                # click_on_picture(files["inv_res_des"],region =region_inventory))
                time.sleep(2)
            except Exception as e:
                print(e)
                print("ressource already activate")
            # first_ressource_empty = get_pixel_color_on_pos(position['first_ressource']) == colors["inventory_no_ressource"]
            second_ressource_empty = (
                get_pixel_color_on_pos(positions["second_ressource_perso_dd"])
                == colors["inventory_no_ressource"]
            )
            third_ressource_empty = (
                get_pixel_color_on_pos(positions["third_ressource_perso_dd"])
                == colors["inventory_no_ressource"]
            )
            keyboard.press("ctrl")
            time.sleep(2)

            start_time = time.time()
            # print(fi second_ressource_empty, third_ressource_empty)
            # while not (second_ressource_empty and third_ressource_empty) or self.dd_full==1 :
            while (
                not (second_ressource_empty and third_ressource_empty)
                or self.dd_full == 1
            ):
                # while not first_ressource_empty or not second_ressource_empty :
                print("debut vidage")
                pyautogui.doubleClick(positions["first_ressource_perso_dd"])
                self.check_if_dd_is_full()
                time.sleep(0.5)
                # first_ressource_empty = get_pixel_color_on_pos(positions['first_ressource_perso_dd']) == colors["inventory_no_ressource"]
                second_ressource_empty = (
                    get_pixel_color_on_pos(positions["second_ressource_perso_dd"])
                    == colors["inventory_no_ressource"]
                )
                third_ressource_empty = (
                    get_pixel_color_on_pos(positions["third_ressource_perso_dd"])
                    == colors["inventory_no_ressource"]
                )
                if start_time - time.time() > 60:
                    keyboard.release("ctrl")
                    return "trop long"
            keyboard.release("ctrl")
            # print(first_ressource_empty, second_ressource_empty )

            # self.dd_full=0
            return "all done"

    def prendre_ressource_on_dd(self):
        self.pers.get_window()
        if self.pers.window is not None:
            if not self.inventory_open == 1:
                self.open_inventory()
            try:
                click_on_picture(files["inv_res_des"])
                # click_on_picture(files["inv_res_des"],region =region_inventory))
                time.sleep(2)
            except Exception as e:
                print(e)
                print("ressource already activate")
            # first_ressource_empty = get_pixel_color_on_pos(positions['first_ressource_dd']) == colors["inventory_no_ressource"]
            second_ressource_empty = (
                get_pixel_color_on_pos(positions["second_ressource_dd"])
                == colors["inventory_no_ressource"]
            )
            third_ressource_empty = (
                get_pixel_color_on_pos(positions["third_ressource_dd"])
                == colors["inventory_no_ressource"]
            )
            # print(first_ressource_empty, second_ressource_empty )
            test = second_ressource_empty and third_ressource_empty
            keyboard.press("ctrl")
            time.sleep(2)
            start_time = time.time()
            # print(first_ressource_empty and second_ressource_empty and third_ressource_empty)
            # print(first_ressource_empty or second_ressource_empty or third_ressource_empty)
            # while not (first_ressource_empty and second_ressource_empty and third_ressource_empty) or self.pers.inventory_full==1 :
            # while  (first_ressource_empty or second_ressource_empty or third_ressource_empty) :
            # print(not second_ressource_empty or not third_ressource_empty)
            while not test:
                # while not first_ressource_empty or not second_ressource_empty :
                print("debut vidage")
                pyautogui.doubleClick(positions["first_ressource_dd"])
                # self.check_if_dd_is_full()
                # self.pers.inventory_full()
                time.sleep(1)
                # first_ressource_empty = get_pixel_color_on_pos(positions['first_ressource_dd']) == colors["inventory_no_ressource"]
                second_ressource_empty = (
                    get_pixel_color_on_pos(positions["second_ressource_dd"])
                    == colors["inventory_no_ressource"]
                )
                third_ressource_empty = (
                    get_pixel_color_on_pos(positions["third_ressource_dd"])
                    == colors["inventory_no_ressource"]
                )
                # print(not second_ressource_empty or not third_ressource_empty)
                test = second_ressource_empty and third_ressource_empty

                print(test)
                if start_time - time.time() > 60:
                    keyboard.release("ctrl")
                    keyboard.press_and_release("escape")
                    time.sleep(0.7)
                    keyboard.press_and_release("escape")
                    return "trop long"
            pyautogui.doubleClick(positions["first_ressource_dd"])
            keyboard.release("ctrl")
            keyboard.press_and_release("escape")
            time.sleep(0.7)
            keyboard.press_and_release("escape")
            # print(first_ressource_empty, second_ressource_empty )

            # self.dd_full=0
            return "all done"

    def check_if_dd_is_full(self):
        self.pers.get_window()
        if self.pers.window is not None:
            if not self.inventory_open == 1:
                self.open_inventory()
            screenshot = pyautogui.screenshot()
            if (
                screenshot.getpixel(positions["inventory_dd_max"])
                == colors["inventory_full"]
            ):
                self.dd_full = 1
                return "inventaire plein"
            else:
                self.dd_full = 0
            try:
                image_positions = list(
                    pyautogui.locateAllOnScreen(
                        files["full_dd_picture"], confidence=0.85
                    )
                )
                print(image_positions)
                if not len(image_positions) == 0:
                    self.dd_full = 1
                return "inventaire plein"
            except Exception as e:
                print(e)
                self.dd_full = 0
