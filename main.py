from Script.utility import save_road
from Script.Player import Player
import logging

logging.basicConfig(level=logging.DEBUG)

anonway = Player("Anonway", 9, 5, "test", 85, [1, 0], "sacri", ["Paysan", "Boulanger"])

anonway.deplacement("dlr")
# anonway = Player("Anonway", 9, 5, "test", 85, [1, 0], "sacri", ["Paysan", "Boulanger"])
Lea = Player(
        "Ironamo",
        8,
        3,
        "test",
        101,
        [10, -13],
        "enutrof",
        ["bucheron", "mineur"],
        hash_name="fa958560613e959d",
        actual_map_key = 10001

    )

Lea.detect_pos_on_mini_map()
print(Lea.position)
Lea.deplacement("u")
Lea.detect_pos_on_mini_map()
print(Lea.position)
