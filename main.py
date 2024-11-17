from Script.utility import save_road
from Script.Player import Player
import logging

logging.basicConfig(level=logging.DEBUG)

anonway = Player("Anonway", 9, 5, "test", 85, [1, 0], "sacri", ["Paysan", "Boulanger"])

anonway.deplacement("dlr")
