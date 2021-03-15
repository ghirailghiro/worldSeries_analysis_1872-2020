import pandas as pd
from itertools import islice
import matplotlib.pyplot as plt


def pretty_print(KeyWord, Value):
    print("--------------------------------------------------------------------------------------------------------------------------------------------------")
    print(KeyWord)
    print(Value)
    print("__________________________________________________________________________________________________________________________________________________")

worldFootball = pd.read_csv("results.csv")

Team = "Italy"

#Creazione DataFrame partite di Team
TeamMatches = worldFootball.loc[(worldFootball.home_team == Team) | (worldFootball.away_team == Team)].copy()

#Andremo ad inserire una colonna con le segueti KeyWords: W = (vittoria/Win), L = (Sconfitta/Lose) e D (Pareggio/Draft)

match_results=[]

for index,row in TeamMatches.iterrows():

#aggiungiamo la colonna con W,L e D al DataFrame
newColumn = pd.Series(match_results)
TeamMatches['result'] = newColumn.values