from os import path, listdir
import pygetwindow as gw
import time 

combat_sound_file = r'C:\Users\apeir\Documents\code\dofus\son\PULSE.mp3'
recolte_time = 10
enu = "Ironamo"
iop = "Laestrea"
version = '1.44.5'



temp_folder=r'C:\Users\apeir\Documents\code\dofus\temp'
pict_folder=r'C:\Users\apeir\Documents\code\dofus\photo'
# screenshot = path.join(temp_folder, f'temp_pict_{0}.png')
map_info_json = r"C:\Users\apeir\Documents\code\dofus\map_info\name.json"
attack_case = path.join(pict_folder,"combat","red_case.png")
full_sac_picture = path.join(pict_folder,'inventaire_plein.png')
full_dd_picture = path.join(pict_folder,'dd_full.png')
ressource_picture_folder = path.join(pict_folder,"ressource")
zap_picture_folder =  path.join(pict_folder,"map","zap")
arrows_picture_folder =  path.join(pict_folder,"map","move")
zap_pictures = [path.join(zap_picture_folder,f) for f in listdir(zap_picture_folder) if f.startswith('zap')]
zap_selector_picture = path.join(zap_picture_folder,"selector_zap.png")
move_arrows = [path.join(arrows_picture_folder,f) for f in listdir(arrows_picture_folder) if f.startswith('arrow')]
move_stars = [path.join(arrows_picture_folder,f) for f in listdir(arrows_picture_folder) if f.startswith('star')]
map_loading_picture= r"C:\Users\apeir\Documents\code\dofus\photo\map_loading.png"
couleur_inventory_full = (255, 102, 0)
couleur_inventory_empty = (0, 0, 0)
couleur_inventory_no_ressource = (190, 185, 152)
position={
    "inventory_max" : (1329 , 157),
    "inventory_dd_max": (445, 752),
    "brak_zapi_milice" : (1305, 258),
    "active_zapy_divers" : (887, 166),
    "enter_brak_bank": (1150, 263),
    "brak_bankier": (1140, 360),
    "open_chest":(564 ,465),
    "bank_ressource":(1368,249),
    "first_ressource":(1312, 344),
    "second_ressource":(1312, 344),
    "first_ressource_dd":(1308, 341),
    "second_ressource_dd":(1362, 342),
    "third_ressource_dd":(1412, 342)
}
saved_road=r"C:\Users\apeir\Documents\code\dofus\map_info\saved_road.json"
zapy_divers_desactivate_picture = path.join(pict_folder,'zapy_Divers_desactivate.png')
zapy_arene = path.join(pict_folder,'zapy_arene.png')
zapy_bank = path.join(pict_folder,'zapy_bank.png')
bombu_harvest_from_up =  "dddddddddll"
bombu_harvest_from_down ="rruuuuuuuuu"
frene_harvest = "lluuurrrddrurddll"
region_inventory = (1300,100,300,700)
region_teste_inventory = (700,50,220,55)

liste_colecte_bois = ["erable", "bombu","oliv","mchene","mnoyer","mchat","mfrene"]
# liste_colecte_ = ["bombu"]
liste_colecte_minerai = ["fer"]

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