import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from sklearn.model_selection import train_test_split

# 1. Load dataset (assumes a local "titanic.csv" file)
df = pd.read_csv("data/titanic.csv")

# 2. Basic cleaning: fill missing Age with mean
df["Age"] = df["Age"].fillna(df["Age"].mean())

# 3. Encode "Sex" -> numeric: {male: 0, female: 1}
df["Sex"] = df["Sex"].map({"male": 0, "female": 1})

# 4. Choose features (Pclass, Sex, Age, Fare) and target (Survived)
X = df[["Pclass", "Sex", "Age", "Fare"]].values
y = df["Survived"].values

# 5. Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Convert NumPy arrays to PyTorch tensors
X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.float32)

# 6. Build a simple feedforward network
model = nn.Sequential(
    nn.Linear(4, 8),  # input: 4 features, hidden: 8 neurons
    nn.ReLU(),
    nn.Linear(8, 1)  # output: 1 neuron (logit for binary classification)
)

# 7. Define loss function & optimizer
criterion = nn.BCEWithLogitsLoss()  # combines sigmoid + BCELoss
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 8. Training loop
num_epochs = 20
for epoch in range(num_epochs):
    model.train()

    # 8a. Reset gradients
    optimizer.zero_grad()

    # 8b. Forward pass
    outputs = model(X_train).flatten()  # shape: [batch_size]

    # 8c. Compute loss
    loss = criterion(outputs, y_train)

    # 8d. Backprop
    loss.backward()
    optimizer.step()

    # (Optional) Print training progress every 5 epochs
    if (epoch + 1) % 5 == 0:
        with torch.no_grad():
            predictions = torch.sigmoid(outputs)
            pred_labels = (predictions > 0.5).float()
            accuracy = (pred_labels == y_train).float().mean()
            print(f"Epoch [{epoch + 1}/{num_epochs}] - Loss: {loss.item():.4f}, "
                  f"Train Accuracy: {accuracy.item():.4f}")

# 9. Evaluate on test set
model.eval()
with torch.no_grad():
    test_outputs = model(X_test).flatten()
    test_preds = torch.sigmoid(test_outputs)
    test_labels = (test_preds > 0.5).float()
    test_accuracy = (test_labels == y_test).float().mean()
    print(f"Test Accuracy: {test_accuracy.item():.4f}")

# 10. Predict on first 5 rows in the test set
with torch.no_grad():
    sample_outputs = model(X_test[:5]).flatten()
    sample_preds = torch.sigmoid(sample_outputs)
    print("Predictions (probability of survival) for first 5 test samples:")
    print(sample_preds.tolist())
