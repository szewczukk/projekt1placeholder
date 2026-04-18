import pickle
import warnings

from .product_presets import ProductCurrent, ProductName

warnings.filterwarnings("ignore")

with open("model.pkl", "rb") as file:
    pickle_data = pickle.load(file)

model = pickle_data["model"]
scaler = pickle_data["scaler"]
X = pickle_data["X_base"]


def get_prediction(product: ProductCurrent):
    product_data = [product.current_demand/product.current_stock, 0, 0, 0, 0]
    column_order = list()
    column_names = ["product_" + prd.value for prd in ProductName]

    for column in X.columns:
        if column in column_names:
            column_order.append(column)

    column_id = column_order.index("product_" + product.name)
    product_data[column_id+1] = 1

    X.loc[0] = product_data
    predicted = model.predict(X)
    return predicted[0]
