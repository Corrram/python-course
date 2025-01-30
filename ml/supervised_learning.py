import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

df = pd.read_csv("data/titanic.csv")
# Suppose df has columns: "Age", "Fare", "Pclass", "Survived"

# 1. Prepare data
df = df[["Age", "Fare", "Pclass", "Survived"]]
df.dropna(inplace=True)
X = df[["Age", "Fare", "Pclass"]]
y = df["Survived"]

# 2. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Train and Evaluate
model = LogisticRegression()  # you can specify a different model here like SVC etc.
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)
print("Accuracy:", accuracy)
# coefficients = dict(zip(X.columns, model.coef_[0]))
# print("Coefficients:", coefficients)

# 4. Predict and Evaluate
y_pred = model.predict(X_test)

cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:\n", cm)

report = classification_report(y_test, y_pred)
print("Classification Report:\n", report)
