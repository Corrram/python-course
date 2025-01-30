import pandas as pd
from sklearn.linear_model import LinearRegression  # change this for ridge, lasso, etc.
from sklearn.model_selection import train_test_split

data = pd.DataFrame(
    {
        "Size": [800, 1200, 1500, 2000, 2500, 3000],
        "Rooms": [2, 3, 3, 4, 4, 5],
        "Price": [150000, 200000, 240000, 320000, 380000, 450000],
    }
)
X = data[["Size", "Rooms"]]
y = data["Price"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)
model = LinearRegression()  # change this for ridge, lasso, etc.
model.fit(X_train, y_train)
predictions = model.predict(X_test)
print("Predictions:", predictions)
print("Actual:", y_test.values)
