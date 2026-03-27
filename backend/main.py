from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

class CartItem(BaseModel):
    product_id: int
    quantity: int

class AddToCartRequest(BaseModel):
    user_id: int
    product_id: int
    quantity: int

class CreateSessionRequest(BaseModel):
    user_id: int

class RemoveFromCartRequest(BaseModel):
    user_id: int
    product_id: int

class CheckoutRequest(BaseModel):
    user_id: int

class CheckoutLineItem(BaseModel):
    product_id: int
    name: str
    quantity: int
    unit_price: float
    subtotal: float

class CheckoutResponse(BaseModel):
    order_id: int
    user_id: int
    items: List[CheckoutLineItem]
    total: float
    message: str

app = FastAPI(
    title="Shop API",
    description="Projekt sklepu z 4 produktami",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Shop API Support",
        "email": "support@shopapi.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

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

cart_db: Dict[int, Dict[int, int]] = {}  # {user_id: {product_id: quantity}}
order_id_counter: int = 0

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
            "products_count": "/products/count",
            "cart_checkout": "/cart/checkout"
        }
    }

# Endpoint: Realizacja zamówienia (checkout koszyka)
@app.post("/cart/checkout", response_model=CheckoutResponse)
async def checkout_cart(request: CheckoutRequest):
    """Realizuje zamówienie: sprawdza stany magazynowe, pomniejsza ilości, czyści koszyk."""
    if request.user_id not in cart_db or not cart_db[request.user_id]:
        raise HTTPException(status_code=400, detail="Koszyk jest pusty")

    cart = cart_db[request.user_id]
    product_by_id = {p.id: p for p in products_db}

    for product_id, qty in cart.items():
        if product_id not in product_by_id:
            raise HTTPException(
                status_code=400,
                detail=f"Produkt o id={product_id} nie istnieje — usuń go z koszyka",
            )
        product = product_by_id[product_id]
        if product.quantity < qty:
            raise HTTPException(
                status_code=409,
                detail=(
                    f"Niewystarczający stan magazynowy dla „{product.name}”: "
                    f"dostępne {product.quantity}, w koszyku {qty}"
                ),
            )

    global order_id_counter
    order_id_counter += 1
    line_items: List[CheckoutLineItem] = []
    total = 0.0

    for product_id, qty in cart.items():
        product = product_by_id[product_id]
        product.quantity -= qty
        subtotal = round(product.price * qty, 2)
        total += subtotal
        line_items.append(
            CheckoutLineItem(
                product_id=product_id,
                name=product.name,
                quantity=qty,
                unit_price=product.price,
                subtotal=subtotal,
            )
        )

    total = round(total, 2)
    cart_db[request.user_id] = {}

    return CheckoutResponse(
        order_id=order_id_counter,
        user_id=request.user_id,
        items=line_items,
        total=total,
        message="Zamówienie zrealizowane pomyślnie",
    )

# Endpoint: Dodanie produktu do koszyka
@app.post("/cart/add")
async def add_to_cart(request: AddToCartRequest):
    """Dodaje produkt do koszyka użytkownika"""
    # Sprawdzenie czy produkt istnieje
    product = None
    for p in products_db:
        if p.id == request.product_id:
            product = p
            break
    
    if not product:
        raise HTTPException(status_code=404, detail="Produkt nie znaleziony")
    
    if request.quantity <= 0:
        raise HTTPException(status_code=400, detail="Ilość musi być większa niż 0")
    
    # Inicjalizacja koszyka użytkownika jeśli nie istnieje
    if request.user_id not in cart_db:
        cart_db[request.user_id] = {}
    
    # Dodanie do koszyka lub aktualizacja ilości
    if request.product_id in cart_db[request.user_id]:
        cart_db[request.user_id][request.product_id] += request.quantity
    else:
        cart_db[request.user_id][request.product_id] = request.quantity
    
    return {
        "status": "success",
        "message": f"Dodano {request.quantity} szt. produktu '{product.name}' do koszyka",
        "user_id": request.user_id,
        "product_id": request.product_id,
        "quantity_in_cart": cart_db[request.user_id][request.product_id]
    }

# Endpoint: Usunięcie produktu z koszyka
@app.delete("/cart/remove")
async def remove_from_cart(request: RemoveFromCartRequest):
    """Usuwa produkt z koszyka użytkownika"""
    if request.user_id not in cart_db:
        raise HTTPException(status_code=404, detail="Sesja użytkownika nie znaleziona")
    
    if request.product_id not in cart_db[request.user_id]:
        raise HTTPException(status_code=404, detail="Produkt nie znajduje się w koszyku")
    
    # Znalezienie produktu dla nazwy
    product = None
    for p in products_db:
        if p.id == request.product_id:
            product = p
            break
    
    del cart_db[request.user_id][request.product_id]
    
    return {
        "status": "success",
        "message": f"Usunięto produkt '{product.name if product else 'nieznany'}' z koszyka",
        "user_id": request.user_id,
        "product_id": request.product_id
    }

# Endpoint: Tworzenie sesji użytkownika
@app.post("/sessions", status_code=204)
async def create_session(request: CreateSessionRequest):
    """Tworzy nową sesję (koszyk) dla użytkownika"""
    if request.user_id not in cart_db:
        cart_db[request.user_id] = {}

# Endpoint: Usunięcie sesji użytkownika
@app.delete("/sessions/{user_id}", status_code=204)
async def delete_session(user_id: int):
    """Usuwa sesję (koszyk) użytkownika"""
    if user_id in cart_db:
        del cart_db[user_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
