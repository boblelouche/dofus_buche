import pyautogui
import pickle
import math
import json
import time
from math import sqrt
from config import files, regions, positions

with open(files["db_player"], "rb") as f:
    Iro, Lea, Taz, Ket = pickle.load(f)

# cell_pos = {"[0,0]":(341,50),
#             "[1,0]":(433,50),
#             "[0,1]":(340,100)}

# def make_mark():
#     cell_pos={}


#     # Iro.get_window()
#     for i in range(3):
#         for j in range(3):
#             cell_pos[f'[{i},{j}]']=get_pixel_color_on_click()
#     with open(files["xy_cell"], 'w') as file:
#         json.dump(cell_pos, file, indent=4)
#     # return cell_pos
# write_json(cell_pos,files["xy_cell"],"r")
def make_mark():
    cell_pos = {}
    # Iro.get_window()
    for i in range(20):
        for j in range(20):
            if j % 2 == 0:
                pos = (340 + (100 * i), 40 + (30 * j))
            else:
                pos = (320 + (100 * i), 40 + (40 * j))

            cell_pos[f"[{i},{j}]"] = pos
    with open(files["xy_cell"], "w") as file:
        json.dump(cell_pos, file, indent=4)


def go_on_cell(cell):
    Iro.get_window()
    with open(files["xy_cell"], "r") as file:
        data = json.load(file)
    pyautogui.moveTo((data[cell][0], data[cell][1]))


# go_on_cell("[0,0]")
# print(make_mark())


# if t!="n":
#     continue


def create_rotated_grid_positions(rows, cols, width, height):
    grid_positions = {}
    offset = width / math.sqrt(2)  # Ajustement pour la rotation

    for x in range(cols):
        for y in range(rows):
            # Calcul des coordonnées en pixels avec rotation
            pixel_x = 340 + (x + y) * offset
            pixel_y = 40 + (x - y) * offset
            grid_positions[(x, y)] = (sqrt(pixel_x**2), sqrt(pixel_y**2))

    return grid_positions


# Paramètres de la grille
rows = 5  # Nombre de lignes
cols = 5  # Nombre de colonnes
width = 90  # Largeur de chaque case en pixels
height = 10  # Hauteur de chaque case en pixels (non utilisé ici)


# Créer le dictionnaire des positions
# def verifiy_cell(Perso, cell):
def verifiy_cell(Perso):
    Perso.get_window()
    # positions = create_rotated_grid_positions(rows, cols, width, height)
    # print(positions)

    for key in positions.keys():
        pyautogui.moveTo(positions[key])
        time.sleep(1)


def look_war_zone(Perso):
    interval = 0.5
    Perso.get_window()

    region = regions["fight_zone"]
    for y in range(region[1], int((region[1] + region[3])), 47):
        for x in range(
            region[0], int((region[0] + region[2])) + 1, 94
        ):  # Déplacement horizontal par pas de 5 pixels
            pyautogui.moveTo(x + 50, y + 50)
            time.sleep(interval)


look_war_zone(Iro)
# print(verifiy_cell(Iro,"[2,1]"))
# print(verifiy_cell(Iro))
# print( pyautogui.moveTo(positions[(1,0)]))
# print(get_pixel_color_on_click())
# 1385 608
# print(1478-1385)
# print(731-634)
# 1434 634
