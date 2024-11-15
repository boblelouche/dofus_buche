from os import path, getcwd

root = getcwd()
combat_sound_file = path.join(root, "son", "PULSE.mp3")
harvest_time = 12
version = "1.44.5"
temps_enemy = 8


DEPLACEMENT_TIMING_RUN = {"horizontal": 0.3, "vertical": 0.2, "diagonal": 0.2}
DEPLACEMENT_TIMING_WALK = {"horizontal": 0.75, "vertical": 0.5, "diagonal": 0.5}

list_direcories = ["temp", "photo", "ressource", "map_info", "combat"]

# Define directories
directories = {
    "temp": path.join(root, "temp"),
    "photo": path.join(root, "photo"),
    "resource": path.join(root, "resource"),
    "map_info": path.join(root, "map_info"),
    # "combat": path.join(root,'resource','photo', "combat"),
    "combat": path.join(root, "photo", "combat"),
    "ressource": path.join(root, "photo", "ressource"),
    "map": path.join(root, "photo", "on_map"),
    "zap": path.join(root, "photo", "on_map", "zap"),
    "move": path.join(root, "photo", "on_map", "move"),
    "map_name": path.join(root, "photo", "on_map", "name"),
    "enemys_pictures": path.join(root, "photo", "combat", "enemy"),
}
# print(directories.keys())
# Define files
files = {
    # "map_info": path.join(directories["map_info"],'name.json'),
    "map_loading_picture": path.join(directories["photo"], "map_loading.png"),
    "attack_case": path.join(directories["combat"], "mini_red_case.png"),
    "full_sac_picture": path.join(directories["photo"], "inventaire_plein.png"),
    "ton_inventaire": path.join(directories["photo"], "ton inventaire.png"),
    "inv_res_des": path.join(
        directories["photo"], "inventaire_ressource_desactivate.png"
    ),
    "inv_div_des": path.join(directories["photo"], "inventaire_divers_desactivate.png"),
    "full_dd_picture": path.join(directories["photo"], "dd_full.png"),
    "picture_txt_end_figth": path.join(directories["photo"], "texte_fin_de_combat.png"),
    "picture_txt_couper": path.join(directories["photo"], "couper.png"),
    "enemy_on_this_position_picture": path.join(directories["photo"], "niveau.png"),
    "zap_selector_picture": path.join(directories["zap"], "selector_zap.png"),
    "zapy_div_des": path.join(directories["photo"], "zapy_Divers_desactivate.png"),
    "zapy_div_act": path.join(directories["photo"], "zapy_Divers_activate.png"),
    "zapy_arene": path.join(directories["photo"], "zapy_arene.png"),
    "zapy_bank": path.join(directories["photo"], "zapy_bank.png"),
    "actual_tour": path.join(
        directories["combat"], "player_miniature", "actual_tour.png"
    ),
    "actual_tour2": path.join(
        directories["combat"], "player_miniature", "actual_tour2.png"
    ),
    "actual_tour3": path.join(
        directories["combat"], "player_miniature", "actual_tour3.png"
    ),
    "connect": path.join(directories["photo"], "Se connecter.png"),
    "db_player": path.join(root, "players.pkl"),
    "db_player_json": path.join(root, "players.json"),
    "db_player_csv": path.join(root, "players.csv"),
    "db_map_position": path.join(root, "position.json"),
    "db_map": path.join(root, "position.json"),
    "db_monture_csv": path.join(root, "montures.csv"),
    "map_position_db": path.join(directories["map_info"], "position.pkl"),
    "map_position_new_db": path.join(directories["map_info"], "position.json"),
    "pictures_db": path.join(root, "picture_db.pkl"),
    "xy_cell": path.join(directories["map_info"], "xy_cell.json"),
    "saved_road": path.join(directories["map_info"], "saved_road.json"),
    "spells": path.join(directories["resource"], "spells.xml"),
    "recolte": path.join(directories["resource"], "recolte.txt"),
}

# Define colors
colors = {
    "inventory_full": (255, 102, 0),
    "inventory_empty": (0, 0, 0),
    "inventory_no_ressource": (190, 185, 152),
    "combat_empty_cell": [(161, 180, 100), (152, 170, 94)],
}

# Define positions
positions = {
    "inventory_max": (1190, 432),
    "inventory_75": (1165, 432),
    "inventory_dd_max": (445, 752),
    "brak_zapi_milice": (1305, 258),
    "active_zapy_divers": (887, 166),
    "enter_brak_bank": (1150, 263),
    "brak_bankier": (1140, 360),
    "open_chest": (564, 465),
    "bank_ressource": (1368, 249),
    "first_ressource": (1312, 344),
    "second_ressource": (1312, 344),
    "first_ressource_perso_dd": (1308, 341),
    "second_ressource_perso_dd": (1362, 342),
    "third_ressource_perso_dd": (1412, 342),
    "first_ressource_dd": (362, 343),
    "second_ressource_dd": (415, 341),
    "third_ressource_dd": (468, 335),
}

# Define regions
regions = {
    # "exemple":("left","top","width","height"),
    "window_dofus": (299, 19, 1299, 1001),
    "inventory": (1300, 100, 300, 700),
    "teste_inventory": (700, 50, 220, 55),
    "inventory_dd": (320, 150, 320, 620),
    "map_name": (450, 60, 100, 60),
    "combat_mini": (290, 690, 1390, 100),
    "chat": (299, 800, 705, 201),
    "vie_centre": (1000, 790, 80, 80),
    "sort_zone": (1100, 890, 470, 110),
    "perso_info": (1185, 810, 300, 100),
    "miniature_name": (1320, 810, 130, 25),
    "vie": (1320, 810, 130, 25),
    "PA": (1320, 810, 130, 25),
    "PM": (1320, 810, 130, 25),
    "chall_zone": (312, 135, 75, 210),
    "fight_zone": (299, 19, 1299, 800),
}

# Define harvest patterns
harvest_patterns = {
    "bombu_harvest_from_up": "dddddddddll",
    "bombu_harvest_from_down": "rruuuuuuuuu",
    "frene_harvest": "lluuurrrddrurddll",
}

# Define resource lists
resource_lists = {
    "bois": ["mfrene", "mchene", "mnoyer", "mchat", "if"],
    "cereal": ["ble"],
}

# Define pictures
list_pictures = {
    "zap": [
        # path.join(directories["zap"], f)
        # for f in listdir(directories["zap"])
        # if f.startswith("zap")
    ],
    "move_arrows": [
        # path.join(directories["move"], f)
        # for f in listdir(directories["move"])
        # if f.startswith("arrow")
    ],
    "move_stars": [
        # path.join(directories["move"], f)
        # for f in listdir(directories["move"])
        # if f.startswith("star")
    ],
    "bucheron_enemys": [
        # path.join(directories["enemys_pictures"], "bucheron", f)
        # for f in listdir(path.join(directories["enemys_pictures"], "bucheron"))
    ],
}
# # with open(files['db_player'], 'rb') as f:
# #     Iro, Lea, Taz = pickle.load(f)
