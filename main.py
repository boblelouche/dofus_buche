# from Script.utility import save_road
from models.Player import Player
import logging

logging.basicConfig(level=logging.INFO)

anonway = Player(
    name="Anonway", PA=9, PM=6, lvl=85, classe="sacri", metier=["Paysan", "Boulanger"]
)

anonway.setup((-2, 0))
anonway.deplacement("drul")
