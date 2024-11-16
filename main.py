# from Script.utility import save_road
from Script.Player import Player
import logging

logging.basicConfig(level=logging.DEBUG)

# anonway = Player("Anonway", 9, 5, "test", 85, [1, 0], "sacri", ["Paysan", "Boulanger"])
Lea = Player(
        "Laestra",
        8,
        3,
        "test",
        101,
        [10, -13],
        "enutrof",
        ["bucheron", "mineur"],
        hash_name="fa958560613e959d",
    )

Lea.detect_pos_on_mini_map()
print(Lea.position)
Lea.deplacement("llr")
Lea.detect_pos_on_mini_map()
print(Lea.position)
