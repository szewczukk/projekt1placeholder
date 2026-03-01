from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

app = FastAPI(title="Shop API", description="Projekt sklepu z 4 produktami")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

products_db: List[Product] = [
    Product(
        id=1,
        name="Laptop",
        description="Nowoczesny laptop z procesorem Intel i7",
        price=3999.99,
        quantity=5
    ),
    Product(
        id=2,
        name="Mysz bezprzewodowa",
        description="Ergonomiczna mysz bezprzewodowa z baterią na 18 miesięcy",
        price=149.99,
        quantity=25
    ),
    Product(
        id=3,
        name="Monitor 4K",
        description="Monitor 27 cali z rozdzielczością 4K UHD",
        price=1299.99,
        quantity=8
    ),
    Product(
        id=4,
        name="Klawiatura mechaniczna",
        description="Klawiatura mechaniczna RGB z przełącznikami Cherry MX",
        price=599.99,
        quantity=12
    ),
]

@app.get("/products", response_model=List[Product])
async def get_all_products():
    """Zwraca listę wszystkich produktów w sklepie"""
    return products_db

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    """Zwraca informacje o konkretnym produkcie"""
    for product in products_db:
        if product.id == product_id:
            return product
    return {"error": "Produkt nie znaleziony"}

@app.get("/products/count")
async def get_products_count():
    """Zwraca liczbę produktów"""
    return {"total_products": len(products_db)}

@app.get("/")
async def root():
    """Strona główna API sklepu"""
    return {
        "message": "Witaj w Shop API",
        "version": "1.0.0",
        "endpoints": {
            "all_products": "/products",
            "product_by_id": "/products/{product_id}",
            "products_count": "/products/count"
        }
    }

# Endpoint: Status sklepu
@app.get("/status")
async def get_status():
    """Zwraca status sklepu"""
    return {
        "status": "online",
        "products_available": len(products_db),
        "total_value": sum(p.price * p.quantity for p in products_db)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
