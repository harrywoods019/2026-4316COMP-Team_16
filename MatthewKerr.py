#imported pandas and matplotlib to read in the data file and are able to plot graphs
import pandas
import matplotlib.pyplot as plt

#reads in the csv file
prem = pandas.read_csv("PremierLeague.csv")

#Graph 1 Home vs away goals
seasonGoals = prem.groupby("Season") [["FullTimeHomeTeamGoals", "FullTimeAwayTeamGoals"]].sum()

#Create list for each variable
seasons = seasonGoals.index.tolist()
homeGoals = seasonGoals["FullTimeHomeTeamGoals"].tolist()
awayGoals = seasonGoals["FullTimeAwayTeamGoals"].tolist()

#Graph 2 Drawn matches per season
drawMatches = prem["FullTimeHomeTeamGoals"] == prem["FullTimeAwayTeamGoals"]

seasonDraws = prem[drawMatches].groupby("Season").size()

seasonDraws = seasonDraws.reindex(seasonGoals.index, fill_value=0)
#Converts variable into list
draws = seasonDraws.tolist()

#Allowing two graphs to show at the same time
fig, (top, bottom) = plt.subplots(2, 1, figsize=(12,10), sharex=True)

#Lines for graph 1
top.plot(seasons, homeGoals, "gs-", label="Home Goals")
top.plot(seasons,awayGoals, "rD-", label = "Away Goals")

top.set_title("Premier League Home Goals vs Away Goals per Season")
top.set_ylabel("Total Goals")
top.grid()
top.legend()

#Lines for graph 2
bottom.bar(seasons, draws)
bottom.set_title("Premier League Drawn Matches per Season")
bottom.set_xlabel("Season")
bottom.set_ylabel("No. of draws")
bottom.grid(axis="y")

#Graph layout changes
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()