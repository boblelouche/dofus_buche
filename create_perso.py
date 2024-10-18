from Dd import Monture
# from Personage import Player
import pickle
from Personage import *


Iro = Player("Ironamo", 8, 3, "test", 93, ["-26","21"], "enutrof", ["bucheron" ,"mineur"])
couzine = Monture(Iro, 666, "effect", 100)
Iro.monture = couzine
Lea = Player("Laestra", 6, 3, "test", 52, ["-25","17"], "iop", ["Bijoutier"])
Taz = Player("Tazmany", 6, 3, "test", 52, ["-25","17"], "cra", ["Paysan"])

# Save the Player objects into a pickle file
with open('players.pkl', 'wb') as f:
    pickle.dump([Iro, Lea, Taz], f)
