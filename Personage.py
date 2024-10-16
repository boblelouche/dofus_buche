import pyautogui
import time
import win32api
import time
from config import *
import keyboard
from os import path, listdir
from json_utility import write_json
import json
from utility import *
from Dd import Monture
import pygame
from combat import *


class Player:
    def __init__(self, name, PA, PM, sort, lvl, position, classe, metier):
        self.PA = PA
        self.PM = PM
        self.name = name
        self.sort = sort
        self.lvl = lvl
        self.position = position
        self.classe = classe
        self.metier = metier
        self.inventory_full = 0
        self.inventory_75 = 0
        self.inventory_open = 0
        # self.dd_full = 0
        self.monture = None
        self.in_combat = 0
        self.collecte_tour = 0 


    def get_screenshot_region(self, region):
        dofus_window = get_window(self.name)
        if dofus_window is not None:
            time.sleep(1)
            i=0
            # pyautogui.click(position['first_ressource'])
            # time.sleep(2)
            screenshot = path.join(temp_folder,f'screenshot_{i}.png')
            pyautogui.screenshot(imageFilename=screenshot, region=region, allScreens=False)
            
    def get_screenshot_first_ressouce(self):
        self.get_screenshot_region((1284,318,43,40))

    def get_position(self):
        print('todo')
    
    
    def detect_combat(self):
        try:
            combat = pyautogui.locateAllOnScreen(attack_case,confidence=0.90)
            if not len(list(combat))==0:
                self.in_combat = 1
                # Initialize the mixer module
                pygame.mixer.init()
                # Load your MP3 file
                pygame.mixer.music.load(combat_sound_file)
                # Play the sound
                pygame.mixer.music.play()
                # Keep the program running long enough to hear the sound
                start_time = time.time()
        # Perform the action for 10 seconds
                while time.time() - start_time < 30:
                # while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                
            # else:
            #   return None
        except:
            return None


    def go_and_vide_on_brak_bank(self):
        self.go_brak_bank()
        time.sleep(2)
        self.vider_ressource_on_bank()
        time.sleep(1.15)
        if self.monture !=None:
            self.monture.prendre_ressource_on_dd()
            pyautogui.click(position["brak_bankier"])
            time.sleep(1)
            pyautogui.click((position["brak_bankier"][0]+10,position["brak_bankier"][1]+11))
            time.sleep(1)
            pyautogui.click(position["open_chest"])
            time.sleep(0.5)
            self.vider_ressource_on_bank()

    def go_brak_bank(self):
        dofus_window = get_window(self.name)
        if dofus_window is not None:
            self.use_brak_popo()
            time.sleep(3)
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
            pyautogui.click(position["brak_bankier"])
            time.sleep(1)
            pyautogui.click((position["brak_bankier"][0]+10,position["brak_bankier"][1]+11))
            time.sleep(1)
            pyautogui.click(position["open_chest"])
            time.sleep(0.5)


    def vider_ressource_on_bank(self):
        dofus_window = get_window(self.name)
        if dofus_window is not None:
            try:    
                # click_on_picture(path.join(pict_folder,"inventaire_ressource_desactivate.png"),region=region_inventory)
                click_on_picture(path.join(pict_folder,"inventaire_ressource_desactivate.png"))
                time.sleep(2)
            except:
                print("divers already activate")  
            first_ressource_empty = get_pixel_color_on_pos(position['first_ressource']) == couleur_inventory_no_ressource
            second_ressource_empty = get_pixel_color_on_pos(position['second_ressource'])  == couleur_inventory_no_ressource
            print(first_ressource_empty, second_ressource_empty )
            keyboard.press('ctrl')
            time.sleep(2)
            start_time = time.time()
            while not first_ressource_empty and not second_ressource_empty:
                pyautogui.doubleClick(position['first_ressource'])
                time.sleep(0.5)
                first_ressource_empty = get_pixel_color_on_pos(position['first_ressource']) == couleur_inventory_no_ressource
                second_ressource_empty = get_pixel_color_on_pos(position['second_ressource'])  == couleur_inventory_no_ressource
                if start_time-time.time()>300:
                    keyboard.release("ctrl")
                    return 'trop long'
            keyboard.release("ctrl")
            keyboard.press_and_release("escape")
            print(first_ressource_empty, second_ressource_empty )

            self.inventory_full=0
            return "all done"

    
    def detect_full_inventory(self):
        # global inventory_full
        dofus_window = get_window(self.name)
        if dofus_window is not None:
            self.detect_inventory_open()
            if self.inventory_open ==0:
                keyboard.press_and_release("i")
                time.sleep(1)
            time.sleep(2)
            screenshot = pyautogui.screenshot()
            # print(screenshot.getpixel(position['inventory_max']))
            pixel = screenshot.getpixel(position['inventory_max'])
            print(pixel)
            if pixel == couleur_inventory_full:
                self.inventory_full = 1
                print("inventaire plein")
            else:
                self.inventory_full = 0
                # pyautogui.locateAllOnScreen(attack_case,confidence=0.90)        
                print("on peut continuer")
            keyboard.press_and_release("i")
            # return inventory_full
    
    def detect_inventory_75(self):
        # global inventory_full
        dofus_window = get_window(self.name)
        if dofus_window is not None:
            self.detect_inventory_open()
            if self.inventory_open ==0:
                keyboard.press_and_release("i")
                time.sleep(1)
            time.sleep(2)
            screenshot = pyautogui.screenshot()
            # print(screenshot.getpixel(position['inventory_max']))
            pixel = screenshot.getpixel(position['inventory_75'])
            print(pixel)
            if pixel == couleur_inventory_full:
                self.inventory_75 = 1
                # print("inventaire plein")
            else:
                self.inventory_75 = 0
                # pyautogui.locateAllOnScreen(attack_case,confidence=0.90)        
                print("on peut continuer")
            keyboard.press_and_release("i")
            # return inventory_full
    

    def detect_inventory_open(self):
        dofus_window = get_window(self.name)
        if dofus_window is not None:
            time.sleep(1)
            try:
                # image_positions = list(pyautogui.locateAllOnScreen(picture, confidence=0.8))
                image_positions = list(pyautogui.locateAllOnScreen(r"./photo/ton inventaire.png", region=region_teste_inventory, confidence=0.7))       
                # print(image_positions)
                if not len(list(image_positions)) == 0:
                    print("inventory detected open")
                    self.inventory_open = 1
                else:
                    print("inventory detected not open")
                    self.inventory_open = 0

            except:
                print("inventory not detected ")
                self.inventory_open = 0
        else:
            return None
    
    
    def test(self):
        if self.inventory_open ==1:
            self.inventory_open =0
        else:
            self.inventory_open =1

    def use_brak_popo(self):
        dofus_window = get_window(self.name)
        if dofus_window is not None:
            self.detect_inventory_open()
            if self.inventory_open !=1:
                keyboard.press_and_release("i")
                time.sleep(2)
            try:    
                # click_on_picture(path.join(pict_folder,"inventaire_divers_desactivate.png"),region=region_inventory)
                click_on_picture_once(path.join(pict_folder,"inventaire_divers_desactivate.png"))
                time.sleep(2)
            except:
                print("divers already activate")    
            # use_ressource(path.join(ressource_picture_folder, "potion", "brakmar.png"))
            click_on_picture_once(path.join(ressource_picture_folder, "potion", "brakmar.png"))
            keyboard.press_and_release('escape')
            time.sleep(2)
            self.position = [-23,38]


    def follow_saved_road(self,road_name):
        dofus_window = get_window(self.name)
        if dofus_window is not None:
            with open(r"C:\Users\apeir\Documents\code\dofus\map_info\saved_road.json", 'r') as file:
                data = json.load(file)
                # print(data[road_name])
                road = data[road_name]
                for point in road:
                    pyautogui.click((point[0], point[1]))
                    time.sleep(5)


    def colecte_on_road(self,chemin):
        for direction in chemin:
            self.alamano("bois")
            self.move_map(direction)


        
    def move_map(self, direction):
        dofus_window = get_window(self.name)
        if dofus_window is not None:
            screen_width, screen_height = pyautogui.size()
            region = {
                "l":(screen_width // 10, 0, screen_width // 7, screen_height-250),
                "r":(screen_width-500, 0, screen_width-250, screen_height-250),
                "u":(0, 0, screen_width, 150),
                "d":(0, screen_height-400, screen_width, screen_height-250)
            }
            print(pyautogui.size())
            i=0
            screenshot = path.join(temp_folder,f'screenshot_{i}.png')
            pyautogui.screenshot(imageFilename=screenshot,region=region[direction])
            print(region[direction])
            if direction =="u":        
                for picture in move_stars:
                    keyboard.press("a")
                    time.sleep(2)
                    try:
                        # image_positions = list(pyautogui.locateAllOnScreen(picture, confidence=0.8))
                        image_positions = list(pyautogui.locateAllOnScreen(picture, region=region[direction], confidence=0.7))       
                        # print(image_positions)
                        if not len(image_positions) == 0:
                            for box in image_positions:
                                keyboard.release("a")
                                pyautogui.click(x = box.left+10, y = box.top+10)
                                return "found on windows"
                    except Exception as e :
                        keyboard.release("a")
                        print(e)
                        continue
            else:       
                for picture in move_arrows:
                    keyboard.press("a")
                    time.sleep(2)
                    try:
                        # image_positions = list(pyautogui.locateAllOnScreen(picture, confidence=0.8))
                        image_positions = list(pyautogui.locateAllOnScreen(picture, region=region[direction], confidence=0.7))       
                        # print(image_positions)
                        if not len(image_positions) == 0:
                            for box in image_positions:
                                keyboard.release("a")
                                pyautogui.click(x = box.left, y = box.top+75)
                                return "found on windows"
                    except Exception as e :
                        keyboard.release("a")
                        print(e)
                        continue
        else:
            raise "window not found"


    def collecte(self, seek_picture):
        try:
            image_positions = list(pyautogui.locateAllOnScreen(seek_picture,confidence=0.85))
    # print(image_positions)
            for box in image_positions:          
                # print(box)            
                # click_and_confirme(box,ressource_name)
                click_and_confirme(box)
                # image_positions.remove(box)
                # time.sleep(harvest_time)
                time.sleep(12)
                self.detect_combat()
                self.collecte_tour+=1
                if self.collecte_tour>=20:
                    self.detect_inventory_75()
                    self.collecte_tour=0
                if self.inventory_75==1:
                    self.detect_full_inventory()
                return 'Récolté'
        except Exception as e:
            return None


    def alamano(self,ressource_type):
        dofus_window = get_window(self.name)
        # try:
        if dofus_window != None:
            i=0
            while i<3:
                for element in liste_colecte_bois:
                    for file in listdir(path.join(pict_folder,ressource_type)): 
                        if file.startswith(element):
                            seek_picture = path.join(pict_folder,ressource_type,file)
                            co = self.collecte(seek_picture)
                            if self.in_combat ==1:
                                make_combat(self)
                            while co!=None :
                                co = self.collecte(seek_picture)
                                time.sleep(0.5)
                                if self.in_combat ==1:
                                    make_combat(self)
                                if self.inventory_full == 1:
                                    if self.monture is None :                            
                                        return self.go_and_vide_on_brak_bank()
                                    else:    
                                        self.monture.remplir_dd()
                                        self.monture.check_if_dd_is_full()
                                        self.detect_full_inventory()
                                        if self.monture.dd_full ==1 and self.inventory_full ==1:
                                            return self.go_and_vide_on_brak_bank()
                                        # print("it's time de ce vider")                           
                        # except Exception as e:
                        #     return 'not found'
            i+=1

    # def detect_full_inventory(self):
    # # global inventory_full
    # dofus_window = get_window(self.name)
    # if dofus_window is not None:
    #     keyboard.press_and_release("i")
    #     time.sleep(0.5)
    #     screenshot = pyautogui.screenshot()
    #     if screenshot.getpixel(position['inventory_max']) == couleur_inventory_full:
    #         self.inventory_full = 1
    #         print("inventaire plein")
    #     else:
    #         self.inventory_full = 0
                     
    #         print("on peut continuer")
    #     keyboard.press_and_release("i")
    #     # return inventory_full
    


# Iro.go_brak_bank()
# time.sleep(2)
# Iro.go_brak_bank()
# Iro.get_screenshot_region(region_inventory)
# print(Iro.monture.remplir_dd())
# print(Iro.monture.check_if_dd_is_full())
# print(Iro.monture.dd_full)