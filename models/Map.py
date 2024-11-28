from models.Cell import Cell
from config import directories
from os import path
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy import Text, String, select, ScalarResult
from typing import Optional, ClassVar
import xml.etree.ElementTree as ET
from .Base import Base


class Map(Base):
    __tablename__ = "map"
    id: Mapped[int] = mapped_column(primary_key=True)
    x: Mapped[int]
    y: Mapped[int]
    map_data: Mapped[str] = mapped_column(Text())
    hash: Mapped[Optional[str]] = mapped_column(String(20))
    width: Mapped[int]
    height: Mapped[int]
    cells: ClassVar[list[Cell]]
    map_changers: ClassVar[list[Cell]]
    left: ClassVar[list[Cell]]
    up: ClassVar[list[Cell]]
    down: ClassVar[list[Cell]]
    right: ClassVar[list[Cell]]

    def __repr__(self) -> str:
        return f"Map(id={self.id},x={self.x}, y={self.y}, height={self.height}, width={self.width})"

    def get_map_info(self):
        self.raw_cells = [
            self.map_data[i : i + 10] for i in range(0, len(self.map_data), 10)
        ]
        self.cells = []
        self.up = []
        self.down = []
        self.right = []
        self.left = []
        self.map_changers = []

        for i in range(len(self.raw_cells)):
            self.cells.append(Cell(self.raw_cells[i], i, self.width))
            cell = self.cells[i]
            if cell.isSun:
                if cell.coordinates[1] == 1:
                    self.up.append(cell)
                elif cell.coordinates[0] == 13:
                    self.right.append(cell)
                elif cell.coordinates[0] == 0:
                    self.left.append(cell)
                elif cell.coordinates[1] == 31:
                    self.down.append(cell)
                else:
                    self.map_changers.append(cell)

    def display_cells(self):
        width = self.width
        i = width - 2
        line_number = 0

        while i < len(self.cells) - width - 2:
            if line_number % 2 == 0:
                for j in range(0, width - 3):
                    self.cells[i + j].print()
                    print(" ", end="")
                i += width - 3
            else:
                print(" ", end="")
                for j in range(1, width - 3):
                    self.cells[i + j].print()
                    print(" ", end="")
                i += width - 2
            line_number += 1
            print("")


def add_xml(file, session):
    print(f"Read {file}")
    tree = ET.parse(path.join(directories["MAP_DIR"], file))
    root = tree.getroot()
    map = Map(
        height=root[1].text,
        width=root[2].text,
        x=root[3].text,
        y=root[4].text,
        map_data=root[5].text,
    )
    print(f"Add {map}")
    session.add(map)
    session.commit()


def get_map_from_db(session: Session, x: int, y: int) -> Map | None:
    map = session.scalar(select(Map).where(Map.x == x).where(Map.y == y))

    if map is not None:
        map.get_map_info()
    return map


def get_maps_from_db(session: Session, x: int, y: int) -> ScalarResult[Map] | None:
    maps = []

    result = session.scalars(select(Map).where(Map.x == x).where(Map.y == y))
    for map in result:
        map.get_map_info()
        maps.append(map)
    return maps


def get_all_maps_from_db(session: Session):
    maps = []

    result = session.execute(select(Map))
    while chunk := result.fetchmany(100):
        for (map,) in chunk:
            map.get_map_info()
            maps.append(map)

    return maps
