from config import *
from utility import *
import json

def fgo_and_vide_on_brak_bank(Perso):
        Perso.go_brak_bank()
        time.sleep(2)
        Perso.vider_ressource_on_bank()
        time.sleep(1.15)
        if Perso.monture !=None:
            Perso.monture.prendre_ressource_on_dd()
            pyautogui.click(positions["brak_bankier"])
            # cursor.click_on(positions["brak_bankier"])
            time.sleep(1)
            pyautogui.click((positions["brak_bankier"][0]+10,positions["brak_bankier"][1]+11))
            # cursor.click_on((positions["brak_bankier"][0]+10,positions["brak_bankier"][1]+11))
            time.sleep(1)
            pyautogui.click(positions["open_chest"])
            # cursor.click_on(positions["open_chest"])
            time.sleep(0.5)
            Perso.vider_ressource_on_bank()

def fgo_brak_bank(Perso):
    Perso.get_window()
    if Perso.window is not None:
        Perso.use_brak_popo()
        time.sleep(3)
    # print(positions_brak_zapi_milice)
        click_and_confirme_absolute(positions["brak_zapi_milice"])
        time.sleep(3)
        pyautogui.click(positions["active_zapy_divers"])
        try:
            click_on_picture(files["zapy_divers_desactivate_picture"])
            time.sleep(1)
        except:
            print("already activate")
        click_on_picture(files["zapy_bank"])
        time.sleep(1)
        pyautogui.click(positions["enter_brak_bank"])
        time.sleep(3)
        pyautogui.click(positions["brak_bankier"])
        time.sleep(1)
        pyautogui.click((positions["brak_bankier"][0]+10,positions["brak_bankier"][1]+11))
        time.sleep(1)
        pyautogui.click(positions["open_chest"])
        time.sleep(0.5)


def fvider_ressource_on_bank(Perso):
    Perso.get_window()
    if Perso.window is not None:
        try:    
            # click_on_picture(path.join(pict_folder,"inventaire_ressource_desactivate.png"),region=region_inventory)
            click_on_picture(files["inventaire_ressource_desactivate.png"])
            time.sleep(2)
        except:
            print("divers already activate")  
        first_ressource_empty = get_pixel_color_on_pos(positions['first_ressource']) == colors["couleur_inventory_no_ressource"]
        second_ressource_empty = get_pixel_color_on_pos(positions['second_ressource'])  == colors["couleur_inventory_no_ressource"]
        print(first_ressource_empty, second_ressource_empty )
        keyboard.press('ctrl')
        time.sleep(2)
        start_time = time.time()
        while not first_ressource_empty and not second_ressource_empty:
            pyautogui.doubleClick(positions['first_ressource'])
            time.sleep(0.5)
            first_ressource_empty = get_pixel_color_on_pos(positions['first_ressource']) == colors["couleur_inventory_no_ressource"]
            second_ressource_empty = get_pixel_color_on_pos(positions['second_ressource'])  == colors["couleur_inventory_no_ressource"]
            if start_time-time.time()>300:
                keyboard.release("ctrl")
                return 'trop long'
        keyboard.release("ctrl")
        keyboard.press_and_release("escape")
        print(first_ressource_empty, second_ressource_empty )

        Perso.inventory_full=0
        Perso.update_player()
        return "all done"

def fverify_actual_map(Perso):
        Perso.get_window()
        if Perso.window is not None:
        # try:
            screenshot = get_map_name_picture(Perso)
            actual_hash = make_image_hash(screenshot)
            try:
                with open(files["map_position"], 'r+') as file:
                    if path.getsize(files["map_position"]) > 0:
                        file_data = json.load(file)
                    else:
                        file_data = {}
            except json.JSONDecodeError:
                file_data = {}
            for key, value in file_data.items():
                if 'image_hash' in value and actual_hash == hex_to_hash(value['image_hash']):
                    if value['position'] == Perso.position:
                        return True
                    else:
                        Perso.actual_map_key = key
                        Perso.positions = value['position']
                        Perso.update_player()
                        return Perso.position
                    
            new_key = str(len(file_data.keys())+1)
            map_changer = find_map_changer(Perso.window)
            # print(map_changer)
            t = { new_key: {
                "position" :["x","y"],
                # "positions" :f'',
                "name":"",
                "picture_path": path.join(directories["map_name"],f'{new_key}.png'),
                "image_hash":f'{actual_hash}',
                "map_changer": map_changer,
                "ressource": {}}}    
            file_data.update(t)
            with open(files["map_position"], 'w+') as file:
                json.dump(file_data, file, indent=4)
         # rename(map_name_picture, path.join(,f'{key}.png'))
            try:
                rename(screenshot, path.join(directories["map_name"],f'{new_key}.png'))
            except:
                rename(screenshot, path.join(directories["map_name"],f'{new_key}bis.png'))

            return 'unknown_positions', new_key

def fcheck_map_changer(Perso):
    print("todo")

def fuse_brak_popo(Perso):
    Perso.get_window()
    if Perso.window is not None:
        Perso.detect_inventory_open()
        if Perso.inventory_open !=1:
            keyboard.press_and_release("i")
            time.sleep(2)
        try:    
            # click_on_picture(path.join(pict_folder,"inventaire_divers_desactivate.png"),region=region_inventory)
            click_on_picture_once(files["inv_div_des"])
            time.sleep(2)
        except:
            print("divers already activate")    
        # use_ressource(path.join(ressource_picture_folder, "potion", "brakmar.png"))
        click_on_picture_once(path.join(directories["ressource"], "potion", "brakmar.png"))
        keyboard.press_and_release('escape')
        time.sleep(2)
        Perso.positions = ["-23","38"]
        Perso.update_player()