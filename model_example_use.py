from model.model import get_prediction
from model.product_presets import ProductCurrent, ProductName

product = ProductCurrent(name=ProductName.LAPTOP,
                         current_demand=0,
                         current_stock=5)
print(get_prediction(product=product))
