from Dd import Monture
# from Personage import Player
import pickle
from Personage import *


Iro = Player("Ironamo", 8, 3, "test", 97, [0,26], "enutrof", ["bucheron" ,"mineur"])
couzine = Monture(Iro, 666, "effect", 100)
Iro.monture = couzine
Lea = Player("Laestra", 6, 3, "test", 52, [-25,17], "iop", ["Bijoutier"])
Taz = Player("Tazmany", 6, 3, "test", 52, [-25,17], "cra", ["Paysan"])
Ket = Player("Ketawoman", 6, 3, "test", 2, [-2,-20], "osa", ["Paysan"])

# Save the Player objects into a pickle file
dbo =  open('players.pkl', 'wb')
pickle.dump([Iro, Lea, Taz, Ket], dbo)
dbo.close()
# with open('players.pkl', 'rb') as f: