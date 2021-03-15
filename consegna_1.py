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

print("Number of Matches : " + str(len(TeamMatches.index)))

wins = len(TeamMatches[((TeamMatches.home_team == Team) & (TeamMatches.home_score > TeamMatches.away_score)) | ((TeamMatches.away_team == Team) & (TeamMatches.home_score < TeamMatches.away_score))].index)

loses = len(TeamMatches[((TeamMatches.home_team == Team) & (TeamMatches.home_score < TeamMatches.away_score)) | ((TeamMatches.away_team == Team) & (TeamMatches.home_score > TeamMatches.away_score))].index)

drafts = len(TeamMatches[TeamMatches.home_score == TeamMatches.away_score].index)


print("Wins : " + str(wins))
print("Loses : " + str(loses))
print("Drafts : " + str(drafts))
print("Sum of W+L+D : " + str(wins+loses+drafts))
#Andremo ad inserire una colonna con le segueti KeyWords: W = (vittoria/Win), L = (Sconfitta/Lose) e D (Pareggio/Draft)
'''
match_results=[]

for index,row in TeamMatches.iterrows():
    if(row['home_team'] == Team and row['home_score'] > row['away_score']):
        match_results.append("W")
    elif(row['home_away'] == Team and row['away_score'] > row['home_score']):
        match_results.append("L")
    elif(row['away_score'] == Team and row['home_score'] > row['home_score']):
        match_results.append("L")
    elif(row['home_away'] == Team and row['away_score'] > row['home_score']):
        match_results.append("W")
    else:
        match_results.append("D")


#aggiungiamo la colonna con W,L e D al DataFrame
newColumn = pd.Series(match_results)
TeamMatches['result'] = newColumn.values'''