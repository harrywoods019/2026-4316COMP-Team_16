import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Function to convert odds to probability
# -----------------------------
def oddsToProbability(odds):
    return 1 / odds

# -----------------------------
# Function to determine predicted result
# -----------------------------
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

# -----------------------------
# Load dataset
# -----------------------------
data = pd.read_csv("PremierLeague.csv")
data = data[data['Season'] >= '2002-03']
data = data.reset_index(drop=True)
data = data.dropna(subset=['B365HomeTeam', 'B365Draw', 'B365AwayTeam'])


results = data['FullTimeResult']
homeOdds = data['B365HomeTeam']
drawOdds = data['B365Draw']
awayOdds = data['B365AwayTeam']

correct = 0
total = 0

predictedProbability = []
actualResults = []

# -----------------------------
# Loop through matches
# -----------------------------
for i in range(len(data)):

    pred, prob = predictResult(homeOdds[i], drawOdds[i], awayOdds[i])
    actual = results[i]

    if pred == actual:
        correct += 1
        actualResults.append(1)
    else:
        actualResults.append(0)

    predictedProbability.append(prob)
    total += 1

# -----------------------------
# Accuracy
# -----------------------------
accuracy = correct / total
print(f"Prediction Accuracy: {accuracy:.2f}")

# -----------------------------
# VISUALISATION 1: Bar Chart
# -----------------------------
plt.figure()
plt.bar(['Correct', 'Incorrect'], [correct, total - correct])
plt.title("Betting Odds Prediction Accuracy")
plt.ylabel("Number of Matches")
plt.show()

