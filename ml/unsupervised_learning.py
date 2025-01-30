import matplotlib.pyplot as plt
import pandas as pd

from sklearn.cluster import DBSCAN, KMeans

# generate sample data
df = pd.read_csv("data/titanic.csv")
df = df[["Age", "Fare"]].dropna().reset_index(drop=True)
X = df.values
dbscan = DBSCAN(eps=10, min_samples=5)
labels = dbscan.fit_predict(X)

inertia = []
for k in range(1, 10):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(X)
    inertia.append(kmeans.inertia_)

plt.plot(range(1, 10), inertia)
plt.xlabel("k")
plt.ylabel("Inertia")
plt.title("Inertia of k-Means versus number of clusters")
plt.grid()
plt.show()
