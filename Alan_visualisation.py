# importing all relevant libraries
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# loading the dataset
df = pd.read_csv("PremierLeague.csv")
#counting the total matches per season
TotalMatches = df.groupby("Season").size()
# filter to home wins only and count per season
HomeWins = df[df["FullTimeResult"] == "H"].groupby("Season").size()
# calculating home win percentage
HomeWinPercentage = (HomeWins / TotalMatches) * 100

#plotting the information
plt.figure(figsize=(14, 6))
plt.plot(HomeWinPercentage.index, HomeWinPercentage.values, marker="o", color="blue")
x_numeric = range(len(HomeWinPercentage))
z = np.polyfit(x_numeric, HomeWinPercentage.values, 1)
p = np.poly1d(z)
plt.plot(HomeWinPercentage.index, p(x_numeric), color="orange", linestyle="--", label="Trend")
plt.title("Home Advantage in the Premier League (1993-2025)")
plt.xlabel("Season")
plt.ylabel("Home Win Percentage (%)")
plt.xticks(rotation=90)
plt.axvline(x="2020-2021", color="red", linestyle="--", label="COVID Season (No Fans)")
plt.legend()
plt.tight_layout()
plt.savefig("home_advantage.png")
plt.show()