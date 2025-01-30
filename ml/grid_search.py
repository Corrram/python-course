import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

# Load dataset (assumes a local "titanic.csv" file)
df = pd.read_csv("data/titanic.csv")

# Basic cleaning: fill missing Age with mean
df["Age"] = df["Age"].fillna(df["Age"].mean())

# Encode "Sex" -> numeric: {male: 0, female: 1}
df["Sex"] = df["Sex"].map({"male": 0, "female": 1})

# Choose features and target
X = df[["Pclass", "Sex", "Age", "Fare"]]
y = df["Survived"]

# Set different values for C and kernel, the two parameters for
# the Support Vector Classifier (SVC) that we already saw above
param_grid = {"C": [0.1, 1, 10], "kernel": ["linear", "rbf"]}

# GridSearchCV behaves as a wrapper around the model
# and applies the different combinations of hyperparameters
model = SVC()
grid = GridSearchCV(model, param_grid, cv=3, scoring="accuracy", verbose=3)
grid.fit(X, y)

print("Best params:", grid.best_params_)
print("Best score:", grid.best_score_)
best_model = grid.best_estimator_
