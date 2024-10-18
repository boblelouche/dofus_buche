from os import path, listdir
import pygetwindow as gw
import time 

root=r'C:\Users\apeir\Documents\code\dofus'

combat_sound_file = path.join(root,'son','PULSE.mp3')
harvest_time = 12

version = '1.44.5'

temps_enemy=8

temp_folder=path.join(root,'temp')
pict_folder=path.join(root,'photo')
# screenshot = path.join(temp_folder, f'temp_pict_{0}.png')
map_info_json = path.join(root,'map_info','name.json')
# map_position = path.join(root,'map_info',".json")
map_position = path.join(root,'map_info',"position.json")
map_loading_picture = path.join(pict_folder,'map_loading.png')
attack_case = path.join(pict_folder,"combat","mini_red_case.png")
full_sac_picture = path.join(pict_folder,'inventaire_plein.png')
full_dd_picture = path.join(pict_folder,'dd_full.png')
ressource_picture_folder = path.join(pict_folder,"ressource")
picture_txt_end_figth = path.join(pict_folder,'texte_fin_de_combat.png')
picture_txt_couper = path.join(pict_folder,"couper.png")
zap_picture_folder =  path.join(pict_folder,"map","zap")
arrows_picture_folder =  path.join(pict_folder,"map","move")
enemy_on_this_position_picture = path.join(pict_folder,"niveau.png")
zap_pictures = [path.join(zap_picture_folder,f) for f in listdir(zap_picture_folder) if f.startswith('zap')]
zap_selector_picture = path.join(zap_picture_folder,"selector_zap.png")
move_arrows = [path.join(arrows_picture_folder,f) for f in listdir(arrows_picture_folder) if f.startswith('arrow')]
move_stars = [path.join(arrows_picture_folder,f) for f in listdir(arrows_picture_folder) if f.startswith('star')]
map_loading_picture= path.join(pict_folder,'map_loading.png')
couleur_inventory_full = (255, 102, 0)
couleur_inventory_empty = (0, 0, 0)
couleur_inventory_no_ressource = (190, 185, 152)
db_player = path.join(root,"players.pkl")

position={
    # "inventory_max" : (1320 , 157),
    "inventory_max" : (1190 , 432),
    "inventory_75" : (1165 , 432),
    # "inventory_max" : (190 , 432),
    "inventory_dd_max": (445, 752),
    "brak_zapi_milice" : (1305, 258),
    "active_zapy_divers" : (887, 166),
    "enter_brak_bank": (1150, 263),
    "brak_bankier": (1140, 360),
    "open_chest":(564 ,465),
    "bank_ressource":(1368,249),
    "first_ressource":(1312, 344),
    "second_ressource":(1312, 344),
    "first_ressource_perso_dd":(1308, 341),
    "second_ressource_perso_dd":(1362, 342),
    "third_ressource_perso_dd":(1412, 342),
    "first_ressource_dd":(362, 343),
    "second_ressource_dd":(415, 341),
    "third_ressource_dd":(468, 335)
}
saved_road=path.join(root,'map_info','saved_road.json')
zapy_divers_desactivate_picture = path.join(pict_folder,'zapy_Divers_desactivate.png')
zapy_arene = path.join(pict_folder,'zapy_arene.png')
zapy_bank = path.join(pict_folder,'zapy_bank.png')
bombu_harvest_from_up =  "dddddddddll"
bombu_harvest_from_down ="rruuuuuuuuu"
frene_harvest = "lluuurrrddrurddll"
region_inventory = (1300,100,300,700)
region_teste_inventory = (700,50,220,55)
region_inventory_dd = (320,150,320,620)
region_map_name = (450,60,100,60)
map_name_picture_folder = path.join(pict_folder,'map','name')
# liste_colecte_bois = ["mfrene","erable", "bombu","oliv","mchene","mnoyer","mchat","if"]
liste_colecte_bois = ["mfrene","mchene","mnoyer","mchat"]
# liste_colecte_bois = ["bombu"]
# liste_colecte_minerai = ["fer"]

def get_window(personage):
    dofus_window = gw.getWindowsWithTitle(dofus_window_name(personage))[0]
        # Load the screenshot and the template image
    dofus_window.activate()
    time.sleep(1)
        # Check if the window was found
    if dofus_window:
        return dofus_window
    else:
        return None

def dofus_window_name(personage):
    return f'{personage} - Dofus Retro v{version}'
# print(get_window(enu))