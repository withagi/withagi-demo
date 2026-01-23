from fastapi import FastAPI, HTTPException
from app.models import Product, Order

app = FastAPI(title='The Aura Shop API')

# Mock DB
products = [
    {'id': 1, 'name': 'Artisan Candle', 'price': 25.0, 'inventory': 100},
    {'id': 2, 'name': 'Handwoven Rug', 'price': 150.0, 'inventory': 10}
]

@app.get('/')
def read_root():
    return {'status': 'active', 'shop': 'The Aura Shop'}

@app.get('/products')
def get_products():
    return products

@app.post('/orders')
def place_order(order: Order):
    for item_id in order.items:
        product = next((p for p in products if p['id'] == item_id), None)
        if not product or product['inventory'] <= 0:
            raise HTTPException(status_code=400, detail=f'Product {item_id} out of stock')
        product['inventory'] -= 1
    return {'status': 'Ordered Successfully', 'order_id': order.id}