import pandas as pd
from config import files, directories
import xml.etree.ElementTree as ET
from os import listdir, path
import ast

class MapChanger:
    def __init__(self,Map_id) -> None:    
        self.id = Map_id
        self.data = {}

    def modify(self,direction, Point):
        self.data[direction]= Point
        
        # self.direction = (Point[0],Point[1])

class Map:
    def __init__(self,id,longeur,largeur,x,y,data) -> None:
        self.x=x
        self.y=y
        self.position =  [int(self.x),int(self.y)]
        self.MAPA_DATA = data
        self.ID = id
        self.hash = None
        self.largeur = largeur
        self.longeur = longeur
        self.object = None
        self.map_changer = MapChanger(self.ID)

    def get_hash(self):
        return "hash"

def init_db_with_xml():
    maps=[]
    for file in listdir(directories["MAP_DIR"])[:5]:
        # add_xmlinfo(path.join(directories["MAP_DIR"],file))
        tree = ET.parse(path.join(directories["MAP_DIR"],file))
        root = tree.getroot()
        # print(root[2].text)
        M4 = Map(root[0].text, root[1].text, root[2].text, root[3].text, root[4].text, root[5].text)
        maps.append(M4)
        
    df_map = pd.DataFrame(
        [[p.ID, p.longeur,p.largeur,p.x,p.y,p.MAPA_DATA,p.hash, p.map_changer,p] for p in maps],
        columns=["ID","longeur","largeur","x","y","data","hash","map_changer","object"])
    df_map.to_json(files["db_map"], orient='index', indent=2)
    # df_map.loc[:,"object"][0].map_changer.modify(4,5)
    # print(df_map.loc[:,"object"][0].map_changer.data)
init_db_with_xml()
# print(t)
# print(df.loc[1000,"position"])
# df.loc[1000,"x"]=13
# df = pd.read_csv(files["db_map"], sep=';', encoding='utf-8',index_col=0)
# print(df.loc[1000]["x"])

# df = pd.read_csv(files["db_map"], sep=';',  encoding='utf-8', index_col=0)
# print(type(df["object"][0]))
def move(Id,direction):
    # if Perso.is_window_inactive():
    #     Perso.get_window()
    direction_dict = {"u": (1, -1), "d": (1, 1), "r": (0, 1), "l": (0, -1)}
    # file_data = read_pkl(files["map_position_db"])
    # file_data = {}
    db_position_key = df.loc[df["ID"]==Id]["ID"].values
    print(db_position_key)
    # print(df.loc[db_position_key[0], "object"])
    # print(df.loc[df["x"]==position]["ID"].values)
    # m = df.loc[db_position_key[0]]["map_changer"]
    # m.modify("u",5)
    # print(m)
    # print(df.loc[db_position_key[0]]["map_changer"])
    # if len(db_position_key)>0:
    #     # Perso.actual_map_key = df.loc[db_position_key]
    #     selected_map = df.loc[db_position_key]
    #     # selected_map.loc[:,"mapchanger"][direction]=(5,0)
    #     ast.literal_eval(selected_map.loc[:,"mapchanger"].values[0])[direction] =(20,20)
    #     print(ast.literal_eval(selected_map.loc[:,"mapchanger"].values[0])[direction])

        # selected_map["mapchanger"][direction]=(0,0)
    # print(selected_map["mapchanger"])


# move(10004,"u")
# # map1 = df.loc[df[10]>11]

# print(map1["x"])
# print(df.loc[0])
# print(df.loc["position",'1000'])