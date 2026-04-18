import pickle
import warnings
import os

from .product_presets import ProductCurrent, ProductName

warnings.filterwarnings("ignore")

# Ścieżka do model.pkl względem katalogu model/
model_path = os.path.join(os.path.dirname(__file__), '..', 'model.pkl')
with open(model_path, "rb") as file:
    pickle_data = pickle.load(file)

model = pickle_data["model"]
scaler = pickle_data["scaler"]
X = pickle_data["X_base"]


def get_prediction(product: ProductCurrent):
    product_data = [product.current_demand, product.current_stock, 0, 0, 0, 0]

    match(product.name):
        case ProductName.KEYBOARD.value:
            product_data[2] = 1
        case ProductName.LAPTOP.value:
            product_data[3] = 1
        case ProductName.SCREEN.value:
            product_data[4] = 1
        case ProductName.MOUSE.value:
            product_data[5] = 1

    X.loc[0] = product_data
    predicted = model.predict(X)
    return predicted[0]
