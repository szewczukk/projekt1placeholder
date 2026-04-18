import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import pickle
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

df = pd.read_csv("product_prices.csv")

X = df.drop("price", axis=1)

X_in_basket = X["in_basket"]
X_in_stock = X["in_stock"]

X["coverage"] = X_in_basket / X_in_stock
X.drop(columns=["in_basket", "in_stock"], inplace=True)

y = df["price"]
X_new = pd.get_dummies(X, drop_first=False)

X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size=0.2,
                                                    random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = RandomForestRegressor()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
mape = mean_absolute_percentage_error(y_test, y_pred)

print("MSE:", mse, sep="\n")
print("MAPE:", mape, sep="\n")

pickle_data = {"model": model, "scaler": scaler, "X_base": X_new[0:0]}
with open("model.pkl", "wb") as file:
    pickle.dump(pickle_data, file, protocol=pickle.HIGHEST_PROTOCOL)
