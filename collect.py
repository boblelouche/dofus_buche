from config import files
import pickle

# from Personage import Player
from Script.Player import WindowNotFoundException
import logging

logging.basicConfig(level=logging.DEBUG)
db = open(files["db_player"], "rb")
[anonway] = pickle.load(db)

db.close()
anonway.position = [2, -2]
# def clean(a)a
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
# try:
anonway.deplacement("u")
# except WindowNotFoundException as e:
# print(e)

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
