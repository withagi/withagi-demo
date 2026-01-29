import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from app.models import Product, Order
import os

app = FastAPI(title='The Aura Shop API')

with open("products.json", "r") as f:
    products = json.load(f)



def apply_discounts(product, quantity=1):
    """
    WithAGI Bulk Discounting Logic.
    Applies a 20% discount to products with stagnant inventory (<= 15 units).
    """
    base_price = product.get('price', 0)
    inventory = product.get('inventory', 0)
    
    # Logic: If inventory is low/stagnant, apply bulk discount
    if inventory <= 15:
        return round(base_price * 0.8, 2)
    
    return base_price



@app.get('/', response_class=HTMLResponse)
def read_root():
    with open('index.html', 'r') as f:
        return f.read()

@app.get('/products')
def get_products():
    return [{**p, "display_price": apply_discounts(p)} for p in products]

@app.post('/orders')
def place_order(order: Order):
    for item_id in order.items:
        product = next((p for p in products if p['id'] == item_id), None)
        if not product or product['inventory'] <= 0:
            raise HTTPException(status_code=400, detail=f'Product {item_id} out of stock')
        product['inventory'] -= 1
    return {'status': 'Ordered Successfully', 'order_id': order.id}