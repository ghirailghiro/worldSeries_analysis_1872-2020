import pandas as pd
from itertools import islice
import matplotlib.pyplot as plt


##  Classe Indicators utilizzata per contener einformazioni su Team (= squadra scelta)  ##
## __init__: inizializza le varie istanze dell'oggetto, che poi saranno gli indicatori di Team ##

class Indicators:

    def __init__(self,DataFrame,TeamChosen):
        self.Team = TeamChosen
        self.TeamMatches = DataFrame.loc[((DataFrame.home_team == self.Team) | (DataFrame.away_team == self.Team)) & (DataFrame.tournament == "FIFA World Cup")].copy()
        self.wins = len(self.TeamMatches[((self.TeamMatches.home_team == self.Team) & (self.TeamMatches.home_score > self.TeamMatches.away_score)) | ((self.TeamMatches.away_team == self.Team) & (self.TeamMatches.home_score < self.TeamMatches.away_score))].index)
        self.loses = len(self.TeamMatches[((self.TeamMatches.home_team == self.Team) & (self.TeamMatches.home_score < self.TeamMatches.away_score)) | ((self.TeamMatches.away_team == self.Team) & (self.TeamMatches.home_score > self.TeamMatches.away_score))].index)
        self.drafts = len(self.TeamMatches[self.TeamMatches.home_score == self.TeamMatches.away_score].index)
        goals_home = self.TeamMatches[['date','home_score','away_score']][(self.TeamMatches.home_team == self.Team)]
        goals_away = self.TeamMatches[['date','away_score','home_score']][(self.TeamMatches.away_team == self.Team)]

        goals_home.columns = ['date','goals_scored','goals_conceded']
        goals_away.columns = ['date','goals_scored','goals_conceded']
        
        frames_goals = [goals_home,goals_away]
        self.goals = pd.concat(frames_goals).sort_index()
        self.goals['date'] = pd.to_datetime(self.goals['date'])
        self.meanScores = self.goals['goals_scored'].mean()
        self.meanConceded = self.goals['goals_conceded'].mean()

    def printData(self):
        print("Wins : " + str(self.wins))
        print("Loses : " + str(self.loses))
        print("Drafts : " + str(self.drafts))
        print("Sum of W+L+D : " + str(self.wins+self.loses+self.drafts))
        print("The mean of the scores made by the team : " + str(self.meanScores))
        print("The mean of the scores conceded by the team : " + str(self.meanConceded))


    ## plotData(): metodo utilizzato per graficare il numero dei gol fatti e subiti di Team ogni anno 
    def plotData(self):
        self.goals['goals_difference'] = self.goals['goals_scored'] - self.goals['goals_conceded']
        perYearPlot = self.goals.groupby(self.goals.date.dt.year).sum()
        perYearPlot.reset_index().plot(kind = "line", x="date", y="goals_scored", label="Goal Scored")
        perYearPlot.reset_index().plot(kind = "line", x="date", y="goals_conceded", label="Goal Conceded")
        perYearPlot.reset_index().plot(kind = "line", x="date", y="goals_difference", label="Goal Difference")
        plt.show()
    
    ## metodi getter ##
    def getData(self):
        return self.wins,self.loses,self.drafts,self.meanScores,self.meanConceded
    def getMeanScores(self):
        return self.meanScores
    def getMeanConceded(self):
        return self.meanConceded
    def getWins(self):
        return self.wins
    def getLoses(self):
        return self.loses
    def getNumMatchesPlayed(self):
        return self.wins + self.drafts + self.loses
    def getTeamMatches(self):
        return self.TeamMatches

    ## isBetter(): metodo utilizzato per paragonare Team con gli indicatori di altre squadre (indicatori in formato tupla) ##
    def isBetter(self, otherTeamIndicators, parameter="wins"):
        if(parameter == "wins"):
            return self.wins >= otherTeamIndicators[0]

        if(parameter == "loses"):
            return self.wins <= otherTeamIndicators[1]

        if(parameter == "attack"):
            return self.meanScores >= otherTeamIndicators[3]

        if(parameter == "defense"): 
            return self.meanConceded <= otherTeamIndicators[4]
    pass




worldFootball = pd.read_csv("results.csv")

worldFootball = worldFootball[worldFootball.tournament == "FIFA World Cup"]


TeamName = "Brazil"

Team = Indicators(worldFootball,TeamName)

#Team.printData()

#Team.plotData()



#Prelevo dal dataframe tutti i team#
#prelevo da sia home_team che away_team perché potrebbero esserci squadre che han giocato solo una volta#

allTeams_home = worldFootball[['home_team']].drop_duplicates()
allTeams_away = worldFootball[['away_team']].drop_duplicates()

allTeams_away.columns = ['team']
allTeams_home.columns = ['team']

allTeams = pd.concat([allTeams_away, allTeams_home]).drop_duplicates()


#associo ad ogni team le proprie statistiche (indicatori)#



allTeams['indicators'] = (allTeams['team'].map(lambda x: Indicators(worldFootball, x).getData()))



allTeams['Pts'] =  (allTeams['indicators'].map(lambda x: x[0]*3 + x[2])) 

TeamPts = Team.getData()
TeamPts = TeamPts[0]*3 + TeamPts[2]

BetterTeamsByPts = allTeams[['team', 'Pts']][allTeams.Pts > TeamPts]


print(f"Teams that have gained more points than {TeamName} ({TeamPts})")
print("------------------------------------------------------------------------------------")
print(BetterTeamsByPts)
print("")

#GET BETTER TEAMS BY WINNING TIMES
allTeams['isBetter'] = (allTeams['indicators'].map(lambda x: not Team.isBetter(x))) 
allTeams['won/played'] = (allTeams['indicators'].map(lambda x: str(x[0]) + '/' + str(x[0]+x[1]+x[2])))
allTeams['winning rate'] = (allTeams['indicators'].map(lambda x: x[0] / (x[0]+x[1]+x[2])))

betterTeams = allTeams[['team','won/played', 'winning rate']][allTeams.isBetter == True]



print(f"Teams that have won more than {TeamName} ({Team.getWins()}/{Team.getNumMatchesPlayed()} with a winning rate of {Team.getWins()/Team.getNumMatchesPlayed()})")
print("------------------------------------------------------------------------------------")
print(betterTeams)
print("")


#GET BETTER TEAMS BY LOSING TIMES
allTeams['isBetter'] = (allTeams['indicators'].map(lambda x: not Team.isBetter(x, "loses"))) 
allTeams['lost/played'] = (allTeams['indicators'].map(lambda x: str(x[1]) + '/' + str(x[0]+x[1]+x[2])))
allTeams['losing rate'] = (allTeams['indicators'].map(lambda x: x[1] / (x[0]+x[1]+x[2])))

betterTeams = allTeams[['team','lost/played', 'losing rate']][allTeams.isBetter == True]

print(f"Teams that have lost less than {TeamName} ({Team.getLoses()}/{Team.getNumMatchesPlayed()} with a losing rate of {Team.getLoses()/Team.getNumMatchesPlayed()})")
print("------------------------------------------------------------------------------------")
print(betterTeams)
print("")


#GET BETTER TEAMS BY BEST ATTACKS
allTeams['isBetter'] = (allTeams['indicators'].map(lambda x: not Team.isBetter(x, "attack"))) 
allTeams['goals scored rate'] = (allTeams['indicators'].map(lambda x: x[3]))
allTeams['Matches played'] = (allTeams['indicators'].map(lambda x: x[0] + x[1] + x[2]))

betterTeams = allTeams[['team', 'goals scored rate','Matches played']][allTeams.isBetter == True]

print(f"Teams that have a better mean goals scored for match than {TeamName} ({Team.getMeanScores()} in {Team.getNumMatchesPlayed()} matches played)")
print("-----------------------------------------------------------------------------------")
print(betterTeams)
print("")



#GET BETTER TEAMS BY BEST DEFENSE
allTeams['isBetter'] = (allTeams['indicators'].map(lambda x: not Team.isBetter(x, "defense"))) 
allTeams['goals conceded rate'] = (allTeams['indicators'].map(lambda x: x[4]))
allTeams['Matches played'] = (allTeams['indicators'].map(lambda x: x[0] + x[1] + x[2]))


betterTeams = allTeams[['team','goals conceded rate','Matches played']][allTeams.isBetter == True]

print(f"Teams that have a better mean goals conceded for maatch than {TeamName} ({Team.getMeanConceded()} in {Team.getNumMatchesPlayed()} matches played)")
print("------------------------------------------------------------------------------------")
print(betterTeams)
print("")




#########################################################
##                  WINNING STREAK                     ##
#########################################################

def getResult(row):
    if(row['home_score'] > row['away_score']):
        if(row['home_team'] == TeamName):
            return "W"
        else:
            return "L"
    elif(row['home_score'] < row['away_score']):
        if(row['away_team'] == TeamName):
            return "W"
        else:
            return "L"
    else:
            return "D"

TeamMatches = Team.getTeamMatches()

TeamMatches['match_result'] = (TeamMatches.apply(getResult, axis=1))

#mezzo copia e incolla da stackof
g = TeamMatches.match_result.__eq__("W").astype(int).diff().fillna(0).abs().cumsum()
TeamMatches['consecutive'] = TeamMatches.groupby(g).match_result.cumcount().add(1)


print(TeamMatches)

#print di verifica
#print(TeamMatches['match_result'].to_string())

MaxStreak = TeamMatches[['consecutive']][TeamMatches.match_result == "W"].max()


print(f"Longest winning streak for {TeamName}:")
print(MaxStreak)
print("")

Team.plotData()