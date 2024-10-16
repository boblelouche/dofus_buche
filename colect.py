import pyautogui
import cv2 as cv
import time 
from os import path, listdir, remove, rename
import numpy as np
from ocr import read_img
# import readline
from json_utility import write_json 
import random
from config import *
# import go_bucheron
from Personage import * 
from utility import *
from init import *
import combat



def collecte(Perso, seek_picture):
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
            Perso.detect_combat()

            return 'Récolté'
    except Exception as e:
        return None



def collecte_all_in_map(Perso,ressource_type, ressource_name): 
    dofus_window = get_window(Perso.name)
    # try:
    if dofus_window != None:
        for file in listdir(path.join(pict_folder,ressource_type)): 
            if file.startswith(ressource_name):
                # print(file)
            # seek = path.join(pict_folder,ressource_type,f'{ressource_name}.png')
                seek_picture = path.join(pict_folder,ressource_type,file)
                # print(seek_picture)
                try:
                    image_positions = list(pyautogui.locateAllOnScreen(seek_picture,confidence=0.85))
                except:
                    image_positions=[]
                    continue
                while len(image_positions)!=0 or not (Perso.monture.dd_full ==1 and Perso.inventory_full ==1) or Perso.in_combat==1:
                    try:
                        image_positions = list(pyautogui.locateAllOnScreen(seek_picture,confidence=0.85))
                # print(image_positions)
                        for box in image_positions:  
                            # print(box)            
                            # click_and_confirme(box,ressource_name)
                            click_and_confirme(box)
                            # image_positions.remove(box)
                            # time.sleep(harvest_time)
                            time.sleep(10)
                            detect_combat(Perso)
                            # if t is not None:
                                # return "combat"
                            Perso.detect_full_inventory()
                            if Perso.inventory_full == 1:
                                if Perso.monture is not None :                            
                                    Perso.monture.vider_ressource_on_dd()
                                    Perso.monture.check_if_dd_is_full()
                                    Perso.detect_full_inventory()
                                    if Perso.monture.dd_full ==1 and Perso.inventory_full ==1:
                                        Perso.go_brak_bank()
                                print("it's time de ce vider")                           
                    except Exception as e:
                        return 'not found'


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
                            # detect_inventory_open(personage)
                            if personage.inventory_full ==1:
                                print("it's time de ce vider")
                except:
                    continue                    
                
                        
            # try:
                # click_on_resssource(seek)
            # except:
# detect_combat()
def harvest_bombu(personage):
    while True:
        # for s in bombu_harvest_from_down:
        #     collecte_all_in_map("bois","bombu")
        #     go_bucheron.deplacement(s)
        for s in bombu_harvest_from_up:
            collecte_all_in_map("bois","bombu", personage)
            deplacement(s)
        for s in bombu_harvest_from_down:
            collecte_all_in_map("bois","bombu", personage)
            deplacement(s)

    
    # while True:


def alamano(Perso,ressource_type):
    dofus_window = get_window(Perso.name)
    # try:
    if dofus_window != None:
        i=0
        while i<3:
            for element in liste_colecte_bois:
                for file in listdir(path.join(pict_folder,ressource_type)): 
                    if file.startswith(element):
                        seek_picture = path.join(pict_folder,ressource_type,file)
                        co = collecte(Perso, seek_picture)
                        if Perso.in_combat ==1:
                            combat.make_combat(Perso)
                        while co!=None :
                            co = collecte(Perso, seek_picture)
                            if Perso.in_combat ==1:
                                combat.make_combat(Perso)
                            Perso.detect_full_inventory()
                            if Perso.inventory_full == 1:
                                if Perso.monture is None :                            
                                   return Perso.go_brak_bank()
                                else:    
                                    Perso.monture.remplir_dd()
                                    Perso.monture.check_if_dd_is_full()
                                    Perso.detect_full_inventory()
                                    if Perso.monture.dd_full ==1 and Perso.inventory_full ==1:
                                        return Perso.go_and_vide_on_brak_bank()
                                    # print("it's time de ce vider")                           
                    # except Exception as e:
                    #     return 'not found'

            # for element in liste_colecte_minerai:
                # collecte_all_in_map('minerai',element)
            i+=1


def harvet_frenne(personage):
    for s in frene_harvest:
        for element in liste_colecte_bois:
        # for element in liste_colecte_minerai:
            collecte_all_in_multy_map('bois',element, personage)
            deplacement(s)
# harvest_bombu()
# harvet_frenne()


# Iro = Personnage("Ironamo", 8, 3, "test", 86, [-23,38], "enutrof", ["bucheron" ,"mineur"])
# couzine = Monture(Iro, 666, "effect", 100)
# Iro.monture = couzine
# Lea = Personnage("Laestra", 6, 3, "test", 52, [-25,17], "iop", ["Bijoutier"])
# Taz = Personnage("Tazmany", 6, 3, "test", 52, [-25,17], "cra", ["Paysan"])

# print(Iro.inventory_full)
# print(Iro.detect_full_inventory())
# print(Iro.inventory_full)''
# 

# print(Iro.monture.remplir_dd())
# Iro.monture.remplir_dd()

# Iro.get_screenshot_region(region_inventory)

# alamano(Iro,"bois")
# vide_on_brak_bank(Iro)
# Iro.go_brak_bank()
# Iro.go_and_vide_on_brak_bank()
# print(Iro.detect_inventory_open())
# print(Iro.inventory_open)
