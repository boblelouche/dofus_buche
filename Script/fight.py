from config import temps_enemy, files, list_pictures
import pyautogui
import time
import keyboard
from math import sqrt

from .utility import click_on_picture_once

active_turn = False


def detect_play_turn():
    return "it s time doing things"


def play_turn(Perso, zone):
    Perso.foreground()
    if Perso.window is not None:
        for enemy in list_pictures[f"{zone}_enemys"]:
            # print(path.join(picture_bois_enemy_folder, enemy))
            try:
                for _ in range(4):
                    keyboard.press_and_release("'")
                    click_on_picture_once(enemy)
                    time.sleep(1)
                keyboard.press_and_release("f1")
                Perso.active_turn = False
                return "end of turn"
            except Exception as e:
                print(e)
                continue


def first_turn(Perso):
    print("todo")


def detect_end_combat(Perso):
    Perso.foreground()
    if Perso.window is not None:
        try:
            image_find = pyautogui.locateAllOnScreen(
                files["picture_txt_end_figth"], confidence=0.85
            )
            if not len(list(image_find)) == 0:
                Perso.in_combat = 1
                # keyboard.press_and_release("escape")
                return 1
            else:
                Perso.in_combat = 0
                keyboard.press_and_release("escape")
                return 0
        except Exception as e:
            print(e)
            Perso.in_combat = 1
            return 1


def fight(Perso):
    while Perso.in_combat == 1:
        play_turn(Perso)
        time.sleep(temps_enemy)
        detect_end_combat(Perso)
    keyboard.press_and_release("escape")
    Perso.in_combat = 0
    return "end of figth"


def detect_enemy(Perso):
    Perso.foreground()
    if Perso.window is not None:
        return []


def convert_coordinates(x, y):
    # Conversion of two orthogonal coordinates between 2 reperes rotated by 45°
    new_x = (x - y) / sqrt(2)
    new_y = (x + y) / sqrt(2)
    return new_x, new_y
