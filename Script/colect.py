from config import *
# from init import *
import pyautogui
import time
import pickle
# from Personage import Player


db = open(files['db_player'], 'rb')
Iro, Lea, Taz, Ket = pickle.load(db)

db.close()

Lea.position=[8,-17]
# def clean(a)
# for i in range(1):
# Iro.get_screenshot_region(regions["windows_dofus"])
# Iro.get_screenshot_region(regions["vie"])
            # 
# Ket.position = [7,-26]
# Ket.deplacem  ent("u")
# for _ in range(3):
#     Iro.deplacement("l")
#     Iro.add_ressource_position_on_map("bois")
#     Iro.collecte_on_know_map("bois")

# Ket.add_ressource_position_on_map("cerminVal, maxVal, minLoc, maxLoc eal")
# Ket.collecte_on_know_map("cereal")
# Iro.position=[20,-25]
# Iro.update_player()
# print(Iro.position)
Lea.deplacement("dlr")
# Iro.add_ressource_position_on_map("bois")
# Iro.collecte_on_know_map("bois")
# Iro.go_brak_bank()
# print(Iro.position)
# get_window(Iro.name)

# Lea.position = [4,-24]
# # print(Lea.position)
# print(Lea.verify_actual_map())
# Lea.deplacement("rrd")
# print(Iro.position[1])
# region=(300,800,1000,50)
# d =[1159,1106]
# pyautogui.click(d[1]-400, d[0]-250)