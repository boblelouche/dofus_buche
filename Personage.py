from config import *

class Personage:
    def __init__(self, name, PA, PM, sort, lvl, position, classe, metier):
        self.PA = PA
        self.PM = PM
        self.name = name
        self.sort = sort
        self.lvl = lvl
        self.position = position
        self.classe = classe
        self.metier = metier
        self.inventory_full = 0
        self.inventory_open = 0


    def get_position(self):
        print('todo')

Iro = Personage("Ironamo", 8, 3, "test", 86, [-23,38], "enutrof", ["bucheron" ,"mineur"])
Lea = Personage("Laestra", 6, 3, "test", 52, [-25,17], "iop", ["Bijoutier"])
