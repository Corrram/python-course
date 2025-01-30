import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow import keras

# 1. Load dataset (assumes a local "titanic.csv" file)
df = pd.read_csv("data/titanic.csv")

# 2. Basic cleaning: fill missing Age with mean
df["Age"] = df["Age"].fillna(df["Age"].mean())

# 3. Encode "Sex" -> numeric: {male: 0, female: 1}
df["Sex"] = df["Sex"].map({"male": 0, "female": 1})

# 4. Choose features and target
X = df[["Pclass", "Sex", "Age", "Fare"]]
y = df["Survived"]

# 5. Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 6. Build the Keras model (Sequential API)
model = keras.Sequential([
    keras.layers.InputLayer(shape=(4,)),
    keras.layers.Dense(8, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

# 7. Compile the model
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# 8. Train (fit) the model
model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=0)

# 9. Evaluate on test set
loss, acc = model.evaluate(X_test, y_test)
print(f"Test Loss: {loss:.4f}, Test Accuracy: {acc:.4f}")

# 10. Predict on first 5 rows in the test set
predictions = model.predict(X_test[:5])
print("Predictions (probability of survival):")
print(predictions)
model.save("my_keras_model.h5")