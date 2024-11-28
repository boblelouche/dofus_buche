from config import constants


def unhash_cell(raw_cell):
    return [constants["ZKARRAY"].index(i) for i in raw_cell]


def cell_id_to_coordinates(cell_id: int, map_width: int):
    even_row_length = map_width - 2
    odd_row_length = map_width - 3
    block_size = even_row_length + odd_row_length

    # Calculate row index (y)
    block = cell_id // block_size
    remainder = cell_id % block_size

    if remainder < even_row_length:
        y = block * 2
        x = remainder
    else:
        y = block * 2 + 1
        x = remainder - even_row_length

    return x, y


class Cell:
    def __init__(self, raw_data, CellID, map_width):
        self.raw_data = raw_data
        self.entity = []
        self.color = "black"
        self.CellID = CellID
        cd = unhash_cell(raw_data)
        if cd[2] == 0 or cd[0] == 1 or cd[0] == 33 and cd[2] == 1:
            self.isActive = False
        else:
            self.isActive = (cd[0] & 32 >> 5) != 0
        self.isInteractive = ((cd[7] & 2) >> 1) != 0
        self.lineOfSight = (cd[0] & 1) == 1
        self.layerGroundRot = cd[1] & 48 >> 4
        self.groundLevel = cd[1] & 15
        self.movement = (cd[2] & 56) >> 3
        self.layerGroundNum = (cd[0] & 24 << 6) + (cd[2] & 7 << 6) + cd[3]
        self.layerObject1Num = (
            ((cd[0] & 4) << 11) + ((cd[4] & 1) << 12) + (cd[5] << 6) + cd[6]
        )
        self.layerObject2Num = (
            ((cd[0] & 2) << 12) + ((cd[7] & 1) << 12) + (cd[8] << 6) + cd[9]
        )
        self.isSun = (
            self.layerObject1Num in constants["SUN_MAGICS"]
            or self.layerObject2Num in constants["SUN_MAGICS"]
        )
        self.text = str(self.movement)
        self.set_default_color()
        self.coordinates = cell_id_to_coordinates(self.CellID, map_width)

    def set_default_color(self):
        if self.entity != []:
            self.color = "red"
        elif self.isSun:
            self.color = "yellow"
            self.text = "S"
        elif self.isInteractive:
            self.text = " "
            self.color = "green"
        elif self.isActive:
            self.text = " "
            self.color = "white"

    def get_entity(self, entity_id):
        for entity in self.entity:
            if entity.id == entity_id:
                return entity

    def set_entity(self, entity, action):
        if action:
            if entity.isMainCharacter:
                self.color = "blue"
                self.text = entity.type[0]
                self.entity.append(entity)
            else:
                self.color = "red"
                self.text = entity.type[0]
                self.entity.append(entity)
        else:
            for i in range(len(self.entity)):
                if self.entity[i].id == entity.id:
                    self.entity.remove(self.entity[i])
                    self.set_default_color()
                    break

    def set_not_interactive(self, good):
        if good:
            self.color = "green"
            self.isInteractive = True
        else:
            self.color = "brown"
            self.isInteractive = False

    def __repr__(self) -> str:
        return f"Cell(CellID={self.CellID}, isInteractive={self.isInteractive}, isSun={self.isSun}, lineOfSight={self.lineOfSight}, movement={self.movement}, layerGroundNum={self.layerGroundNum}, layerObject1Num={self.layerObject1Num}, layerObject2Num={self.layerObject2Num}, coordinates={self.coordinates})"

    def __str__(self):
        return self.text

    def print(self):
        if self.isSun:
            print("X", end="")
        elif self.movement != 0:
            print(self.movement, end="")
        elif self.lineOfSight:
            print("_", end="")
        elif self.isInteractive:
            print("O", end="")
        else:
            print("^", end="")