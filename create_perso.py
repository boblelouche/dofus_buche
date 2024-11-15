from Script.Dd import Mount

# from Personage import Player
# import pickle
import dill as pickle
from .Script.Player import Player


Iro = Player(
    "Ironamo",
    8,
    3,
    "test",
    101,
    [21, -26],
    "enutrof",
    ["bucheron", "mineur"],
    hash_name="fa958560613e959d",
)
couzine = Mount(Iro, 666, "effect", 100)
Iro.monture = couzine
Lea = Player(
    "Laestra",
    6,
    3,
    "test",
    52,
    [-25, 17],
    "iop",
    ["Bijoutier"],
    hash_name="e89d9562c6799d84",
)
Taz = Player("Tazmany", 6, 3, "test", 52, [-25, 17], "cra", ["Paysan"])
Ket = Player("Ketawoman", 6, 3, "test", 2, [-2, -20], "osa", ["Paysan"])

# Save the Player objects into a pickle file
dbo = open("players.pkl", "wb")
pickle.dump([Iro, Lea, Taz, Ket], dbo)
dbo.close()
# with open('players.pkl', 'rb') as f:
