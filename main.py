"""
4316COMP Team 16 - Premier League Data Analysis
================================================
Combined entry point. Run this file to display all team visualisations.
 
Each team member's work is wrapped in its own function:
  - run_alan()   : Home advantage trend (1993-2025)
  - run_harry()  : Betting odds prediction accuracy
  - run_hamzah() : Cards vs points analysis
  - run_dylan()  : Shots vs goals & fouls vs points
  - run_tom()    : Match competitiveness & result trends
 
CSV files required in the same directory as this script:
  - PremierLeague.csv   (used by Alan, Harry, Dylan, Tom)
  - pl_matches.csv      (used by Hamzah)
"""
 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
 
# Make sure relative file paths work wherever the script is run from
os.chdir(os.path.dirname(os.path.abspath(__file__)))
 
 
# ==============================================================
# ALAN — Home Advantage Trend
# ==============================================================
def run_alan():
    print("\n[Alan] Home Advantage Visualisation...")
    df = pd.read_csv("PremierLeague.csv")
 
    total_matches = df.groupby("Season").size()
    home_wins = df[df["FullTimeResult"] == "H"].groupby("Season").size()
    home_win_pct = (home_wins / total_matches) * 100
 
    plt.figure(figsize=(14, 6))
    plt.plot(home_win_pct.index, home_win_pct.values, marker="o", color="blue", label="Home Win %")
 
    x_numeric = range(len(home_win_pct))
    z = np.polyfit(x_numeric, home_win_pct.values, 1)
    p = np.poly1d(z)
    plt.plot(home_win_pct.index, p(x_numeric), color="orange", linestyle="--", label="Trend")
 
    plt.title("Home Advantage in the Premier League (1993-2025)")
    plt.xlabel("Season")
    plt.ylabel("Home Win Percentage (%)")
    plt.xticks(rotation=90)
    plt.axvline(x="2020-2021", color="red", linestyle="--", label="COVID Season (No Fans)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("home_advantage.png")
    plt.show()
    print("[Alan] Done. Saved: home_advantage.png")
 
 
# ==============================================================
# HARRY — Betting Odds Prediction Accuracy
# ==============================================================
def odds_to_probability(odds):
    return 1 / odds
 
def predict_result(home_odds, draw_odds, away_odds):
    home_prob = odds_to_probability(home_odds)
    draw_prob = odds_to_probability(draw_odds)
    away_prob = odds_to_probability(away_odds)
 
    if home_prob > draw_prob and home_prob > away_prob:
        return 'H', home_prob
    elif draw_prob > home_prob and draw_prob > away_prob:
        return 'D', draw_prob
    else:
        return 'A', away_prob
 
def run_harry():
    print("\n[Harry] Betting Odds Prediction Accuracy...")
    data = pd.read_csv("PremierLeague.csv")
    data = data[data['Season'] >= '2002-03'].reset_index(drop=True)
    data = data.dropna(subset=['B365HomeTeam', 'B365Draw', 'B365AwayTeam'])
 
    correct = 0
    total = 0
 
    for i in range(len(data)):
        pred, _ = predict_result(
            data['B365HomeTeam'][i],
            data['B365Draw'][i],
            data['B365AwayTeam'][i]
        )
        if pred == data['FullTimeResult'][i]:
            correct += 1
        total += 1
 
    accuracy = correct / total
    print(f"[Harry] Prediction Accuracy: {accuracy:.2%}")
 
    plt.figure()
    plt.bar(['Correct', 'Incorrect'], [correct, total - correct], color=['steelblue', 'salmon'])
    plt.title(f"Betting Odds Prediction Accuracy ({accuracy:.2%})")
    plt.ylabel("Number of Matches")
    plt.tight_layout()
    plt.show()
    print("[Harry] Done.")
 
 
# ==============================================================
# HAMZAH — Cards vs Points Analysis
# ==============================================================
def run_hamzah():
    print("\n[Hamzah] Cards vs Points Analysis...")
    df = pd.read_csv("PremierLeague.csv")
 
    team_season_data = []
    for season in df["Season"].unique():
        season_df = df[df["Season"] == season]
        all_teams = set(season_df["HomeTeam"].tolist() + season_df["AwayTeam"].tolist())
 
        for team in all_teams:
            home = season_df[season_df["HomeTeam"] == team]
            away = season_df[season_df["AwayTeam"] == team]
 
            points = (
                (home["FullTimeResult"] == "H").sum() * 3 +
                (home["FullTimeResult"] == "D").sum() +
                (away["FullTimeResult"] == "A").sum() * 3 +
                (away["FullTimeResult"] == "D").sum()
            )
            cards = (
                home["HomeTeamYellowCards"].sum() + away["AwayTeamYellowCards"].sum() +
                home["HomeTeamRedCards"].sum() * 2 + away["AwayTeamRedCards"].sum() * 2
            )
            team_season_data.append({"Season": season, "Team": team, "Points": points, "Cards": cards})
 
    stats = pd.DataFrame(team_season_data)
 
    # Scatter: Cards vs Points
    plt.figure(figsize=(8, 5))
    plt.scatter(stats["Cards"], stats["Points"], alpha=0.4, color="steelblue", s=20)
 
    z = np.polyfit(stats["Cards"], stats["Points"], 1)
    p = np.poly1d(z)
    x_line = np.linspace(stats["Cards"].min(), stats["Cards"].max(), 100)
    plt.plot(x_line, p(x_line), color="orange", linestyle="--", label="Trend")
 
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
 
    # Bar: Average points by card volume band
    bins = [0, 25, 40, 55, 70, 999]
    labels = ["0-25", "26-40", "41-55", "56-70", "70+"]
    stats["CardBand"] = pd.cut(stats["Cards"], bins=bins, labels=labels)
    avg_points = stats.groupby("CardBand", observed=True)["Points"].mean()
 
    plt.figure(figsize=(8, 5))
    bars = plt.bar(avg_points.index, avg_points.values,
                   color=["green", "steelblue", "gold", "orange", "red"])
 
    for i, val in enumerate(avg_points.values):
        plt.text(i, val + 0.3, f"{val:.0f} pts", ha="center", fontsize=10, fontweight="bold")
 
    plt.title("Average Points by Card Volume Band")
    plt.xlabel("Total Cards Received That Season")
    plt.ylabel("Average Points")
    plt.tight_layout()
    plt.savefig("cards_vs_points_bands.png")
    plt.show()
    print("[Hamzah] Done. Saved: cards_vs_points_scatter.png, cards_vs_points_bands.png")
 
 
# ==============================================================
# DYLAN — Shots vs Goals & Fouls vs Points
# ==============================================================
def run_dylan():
    print("\n[Dylan] Shots/Goals & Fouls/Points Analysis...")
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
 
    # 2 graphs in 1 window
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
 
    # Shots vs Goals
    axes[0].scatter(
        home_stats["HomeTeamShots"],
        home_stats["FullTimeHomeTeamGoals"]
    )
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
 
    # Graph 2
    axes[1].scatter(
        foul_points["HomeTeamFouls"],
        foul_points["HomeTeamPoints"]
    )
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
    print("[Dylan] Done.")
 
 
# ==============================================================
# TOM — Match Competitiveness & Result Trends
# ==============================================================
def run_tom():
    print("\n[Tom] Match Competitiveness & Result Trends...")
    df = pd.read_csv("PremierLeague.csv")
 
    df["goal_diff"] = abs(df["FullTimeHomeTeamGoals"] - df["FullTimeAwayTeamGoals"])
    avg_diff = df.groupby("Season")["goal_diff"].mean()
 
    big_wins = df[df["goal_diff"] >= 2]
    one_sided_pct = (big_wins.groupby("Season").size() / df.groupby("Season").size()) * 100
 
    res_counts = df.groupby(["Season", "FullTimeResult"]).size().unstack().fillna(0)
    res_pct = res_counts.div(res_counts.sum(axis=1), axis=0) * 100
    away_pct = res_pct["A"]
 
    fig, axs = plt.subplots(4, 1, figsize=(12, 14), sharex=True)
    seasons = avg_diff.index
    step = 3
 
    axs[0].plot(seasons, avg_diff)
    axs[0].set_title("Avg Goal Difference per Season")
    axs[0].set_ylabel("Goal Diff")
    axs[0].grid()
 
    axs[1].bar(seasons, one_sided_pct)
    axs[1].set_title("% One-Sided Games per Season (goal diff ≥ 2)")
    axs[1].set_ylabel("%")
    axs[1].grid()
 
    axs[2].bar(seasons, res_pct["H"], label="Home Win")
    axs[2].bar(seasons, res_pct["D"], bottom=res_pct["H"], label="Draw")
    axs[2].bar(seasons, res_pct["A"], bottom=res_pct["H"] + res_pct["D"], label="Away Win")
    axs[2].set_title("Result Split per Season")
    axs[2].set_ylabel("%")
    axs[2].legend()
    axs[2].grid()
 
    axs[3].plot(seasons, away_pct)
    axs[3].set_title("Away Win % Trend")
    axs[3].set_xlabel("Season")
    axs[3].set_ylabel("Away %")
    axs[3].set_xticks(seasons[::step])
    axs[3].set_xticklabels(seasons[::step], rotation=45)
    axs[3].grid()
 
    plt.tight_layout(h_pad=2)
    plt.show()
    print("[Tom] Done.")
 
 
# ==============================================================
# MAIN — Run all visualisations
# ==============================================================
if __name__ == "__main__":
    print("=" * 50)
    print(" 4316COMP Team 16 — PL Data Analysis")
    print("=" * 50)
 
    run_alan()
    run_harry()
    run_hamzah()
    run_dylan()
    run_tom()
 
    print("\n All visualisations complete.")