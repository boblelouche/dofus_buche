from config import *
# from init import *
# import pyautogui
import pickle
# from Personage import *

# Iro.alamano("bois")
with open('C:\\Users\\apeir\\Documents\\code\\dofus\\players.pkl', 'rb') as f:
    Iro, Lea, Taz = pickle.load(f)

Iro.position = ["5","7"]

Iro.add_ressource_position_on_map("bois")
# Iro.go_brak_bank()
# print(Iro.position)
# get_window(Iro.name)

# d =[1159,1106]
# pyautogui.click(d[1]-400, d[0]-250)