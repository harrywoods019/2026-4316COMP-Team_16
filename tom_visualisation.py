import pandas as pd
import matplotlib.pyplot as plt

# load the dataset from csv file
df = pd.read_csv("PremierLeague.csv")

# create a new column for goal difference (how close each game was)
df["goal_diff"] = abs(df["FullTimeHomeTeamGoals"] - df["FullTimeAwayTeamGoals"])

# group by season and work out average goal difference
# this helps show if games are getting closer or more one-sided
avg_diff = df.groupby("Season")["goal_diff"].mean()

# find matches that are clearly one-sided (goal difference 2 or more)
big_wins = df[df["goal_diff"] >= 2]

# calculate percentage of one-sided matches per season
one_sided_pct = (big_wins.groupby("Season").size() / df.groupby("Season").size()) * 100


# now looking at unpredictability using match results

# count how many home wins, draws and away wins per season
res_counts = df.groupby(["Season","FullTimeResult"]).size().unstack()

# fill missing values with 0 just in case
res_counts = res_counts.fillna(0)

# convert counts into percentages so seasons can be compared fairly
res_pct = res_counts.div(res_counts.sum(axis=1), axis=0) * 100

# specifically track away wins as they show unpredictability
away_pct = res_pct["A"]


# create graphs (4 total)
fig, axs = plt.subplots(4,1,figsize=(12,14),sharex=True)

# get seasons for x axis
seasons = avg_diff.index
step = 3   # only show every 3rd season to avoid clutter


# --- graph 1 ---
# average goal difference (main competitiveness measure)
axs[0].plot(seasons, avg_diff)
axs[0].set_title("Q1 - Avg Goal Diff per Season")
axs[0].set_ylabel("Goal Diff")
axs[0].grid()


# --- graph 2 ---
# percentage of one-sided games
axs[1].bar(seasons, one_sided_pct)
axs[1].set_title("Q1 - % One Sided Games")
axs[1].set_ylabel("%")
axs[1].grid()


# --- graph 3 ---
# stacked bar showing distribution of results
axs[2].bar(seasons, res_pct["H"], label="Home")
axs[2].bar(seasons, res_pct["D"], bottom=res_pct["H"], label="Draw")
axs[2].bar(seasons, res_pct["A"], bottom=res_pct["H"] + res_pct["D"], label="Away")

axs[2].set_title("Q2 - Results Split")
axs[2].set_ylabel("%")
axs[2].legend()
axs[2].grid()


# --- graph 4 ---
# trend in away wins over time
axs[3].plot(seasons, away_pct)
axs[3].set_title("Q2 - Away Wins Trend")
axs[3].set_xlabel("Season")
axs[3].set_ylabel("Away %")

# only label some seasons to keep it readable
axs[3].set_xticks(seasons[::step])
axs[3].set_xticklabels(seasons[::step], rotation=45)

axs[3].grid()


# adjust spacing so graphs don't overlap
plt.tight_layout(h_pad=2)

# display graphs
plt.show()
