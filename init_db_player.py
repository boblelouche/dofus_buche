from Script.Player import Player
from Script.Dd import Mount
import pandas as pd
from config import files

team =[Player(
        "Ironamo",
        8,
        3,
        "test",
        101,
        [21, -26],
        "enutrof",
        ["bucheron", "mineur"],
        hash_name="fa958560613e959d",
    ),
    Player(
        "Laestra",
        6,
        3,
        "test",
        52,
        [-25, 17],
        "iop",
        ["Bijoutier"],
        hash_name="e89d9562c6799d84",
    ),
    Player("Tazmany", 6, 3, "test", 52, [-25, 17], "cra", ["Paysan"]),  
    Player("Ketawoman", 6, 3, "test", 2, [-2, -20], "osa", ["Paysan"])
    ]


cheptail=[
    Mount("couzine","Iro", 666, "effect", 100)
    ]
df_player = pd.DataFrame(columns= [player.name for player  in team], index=dir(team[0]))
# df_monture  = pd.DataFrame(columns= [monture.name for monture  in cheptail], index=dir(cheptail[0]))
# for player in team[:1]: #

for player in team:
    for _ in dir(team[0]):
        df_player[player.name][_]= getattr(player,_)

df_player.to_csv(files["db_player_csv"], sep=',',  encoding='utf-8')
    # print(fteam[0].name)
# print(team_dict["Iro"].PA)