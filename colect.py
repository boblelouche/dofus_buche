import pyautogui
import pygetwindow as gw
import time 
import keyboard
import cv2 as cv
from os import path, listdir, remove, rename
import numpy as np
from ocr import read_img
# import readline
import json
from json_utility import write_json 
import random
import pygame
from config import *
import go_bucheron
import Personage
from utility import *
# collecte_time = {
#     "mchat":11,
#     "mfrene":11,
#     "mnoyer":15
# }


    
def detect_image_in_screenshot(template_path, screenshot_path):    
    cv_reader = cv.imread(screenshot_path)
    template = cv.imread(template_path, 0)
    # Convert the screenshot to grayscale
    gray_screenshot = cv.cvtColor(cv_reader, cv.COLOR_BGR2GRAY)
    # Perform template matching
    res = cv.matchTemplate(gray_screenshot, template, cv.TM_CCOEFF_NORMED)
    # print(res)
    # Set a threshold
    threshold = 0.8   
    # Store the coordinates of matched area in a numpy array
    loc = np.where(res >= threshold)
    # print(loc[::-1][1])
    # # If the image was found, return the top-left corner coordinates
    if len(loc[0]) > 0:
        return loc[::-1]  
    # If the image was not found, return None
    return None


def detect_combat():
    if not len(list(pyautogui.locateAllOnScreen(attack_case,confidence=0.90)))==0:
          # Initialize the mixer module
        pygame.mixer.init()
        # Load your MP3 file
        pygame.mixer.music.load(combat_sound_file)
        # Play the sound
        pygame.mixer.music.play()
        # Keep the program running long enough to hear the sound
        start_time = time.time()

# Perform the action for 10 seconds
        while time.time() - start_time < 50:
        # while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        return 'combat detected'
    else:
          return None



def click_on_resssource(seek_ressource, personage):
    # Use the function to detect the image in the screenshot
    screenshot_path = get_map_info(get_window(personage))
    print(screenshot_path)
    image_position = detect_image_in_screenshot(seek_ressource, screenshot_path)
    # If the image was found, print its position
    if image_position is not None:
        # print(f"Image found at position: {image_position}")
        print(image_position)
        # Get the size of the image
        # time.sleep(1)
        # pyautogui.click('Couper')
        # time.sleep(recolte_time)
    else:
        print("Image not found.")
        # while not path.isfile(path.join(temp_folder,'temp_pict_50')):
    

def collecte(ressource_type, ressource_name):
  
                print('again')


def get_map_info(personage):
    dofus_window = get_window(personage)
    # Check if the window was found
    if dofus_window != None:
        print('windows detected')
        left = 250
        top = 10
        width = 1380
        height = 900
        # dofus_window.activate()
        i=0
        screenshot_path = path.join(temp_folder, f'temp_actual_{i}.png')
        while path.isfile(screenshot_path):
            i+=1
            screenshot_path = path.join(temp_folder, f'temp_actual_{i}.png')
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        screenshot.save(screenshot_path)
        return screenshot_path
    else:
        print('windows not detected')
        return None
    

def collecte_all_in_map(ressource_type, ressource_name, personage): 
    dofus_window = get_window(personage.name)
    # try:
    if dofus_window != None:
        for file in listdir(path.join(pict_folder,ressource_type)): 
            if file.startswith(ressource_name):
            # print(file)
            # seek = path.join(pict_folder,ressource_type,f'{ressource_name}.png')
                seek_picture = path.join(pict_folder,ressource_type,file)
                while True:
                    try:
                        image_positions = list(pyautogui.locateAllOnScreen(seek_picture,confidence=0.8))
                # print(image_positions)
                        for box in image_positions:              
                            click_and_confirme(box,ressource_name)
                            t = detect_combat()
                            if t is not None:
                                print("combat")
                            detect_full_inventory(personage)
                            if personage.inventory_full == 1:
                                print("it's time de ce vider")                           
                    except Exception as e:
                        break 


def collecte_all_in_multy_map(ressource_type, ressource_name, personage): 
    dofus_window = get_window(personage.name)
    if dofus_window != None:
        for file in listdir(path.join(pict_folder,ressource_type)): 
            if file.startswith(ressource_name):
            # print(file)
            # seek = path.join(pict_folder,ressource_type,f'{ressource_name}.png')
                seek_picture = path.join(pict_folder,ressource_type,file)
                try:
                    image_positions = list(pyautogui.locateAllOnScreen(seek_picture,confidence=0.8))
                    while len(image_positions) !=0:
                        image_positions = list(pyautogui.locateAllOnScreen(seek_picture,confidence=0.8))
                    # print(image_positions)
                        for box in image_positions:              
                            click_and_confirme(box,ressource_name)
                            t = detect_combat()
                            if t is not None:
                                print("combat")
                            detect_inventory_open(personage)
                            if personage.inventory_full ==1:
                                print("it's time de ce vider")
                except:
                    continue                    
                
                        
            # try:
                # click_on_resssource(seek)
            # except:
        
# detect_combat()

i = 0

def harvest_bombu(personage):
    while True:
        # for s in bombu_harvest_from_down:
        #     collecte_all_in_map("bois","bombu")
        #     go_bucheron.deplacement(s)
        for s in bombu_harvest_from_up:
            collecte_all_in_map("bois","bombu", personage)
            go_bucheron.deplacement(s)
        for s in bombu_harvest_from_down:
            collecte_all_in_map("bois","bombu", personage)
            go_bucheron.deplacement(s)

    
    # while True:
def alamano(personage):
    i=0
    while i<3:
        for element in liste_colecte_bois:
        # for element in liste_colecte_minerai:
            collecte_all_in_map('bois',element, personage)
            # collecte_all_in_map('minerai',element)
        i+=1


def harvet_frenne(personage):
    for s in frene_harvest:
        for element in liste_colecte_bois:
        # for element in liste_colecte_minerai:
            collecte_all_in_multy_map('bois',element, personage)
            go_bucheron.deplacement(s)
# harvest_bombu()
# harvet_frenne()
# alamano()