import json_utility
from config import * 
import pickle
import pyautogui 
from json_utility import *
import threading
from utility import * 
from os import remove
from shutil import copyfile
import concurrent.futures
from ocr import *
import PIL

db = open(files['db_player'], 'rb')
Iro, Lea, Taz, Ket = pickle.load(db)
db.close()
print(Iro.hash_name)
# 
class Groupe:
    def __init__(self,Leader, followers):
        self.Leader = Leader
        self.followers = followers
        self.ended = False 
        self.in_fight = False
        self.combat = False
        self.perso_turn = None
        self.Leader_turn = False


    def detect_escape(self):
        print("waiting for escap is pressed")
        state_left = win32api.GetKeyState(0x1B)  # Left button up = 0 or 1. Button down = -127 or -128
        while True:
            a = win32api.GetKeyState(0x1B)
            if a != state_left:  # Button state changed
                state_left = a
                if a < 0:
                    self.ended=True
                    return 
                    # return pyautogui.position()
            time.sleep(0.001)

    def gfollow(self):
        detec_end = threading.Thread(target=self.detect_escape)
        # folow = threading.Thread(target= follow, args=(self,))
        detec_end.start()
        while self.ended == False:
            follow(self)
            # print(self.ended)
            time.sleep(0.1)

    def detect_active_turn(self):
        if self.Leader.window == None or self.Leader.window_activate !=True:
            self.Leader.get_window()
        # arrow_pos = pyautogui.locateOnWindow(files["actual_tour"], title=self.Leader.window.title, grayscale=True, region=regions["combat_mini"])
        pyautogui.screenshot(imageFilename=path.join(directories["temp"],"testt.png"), region=regions["combat_mini"], allScreens=False)
        try:
            # arrow_pos = pyautogui.locateOnWindow(files["actual_tour2"], title=self.Leader.window.title, grayscale=True)
            arrow_pos = pyautogui.locateOnScreen(files["actual_tour"], confidence=0.75,region=regions["combat_mini"])
            pyautogui.moveTo((int(arrow_pos.left)+20, int(arrow_pos.top) +50))
            time.sleep(0.2)
            actual_turn_name_picture_path = path.join(directories["temp"],f"name_actual_turn.png")
            pyautogui.screenshot(imageFilename=actual_turn_name_picture_path, region=regions["miniature_name"], allScreens=False)
            actual_info_picture_path = path.join(directories["temp"],f"info_actual_turn.png")
            pyautogui.screenshot(imageFilename=actual_info_picture_path, region=regions["perso_info"], allScreens=False)

            return actual_turn_name_picture_path
        except Exception as e:
            # print(e)
            return None
    
    def play_turn(self):
        "to do"

    def detect_actual_caract(self):
        actual_info_picture_path = path.join(directories["temp"],f"info_actual_turn.png")

        read_info_from_actual_turn(actual_info_picture_path)

    def gcombat(self):
        # detec_end = threading.Thread(target=detect_escape,args=(self,))
        detec_end = threading.Thread(target=self.detect_escape)
        # folow = threading.Thread(target= follow, args=(self,))
        detec_end.start()
        while self.ended == False:
            player_turn_path = self.detect_active_turn()
            while player_turn_path is None:
                player_turn_path = self.detect_active_turn()            
            hash_namm_active_tour = make_image_hash(player_turn_path)
            # print(hash_namm_active_tour)
            for Player in self.followers:
                if hex_to_hash(Player.hash_name) == hash_namm_active_tour:
                    self.perso_turn = Player
                    # return Player
            if hex_to_hash(self.Leader.hash_name) == hash_namm_active_tour:
                self.Leader_turn = True
                self.perso_turn = self.Leader
                # return self.Leader.name
            time.sleep(1)
            
            
            # time.sleep(0.5)

            # print(self.ended)
            # detec_end.start()
            # time.sleep(1)
            # with concurrent.futures.ThreadPoolExecutor(max_workers=None) as monitor:
                # monitor.submit(detect_escape(self))
                # monitor.submit(routine(self.Leader, self.followers))
            # folow.run()
            # detec_end.run()
                # monitor.submit(routine(self.Leader, self.followers))
            # routine(self.Leader, self.followers)

def detect_change_in_screenshot(Perso):
    # print("analyse changement")
    old_path =  path.join(directories["temp"],f'screenshot_old{Perso.name}.png')
    if not path.isfile(old_path):
        # old_path =  path.join(directories["temp"],f'screenshot_old{Perso.name}.png')
        pyautogui.screenshot(imageFilename= old_path, region=regions['fight_zone'],  allScreens=False)
    # else:

    # time.sleep(3)
    
    screen_path =  path.join(directories["temp"],f'screenshot_last{Perso.name}.png')
    pyautogui.screenshot(imageFilename= screen_path, region=regions['fight_zone'],  allScreens=False)
    Perso.variation = make_image_hash(old_path) - make_image_hash(screen_path)
    remove(old_path)
    copyfile(screen_path, old_path)
    return 
    # print(diff)
     
    
def detect_map_changed(Perso):
    if Perso.window == None or Perso.window_activate !=True:
        Perso.get_window()
    diff = make_image_hash(path.join(directories["temp"], f'actual_map_{Perso.name}.png')) - make_image_hash(get_map_name_picture(Perso))
    if diff >2:
        return True
    else:
        return False
    
    # print(Perso.actual_map_key)
        # return("bad")
    # arrow_pos = pyautogui.locateOnWindow()
# detect_map_changed(Iro)

# Perso.postion = [20,-26]
# print(Perso.find_actual_map())
# Perso.move_map("d")
def detect_click_left_perso(Perso):
    print('waiting for an click is done')
    state_left = win32api.GetKeyState(0x01)  # Left button up = 0 or 1. Button down = -127 or -128
    while True:
        a = win32api.GetKeyState(0x01)
        if a != state_left:  # Button state changed
            state_left = a
            if a < 0:
                pos = pyautogui.position()
                Perso.last_click_pos= [pos.x,pos.y]
                return
                # return pyautogui.position()
        time.sleep(0.001)

# print(detect_change_in_screenshot(Perso))
def add_info_to_db():
    file_data=read_pkl(files["map_position_db"])           
    
# pool = concurrent.futures.ThreadPoolExecutor(max_workers=2) 


def follow(Groupe):
    # Perso.get_window()
    # bots.get_window()
    # time.sleep(1)
    # # Perso.update_player()
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        # executor.submit(detect_escape(Groupe))
        
    #     # for i in range(3):
    #     # processes.append(executor.submit(detect_click_left_perso(Perso),Perso))
    #     # print(processes.append(executor.submit(detect_click_left_perso(Perso),Perso)))
        # while Groupe.ended == False:
            Groupe.Leader.get_window()
            executor.submit(detect_click_left_perso(Groupe.Leader),Groupe.Leader)
            pyautogui.click((Groupe.Leader.last_click_pos[0],Groupe.Leader.last_click_pos[1]))
            # time.sleep(0.1)
            for bot in Groupe.followers:
                bot.get_window()
                time.sleep(0.2)
                pyautogui.click((Groupe.Leader.last_click_pos[0],Groupe.Leader.last_click_pos[1]))
            Groupe.Leader.get_window()
            # executor.submit(detect_map_changed(Groupe.Leader), Groupe.Leader)
            cm=detect_map_changed(Groupe.Leader)
            if cm ==True:
                print("map have change") 
            # while cm!=True:
                # time.sleep(0.5)
                # cm=detect_map_changed(Perso)
                # Perso.update_player()
            
        # print(processes[0].result())
            # executor.submit(detect_change_in_screenshot(Perso),Perso)
            # print(Perso.variation)
        # processes.append(executor.submit(detect_change_in_screenshot(Perso),Perso))
        # print("changement detected")
        # print(type(processes[0].))
            # processes[1]
        # if Perso.variation>=4:
            # print(Perso.last_click_pos)
            # processes.append(executor.submit(detect_change_in_screenshot(Perso),Perso))
    #    parallel_func(Perso)
        # t= pool.submit(print(detect_click_left_perso()))
        # Perso.last_click_pos = pyautogui.position()
        # # print(t)
        # # Perso.update_player()
        # diff =pool.submit(return (f'variaton on {Perso.name} window:{detect_change_in_screenshot(Perso)}'))
        # if int(diff.replace(f'variaton on {Perso.name} window:',''))<=0:
        #     print("no_change")
        # # print(diff)
        # cliked_posion = threading.Thread(target=detect_click_left(), name="cliked_posion" )
        # change_detected= threading.Thread(target= print(detect_change_in_screenshot(Perso)), args=(Perso,),name="change_detected")
        # while :
        #     change_detected= threading.Thread(target= print(detect_change_in_screenshot(Perso)), args=(Perso,),name="change_detected")

# Iro.position=[25,-31]
# Iro.update_player()
# print(Iro.position)
# routine(Iro, [Lea])
# print(Perso.window)
# add_info_to_db()

allStar = Groupe(Iro, [Lea])
# allStar = Groupe(Iro, Lea)
allStar.gfollow()
# allStar.gcombat()
# allStar.detect_actual_caract()