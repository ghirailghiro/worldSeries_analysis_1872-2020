import pandas as pd
from itertools import islice
import matplotlib.pyplot as plt

def team_Indicators(DataFrame,Team,printData,plot):
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
    scored_mean = goals['goals_scored'].mean()
    conceded_mean = goals['goals_conceded'].mean()
    if(printData):
        print("Wins : " + str(wins))
        print("Loses : " + str(loses))
        print("Drafts : " + str(drafts))
        print("Sum of W+L+D : " + str(wins+loses+drafts))
        print("Average scored goals : "+ str(scored_mean))
        print("Average conceded goals : "+ str(conceded_mean))
    
    if(plot):
        goals['goals_difference']=goals['goals_scored']-goals['goals_conceded']
        goals.plot(kind = "line", x="date", y="goals_scored", label="Goal Scored")
        goals.plot(kind = "line", x="date", y="goals_conceded", label="Goal Conceded")
        goals.plot(kind = "line", x="date", y="goals_difference", label="Goal Difference")
        plt.show()

    del TeamMatches

    return wins,loses,drafts,scored_mean,conceded_mean

def pretty_print(KeyWord, Value):
    print("--------------------------------------------------------------------------------------------------------------------------------------------------")
    print(KeyWord)
    print(Value)
    print("__________________________________________________________________________________________________________________________________________________")

worldFootball = pd.read_csv("results.csv")

Team = "Italy"

print(team_Indicators(worldFootball,Team,False,False))
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