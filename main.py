from fastapi import FastAPI, Query

app = FastAPI()

# ✅ Sample products
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"},
]

# ✅ Orders list
orders = []


# -------------------------------
# BASIC ENDPOINT
# -------------------------------
@app.get("/")
def home():
    return {"message": "API is running"}


# -------------------------------
# SEARCH PRODUCTS
# -------------------------------
@app.get("/products/search")
def search_products(keyword: str):
    result = [p for p in products if keyword.lower() in p["name"].lower()]

    if not result:
        return {"message": f"No products found for: {keyword}"}

    return {"total": len(result), "products": result}


# -------------------------------
# SORT PRODUCTS
# -------------------------------
@app.get("/products/sort")
def sort_products(sort_by: str = "price", order: str = "asc"):

    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}

    result = sorted(
        products,
        key=lambda p: p[sort_by],
        reverse=(order == "desc")
    )

    return {"products": result}


# -------------------------------
# PAGINATION
# -------------------------------
@app.get("/products/page")
def paginate(page: int = 1, limit: int = 2):

    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total_pages": -(-len(products) // limit),
        "products": products[start:end]
    }


# -------------------------------
# ADD ORDER
# -------------------------------
@app.post("/orders")
def add_order(order: dict):
    order["order_id"] = len(orders) + 1
    orders.append(order)
    return {"message": "Order added", "order": order}


# -------------------------------
# Q4: SEARCH ORDERS
# -------------------------------
@app.get("/orders/search")
def search_orders(customer_name: str):
    result = [o for o in orders if customer_name.lower() in o["customer_name"].lower()]

    if not result:
        return {"message": f"No orders found for: {customer_name}"}

    return {"total": len(result), "orders": result}


# -------------------------------
# Q5: SORT BY CATEGORY + PRICE
# -------------------------------
@app.get("/products/sort-by-category")
def sort_by_category():
    result = sorted(products, key=lambda p: (p["category"], p["price"]))
    return {"products": result}


# -------------------------------
# Q6: BROWSE (SEARCH + SORT + PAGE)
# -------------------------------
@app.get("/products/browse")
def browse(
    keyword: str = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):
    result = products

    # Search
    if keyword:
        result = [p for p in result if keyword.lower() in p["name"].lower()]

    # Sort
    if sort_by in ["price", "name"]:
        result = sorted(result, key=lambda p: p[sort_by], reverse=(order == "desc"))

    # Pagination
    total = len(result)
    start = (page - 1) * limit
    result = result[start:start + limit]

    return {
        "total": total,
        "page": page,
        "products": result
    }