import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("PremierLeague.csv")


# Shots vs Goals
home_stats = df.groupby("HomeTeam").agg({
    "HomeTeamShots": "sum",
    "FullTimeHomeTeamGoals": "sum"
}).reset_index()

# Fouls vs Points
foul_points = df.groupby("HomeTeam").agg({
    "HomeTeamFouls": "sum",
    "HomeTeamPoints": "sum"
}).reset_index()

# CREATE SUBPLOTS (2 graphs in 1 window)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))


# Shots vs Goals

axes[0].scatter(
    home_stats["HomeTeamShots"],
    home_stats["FullTimeHomeTeamGoals"]
)

# labels
for i in range(len(home_stats)):
    axes[0].text(
        home_stats["HomeTeamShots"][i] + 5,
        home_stats["FullTimeHomeTeamGoals"][i] + 0.5,
        home_stats["HomeTeam"][i],
        fontsize=6
    )

axes[0].set_xlabel("Total Shots")
axes[0].set_ylabel("Total Goals")
axes[0].set_title("Shots vs Goals Efficiency")


# graph 2


axes[1].scatter(
    foul_points["HomeTeamFouls"],
    foul_points["HomeTeamPoints"]
)

# team labels
for i in range(len(foul_points)):
    axes[1].text(
        foul_points["HomeTeamFouls"][i] + 5,
        foul_points["HomeTeamPoints"][i] + 0.5,
        foul_points["HomeTeam"][i],
        fontsize=6
    )

axes[1].set_xlabel("Total Fouls")
axes[1].set_ylabel("Total Points")
axes[1].set_title("Fouls vs Points")


plt.tight_layout()
plt.show()