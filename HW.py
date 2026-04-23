#This imports all the packages needed to create visualisation graphs
import pandas as pd
import matplotlib.pyplot as plt

#This turns odds to probability so we can work with it easier 

def oddsToProbability(odds):
    return 1 / odds

# Function that determines predicted result

def predictResult(homeOdds, drawOdds, awayOdds):
    homeProbability = oddsToProbability(homeOdds)
    drawProbability = oddsToProbability(drawOdds)
    awayProbability = oddsToProbability(awayOdds)

    # choose highest probability
    if homeProbability > drawProbability and homeProbability > awayProbability:
        return 'H', homeProbability
    elif drawProbability > homeProbability and drawProbability > awayProbability:
        return 'D', drawProbability
    else:
        return 'A', awayProbability

#This section loads the dataset

data = pd.read_csv("PremierLeague.csv")
data = data[data['Season'] >= '2002-03']
data = data.reset_index(drop=True)
data = data.dropna(subset=['B365HomeTeam', 'B365Draw', 'B365AwayTeam'])


results = data['FullTimeResult']
homeOdds = data['B365HomeTeam']
drawOdds = data['B365Draw']
awayOdds = data['B365AwayTeam']
seasons = data['Season']

correct = 0
total = 0

predictedProbability = []
actualResults = []
seasonList = []

#This section loops through all the matches in the dataset

for i in range(len(data)):

    pred, prob = predictResult(homeOdds[i], drawOdds[i], awayOdds[i])
    actual = results[i]
    season = seasons[i]

    if pred == actual:
        correct += 1
        actualResults.append(1)
    else:
        actualResults.append(0)

    predictedProbability.append(prob)
    seasonList.append(season)
    total += 1

# Visualisation 1 - Showing how many matches Bet365 predicted right
accuracy = correct / total
print(f"Prediction Accuracy: {accuracy:.2f}")

plt.figure()
plt.bar(['Correct', 'Incorrect'], [correct, total - correct])
plt.title("Betting Odds Prediction Accuracy")
plt.ylabel("Number of Matches")

#Visualisation 2 - Showing a season by season accuracy trend

seasonResults = pd.DataFrame({
    'Season': seasonList,
    'Correct': actualResults
})

seasonAccuracy = seasonResults.groupby('Season')['Correct'].mean()

plt.figure(figsize=(10, 5))
plt.plot(seasonAccuracy.index, seasonAccuracy.values, marker='o')
plt.title("Betting Odds Prediction Accuracy by Season")
plt.xlabel("Season")
plt.ylabel("Accuracy")
plt.xticks(rotation=45)
plt.ylim(0, 1)
plt.grid(True)
plt.tight_layout()


plt.show()
