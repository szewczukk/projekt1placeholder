import numpy as np
import csv
from random import choice, random

from product_presets import Product, laptop, mouse, screen, keyboard


def generate_point(demand: int, max_stock: int, base_price: float,
                   base_mult_at_zero_dem: float, base_mult_at_half_dem: float,
                   base_st_dev: float, st_dev_at_zero_dem: float):

    stock_coverage = demand / max_stock
    factor = 2 * (base_mult_at_half_dem - base_mult_at_zero_dem)
    multiplier = factor * stock_coverage + base_mult_at_zero_dem

    dev_factor = 2 * (1 - st_dev_at_zero_dem)
    deviation = (stock_coverage * base_st_dev * dev_factor + \
                 st_dev_at_zero_dem) * np.random.standard_normal() * 0.2

    final_price = (base_price * multiplier) + deviation
    return final_price


def generate_dataset(sample_count: int, products: list[Product],
                     max_demand_to_stock_ratio: float, max_stocksize: int):

    datapoints = list()

    for _ in range(sample_count):
        data = dict()

        product = choice(products)
        stock = int(random() * max_stocksize)
        if stock <= 0:
            stock = 1
        demand = int(random() * \
                     max_demand_to_stock_ratio * stock)

        data["in_basket"] = demand
        data["in_stock"] = stock
        data["product"] = product.name
        data["price"] = generate_point(
            demand=demand,
            max_stock=stock,
            base_price=product.base_price,
            base_mult_at_zero_dem=product.base_at_zero_dem,
            base_mult_at_half_dem=product.base_at_half_dem,
            base_st_dev=product.base_st_dev,
            st_dev_at_zero_dem=product.st_dev_at_zero_dem
        )
        datapoints.append(data)

    return datapoints


products = [laptop, mouse, screen, keyboard]
dataset = generate_dataset(1000, products=products,
                           max_demand_to_stock_ratio=1.6, max_stocksize=200)

with open("product_prices.csv", "w", newline="") as csvfile:
    fieldnames = ["in_basket", "in_stock", "product", "price"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(dataset)
