import pickle
import concurrent.futures
from os import path, remove
from shutil import copyfile
import pyautogui
import threading
import time
from imagehash import hex_to_hash
import logging
import Script.ocr as viewer
from config import files, regions, directories
from Script.inputs import wait_for_esc, wait_for_click
import Script.ocr as viewer
import pandas as pd
import ast
from Script.Player import Player

from Script.utility import (
    make_image_hash,
    get_map_name_picture,
    read_pkl,
)


class Dict2Obj(object):
    def __init__(self, dictionary):
        for key in dictionary:
            setattr(self, key, dictionary[key])

    def __repr__(self):
        return "<dict2obj: %s>" % self.__dict__



# def myfun(d):
#   for k, v in d.iteritems():
#     if isinstance(v, dict):
#       d[k] = myfun(v)
#     else:
#       d[k] = f(v)
#   return d
# df_monture = pd.read_csv(files["db_monture_csv"], sep=',',  encoding='utf-8')
df_player = pd.read_csv(files["db_player_csv"], sep=",", encoding="utf-8")
# db = open(files["db_player"], "rb")
# db = pd.read_csv()
# Iro, Lea, Taz, Ket = pickle.load(db)
# Iro = df_player[player.name]["__dict__"]["PA"]

# for player in range(len(df_player.columns)):
# print(ast.literal_eval(df_player[player+1]) )
team = {}
# for perso in range(team) :

#     ast.literal_eval(team[perso][4])
for player in df_player.columns[1:]:
    # team[player] = ast.literal_eval(df_player[pla xxxxxyer][4]).
    # team.append(ast.literal_eval(df_player[player][4]))
    # print(ast.literal_eval(df_player[player][4]))
    # team.append(Dict2Obj(ast.literal_eval(df_player[player][4])))
    team[player] = Dict2Obj(ast.literal_eval(df_player[player][4]))


# Lea = team["Laestra"]
# print(team["Ironamo"].lvl)
# print(team["Ironamo"]["position"])
# print(df_player["Ironamo"].items())
# print(df_player[df_player["Ironamo"]])
# print(df_player["Ironamo"][0:5])
#
class Groupe:
    def __init__(self, Leader: Player, followers: list[Player]):
        self.Leader = Leader
        # self.followers = followers
        self.ended = False
        self.in_fight = False
        self.combat = False
        self.perso_turn = None
        self.Leader_turn = False

    def gfollow(self):
        detec_end = threading.Thread(target=wait_for_esc)
        # folow = threading.Thread(target= follow, args=(self,))
        detec_end.start()
        while not self.ended:
            follow(self)
            # print(self.ended)
            time.sleep(0.1)

    def detect_pos_on_mini_map(self):
        if self.Leader.is_window_inactive():
            self.Leader.get_window()
        time.sleep(1)
        mini_map_screenshot = path.join(
            directories["temp"], f"{self.Leader.name}_mini_map.png"
        )
        mini_map_ocr = path.join(
            directories["temp"], f"{self.Leader.name}_mini_map_ocr.png"
        )
        actual_map_ocr_path_txt = mini_map_ocr.replace(
            path.splitext(mini_map_ocr)[1], ".txt"
        )
        # arrow_pos = pyautogui.locateOnWindow(files["actual_tour"], title=self.Leader.window.title, grayscale=True, region=regions["combat_mini"])
        time.sleep(1)
        pyautogui.moveTo(regions["center_mini_map"])
        time.sleep(1)
        pyautogui.screenshot(
            imageFilename=mini_map_screenshot,
            region=regions["mini_map"],
            allScreens=False,
        )
        pyautogui.screenshot(
            imageFilename=mini_map_ocr,
            region=regions["ocr_mini_map"],
            allScreens=False,
        )
        viewer.read_img(mini_map_ocr)

        info = open(actual_map_ocr_path_txt, "r")
        # print([info.readline().split(",")[0],info.readline().split(",")[-1]])
        pos = info.readline().split(",")
        # = pos
        # print(info.readline().split(","))
        info.close()
        self.Leader.position = [int(pos[0]), int(pos[1])]

    def detect_active_turn(self):
        if self.Leader.is_window_inactive():
            self.Leader.foreground()
        # arrow_pos = pyautogui.locateOnWindow(files["actual_tour"], title=self.Leader.window.title, grayscale=True, region=regions["combat_mini"])
        pyautogui.screenshot(
            imageFilename=path.join(directories["temp"], "testt.png"),
            region=regions["combat_mini"],
            allScreens=False,
        )
        try:
            # arrow_pos = pyautogui.locateOnWindow(files["actual_tour2"], title=self.Leader.window.title, grayscale=True)
            arrow_pos = pyautogui.locateOnScreen(
                files["actual_tour"], confidence=0.75, region=regions["combat_mini"]
            )
            pyautogui.moveTo((int(arrow_pos.left) + 20, int(arrow_pos.top) + 50))
            time.sleep(0.2)
            actual_turn_name_picture_path = path.join(
                directories["temp"], "name_actual_turn.png"
            )
            pyautogui.screenshot(
                imageFilename=actual_turn_name_picture_path,
                region=regions["miniature_name"],
                allScreens=False,
            )
            actual_info_picture_path = path.join(
                directories["temp"], "info_actual_turn.png"
            )
            pyautogui.screenshot(
                imageFilename=actual_info_picture_path,
                region=regions["perso_info"],
                allScreens=False,
            )

            return actual_turn_name_picture_path
        except Exception as e:
            # print(e)
            return None

    def play_turn(self):
        "to do"

    def detect_actual_character(self):
        actual_info_picture_path = path.join(
            directories["temp"], "info_actual_turn.png"
        )

        viewer.read_info_from_actual_turn(actual_info_picture_path)

    def gcombat(self):
        # detec_end = threading.Thread(target=wait_for_esc),args=(self,))
        detec_end = threading.Thread(target=wait_for_esc)
        # folow = threading.Thread(target= follow, args=(self,))
        detec_end.start()
        while not self.ended:
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
            # monitor.submit(wait_for_esc)(self))
            # monitor.submit(routine(self.Leader, self.followers))
            # folow.run()
            # detec_end.run()
            # monitor.submit(routine(self.Leader, self.followers))
            # routine(self.Leader, self.followers)


def detect_change_in_screenshot(Perso):
    # print("analyse changement")
    old_path = path.join(directories["temp"], f"screenshot_old{Perso.name}.png")
    if not path.isfile(old_path):
        # old_path =  path.join(directories["temp"],f'screenshot_old{Perso.name}.png')
        pyautogui.screenshot(
            imageFilename=old_path, region=regions["fight_zone"], allScreens=False
        )
    # else:

    # time.sleep(3)

    screen_path = path.join(directories["temp"], f"screenshot_last{Perso.name}.png")
    pyautogui.screenshot(
        imageFilename=screen_path, region=regions["fight_zone"], allScreens=False
    )
    Perso.variation = make_image_hash(old_path) - make_image_hash(screen_path)
    remove(old_path)
    copyfile(screen_path, old_path)
    return
    # print(diff)


def detect_map_change(Perso):
    if Perso.is_window_inactive():
        Perso.foreground()
    diff = make_image_hash(
        path.join(directories["temp"], f"actual_map_{Perso.name}.png")
    ) - make_image_hash(get_map_name_picture(Perso))
    if diff > 2:
        return True
    else:
        return False

    # print(Perso.actual_map_key)
    # return("bad")
    # arrow_pos = pyautogui.locateOnWindow()


# detect_map_change(Iro)


# Perso.postion = [20,-26]
# print(Perso.find_actual_map())
# Perso.move_map("d")
def detect_click_left_perso(Perso):
    logging.info("waiting for left click")
    (x, y) = wait_for_click()

    Perso.last_click_pos = [x, y]


# print(detect_change_in_screenshot(Perso))
def add_info_to_db():
    read_pkl(files["map_position_db"])


# pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)


def follow(Groupe):
    # Perso.get_window()
    get_map_name_picture(Groupe.Leader)

    # bots.get_window()
    # time.sleep(1)
    # # Perso.update_player()
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        # executor.submit(wait_for_esc)(Groupe))

        #     # for i in range(3):
        #     # processes.append(executor.submit(detect_click_left_perso(Perso),Perso))
        #     # print(processes.append(executor.submit(detect_click_left_perso(Perso),Perso)))
        # while Groupe.ended == False:
        Groupe.Leader.foreground()
        executor.submit(detect_click_left_perso(Groupe.Leader), Groupe.Leader)
        pyautogui.click(
            (Groupe.Leader.last_click_pos[0], Groupe.Leader.last_click_pos[1])
        )
        # time.sleep(0.1)
        for bot in Groupe.followers:
            bot.foreground()
            time.sleep(0.2)
            pyautogui.click(
                (Groupe.Leader.last_click_pos[0], Groupe.Leader.last_click_pos[1])
            )
        Groupe.Leader.foreground()
        # executor.submit(detect_map_change(Groupe.Leader), Groupe.Leader)
        if detect_map_change(Groupe.Leader):
            print("map have change")
        # while cm!=True:
        # time.sleep(0.5)
        # cm=detect_map_change(Perso)
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
# (team['Ironamo'].name)
# allStar = Groupe(team['Ironamo'],[team['Laestra']])
# allStar = Groupe(Iro, Lea)
# allStar.gfollow()
# allStar.detect_pos_on_mini_map()
# print(Iro.position)
# allStar.gcombat()
# allStar.detect_actual_character()
