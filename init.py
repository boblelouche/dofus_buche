# from Personage import *
from Dd import *
from Personage import Player


Iro = Player("Ironamo", 8, 3, "test", 86, [-23,38], "enutrof", ["bucheron" ,"mineur"])
couzine = Monture(Iro, 666, "effect", 100)
Iro.monture = couzine
Lea = Player("Laestra", 6, 3, "test", 52, [-25,17], "iop", ["Bijoutier"])
Taz = Player("Tazmany", 6, 3, "test", 52, [-25,17], "cra", ["Paysan"])