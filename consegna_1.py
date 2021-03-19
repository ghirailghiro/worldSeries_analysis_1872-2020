import pandas as pd
from itertools import islice
import matplotlib.pyplot as plt

class Indicators:
    meanScores = 0
    meanConceded = 0
    TeamMatches = None
    Team = ""
    wins = 0
    loses = 0
    Drafts = 0
    goals = None
    def __init__(self,DataFrame,TeamChosen):
        self.TeamMatches = DataFrame.loc[((DataFrame.home_team == Team) | (DataFrame.away_team == Team)) & (DataFrame.tournament == "FIFA World Cup")].copy()
        self.Team = TeamChosen
        self.wins = len(self.TeamMatches[((self.TeamMatches.home_team == Team) & (self.TeamMatches.home_score > self.TeamMatches.away_score)) | ((self.TeamMatches.away_team == Team) & (self.TeamMatches.home_score < self.TeamMatches.away_score))].index)
        self.loses = len(self.TeamMatches[((self.TeamMatches.home_team == Team) & (self.TeamMatches.home_score < self.TeamMatches.away_score)) | ((self.TeamMatches.away_team == Team) & (self.TeamMatches.home_score > self.TeamMatches.away_score))].index)
        self.drafts = len(self.TeamMatches[self.TeamMatches.home_score == self.TeamMatches.away_score].index)
        goals_home = self.TeamMatches[['date','home_score','away_score']][(self.TeamMatches.home_team == Team)]
        goals_away = self.TeamMatches[['date','away_score','home_score']][(self.TeamMatches.away_team == Team)]

        goals_home.columns = ['date','goals_scored','goals_conceded']
        goals_away.columns = ['date','goals_scored','goals_conceded']
        
        frames_goals = [goals_home,goals_away]
        self.goals= pd.concat(frames_goals).sort_index()
        self.goals['date'] = pd.to_datetime(self.goals['date'])
        self.meanScores = self.goals['goals_scored'].mean()
        self.meanConceded = self.goals['goals_conceded'].mean()

    def printData(self):
        print("Wins : " + str(self.wins))
        print("Loses : " + str(self.loses))
        print("Drafts : " + str(self.drafts))
        print("Sum of W+L+D : " + str(self.wins+self.loses+self.drafts))
        print("The mean of the scores made by the team : "+str(self.meanScores))
        print("The mean of the scores conceded by the team : "+str(self.meanConceded))

    def plotData(self):
        self.goals['goals_difference']=self.goals['goals_scored']-self.goals['goals_conceded']
        perYearPlot = self.goals.groupby(self.goals.date.dt.year).sum()
        print(perYearPlot)
        #self.goals.plot(kind = "line", x="date", y="goals_scored", label="Goal Scored")
        #self.goals.plot(kind = "line", x="date", y="goals_conceded", label="Goal Conceded")
        #self.goals.plot(kind = "line", x="date", y="goals_difference", label="Goal Difference")
        perYearPlot.reset_index().plot(kind = "line", x="date", y="goals_scored", label="Goal Scored")
        perYearPlot.reset_index().plot(kind = "line", x="date", y="goals_conceded", label="Goal Conceded")
        perYearPlot.reset_index().plot(kind = "line", x="date", y="goals_difference", label="Goal Difference")
        plt.show()
    
    def printDataFrameGoals(self):
        print(self.goals['date'])
        print(self.goals.dtypes)

    def getData(self):
        return self.wins,self.loses,self.drafts,self.meanScores,self.meanConceded
    
    def getPercentuale(self):
        total = self.wins+self.loses+self.drafts
        return (self.wins*100)/total,(self.loses*100)/total,(self.drafts*100)/total



    pass


def team_indicators(DataFrame, Team, printData=False, plot=False):
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

italia = Indicators(worldFootball,Team)

italia.plotData()

'''
#italia.plotData()

#Prelevo dal dataframe tutti i team#
#prelevo da sia home_team che away_team perché potrebbero esserci squadre che han giocato solo una volta#

allTeams_home = worldFootball[['home_team']].drop_duplicates()
allTeams_away = worldFootball[['away_team']].drop_duplicates()

allTeams_away.columns = ['team']
allTeams_home.columns = ['team']

allTeams = pd.concat([allTeams_away, allTeams_home]).drop_duplicates()


#associo ad ogni team le proprie statistiche (indicatori)#



allTeams['indicators'] = (allTeams['team'].map(lambda x: team_indicators(worldFootball, x)))

TeamStats = team_indicators(worldFootball, Team)

BetterTeams = allTeams[['team']][allTeams.indicators > TeamStats]


print(BetterTeams)
#print(team_Indicators(worldFootball,Team,True,True))
#Andremo ad inserire una colonna con le segueti KeyWords: W = (vittoria/Win), L = (Sconfitta/Lose) e D (Pareggio/Draft)


print(BetterTeams)
'''
