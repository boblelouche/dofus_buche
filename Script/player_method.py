from config import *
from utility import *
import json
import cv2 as cv
import numpy as np

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
    if Perso.window == None or Perso.window_activate !=True:
        Perso.get_window()
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
    if Perso.window == None or Perso.window_activate !=True:
        Perso.get_window()
    # click_on_picture(path.join(pict_folder,"inventaire_ressource_desactivate.png"),region=region_inventory)
    try:
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


def fcheck_map_changer(Perso):
    print("todo")

def fuse_brak_popo(Perso):
    if Perso.window == None or Perso.window_activate !=True:
        Perso.get_window()
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

def ffind_actual_map(Perso):
    if Perso.window == None or Perso.window_activate !=True:
        Perso.get_window()
    map_name_picture =  get_map_name_picture(Perso)
    # time.sleep(1)
    # print(map_name_picture)
    actual_hash = make_image_hash(map_name_picture)
    # print(actual_hash)
    file_data=read_pkl(files["map_position_db"])
    for key, value in file_data.items():
        if 'image_hash' in value:
            if hex_to_hash(value['image_hash']) - actual_hash <= 5:
                print(f"Image hash found in key: {key}")
                
                return key
    new_key = str(len(file_data.keys())+1)
    # map_changer = find_map_changer(Perso.window)
    # print(map_changer)
    t = {}
    t[new_key]={
        # "position" :["x","y"],
        "position" :f'{Perso.position}',
        "name":"",
        "picture_path": path.join(directories["map_name"],f'{new_key}.png'),
        "image_hash":f'{actual_hash}',
        "map_changer": find_map_changer(Perso.window),
        "ressource": {}}
    # file_data.update(t)
    update_pkl(files["map_position_db"],t)

    # rename(map_name_picture, path.join(,f'{key}.png'))
    try:
        rename(map_name_picture, path.join(directories["map_name"],f'{new_key}.png'))
    except:
        print('picture already in db')
    return new_key



def find_map_changer(window):
    # Perso.get_window()
    # if Perso.window is not None:
        left = window.left+300
        top = window.top + 35
        width = window.width - 600
        height = window.height -45
        region = {
            "l":(0, 0, width //10, height),
            "r":(width-width//10, 0, width//10,  height),
            "d":(0,height - height//10-210,width, height//10)
        }
      
        u=(left, top,width, height//10)
        map_changer={"l":(),"r":(),"d":(),"u":()}
        keyboard.press("a")
        time.sleep(2)
        screenshot_path = path.join(directories['temp'],f'window screenshot.png')
        screenshot = pyautogui.screenshot(screenshot_path, region=(left,top,width, height))
        keyboard.release("a")
        haystack = cv.imread(screenshot_path)
        screenshotl=haystack[0:0+height-210,0:0+width//10]
        screenshotd=haystack[0+height-height//10-210:0+height-210,0:0+width]
        screenshotr=haystack[0:0+height-210,0+width-width//10:0+width]
        screenshot_region = {
            "l":screenshotl,
            "r":screenshotr,
            "d":screenshotd
        }

        for direction in region:
            for name, picture in pictures["on_map"]["move"].items():
                if name.startswith("arrow"):
                    try:
                        (min_x ,min_y) = locate_in_picture(screenshot_region[direction], picture.path)
                        (image_left, image_top) = (region[direction][0]+min_x+left+15 ,region[direction][1]+min_y+top+40) 
                        logging.debug(f"arrow {direction}",image_left, image_top)
                        map_changer[direction]=(int(image_left), int(image_top))
                        screenshot = pyautogui.screenshot(path.join(directories['temp'],f'{image_left}_{image_top}_screenshot.png'), region=(int(image_left)-50,int(image_top)-50,150,150))
                        break
                    except Exception as e :
                        logging.info(f"{name} not found {e}")
                        keyboard.release("a")
                        # print(e)   
        for name, picture in pictures["on_map"]["move"].items():
                if name.startswith("star"):
                    try:
                        image = pyautogui.locate(picture.path, screenshot_path,region=u, confidence=0.7)       
                        (image_left, image_top) = (image.left ,image.top) 
                        # print(image_positions)
                        map_changer["u"]=(int(image_left+left), int(image_top+top))
                        screenshot = pyautogui.screenshot(path.join(directories['temp'],f'{image_left}_{image_top}_screenshot.png'), region=(int(image_left)-50,int(image_top)-50,150,150))
                        break
                    except Exception as e :
                        logging.info(f"{name} not found")
                        continue
        return map_changer





def locate_in_picture(haystack, needle_path):
    needle = cv.imread(needle_path)
    scGray = cv.cvtColor(np.array(haystack.astype(np.float32)), cv.COLOR_RGB2GRAY)
    needleGray = cv.cvtColor(np.array(needle.astype(np.float32)), cv.COLOR_RGB2GRAY)
    result = cv.matchTemplate(scGray, needleGray, cv.TM_CCOEFF_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(result)
    return minLoc



def fmove_map(Perso, direction):
        # check=None    
    if Perso.window == None or Perso.window_activate !=True:
        Perso.get_window()    
        
    direction_dict = {"u": (1, -1),"d": (1, 1),"r": (0, 1),"l": (0, -1)}
    file_data=read_pkl(files["map_position_db"])           
    for key in file_data:
        if file_data[key]["position"]==Perso.position:
            logging.info(f"actual position knowed")
            Perso.position = [int(Perso.position[0]),int(Perso.position[1])]
            Perso.actual_map_key=key
            if file_data[Perso.actual_map_key]["map_changer"][direction]==():
                # print(key, Perso.actual_map_key, Perso.position)
                find_map_changer(Perso.window)
                return "direction move not know"    
            else:
                pos=file_data[Perso.actual_map_key]["map_changer"][direction]
                pyautogui.click((pos[0],pos[1]))
                check = confirme_changement_map()
                if check == True:
                    logging.info(f"{Perso.name} move to direction : {direction}")
                    time.sleep(0.5)
                    if direction in direction_dict:
                        index, value = direction_dict[direction]
                        Perso.position[index] = Perso.position[index] + value
                    Perso.update_player()
                    return
                else:
                    logging.warning(f"bad map_changer[{direction}] for map {Perso.actual_map_key}")
                    return
        
    logging.info(f"{Perso.position} not in db")        
    Perso.actual_map_key = ffind_actual_map(Perso)
    file_data=read_pkl(files["map_position_db"])           
    pos=file_data[Perso.actual_map_key]["map_changer"][direction]
    logging.info(f"{pos} will be clicked")
    pyautogui.click((pos[0],pos[1]))
    check = confirme_changement_map()
    if check == True:
        logging.info(f"db_updated {Perso.name} move to direction : {direction}")
        time.sleep(0.5)
        if direction in direction_dict:
            index, value = direction_dict[direction]
            Perso.position[index] = Perso.position[index] + value
        Perso.position = [int(Perso.position[0]),int(Perso.position[1])]
        Perso.update_player()
    else:
        logging.warning(f"bad map_changer[{direction}] for map {Perso.actual_map_key}")
        return
