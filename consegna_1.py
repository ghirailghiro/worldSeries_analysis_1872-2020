import pandas as pd
from itertools import islice
import matplotlib.pyplot as plt

def team_Indicators(DataFrame,Team):
    TeamMatches = DataFrame.loc[(DataFrame.home_team == Team) | (DataFrame.away_team == Team)].copy()

    wins = len(TeamMatches[((TeamMatches.home_team == Team) & (TeamMatches.home_score > TeamMatches.away_score)) | ((TeamMatches.away_team == Team) & (TeamMatches.home_score < TeamMatches.away_score))].index)

    loses = len(TeamMatches[((TeamMatches.home_team == Team) & (TeamMatches.home_score < TeamMatches.away_score)) | ((TeamMatches.away_team == Team) & (TeamMatches.home_score > TeamMatches.away_score))].index)

    drafts = len(TeamMatches[TeamMatches.home_score == TeamMatches.away_score].index)

    goals_home = TeamMatches[['date','home_score','away_score']][(TeamMatches.home_team == Team)]
    goals_away = TeamMatches[['date','away_score','home_score']][(TeamMatches.away_team == Team)]

    goals_home.columns = ['date','goals_scored','goals_conceded']
    goals_away.columns = ['date','goals_scored','goals_conceded']
    frames_goals = [goals_home,goals_away]

    goals= pd.concat(frames_goals).sort_index()

    return wins,loses,drafts,goals['goals_scored'].mean(),goals['goals_conceded'].mean()

def pretty_print(KeyWord, Value):
    print("--------------------------------------------------------------------------------------------------------------------------------------------------")
    print(KeyWord)
    print(Value)
    print("__________________________________________________________________________________________________________________________________________________")

worldFootball = pd.read_csv("results.csv")

Team = "Italy"

print(team_Indicators(worldFootball,Team))
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

goals_home = TeamMatches[['date','home_score','away_score']][(TeamMatches.home_team == Team)]
goals_away = TeamMatches[['date','away_score','home_score']][(TeamMatches.away_team == Team)]

goals_home.columns = ['date','goals_scored','goals_conceded']
goals_away.columns = ['date','goals_scored','goals_conceded']

#print(goals_home)
#print(goals_away)

frames_goals = [goals_home,goals_away]

goals= pd.concat(frames_goals).sort_index()

#print(goals)

averageScored = goals['goals_scored'].mean()
averageConceded = goals['goals_conceded'].mean()

goals['goals_difference']=goals['goals_scored']-goals['goals_conceded']

print("Average scored goals : "+ str(averageScored))
print("Average conceded goals : "+ str(averageConceded))

print(goals)

#Ploting the results
'''
goals.plot(kind = "line", x="date", y="goals_scored", label="Goal Scored")
goals.plot(kind = "line", x="date", y="goals_conceded", label="Goal Conceded")
goals.plot(kind = "line", x="date", y="goals_difference", label="Goal Difference")

plt.show()
'''

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