from config import *
import pyautogui
import time 
import keyboard
import cv2 as cv
from os import path, listdir, remove, rename
import numpy as np
from Personage import *
import keyboard
# from init import *
from utility import * 

active_turn = False
picture_bois_enemy_folder = r"C:\Users\apeir\Documents\code\dofus\photo\bois\enemy" 

def detect_play_turn():
    return 'it s time doing things'


def play_turn(Perso):
    dofus_window = get_window(Perso.name)
    # try:
    if dofus_window != None:
        for enemy in listdir(picture_bois_enemy_folder):
            # print(path.join(picture_bois_enemy_folder, enemy))
            try:
                keyboard.press_and_release("'")
                click_on_picture_once(path.join(picture_bois_enemy_folder, enemy))
                time.sleep(1)
                keyboard.press_and_release("'")
                click_on_picture_once(path.join(picture_bois_enemy_folder, enemy))
                time.sleep(1)
                keyboard.press_and_release("'")
                click_on_picture_once(path.join(picture_bois_enemy_folder, enemy))
                time.sleep(1)
                keyboard.press_and_release("'")
                click_on_picture_once(path.join(picture_bois_enemy_folder, enemy))
                time.sleep(1)
                keyboard.press_and_release("f1")
                return 'end of turn'
            except:           
                continue
                print('relou')

def first_turn(Perso):
    print("todo")

def detec_end_combat(Perso):
    dofus_window = get_window(Perso.name)
    # try:
    if dofus_window != None:
        try:
            image_find = pyautogui.locateAllOnScreen(picture_txt_en_figth, confidence=0.90)
            if not len(list(image_find)) ==0:
                Perso.in_combat =1
                # keyboard.press_and_release("escape")
                return 1
            else:
                Perso.in_combat =0
                keyboard.press_and_release("escape")
                return 0
        except:
            Perso.in_combat =1
            return 1

def make_combat(Perso):
    
    while Perso.in_combat ==1:
        play_turn(Perso)
        time.sleep(temps_enemy)
        detec_end_combat(Perso)
    keyboard.press_and_release('escape')
    Perso.in_combat = 0
    return 'end of figth'

# print()
# make_combat(Iro)