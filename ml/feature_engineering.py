import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures, StandardScaler

df = pd.DataFrame({
    "City": ["London", "Paris", None, "London", "Berlin"],
    "Rooms": [3, 2, 4, 3, 2],
    "Price": [200, 180, 300, 220, 190]
})

# 1) Imputation for missing City
df["City"] = df["City"].replace({None: np.nan})  # only np.nan recognized as missing
imputer = SimpleImputer(strategy="most_frequent")
df["City"] = imputer.fit_transform(df[["City"]])[:, 0]

# 2) One-Hot Encode 'City'
ohe = OneHotEncoder()
city_encoded_sparse = ohe.fit_transform(df[["City"]])
city_encoded_dense = city_encoded_sparse.toarray()
df_ohe = pd.DataFrame(city_encoded_dense, columns=ohe.get_feature_names_out(["City"]))

df_final = pd.concat([df.reset_index(drop=True), df_ohe], axis=1)

# 3) Polynomial Features on 'Rooms'
poly = PolynomialFeatures(degree=2, include_bias=False)
rooms_poly = poly.fit_transform(df_final[["Rooms"]])
df_final["Rooms^2"] = rooms_poly[:, 1]

# 4) Standardize numeric features: Rooms, Rooms^2, Price (example)
scaler = StandardScaler()
df_final[["Rooms", "Rooms^2", "Price"]] = scaler.fit_transform(df_final[["Rooms", "Rooms^2", "Price"]])

print(df_final)
