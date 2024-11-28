from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from typing import ClassVar
import logging
import time
from .Base import Base
from config import version
from .Window import Window
from db import session
from .Map import get_map_from_db
from .Cell import Cell


class MapChangeFailed(Exception):
    pass


direction_names = {
    "u": "up",
    "d": "down",
    "l": "left",
    "r": "right",
}

direction_vectors = {
    "u": [0, -1],
    "d": [0, 1],
    "l": [-1, 0],
    "r": [1, 0],
}


class Player(Base):
    __tablename__ = "player"
    id: Mapped[int] = mapped_column(primary_key=True)
    PM: Mapped[int]
    PA: Mapped[int]
    name: Mapped[str] = mapped_column(String(30))
    lvl: Mapped[int]
    classe: Mapped[str] = mapped_column(String(10))
    metier: Mapped[str] = mapped_column(String(50))
    position: ClassVar[tuple[int, int]]
    window: ClassVar[Window]

    def setup(self, position):
        title = f"{self.name} - Dofus Retro v{version}"
        self.position = position
        self.window = Window(title)

    def foreground(self):
        self.window.foreground()

    def is_window_inactive(self):
        active_window = Window.get_active_window_title()
        return (
            active_window is None
            or self.window is None
            or active_window.title != self.window.title
        )

    def move_map(self, direction):
        map = get_map_from_db(session, self.position[0], self.position[1])
        if map is not None:
            logging.info("actual position knowed")
            direction_name = direction_names[direction]
            cell: Cell = getattr(map, direction_name)[0]
            if cell is None:
                raise MapChangeFailed(
                    f"Map changer not found for direction {direction_name}"
                )
            logging.info(f"{cell.coordinates} will be clicked")
            self.window.click_cell(cell, map.width)

            direction_vector = direction_vectors[direction]
            next_position = [
                self.position[0] + direction_vector[0],
                self.position[1] + direction_vector[1],
            ]
            if self.window.confirm_map_change(next_position):
                logging.info(
                    f"{self.name} moved to direction : {direction_vector} from {self.position} to {next_position}"
                )
                time.sleep(0.5)
                self.position = next_position
            else:
                raise MapChangeFailed(
                    f"Move to direction : {direction_vector} from {self.position} to {next_position} failed"
                )
        else:
            raise MapChangeFailed("Map not found")

    def deplacement(self, chemin):
        if self.is_window_inactive():
            self.foreground()
        for s in chemin:
            self.move_map(s)

    def __repr__(self) -> str:
        return f"Player(id={self.id}, PM={self.PM}, PA={self.PA}, name={self.name}, lvl={self.lvl} )"
