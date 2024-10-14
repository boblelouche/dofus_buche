import pyautogui
import time
import time
from config import *
import keyboard
from os import path, listdir
from json_utility import write_json
import json
from utility import *



class Monture:
    def __init__(self, pers, Pods, effect, lvl):
        self.pers = pers
        self.Pods = Pods
        self.effect = effect
        self.lvl = lvl
        self.dd_full = 0 
        self.inventory_open = 0


    def open_inventory(self):
        dofus_window = get_window(self.pers.name)
        if dofus_window is not None:
            keyboard.press_and_release("escape")
            time.sleep(0.5)            
            keyboard.press_and_release("escape")            
            with open(r"C:\Users\apeir\Documents\code\dofus\map_info\saved_road.json", 'r') as file:
                data = json.load(file)
                # print(data[road_name])
                road = data["open_dd"]
                for point in road:
                    pyautogui.click((point[0], point[1]))
                    time.sleep(0.8)
            self.inventory_open = 1
            time.sleep(0.5)

    def remplir_dd(self):
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
        if not self.inventory_open == 1:
            self.open_inventory()
        first_ressource_empty = get_pixel_color_on_pos(position['first_ressource_dd']) == couleur_inventory_no_ressource
        second_ressource_empty = get_pixel_color_on_pos(position['second_ressource_dd'])  == couleur_inventory_no_ressource
        third_ressource_empty = get_pixel_color_on_pos(position['third_ressource_dd'])  == couleur_inventory_no_ressource
        # print(first_ressource_empty, second_ressource_empty )
        dofus_window = get_window(self.pers.name)
        if dofus_window is not None:
            try:    
                click_on_picture(path.join(pict_folder,"inventaire_ressource_desactivate.png"))
                # click_on_picture(path.join(pict_folder,"inventaire_ressource_desactivate.png",region =region_inventory))
                time.sleep(2)
            except:
                print("ressource already activate")  
            keyboard.press('ctrl')
            time.sleep(2)

            start_time = time.time()
            print(first_ressource_empty, second_ressource_empty, third_ressource_empty)
            while not first_ressource_empty or not second_ressource_empty or not third_ressource_empty or self.dd_full==1 :
            # while not first_ressource_empty or not second_ressource_empty :
                print('debut vidage')
                pyautogui.doubleClick(position['first_ressource_dd'])
                self.check_if_dd_is_full()
                time.sleep(0.5)
                first_ressource_empty = get_pixel_color_on_pos(position['first_ressource_dd']) == couleur_inventory_no_ressource
                second_ressource_empty = get_pixel_color_on_pos(position['second_ressource_dd'])  == couleur_inventory_no_ressource
                third_ressource_empty = get_pixel_color_on_pos(position['third_ressource_dd'])  == couleur_inventory_no_ressource
                if start_time-time.time()>200:
                    keyboard.release("ctrl")
                    return 'trop long'
            keyboard.release("ctrl")
            # print(first_ressource_empty, second_ressource_empty )

            # self.dd_full=0
            return "all done"

    def check_if_dd_is_full(self):
        dofus_window = get_window(self.pers.name)
        if dofus_window is not None:
            if not self.inventory_open == 1:
                self.open_inventory()
            screenshot = pyautogui.screenshot()
            if screenshot.getpixel(position['inventory_dd_max']) == couleur_inventory_full:
                self.dd_full = 1
                return "inventaire plein"
            else:
                self.dd_full = 0
            try:
                image_positions = list(pyautogui.locateAllOnScreen(full_dd_picture, confidence=0.85))       
                print(image_positions)
                if not len(image_positions) == 0:
                  self.dd_full=1
                return "inventaire plein"
            except:
                self.dd_full=0
