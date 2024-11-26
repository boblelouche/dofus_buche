from sql_connect import  user, Password, Host, database,port
from typing import List, Optional, ClassVar
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship, Session
from sqlalchemy import select, Text, create_engine, ForeignKey, String
from config import directories
from os import path
import xml.etree.ElementTree as ET
from Cell import Cell


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
    cells : ClassVar[list[Cell]]
    # object = None
    # clickable = 
    map_changers:Mapped[List["MapChanger"]] = relationship(
        back_populates="", cascade="all, delete-orphan"
    ) 
    def __repr__(self) -> str:
        return f"Map(id={self.id},x={self.x}, y={self.y}, longueur={self.longueur}, largeur={self.largeur})"
    
    
    def get_map_info(self):
        raw_cells = [self.MAPA_DATA[i : i + 10] for i in range(0, len(self.MAPA_DATA), 10)]
        self.cells = [Cell(raw_cells[i], i) for i in range(len(raw_cells))]



    def display_cells(self):
        i = 15
        line_number = 0
        # print(len(self.cells))
        while i < len(self.cells) - 15:
            # print(i)
            if line_number % 2 == 0:
                for j in range(0, 14):
                    # print(i + j)
                    self.cells[i + j].print()
                    print(" ", end="")
                i += 14
            else:
                print(" ", end="")
                for j in range(1, 14):
                    # print(i + j)
                    self.cells[i + j].print()
                    print(" ", end="")
                i += 15
            line_number += 1
            print("")

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
    

def add_xml(file, session):
        tree = ET.parse(path.join(directories["MAP_DIR"],file))
        root = tree.getroot()
        map = Map(longueur=root[1].text, largeur=root[2].text, x=root[3].text, y=root[4].text, MAPA_DATA=root[5].text)
        session.add(map)
        session.commit()


def get_map_from_db(session,x,y):
    r=session.scalar(select(Map)
                      .where(Map.x==x)
                      .where(Map.y==y))
    return r


engine = create_engine(f"mariadb+mariadbconnector://{user}:{Password}@{Host}:{port}/{database}")
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
with Session(engine) as session:
    map= get_map_from_db(session, 26,-37)
    map.get_map_info()
    
    map.display_cells()
  