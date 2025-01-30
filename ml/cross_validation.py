from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
import pandas as pd

df = pd.read_csv("data/titanic.csv").dropna()
X = df[["Age", "Fare", "Pclass"]]
y = df["Survived"]

model = LogisticRegression()
scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
print("CV Accuracy Scores:", scores)
print("Mean accuracy:", scores.mean())
