import pyautogui
import time
from config import *
import keyboard
from os import path, listdir
from json_utility import update_pkl
# from utility import *
import pickle
from Dd import Monture
import pygame
import json
from combat import *
from player_method import *
import logging
logging.basicConfig(level=logging.INFO)

class Player:
    def __init__(self, name, PA, PM, sort, lvl, position, classe, metier):
        self.PA = PA
        self.PM = PM
        self.name = name
        self.sort = sort
        self.lvl = lvl
        self.position = position
        self.actual_map_key= None
        self.classe = classe
        self.metier = metier
        self.inventory_full = 0
        self.inventory_75 = 0
        self.inventory_open = 0
        # self.dd_full = 0
        self.monture = None
        self.in_combat = 0    
        self.collecte_tour = 0 
        # self.window = self.get_window()
        self.window = None
    
    
    def get_window(self):
        dofus_window_name = f'{self.name} - Dofus Retro v{version}'
        dofus_window = gw.getWindowsWithTitle(dofus_window_name)[0]
        dofus_window.activate()
        # time.sleep(0.5)
        if dofus_window: 
            self.window = dofus_window
            logging.info(f"windows of {self.name} activated") 
        else:
            self.window = None 
            raise Exception (f"windows of {self.name} not find")


    def update_player(self):
        with open(files["db_player"], 'rb') as f:
            players = pickle.load(f)
        for i, player in enumerate(players):
            if player.name == self.name:
                players[i] = self
                break
        with open(files["db_player"], 'wb') as f:
            pickle.dump(players, f)

    def go_brak_bank(self):
        fgo_brak_bank(self)


    def go_and_vide_on_brak_bank(self):
        fgo_and_vide_on_brak_bank(self)


    def verify_actual_map(self):
        fverify_actual_map(self)


    def vider_ressource_on_bank(self):
        fvider_ressource_on_bank(self)

    def get_screenshot_region(self, region):
        self.get_window()
        # if self.window is not None:
        time.sleep(1)
        # pyautogui.click(position['first_ressource'])
        # time.sleep(2)
        screenshot = path.join(directories["temp"],f'screenshot_{self.name}.png')
        pyautogui.screenshot(imageFilename=screenshot, region=region, allScreens=False)
        
    def get_screenshot_first_ressouce(self):
        self.get_screenshot_region((1284,318,43,40))

    
    def detect_combat(self):
        try:
            combat = pyautogui.locateAllOnScreen(files["attack_case"],confidence=0.90)
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
                self.update_player()
        # Perform the action for 10 seconds
                while time.time() - start_time < 30:
                # while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)         
            # else:
            #   return None
        except:
            return None

    def detect_full_inventory(self):
        # global inventory_full
        self.get_window()
        if self.window is not None:
            self.detect_inventory_open()
            if self.inventory_open ==0:
                keyboard.press_and_release("i")
                time.sleep(1)
            time.sleep(2)
            screenshot = pyautogui.screenshot()
            # print(screenshot.getpixel(position['inventory_max']))
            pixel = screenshot.getpixel(positions['inventory_max'])
            print(pixel)
            if pixel == colors["inventory_full"]:
                self.inventory_full = 1
                self.update_player()
                print("inventaire plein")
            else:
                self.inventory_full = 0
                self.update_player()
                # pyautogui.locateAllOnScreen(attack_case,confidence=0.90)        
                print("on peut continuer")
            keyboard.press_and_release("i")
            # return inventory_full
    
    def detect_inventory_75(self):
        # global inventory_full
        self.get_window()
        if self.window is not None:
            self.detect_inventory_open()
            if self.inventory_open ==0:
                keyboard.press_and_release("i")
                time.sleep(1)
            time.sleep(2)
            screenshot = pyautogui.screenshot()
            # print(screenshot.getpixel(position['inventory_max']))
            pixel = screenshot.getpixel(positions['inventory_75'])
            print(pixel)
            if pixel == colors["inventory_full"]:
                self.inventory_75 = 1
                self.update_player()
                # print("inventaire plein")
            else:
                self.inventory_75 = 0
                self.update_player()
                # pyautogui.locateAllOnScreen(attack_case,confidence=0.90)        
                print("on peut continuer")
            keyboard.press_and_release("i")
            # return inventory_full
    

    def detect_inventory_open(self):
        self.get_window()
        if self.window is not None:
            time.sleep(1)
            try:
                # image_positions = list(pyautogui.locateAllOnScreen(picture, confidence=0.8))
                image_positions = list(pyautogui.locateAllOnScreen(files["ton_inventaire.png"], region=regions["teste_inventory"], confidence=0.7))       
                # print(image_positions)
                if not len(list(image_positions)) == 0:
                    print("inventory detected open")
                    self.inventory_open = 1
                    self.update_player()
                else:
                    print("inventory detected not open")
                    self.inventory_open = 0
                    self.update_player()

            except:
                print("inventory not detected ")
                self.inventory_open = 0
                self.update_player()
        else:
            return None
    
    
    def test(self):
        if self.inventory_open ==1:
            self.inventory_open =0
        else:
            self.inventory_open =1

    def use_brak_popo(self):
        fuse_brak_popo(self)


    def follow_saved_road(self,road_name):
        self.get_window()
        if self.window is not None:
            with open(files["saved_road"], 'r') as file:
                data = json.load(file)
                # print(data[road_name])
                road = data[road_name]
                for point in road:
                    pyautogui.click((point[0], point[1]))
                    time.sleep(5)


    def move_map(self,direction):
        # check=None
        self.get_window()
        if self.window is not None:
            direction_dict = {"u": (1, -1),"d": (1, 1),"r": (0, 1),"l": (0, -1)}
            file_data=read_pkl(files["map_position_db"])           
            for key in file_data:
                if file_data[key]["position"]==self.position:
                    logging.info(f"actual position knowed")
                    self.position = [int(self.position[0]),int(self.position[1])]
                    self.actual_map_key=key
                    pos=file_data[self.actual_map_key]["map_changer"][direction]
                    pyautogui.click((pos[0],pos[1]))
                    # try:
                    check = confirme_changement_map()
                    # except:

                    if check == True:
                        logging.info(f"{self.name} move to direction : {direction}")
                        time.sleep(0.5)
                        if direction in direction_dict:
                            index, value = direction_dict[direction]
                            self.position[index] = self.position[index] + value
                                                
                        self.update_player()
                        return
                    else:
                        logging.warning(f"bad map_changer[{direction}] for map {self.actual_map_key}")
                        return
            
            logging.info(f"{self.position} not in db")        
            self.actual_map_key = find_actual_map(self)
            file_data = read_pkl(files["map_position_db"])
            pos=file_data[self.actual_map_key]["map_changer"][direction]
            print(pos)
            logging.info(f"{pos} will be clicked")
            pyautogui.click((pos[0],pos[1]))
            check = confirme_changement_map()
            if check == True:
                logging.info(f"db_updated {self.name} move to direction : {direction}")
                time.sleep(0.5)
                if direction in direction_dict:
                    index, value = direction_dict[direction]
                    self.position[index] = self.position[index] + value
                self.position = [int(self.position[0]),int(self.position[1])]
                self.update_player()
            else:
                logging.warning(f"bad map_changer[{direction}] for map {self.actual_map_key}")
                return
    def colecte_on_road(self,chemin):
        for direction in chemin:
            self.get_window()
            if self.window is not None:
                self.alamano("bois")
                self.move_map(direction)
                # time.sleep(2)


    def deplacement(self, chemin):
        self.get_window()
        if self.window is not None:
            for s in chemin :
                self.move_map(s)

        
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
                self.update_player()
                if self.collecte_tour>=20:
                    self.detect_inventory_75()
                    self.collecte_tour=0
                    self.update_player()
                if self.inventory_75==1:
                    self.detect_full_inventory()
                return 'Récolté'
        except Exception as e:
            return None


    def alamano(self,ressource_type):
        self.get_window()
        if self.window is not None:
            it=0
            while it<3:
                for element in resource_lists[ressource_type]:
                    for file in listdir(path.join(directories["photo"],ressource_type)): 
                        if file.startswith(element):
                            seek_picture = path.join(directories["photo"],ressource_type,file)
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
            it+=1


    def add_ressource_position_on_map(self,ressource_type):
        self.get_window()
        if self.window is not None:
            file_data=read_pkl(files["map_position_db"])
            for key in file_data:
                if file_data[key]["position"]==self.position:
                    self.actual_map_key=key
                    try:
                        file_data[key]["ressource"][ressource_type]
                    except:
                        file_data[key]["ressource"][ressource_type]=[]

                    for file in listdir(path.join(directories["photo"],ressource_type)):
                        seek_picture= path.join(directories["photo"],ressource_type,file)
                        try:
                            image_positions = list(pyautogui.locateAllOnScreen(seek_picture,confidence=0.85))
                            print(image_positions)
                            for box in image_positions:
                                if not (int(box.left),int(box.top)) in file_data[key]["ressource"][ressource_type]:
                                    file_data[key]["ressource"][ressource_type].append((int(box.left),int(box.top)))
                            file_data.update()
                            update_pkl(files["map_position_db"],file_data)
                        except  Exception as e:
                            print(e)

    def collecte_on_know_map(self,ressource_type):
        self.get_window()
        if self.window is not None:
            file_data=read_pkl(files["map_position_db"])
            for key in file_data:
                if file_data[key]["position"]==self.position:
                    self.actual_map_key=key
                    for point in file_data[key]["ressource"][ressource_type]:
                        pyautogui.click((int(point[0]),int(point[1])))
                        time.sleep(0.5)
                        recolte = click_on_picture_once(files["picture_txt_couper"])
                        if recolte !=None:
                            time.sleep(12)
                        # except:

    
            
            
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