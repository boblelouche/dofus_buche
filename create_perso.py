from Script.Dd import Mount

# from Personage import Player
# import pickle
import dill as pickle
import pandas as pd
from Script.Player import Player
import logging

logging.basicConfig(level=logging.DEBUG)

anonway = Player("Anonway", 9, 5, "test", 85, [1, 0], "sacri", ["Paysan", "Boulanger"])

# Save the Player objects into a pickle file
dbo = open("players.pkl", "wb")
pickle.dump([anonway], dbo)
dbo.close()
# with open('players.pkl', 'rb') as f:

# save the data into an pandas db:
# init_player = pd.DataFrame()