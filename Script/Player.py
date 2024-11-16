import pyautogui
import time
import keyboard
from os import path, listdir
from .json_utility import update_pkl
import pywinctl as pwc
import pygetwindow as gw
import dill as pickle
import pygame
import json
import logging
from config import (
    files,
    directories,
    colors,
    regions,
    positions,
    version,
    combat_sound_file,
    resource_lists,
)
from .utility import (
    click_and_confirm,
    click_on_picture_once,
    read_pkl
)
from .player_method import(
    fuse_brak_popo,
    fgo_brak_bank,
    fgo_and_vide_on_brak_bank,
    fvider_ressource_on_bank,
    fmove_map,
    ffind_actual_map,
    fdetect_pos_on_mini_map
)
from .fight import fight
class WindowNotFoundException(Exception):
    pass
class Player:
    def __init__(
        self, name, PA, PM, sort, lvl, position, classe, metier, hash_name=None
    ):
        self.window_title = f"{name} - Dofus Retro v{version}"
        self.PA = PA
        self.PM = PM
        self.name = name
        self.sort = sort
        self.lvl = lvl
        self.hash_name = hash_name
        self.position = position
        self.actual_map_key = None
        self.classe = classe
        self.metier = metier
        self.inventory_full = 0
        self.inventory_75 = 0
        self.inventory_open = 0
        # self.dd_full = 0
        self.monture = None
        self.in_combat = 0
        self.collecte_tour = 0
        self.variation = 0
        self.playing_time = False
        # self.window = self.get_window()
        self.window = None
        self.window_resolution = None
        self.last_click_pos = None
        self.color = colors["inventory_empty"]
        # self.is_window_inactive = self.is_window_inactiv()

    def active_player(self):
        try:
            try:
                # implementation
                self.window.activate()
            except Exception as e:
                print(e)
                if e.__class__.__name__ == "PyGetWindowException":
                    # handle exception
                    print("mini pb")
                else:
                    raise e

        except Exception as e:
            print(e)
            print("gros pb")
        

    def is_window_inactive(self):
        active_window= gw.getActiveWindow()
        return active_window is None or self.window is None or active_window.title != self.window_title 

    def get_window(self):
        try:
            self.window = pwc.getWindowsWithTitle(self.window_title)[0]
        except IndexError as e:
            print(e)
            raise WindowNotFoundException()
            
        self.active_player()
        # self.window_resolution = self.window.resolution()
        # 
        logging.info(f"windows of {self.name} activated")

    def logg_player(self):
        dofus_window_lancher = f"Dofus Retro v{version}"
        try:
            dofus_launcher = pwc.getWindowsWithTitle(dofus_window_lancher)[0]
        except IndexError as e:
            print(e)
            # raise
            return "Not launched"
        dofus_launcher.activate()
        dofus_launcher.maximize()

        pyautogui.click((936, 548))
        time.sleep(0.5)
        pyautogui.click((490, 557))
        time.sleep(2)
        pyautogui.click((670, 456))
        time.sleep(2)
        pyautogui.click((490, 557))
        time.sleep(2)
        pyautogui.click((490, 557))
        time.sleep(2)
        pyautogui.doubleClick((490, 557))
        time.sleep(1.5)
        pyautogui.doubleClick((490, 557))
        # pyautogui.click((490,557))

        # self.window = dofus_launcher
        # self.window_resolution = self.window.resolution()
        logging.info(f"{self.name} have been logged")

    def update_player(self):
        f = open(files["db_player"], "rb")
        players = pickle.load(f)
        for i, player in enumerate(players):
            if player.name == self.name:
                players[i] = self
                break
        f.close()
        d = open(files["db_player"], "wb")
        # print(players)
        # players.update()
        pickle.dump(players, d)
        d.close()
    def detect_pos_on_mini_map(self):
        fdetect_pos_on_mini_map(self)
        
    def go_brak_bank(self):
        fgo_brak_bank(self)

    def go_and_vide_on_brak_bank(self):
        fgo_and_vide_on_brak_bank(self)

    def vider_ressource_on_bank(self):
        fvider_ressource_on_bank(self)

    def get_screenshot_region(self, region):
        if self.is_window_inactive():
            self.get_window()

        # if self.window is not None:
        time.sleep(1)
        # pyautogui.click(position['first_ressource'])
        # time.sleep(2)
        screenshot = path.join(directories["temp"], f"screenshot_{self.name}.png")
        pyautogui.screenshot(imageFilename=screenshot, region=region, allScreens=False)

    def get_screenshot_first_ressouce(self):
        self.get_screenshot_region((1284, 318, 43, 40))

    def detect_combat(self):
        try:
            combat = pyautogui.locateAllOnScreen(files["attack_case"], confidence=0.90)
            if not len(list(combat)) == 0:
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
        except Exception as e:
            print(e)
            return None

    def detect_full_inventory(self):
        # global inventory_full
        if self.is_window_inactive():
            self.get_window()

        self.detect_inventory_open()
        if self.inventory_open == 0:
            keyboard.press_and_release("i")
            time.sleep(1)
        time.sleep(2)
        screenshot = pyautogui.screenshot()
        # print(screenshot.getpixel(position['inventory_max']))
        pixel = screenshot.getpixel(positions["inventory_max"])
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
        if self.is_window_inactive():
            self.get_window()

        self.detect_inventory_open()
        if self.inventory_open == 0:
            keyboard.press_and_release("i")
            time.sleep(1)
        time.sleep(2)
        screenshot = pyautogui.screenshot()
        # print(screenshot.getpixel(position['inventory_max']))
        pixel = screenshot.getpixel(positions["inventory_75"])
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
        if self.is_window_inactive():
            self.get_window()

        time.sleep(1)
        try:
            # image_positions = list(pyautogui.locateAllOnScreen(picture, confidence=0.8))
            image_positions = list(
                pyautogui.locateAllOnScreen(
                    files["ton_inventaire.png"],
                    region=regions["teste_inventory"],
                    confidence=0.7,
                )
            )
            # print(image_positions)
            if not len(list(image_positions)) == 0:
                print("inventory detected open")
                self.inventory_open = 1
                self.update_player()
            else:
                print("inventory detected not open")
                self.inventory_open = 0
                self.update_player()

        except Exception as e:
            print(e)
            print("inventory not detected ")
            self.inventory_open = 0
            self.update_player()

    def test(self):
        if self.inventory_open == 1:
            self.inventory_open = 0
        else:
            self.inventory_open = 1

    def use_brak_popo(self):
        fuse_brak_popo(self)

    def follow_saved_road(self, road_name):
        if self.is_window_inactive():
            self.get_window()

            with open(files["saved_road"], "r") as file:
                data = json.load(file)
                # print(data[road_name])
                road = data[road_name]
                for point in road:
                    pyautogui.click((point[0], point[1]))
                    time.sleep(5)

    def move_map(self, direction):
        return fmove_map(self, direction)


    def find_actual_map(self):
        return ffind_actual_map(self)

    # direction_dict = {"u": (1, -1),"d": (1, 1),"r": (0, 1),"l": (0, -1)}
    # file_data=read_pkl(files["map_position_db"])
    # for key in file_data:
    #     if file_data[key]["position"]==self.position:
    #         logging.info(f"actual position knowed")
    #         self.position = [int(self.position[0]),int(self.position[1])]
    #         self.actual_map_key=key
    #         pos=file_data[self.actual_map_key]["map_changer"][direction]
    #         pyautogui.click((pos[0],pos[1]))
    #         # try:
    #         check = confirme_changement_map()
    #         # except:

    #         if check == True:
    #             logging.info(f"{self.name} move to direction : {direction}")
    #             time.sleep(0.5)
    #             if direction in direction_dict:
    #                 index, value = direction_dict[direction]
    #                 self.position[index] = self.position[index] + value

    #             self.update_player()
    #             return
    #         else:
    #             logging.warning(f"bad map_changer[{direction}] for map {self.actual_map_key}")
    #             return

    # logging.info(f"{self.position} not in db")
    # self.actual_map_key = find_actual_map(self)
    # file_data = read_pkl(files["map_position_db"])
    # pos=file_data[self.actual_map_key]["map_changer"][direction]
    # print(pos)
    # logging.info(f"{pos} will be clicked")
    # pyautogui.click((pos[0],pos[1]))
    # check = confirme_changement_map()
    # if check == True:
    #     logging.info(f"db_updated {self.name} move to direction : {direction}")
    #     time.sleep(0.5)
    #     if direction in direction_dict:
    #         index, value = direction_dict[direction]
    #         self.position[index] = self.position[index] + value
    #     self.position = [int(self.position[0]),int(self.position[1])]
    #     self.update_player()
    # else:
    #     logging.warning(f"bad map_changer[{direction}] for map {self.actual_map_key}")
    #     return

    def deplacement(self, chemin):
        if self.is_window_inactive():
            self.get_window()
        for s in chemin:
            self.move_map(s)

    def collecte(self, seek_picture):
        try:
            image_positions = list(
                pyautogui.locateAllOnScreen(seek_picture, confidence=0.85)
            )
            # print(image_positions)
            for box in image_positions:
                # print(box)
                # click_and_confirm(box,ressource_name)
                click_and_confirm(box)
                # image_positions.remove(box)
                # time.sleep(harvest_time)
                time.sleep(12)
                self.detect_combat()
                self.collecte_tour += 1
                self.update_player()
                if self.collecte_tour >= 20:
                    self.detect_inventory_75()
                    self.collecte_tour = 0
                    self.update_player()
                if self.inventory_75 == 1:
                    self.detect_full_inventory()
                return "Récolté"
        except Exception as e:
            print(e)
            return None

    def alamano(self, ressource_type):
        if self.is_window_inactive():
            self.get_window()

            it = 0
            while it < 3:
                for element in resource_lists[ressource_type]:
                    for file in listdir(
                        path.join(directories["photo"], ressource_type)
                    ):
                        if file.startswith(element):
                            seek_picture = path.join(
                                directories["photo"], ressource_type, file
                            )
                            co = self.collecte(seek_picture)
                            if self.in_combat == 1:
                                fight(self)
                            while co is not None:
                                co = self.collecte(seek_picture)
                                time.sleep(0.5)
                                if self.in_combat == 1:
                                    fight(self)
                                if self.inventory_full == 1:
                                    if self.monture is None:
                                        return self.go_and_vide_on_brak_bank()
                                    else:
                                        self.monture.remplir_dd()
                                        self.monture.check_if_dd_is_full()
                                        self.detect_full_inventory()
                                        if (
                                            self.monture.dd_full == 1
                                            and self.inventory_full == 1
                                        ):
                                            return self.go_and_vide_on_brak_bank()
                                        # print("it's time de ce vider")
                        # except Exception as e:
                        #   print(e)
                        #   return 'not found'
            it += 1

    def add_ressource_position_on_map(self, ressource_type):
        if self.is_window_inactive():
            self.get_window()

            file_data = read_pkl(files["map_position_db"])
            for key in file_data:
                if file_data[key]["position"] == self.position:
                    self.actual_map_key = key
                    try:
                        file_data[key]["ressource"][ressource_type]
                    except Exception as e:
                        print(e)
                        file_data[key]["ressource"][ressource_type] = []

                    for file in listdir(
                        path.join(directories["photo"], ressource_type)
                    ):
                        seek_picture = path.join(
                            directories["photo"], ressource_type, file
                        )
                        try:
                            image_positions = list(
                                pyautogui.locateAllOnScreen(
                                    seek_picture, confidence=0.85
                                )
                            )
                            print(image_positions)
                            for box in image_positions:
                                if (int(box.left), int(box.top)) not in file_data[key][
                                    "ressource"
                                ][ressource_type]:
                                    file_data[key]["ressource"][ressource_type].append(
                                        (int(box.left), int(box.top))
                                    )
                            file_data.update()
                            update_pkl(files["map_position_db"], file_data)
                        except Exception as e:
                            print(e)
                            print(e)

    def collecte_on_know_map(self, ressource_type):
        if self.is_window_inactive():
            self.get_window()

            file_data = read_pkl(files["map_position_db"])
            for key in file_data:
                if file_data[key]["position"] == self.position:
                    self.actual_map_key = key
                    for point in file_data[key]["ressource"][ressource_type]:
                        pyautogui.click((int(point[0]), int(point[1])))
                        time.sleep(0.5)
                        recolte = click_on_picture_once(files["picture_txt_couper"])
                        if recolte is not None:
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
