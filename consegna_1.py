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
numberOfMatches = len(TeamMatches.index)

print("Number of Matches : " + str(numberOfMatches))

wins = len(TeamMatches[((TeamMatches.home_team == Team) & (TeamMatches.home_score > TeamMatches.away_score)) | ((TeamMatches.away_team == Team) & (TeamMatches.home_score < TeamMatches.away_score))].index)

loses = len(TeamMatches[((TeamMatches.home_team == Team) & (TeamMatches.home_score < TeamMatches.away_score)) | ((TeamMatches.away_team == Team) & (TeamMatches.home_score > TeamMatches.away_score))].index)

drafts = len(TeamMatches[TeamMatches.home_score == TeamMatches.away_score].index)

print("Wins : " + str(wins))
print("Loses : " + str(loses))
print("Drafts : " + str(drafts))
print("Sum of W+L+D : " + str(wins+loses+drafts))

goals_scored_home = TeamMatches.loc[['home_score']][(TeamMatches.home_team == Team)]
goals_scored_away = TeamMatches.loc[['away_score']][(TeamMatches.away_team == Team)]

goals_scored_home.rename(columns={'home_score': 'goals_scored'})
goals_scored_away.rename(columns={'away_score': 'goals_scored'})

print(goals_scored_home)
print(goals_scored_away)
frames_goals = [goals_scored_home,goals_scored_away]

goals_scored= pd.concat(frames_goals)

#print(goals_scored)

scores_received = TeamMatches[((TeamMatches.home_team == Team) & (TeamMatches.home_score > TeamMatches.away_score)) | ((TeamMatches.away_team == Team) & (TeamMatches.home_score < TeamMatches.away_score))]


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