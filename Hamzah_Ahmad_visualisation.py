#importing all the stuff
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


df = pd.read_csv("pl_matches.csv")

# calculating points and cards for each team stats.
team_season_data = []

for season in df["Season"].unique():
    season_df = df[df["Season"] == season]
    all_teams = set(season_df["HomeTeam"].tolist() + season_df["AwayTeam"].tolist())

    for team in all_teams:
        home = season_df[season_df["HomeTeam"] == team]
        away = season_df[season_df["AwayTeam"] == team]

        # points: win = 3, draw = 1, loss = 0
        points = (
            (home["FTR"] == "H").sum() * 3 +
            (home["FTR"] == "D").sum() +
            (away["FTR"] == "A").sum() * 3 +
            (away["FTR"] == "D").sum()
        )

        # cards: yellow = 1, red = 2
        cards = (
            home["HY"].sum() + away["AY"].sum() +
            home["HR"].sum() * 2 + away["AR"].sum() * 2
        )

        team_season_data.append({"Season": season, "Team": team, "Points": points, "Cards": cards})

stats = pd.DataFrame(team_season_data)

#  Scatter plot of cards vs points 

plt.figure(figsize=(8, 5))
plt.scatter(stats["Cards"], stats["Points"], alpha=0.4, color="steelblue", s=20)

# trend line
z = np.polyfit(stats["Cards"], stats["Points"], 1)
p = np.poly1d(z)
x_line = np.linspace(stats["Cards"].min(), stats["Cards"].max(), 100)
plt.plot(x_line, p(x_line), color="orange", linestyle="--", label="Trend")

# correlation value
r = stats["Cards"].corr(stats["Points"])
plt.text(0.97, 0.97, f"r = {r:.3f}", transform=plt.gca().transAxes,
         ha="right", va="top", fontsize=10,
         bbox=dict(boxstyle="round", facecolor="white", alpha=0.7))

plt.title("Cards vs Points Per Team Per Season")
plt.xlabel("Total Cards (Yellow + 2x Red)")
plt.ylabel("Season Points")
plt.legend()
plt.tight_layout()
plt.savefig("cards_vs_points_scatter.png")
plt.show()

# Average points by card volume band 

bins   = [0, 25, 40, 55, 70, 999]
labels = ["0-25", "26-40", "41-55", "56-70", "70+"]
stats["CardBand"] = pd.cut(stats["Cards"], bins=bins, labels=labels)
avg_points = stats.groupby("CardBand", observed=True)["Points"].mean()

plt.figure(figsize=(8, 5))
plt.bar(avg_points.index, avg_points.values, color=["green", "steelblue", "gold", "orange", "red"])

for i, val in enumerate(avg_points.values):
    plt.text(i, val + 0.3, f"{val:.0f} pts", ha="center", fontsize=10, fontweight="bold")

plt.title("Average Points by Card Volume Band")
plt.xlabel("Total Cards Received That Season")
plt.ylabel("Average Points")
plt.tight_layout()
plt.savefig("cards_vs_points_bands.png")
plt.show()
