from pydantic import BaseModel, Field
from enum import Enum



class ProductName(Enum):
    LAPTOP = "laptop"
    MOUSE = "Mysz bezprzewodowa"
    SCREEN = "Monitor 4K"
    KEYBOARD = "Klawiatura mechaniczna"



class ProductCurrent(BaseModel):
    name: str = Field(min_length=1)
    current_demand: int
    current_stock: int



class Product(BaseModel):
    name: str = Field(min_length=1)
    base_price: float = Field(ge=0)
    base_at_zero_dem: float = Field(default=0.5, ge=0)
    base_at_half_dem: float = Field(default=1, ge=0)
    base_st_dev: float = Field(default=0.5, ge=0)
    st_dev_at_zero_dem: float = Field(default=1, ge=0)



laptop = Product(
    name=ProductName.LAPTOP,
    base_price=3999.99,
    base_at_zero_dem=0.8,
    base_at_half_dem=0.9,
    base_st_dev=100,
    st_dev_at_zero_dem=0.1
)

mouse = Product(
    name=ProductName.MOUSE,
    base_price=149.99,
    base_at_zero_dem=0.7,
    base_at_half_dem=0.9,
    base_st_dev=20,
    st_dev_at_zero_dem=0.1
)

screen = Product(
    name=ProductName.SCREEN,
    base_price=1299.99,
    base_at_zero_dem=0.95,
    base_at_half_dem=1.2,
    base_st_dev=120,
    st_dev_at_zero_dem=0
)

keyboard = Product(
    name=ProductName.KEYBOARD,
    base_price=599.99,
    base_at_zero_dem=0.4,
    base_at_half_dem=0.7,
    base_st_dev=50,
    st_dev_at_zero_dem=0.3
)
