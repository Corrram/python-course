import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA

df = pd.read_csv("data/titanic.csv")
X = df[["Pclass", "Age", "SibSp", "Parch", "Fare"]].dropna().values

pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

print("Reduced shape:", X_reduced.shape)
print("Explained variance ratio:", pca.explained_variance_ratio_)
# the weights show we should scale the data, compare feature_engineering.py:
print("Weights:", pca.components_)

# plot X_reduced
plt.scatter(X_reduced[:, 0], X_reduced[:, 1])
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("Titanic Data PCA")
plt.show()
