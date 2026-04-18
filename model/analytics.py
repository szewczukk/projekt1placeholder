import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import pickle

df = pd.read_csv("product_prices.csv")
print(df.head())
print(df.isnull().sum())
print(df.describe())
print(df.info())


def eda(df, column):
    if df[column].dtype == "str":
        sns.boxplot(data=df, x=column, y="price")
        plt.show()
    else:
        sns.scatterplot(data=df, x=column, y="price")
        plt.show()


for column in df.columns:
    if column == "price":
        continue
    eda(df, column)

sns.heatmap(df.corr(numeric_only=True), annot=True)
plt.show()

with open("model.pkl", "rb") as file:
    pickle_data = pickle.load(file)

model = pickle_data["model"]

X = df.drop("price", axis=1)
X_in_basket = X["in_basket"]
X_in_stock = X["in_stock"]

X["coverage"] = X_in_basket / X_in_stock
X.drop(columns=["in_basket", "in_stock"], inplace=True)

X_new = pd.get_dummies(X, drop_first=False)
feature_imp = model.feature_importances_
feature = X_new.columns

imp_df = pd.DataFrame({"Feature":feature, "Importance":feature_imp})
print(imp_df.sort_values("Importance", ascending=False))

plt.barh(imp_df["Feature"], imp_df["Importance"], color="skyblue")
