# # from sqlalchemy import create_engine
# import sqlalchemy
# from sqlalchemy.ext.declarative import declarative_base

# engine = create_engine("sqlite://", echo=True)


from sql_connect import  user, Password, Host, database,port
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
# from sqlalchemy import dialects
from sqlalchemy import Text
from sqlalchemy.orm import Session
from Script.Player2 import Player2
from config import directories
from os import listdir, path
import xml.etree.ElementTree as ET
import json


class Map2:
    def __init__(self,id,longueur,largeur,x,y,data) -> None:
        self.x=x
        self.y=y
        self.position =  [int(self.x),int(self.y)]
        self.MAPA_DATA = data
        self.ID = id
        self.hash = None
        self.largeur = largeur
        self.longueur = longueur
        self.object = None
        self.map_changer = MapChanger(self.ID)

    def get_hash(self):
        return "hash"
    
class Base(DeclarativeBase):
    pass

class Map(Base):
    __tablename__="map"
    id:Mapped[int] = mapped_column(primary_key=True)
    x:Mapped[int]
    y:Mapped[int]
    # position =  [int(x),int(y)]
    MAPA_DATA :Mapped[str] =mapped_column(Text())
    hash:Mapped[Optional[str]] = mapped_column(String(20))
    largeur:Mapped[int]
    longueur: Mapped[int]
    # object = None
    # clickable = 
    map_changers:Mapped[List["MapChanger"]] = relationship(
        back_populates="", cascade="all, delete-orphan"
    ) 
    def __repr__(self) -> str:
        return f"Map(id={self.id}, type={self.type},x={self.x}, y={self.y}, longueur={self.longueur}, largeur={self.largeur})"

class MapChanger(Base):
    __tablename__ = "map_changer"
    id : Mapped[int] = mapped_column(primary_key=True)
    type : Mapped[str] = mapped_column(String(8))
    x : Mapped[int]
    y : Mapped[int]
    map: Mapped["Map"]= relationship(
        back_populates="map_changers")
    map_id:Mapped["int"] =  mapped_column(ForeignKey("map.id"))

    def __repr__(self)-> str:
        return f"MapChanger(id={self.id}, type={self.type}, x={self.x}, y={self.y} )"

    
    
class Player(Base):
    __tablename__ = "player"
    id: Mapped[int] = mapped_column(primary_key=True)
    # window_title : Mapped[str] = mapped_column(String(30))
    PM: Mapped[int] 
    PA : Mapped[int] 
    name : Mapped[str] = mapped_column(String(30))
    # sort = sort
    lvl : Mapped[int]  
    # hash_name = hash_name
    # position : Mapped[str] = mapped_column(String(10))
    # actual_map_key : Mapped[str] = mapped_column(String(10))
    classe : Mapped[str] = mapped_column(String(10))
    metier : Mapped[str] = mapped_column(String(50))
   
    def __repr__(self)-> str:
        return f"Player(id={self.id}, PM={self.PM}, PA={self.PA}, name={self.name}, lvl={self.lvl} )"
    
print("ok")

def create_player(player):
    return Player(
        name=player.name,
        PM = player.PM,
        PA = player.PA,
        lvl = player.lvl,
        metier=  json.dumps(player.metier),
        classe = player.classe,
        )

def create_map(map):
    return Map(
    x=map.x,
    y=map.y,
    MAPA_DATA= map.MAPA_DATA,
    hash= map.hash,
    largeur= map.largeur,
    longueur= map.longueur
    # map_changer= map.map_changer 
    )

def add_xml(file, session):
        # add_xmlinfo(path.join(directories["MAP_DIR"],file))
        tree = ET.parse(path.join(directories["MAP_DIR"],file))
        root = tree.getroot()
        # print(root[2].text)
        M4 = Map2(root[0].text, root[1].text, root[2].text, root[3].text, root[4].text, root[5].text)
        session.add(create_map(M4))
        session.commit()

Iro = Player2(
    "Ironamo",
    8,
    3,
    "test",
    101,
    [21, -26],
    "enutrof",
    ["bucheron", "mineur"],
    hash_name="fa958560613e959d",
)
Lea = Player2(
    "Laestra",
    6,
    3,
    "test",
    52,
    [-25, 17],
    "iop",
    ["Bijoutier"],
    hash_name="e89d9562c6799d84",
)
Taz = Player2("Tazmany", 6, 3, "test", 52, [-25, 17], "cra", ["Paysan"])
Ket = Player2("Ketawoman", 6, 3, "test", 2, [-2, -20], "osa", ["Paysan"])


engine = create_engine(f"mariadb+mariadbconnector://{user}:{Password}@{Host}:{port}/{database}")
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add_all([create_player(Iro),create_player(Lea),create_player(Ket),create_player(Taz)])
    session.commit()
    for file in listdir(directories["MAP_DIR"]):
        add_xml(file, session)
        
