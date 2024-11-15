from lxml import etree
from config import directories
from os import path


class Spells:
    def __init__(self, interface):
        self.interface = interface
        self.list_spell = {}

    def update_spells(self, spells_data):
        self.interface.spellsTab.removes_spells()
        for spell in spells_data[: len(spells_data) - 1]:
            spell = spell.split("~")
            self.get_name(spell[0])
            self.interface.spellsTab.add_spell(
                spell[0], self.get_name(spell[0]), spell[1]
            )

    def get_name(self, id_):
        dir_path = path.join(directories["resource"], "spells.xml")
        # dir_path = "D:/Users/remic/Desktop/MyProjet/Bot_socket/resource/spells.xml"
        spell_name = "None"
        tree = etree.parse(dir_path)

        for spell in tree.xpath("/SPELLS/SPELL"):
            if id_ == spell.get("ID"):
                spell_name = spell.find("NAME").text

        return spell_name
